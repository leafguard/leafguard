"""MANUAL deploy to the Hugging Face Space. Run by a HUMAN only (never by the coding agent).

  python scripts/deploy.py --url https://handle-leafguard.hf.space [--allow-dummy] [--record]

One-time setup:  git remote add hf https://huggingface.co/spaces/<handle>/leafguard
What it does: safety checks -> tests -> stamp app/version.json on a TEMPORARY branch -> force-push that
branch to the Space -> wait until the live /version equals this commit -> smoke test the live site.
Your main branch is never modified by this script."""
import argparse, datetime, json, os, pathlib, subprocess, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
os.chdir(ROOT)


def sh(*cmd, check=True, capture=True) -> str:
    r = subprocess.run(cmd, capture_output=capture, text=True)
    if check and r.returncode != 0:
        sys.exit(f"FAILED: {' '.join(cmd)}\n{r.stdout}{r.stderr}")
    return (r.stdout or "").strip()


def step(msg: str) -> None:
    print(f"\n== {msg}")


ap = argparse.ArgumentParser()
ap.add_argument("--url", required=True, help="public Space URL, e.g. https://handle-leafguard.hf.space")
ap.add_argument("--allow-dummy", action="store_true", help="allow the placeholder model (early checkpoints only)")
ap.add_argument("--record", action="store_true", help="also record a GitHub deployment (needs the gh CLI)")
ap.add_argument("--remote", default="hf")
args = ap.parse_args()

step("1/7 Safety checks")
if sh("git", "rev-parse", "--abbrev-ref", "HEAD") != "main":
    sys.exit("Switch to the main branch first.")
if sh("git", "status", "--porcelain"):
    sys.exit("Working tree is not clean. Commit or stash your changes first.")
sh("git", "fetch", "origin")
head = sh("git", "rev-parse", "HEAD")
if head != sh("git", "rev-parse", "origin/main"):
    sys.exit("Local main differs from origin/main. Push (or pull) so GitHub has exactly what you deploy.")
if args.remote not in sh("git", "remote").split():
    sys.exit(f"Remote '{args.remote}' missing. Run: git remote add {args.remote} https://huggingface.co/spaces/<handle>/leafguard")
if not (ROOT / ".banned_terms.txt").exists():
    sys.exit("Create .banned_terms.txt first (anonymity audit is mandatory before every deploy).")
dummy = (ROOT / "app/model/MODEL_IS_DUMMY").exists()
if dummy and not args.allow_dummy:
    sys.exit("The placeholder model is present. Replace it with the real model, or pass --allow-dummy for an early checkpoint.")

step("2/7 Tests")
sh(sys.executable, "-m", "pytest", "-q", capture=False)
if (ROOT / "app/data/advisory.json").exists() and not dummy:
    sh(sys.executable, "scripts/check_advisory.py", capture=False)

step("3/7 Anonymity audit")
sh(sys.executable, "scripts/anonymity_audit.py", capture=False)

sha, now = head, datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
tmp = f"deploy-tmp-{sha[:7]}"
step(f"4/7 Stamp version {sha[:7]} on temporary branch {tmp}")
sh("git", "switch", "-c", tmp)
try:
    (ROOT / "app/version.json").write_text(json.dumps({"sha": sha, "deployed_at": now, "run_url": None}) + "\n")
    sh("git", "add", "-f", "app/version.json")
    sh("git", "-c", "user.name=leafguard-deploy", "-c", "user.email=deploy@users.noreply.github.com",
       "commit", "-m", f"deploy {sha[:7]}")
    step(f"5/7 Push to the Space ({args.remote})")
    sh("git", "push", "--force", args.remote, "HEAD:main", capture=False)
finally:
    sh("git", "switch", "main", check=False)
    sh("git", "branch", "-D", tmp, check=False)

step("6/7 Wait for the build and smoke test the LIVE site")
env = dict(os.environ, BASE_URL=args.url, EXPECTED_SHA=sha, REQUIRE_REAL_MODEL="0" if args.allow_dummy else "1")
ok = subprocess.run([sys.executable, "scripts/smoke_test.py"], env=env).returncode == 0

step("7/7 Record")
if args.record:
    try:
        repo = sh("gh", "repo", "view", "--json", "nameWithOwner", "-q", ".nameWithOwner")
        body = json.dumps({"ref": sha, "environment": "production", "auto_merge": False, "required_contexts": [],
                           "description": f"manual deploy {sha[:7]}"})
        dep = json.loads(subprocess.run(["gh", "api", f"repos/{repo}/deployments", "--input", "-"],
                                        input=body, capture_output=True, text=True, check=True).stdout)
        subprocess.run(["gh", "api", f"repos/{repo}/deployments/{dep['id']}/statuses", "--input", "-"],
                       input=json.dumps({"state": "success" if ok else "failure", "environment_url": args.url,
                                         "description": "live smoke test " + ("passed" if ok else "failed")}),
                       capture_output=True, text=True, check=True)
        print("GitHub deployment recorded.")
    except Exception as e:  # recording is optional, never block the deploy on it
        print("Could not record the GitHub deployment (optional):", e)
print(f"\nPaste this row into docs/DEPLOYMENTS.md:\n| {now[:10]} | <tag> | `{sha[:7]}` | {'success' if ok else 'FAILED'} | "
      f"{'pass' if ok else 'fail'} | <notes, measured numbers> |")
sys.exit(0 if ok else 1)
