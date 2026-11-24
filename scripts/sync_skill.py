"""Stage a deploy-skill snapshot from a selected commit on the public main branch."""
import argparse
from pathlib import Path
import re
import subprocess


ROOT = Path(__file__).resolve().parents[1]
UPSTREAM = "https://github.com/AnthonyZZH/xiaoqian-weixin.git"
SKILL = "skills/xiaoqian-deploy"
TEST = "tests/test_verify_manifest.py"
RECORD = "UPSTREAM_COMMIT"


def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()


def sync(commit):
    if not re.fullmatch("[0-9a-fA-F]{40}", commit):
        raise ValueError("Supply the full 40-character commit SHA from the public main branch.")
    commit = commit.lower()
    if Path(git("rev-parse", "--show-toplevel")).resolve() != ROOT:
        raise ValueError("Run this script from a checkout of the standalone skill repository.")
    if git("status", "--porcelain", "--untracked-files=all", "--", SKILL, TEST, RECORD):
        raise ValueError("Review outstanding changes to the published snapshot before syncing.")

    git("fetch", "--quiet", "--no-tags", "--no-recurse-submodules", UPSTREAM, "refs/heads/main")
    git("merge-base", "--is-ancestor", commit, "FETCH_HEAD")
    entries = git("ls-tree", "-r", commit, "--", SKILL, TEST).splitlines()
    names = set()
    for entry in entries:
        metadata, name = entry.split("\t", 1)
        if not metadata.startswith(("100644 blob ", "100755 blob ")):
            raise ValueError("The skill snapshot must contain ordinary files.")
        names.add(name)
    if not {f"{SKILL}/SKILL.md", f"{SKILL}/scripts/verify_manifest.py", TEST} <= names:
        raise ValueError("The selected commit is missing the deploy skill or its manifest test.")

    git("restore", "--source", commit, "--staged", "--worktree", "--", SKILL, TEST)
    git("diff", "--cached", "--exit-code", commit, "--", SKILL, TEST)
    (ROOT / RECORD).write_bytes((commit + "\n").encode("ascii"))
    git("add", "--", RECORD)
    print(f"Verified {len(names)} files against public main commit {commit}. Review git diff --cached.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("commit")
    try:
        sync(parser.parse_args().commit)
    except (ValueError, subprocess.CalledProcessError) as exc:
        parser.exit(1, f"{exc}\n")
