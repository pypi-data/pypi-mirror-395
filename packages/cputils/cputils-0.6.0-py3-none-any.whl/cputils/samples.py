#!/usr/bin/env python3
"""Download problem samples"""
import os
import zipfile
import re

import requests


from .config import config
from .common import ensure_dir_exists


def get_samples(problem):
    """Download the samples to the problem directory"""
    # Check previously download
    if config["source"] in {"kattis", "aceptaelreto"}:
        if os.path.isdir(os.path.join(problem, "samples")):
            return False
    elif config["source"]=="aoc":
        # Expecting year-day
        try:
            year, day = problem.split("-")
        except ValueError as e:
            raise ValueError("In 'aoc', problem names are of the form 2020-15") from e
        if os.path.isfile(os.path.join(year, day, "input.txt")):
            return False
    elif re.match(r"aoc\d+", config["source"]):
        # Expecting day
        if os.path.isfile(os.path.join(problem, "input.txt")):
            return False

    if config["source"] == "kattis":
        r = requests.get(
            "https://open.kattis.com/problems/%s/file/statement/samples.zip" % problem
        )
        with open(os.path.join(problem, "samples.zip"), "wb") as f:
            for chunk in r.iter_content(chunk_size=128):
                f.write(chunk)

        with zipfile.ZipFile(os.path.join(problem, "samples.zip"), "r") as f:
            f.extractall(os.path.join(problem, "samples"))

        os.remove(os.path.join(problem, "samples.zip"))

    elif config["source"] == "aceptaelreto":
        r = requests.get(
            "https://www.aceptaelreto.com/problem/statement.php?id=%s" % problem
        )

        ensure_dir_exists(os.path.join(problem, "samples"))
        from bs4 import BeautifulSoup

        soup = BeautifulSoup(r.text, features="lxml")
        with open(os.path.join(problem, "samples", "1.in"), "w") as f:
            f.write(soup.find(id="sampleIn").pre.text)

        with open(os.path.join(problem, "samples", "1.ans"), "w") as f:
            f.write(soup.find(id="sampleOut").pre.text)

    elif re.match(r"aoc\d*", config["source"]):
        if config["source"]=="aoc":
            # Expecting year-day
            year, day = problem.split("-")
            base_dir = os.path.join(year, day)
        else:
            year, day = config["source"][3:], problem
            base_dir = problem

        try:
            from aocd import get_data
        except ImportError as e:
            raise ImportError("Install the advent-of-code-data package to download input")

        sample = get_data(day=int(day), year=int(year))

        ensure_dir_exists(base_dir)

        with open(os.path.join(base_dir, "input.txt"), "w") as f:
            f.write(sample)
        

    else:
        raise NotImplementedError("Unknown source: %s" % config["source"])

    return True


def main():
    import sys

    if len(sys.argv) != 2:
        name = os.path.basename(sys.argv[0])
        print("Usage:\n%s <problem>: Download test files for the given problem" % name)
    else:
        if not get_samples(sys.argv[1]):
            print("Samples already available")


if __name__ == "__main__":
    main()
