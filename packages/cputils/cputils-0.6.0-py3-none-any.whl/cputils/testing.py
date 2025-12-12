#!/usr/bin/env python3
"""Test a set of problems against their samples"""
import os, sys
from glob import glob
import subprocess
import time

from .config import config


def get_format(folder):
    if config["sample_format"] == "auto":
        if config["source"] in {"kattis", "aceptaelreto"}:
            return "samples-in-ans"
        # TODO: Automatic detection
        if (
            os.path.isdir(os.path.join(folder, "samples"))
            and glob(os.path.join(folder, "samples", "*.in"))
            and glob(os.path.join(folder, "samples", "*.ans"))
        ):
            return "samples-in-ans"
        if (
            os.path.isdir(os.path.join(folder, "input"))
            and glob(os.path.join(folder, "input", "*"))
            and os.path.isdir(os.path.join(folder, "output"))
            and glob(os.path.join(folder, "output", "*"))
        ):
            return "input-output"
        if (
            os.path.isdir(os.path.join(folder, "inputs"))
            and glob(os.path.join(folder, "inputs", "*"))
            and os.path.isdir(os.path.join(folder, "outputs"))
            and glob(os.path.join(folder, "outputs", "*"))
        ):
            return "inputs-outputs"
        raise NotImplementedError("Unable to detect sample format")
    return config["sample_format"]


def get_inputs(folder):
    sample_format = get_format(folder)
    if sample_format == "samples-in-ans":
        input_pattern = os.path.join("samples", "*.in")
    elif sample_format == "input-output":
        input_pattern = os.path.join("input", "*")
    elif sample_format == "inputs-outputs":
        input_pattern = os.path.join("inputs", "*")
    else:
        raise NotImplementedError("Invalid sample format")

    return sorted(glob(input_pattern, root_dir=folder))


def input_to_output(folder, inp):
    sample_format = get_format(folder)
    if sample_format == "samples-in-ans":
        return inp[:-2] + "ans"
    elif sample_format == "input-output":  # TODO: Refactor to avoid repeated code
        # Try exact match
        candidate = os.path.join("output", os.path.basename(inp))
        if os.path.isfile(candidate):
            return candidate

        # Otherwise, look for a single file with the same number in the name
        number = "".join(filter(str.isdigit, inp))
        matching_files = [filename for filename in os.listdir("output") if number in filename]
        
        if len(matching_files) == 1:
            return os.path.join("output", matching_files[0])
        elif not matching_files:
            raise ValueError("No matching file found.")
        else:
            raise ValueError("Multiple matching files found.")
    elif sample_format == "inputs-outputs":
        # Try exact match
        candidate = os.path.join("outputs", os.path.basename(inp))
        if os.path.isfile(candidate):
            return candidate

        # Otherwise, look for a single file with the same number in the name
        number = "".join(filter(str.isdigit, inp))
        matching_files = [filename for filename in os.listdir("outputs") if number in filename]
        
        if len(matching_files) == 1:
            return os.path.join("outputs", matching_files[0])
        elif not matching_files:
            raise ValueError("No matching file found.")
        else:
            raise ValueError("Multiple matching files found.")

    else:
        raise NotImplementedError("Invalid sample format")


supported_extensions = ["py", "c", "cpp", "rs", "java", "rb", "sh", "nim"]


def test_code(code, verbose=False):
    """Test a code, returning a list with either float describing the running time or str describing error(s)"""
    folder = os.path.dirname(os.path.abspath(code))
    code = os.path.basename(code)
    language = code.rsplit(".", 1)[-1].lower()

    tests = get_inputs(folder)

    # Compilation
    if language in {"c", "cpp", "rs", "java", "nim"}:
        if language in {"c"}:
            args = ["gcc", code, "-lm", "-o", "a.out"]

        elif language in {"cpp"}:
            args = ["g++", code, "-lm", "-o", "a.out"]
        elif language == "rs":
            args = ["rustc", code, "-o", "a.out"]
        elif language == "java":
            args = ["javac", code]
        elif language == "nim":
            args = ["nim", "c", "--opt:speed", "-o:a.out", code]

        proc = subprocess.Popen(
            args,
            cwd=folder,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=False,
        )

        out, err = proc.communicate()
        if proc.returncode:
            return ["CE"] * len(tests)

    times = []
    for test in tests:
        t1 = time.time()
        if language == "py":
            args = ["python", code]
        elif language == "rb":
            args = ["ruby", code]
        elif language == "sh":
            args = ["bash", code]
        elif language in {"c", "cpp", "rs", "nim"}:
            args = [os.path.join(folder, "a.out")]
        elif language == "java":
            args = ["java", code.rsplit(".", 1)[0]]
        else:
            raise NotImplementedError

        proc = subprocess.Popen(
            args,
            cwd=folder,
            stdin=open(os.path.join(folder, test), "r"),
            stdout=subprocess.PIPE,
            shell=False,
        )

        try:
            out, err = proc.communicate(timeout=config["timeout"])
            t2 = time.time()
            times.append(t2 - t1)
            if proc.returncode != 0:
                times[-1] = f"IR({proc.returncode})"
                continue
            out = out.decode()
            reference = open(os.path.join(folder, input_to_output(folder, test))).read()
            # Allow for differences in trailing or heading new lines
            if out.strip() != reference.strip():
                times[-1] = "WA"
                if verbose:
                    print(
                        "\nError in test %s. Expected output:\n%s\nCurrent output:\n%s"
                        % (test, reference, out),
                        file=sys.stderr,
                    )
                    return times

        except subprocess.TimeoutExpired:
            times.append("TLE(>%g)" % config["timeout"])
            proc.kill()

    return times


def main():
    import argparse

    # Create the argument parser
    parser = argparse.ArgumentParser(description="Test code files or directories.")
    parser.add_argument("paths", nargs="*", help="File(s) or folder to test.")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output.")

    # Parse the arguments
    args = parser.parse_args()

    if not args.paths:
        name = os.path.basename(sys.argv[0])
        print(
            "Usage:\n%s file(s): test the given files\n"
            "%s folder: test every supported file in the folder" % (name, name)
        )
    else:
        files = []
        for path in args.paths:
            if os.path.isdir(path):
                for ext in supported_extensions:
                    files.extend(glob(os.path.join(path, "*." + ext)))
            else:
                files.append(path)

        for code in files:
            times = test_code(code, verbose=args.verbose)

            print(os.path.basename(code), end=", ")
            print(
                ", ".join("%.3f" % t if isinstance(t, float) else str(t) for t in times)
            )


if __name__ == "__main__":
    main()
