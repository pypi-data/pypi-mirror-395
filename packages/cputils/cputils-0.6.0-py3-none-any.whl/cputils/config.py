#!/usr/bin/env python3
"""Create a config file for cputils"""

import yaconfig


sources = ["none", "kattis", "aceptaelreto", "aoc", "aoc<year>"]

format_help = """
auto: Pick from the source or try to guess if none. Recommended option.
inputs-outputs: Two folders with txt files with the same names or with unique numbers in them, identifying each case.
samples-in-ans: A single "samples" folder with files *.in and matching *.ans
"""

metaconfig = yaconfig.MetaConfig(
    yaconfig.Variable(
        "source",
        type=str,
        default="none",
        help="Source to fetch samples. Available options: %s" % "\n".join(sources),
    ),
    yaconfig.Variable(
        "sample_format",
        type=str,
        default="auto",
        help="Format of input/out pairs. Available options include:" + format_help,
    ),
    yaconfig.Variable(
        "timeout", type=float, default="2", help="Timeout to run tests in seconds"
    ),
    yaconfig.Variable(
        "problem_dir", type=str, default="problems", help="Name of directory where problems are stored when using the menu"
    ),
    yaconfig.Variable(
        "editor", type=str, default="code", help="Name of the editor to run"
    ),
    yaconfig.Variable(
        "language", type=str, default="py", help="Name of the default language (extension only)"
    ),
)

config = yaconfig.Config(metaconfig)

try:
    config.load_json("cpconfig.json")
except FileNotFoundError:
    pass


def main():
    metaconfig.interactive_json("cpconfig.json")


if __name__ == "__main__":
    main()
