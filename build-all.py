#!/usr/bin/env python3

import json
import shlex
import subprocess
from pathlib import PurePath


def main(clean=False, build=False):
    with open("crates.json", "r") as f:
        crates = json.load(f)

    for (board, jobs) in crates["boards"].items():
        print()
        print("-" * 80)
        print(f"Crate:   {board}")
        print(f"Command: {jobs['build']}\n")

        command = shlex.split(jobs["build"])
        crate_path = PurePath("boards", board)

        if clean:
            subprocess.check_call(shlex.split("cargo clean"), cwd=crate_path)
            subprocess.check_call(shlex.split("cargo update"), cwd=crate_path)
        if build:
            subprocess.check_call(command, cwd=crate_path)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--clean", action="store_true", help="run `cargo clean` and `cargo update` before building")
    parser.add_argument("--no-build", action="store_true", help="Don't build the crates")

    args = parser.parse_args()

    main(clean=args.clean, build=not args.no_build)
