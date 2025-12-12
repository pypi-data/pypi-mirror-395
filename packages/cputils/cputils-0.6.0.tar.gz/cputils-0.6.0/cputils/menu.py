#!/usr/bin/env python
# Prepare a menu for CP operations

import sys
import subprocess
import webbrowser

from .config import config


# getch-like function
# based on https://code.activestate.com/recipes/134892/

class _Getch:
    """Gets a single character from standard input, not echoing to the screen and consuming everything else in the buffer"""
    def __init__(self):
        try:
            self.impl = _GetchWindows()
        except ImportError:
            self.impl = _GetchUnix()

    def __call__(self):
        return self.impl()

class _GetchWindows:
    def __init__(self):
        import msvcrt

    def __call__(self):
        import msvcrt
        ch = msvcrt.getch()
        while msvcrt.kbhit():
            msvcrt.getch()
        
        return ch

class _GetchUnix:
    def __init__(self):
        import tty, termios, fcntl, os
    def __call__(self):
        import tty, termios, fcntl, os
        fd = sys.stdin.fileno()
        # Save old terminal settings and file status flags
        old_settings = termios.tcgetattr(fd)
        old_flags = fcntl.fcntl(fd, fcntl.F_GETFL)
        try:
            # Set the terminal to raw mode to read a single character
            tty.setraw(fd)
            ch = sys.stdin.read(1) 

            # Set non-blocking mode to drain the rest of the input
            fcntl.fcntl(fd, fcntl.F_SETFL, old_flags | os.O_NONBLOCK)

            # Read until no more data is available
            while True:
                try:
                    extra = sys.stdin.read(1)
                    if not extra:  
                        break
                except (BlockingIOError, OSError):
                    break

        finally:
            # Restore terminal and file status flags
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
            fcntl.fcntl(fd, fcntl.F_SETFL, old_flags)
        
        return ch
        
# Update this to make the code compatible with other systems
getch=_Getch()

help_message="""CPUTILS
1-\tTest
2-\tSubmit
3-\tGit add
b-\tOpen statement in browser
d-\tDownload problem data
e-\tOpen in editor
p-\tChange active problem
l-\tChange active language
q-\tLeave
!-\tCustom command
h-\tDisplay help
"""

def main():
    problem = sys.argv[1] if len(sys.argv)>=2 else None
    language = sys.argv[2] if len(sys.argv)>=3 else config['language']
    
    option="-"
    print(help_message)
    
    while (option not in "qQ" and option!="\0"):
        print("\n>", end='')
        sys.stdout.flush()
        option=getch()
        
        if option == "1":
            if problem is None:
                print("No problem set. Use 'p' to choose it")
                continue
            print("Testing")
            subprocess.Popen(
                ["cptest", "--verbose", f"{config['problem_dir']}/{problem}/{problem}.{language}"]
            ).wait()

        elif option == "2":
            if problem is None:
                print("No problem set. Use 'p' to choose it")
                continue
            print("Submitting")
            subprocess.Popen(
                ["cpsubmit", f"{config['problem_dir']}/{problem}/{problem}.{language}"]
            ).wait()

        elif option == "3":
            if problem is None:
                print("No problem set. Use 'p' to choose it")
                continue
            print("Adding to git")
            subprocess.Popen(
                ["git", "add", f"{problem}.{language}"], cwd=f"{config['problem_dir']}/{problem}"
            ).wait()
            print("ok")

        elif option in "pP":
            print("New problem name?")
            problem = input()
            print("ok")
        
        elif option in "lL":
            print("New language (extension only)?")
            language = input()
            print("ok")

        elif option in "bB":
            if config["source"]=="kattis":
                webbrowser.open(f"https://open.kattis.com/problems/{problem}")
            elif config["source"]=="aceptaelreto":
                webbrowser.open(f"https://www.aceptaelreto.com/problem/statement.php?id={problem}")
            elif config["source"]=="aoc":
                year, day = problem.split("-")
                webbrowser.open(f"https://adventofcode.com/{year}/day/{day}")
            elif config["source"].startswith("aoc"):
                year = config["source"][3:]
                webbrowser.open(f"https://adventofcode.com/{year}/day/{problem}")
            else:
                print(f"Statement not available for source {config['source']}")

        elif option in "dD":
            if problem is None:
                print("No problem set. Use 'p' to choose it")
                continue
            print("Downloading data")
            subprocess.Popen(["mkdir", "-p", f"{config['problem_dir']}/{problem}"]).wait()
            subprocess.Popen(
                ["cpsamples", problem], cwd=config["problem_dir"]
            ).wait()

        elif option in "eE":
            if problem is None:
                print("No problem set. Use 'p' to choose it")
                continue
            print("Opening editor...")
            subprocess.Popen(
                [config["editor"], f"{problem}/{problem}.{language}"],
                cwd=config["problem_dir"],
                stdout=subprocess.DEVNULL, # Suppress standard output
                stderr=subprocess.DEVNULL  # Suppress error output
            )

        elif option == "!":
            print("Enter command: ")
            cmd = input()
            subprocess.Popen(cmd, cwd=f"{config['problem_dir']}/{problem}", shell=True).wait()

        elif option in "hH":
            print(help_message)
            print(f"Problem: {problem}\nLanguage: {language}")

        elif option in "qQ":
            pass

        else:
            print("Invalid option")
    
    
if __name__ == '__main__':
    main()
