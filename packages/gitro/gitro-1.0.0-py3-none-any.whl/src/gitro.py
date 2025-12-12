import argparse
import platform
import subprocess
import sys


def parse_args(args: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--repo-path",
        "-p",
        type=str,
        help="Relative path to a repository",
        default="./",
    )
    parser.add_argument(
        "--remote",
        type=str,
        help="Name of your remote, default: origin",
        default="origin",
    )
    return parser.parse_args(args)


def main() -> int:
    args = parse_args(sys.argv[1:])
    proc = subprocess.run(
        ["git", "remote", "get-url", "origin"],  # noqa: S607
        check=False,
        cwd=args.repo_path,
        stdout=subprocess.PIPE,
        text=True,
    )
    if proc.returncode:
        print(proc.stdout)  # noqa: T201
        sys.exit(1)

    origin = proc.stdout.strip()
    if not origin:
        return 1

    remote = origin.replace(":", "/").replace("git@", "https://")
    if platform.system() == "Darwin":
        return subprocess.run(["open", remote], check=False).returncode  # noqa: S603, S607
    if platform.system() == "Linux":
        return subprocess.run(["xdg-open", remote], check=False).returncode  # noqa: S603, S607
    if platform.system() == "Windows":
        return subprocess.run(["start", remote], shell=True, check=True).returncode  # noqa: S602, S607
    return 0


if __name__ == "__main__":
    sys.exit(main())
