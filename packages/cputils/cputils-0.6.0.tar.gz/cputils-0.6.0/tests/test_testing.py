from cputils import testing
from cputils.config import config
from cputils.common import ensure_dir_exists


import os
import tempfile
import shutil


original_cwd = os.getcwd()

py_successor = "print(int(input())+1)"

c_successor = r"""
#include <stdio.h>
int main(){int n;scanf("%d",&n);printf("%d",n+1);return 0;}"""

cpp_successor = r"""
#include <iostream>
using namespace std;

int main() {
    int n;
    cin >> n;
    cout << n + 1 << endl;
    return 0;
}
"""

rs_successor = r"""
use std::io;

fn main() {
    let mut input = String::new();
    io::stdin().read_line(&mut input).expect("Failed to read line");
    let n: i32 = input.trim().parse().expect("Invalid input");
    println!("{}", n + 1);
}
"""

java_successor = r"""import java.util.Scanner;
public class code {
    public static void main(String[] args) {
        System.out.println(new Scanner(System.in).nextInt() + 1);
    }
}
"""

sh_successor = r"""read n;echo $((n+1))"""

rb_successor = r"""puts gets.to_i+1"""

nim_successor = r"""import strutils
echo readLine(stdin).parseInt+1
"""


successor_codes = {
    "py": py_successor,
    "c": c_successor,
    "cpp": cpp_successor,
    "rs": rs_successor,
    "java": java_successor,
    "sh":sh_successor,
    "rb":rb_successor,
    "nim":nim_successor,
}


c_successor_WA = r"""
#include <stdio.h>
int main(){int n;scanf("%d",&n);printf("%d",n+2);return 0;}"""

c_successor_IR = r"""
#include <stdio.h>
int main(){int n;scanf("%d",&n);printf("%d",n+1);return 1;}"""

sleep_python = "import time;time.sleep(100)"


def perform_success_testing(language):
    config.config["sample_format"] = "inputs-outputs"
    try:
        temp_dir = tempfile.mkdtemp(prefix="cputils_test_")

        os.chdir(temp_dir)

        ensure_dir_exists("inputs")
        ensure_dir_exists("outputs")

        with open("inputs/1.txt", "w") as file:
            file.write("1")
        with open("outputs/1.txt", "w") as file:
            file.write("2")

        with open(f"code.{language}", "w") as file:
            file.write(successor_codes[language])

        times = testing.test_code(f"code.{language}")
        assert len(times) == 1 and isinstance(times[0], float)

    finally:
        os.chdir(original_cwd)
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)


def test_python_success():
    perform_success_testing("py")


def test_c_success():
    perform_success_testing("c")


def test_cpp_success():
    perform_success_testing("cpp")


def test_rust_success():
    perform_success_testing("rs")


def test_java_success():
    perform_success_testing("java")

def test_sh_success():
    perform_success_testing("sh")

def test_rb_success():
    perform_success_testing("rb")

def test_nim_success():
    perform_success_testing("nim")


def test_testing_errors():
    config.config["sample_format"] = "inputs-outputs"
    config.config["timeout"] = 1
    try:
        temp_dir = tempfile.mkdtemp(prefix="cputils_test_")

        os.chdir(temp_dir)

        ensure_dir_exists("inputs")
        ensure_dir_exists("outputs")

        with open("inputs/1.txt", "w") as file:
            file.write("1")
        with open("outputs/1.txt", "w") as file:
            file.write("2")

        with open("code_WA.c", "w") as file:
            file.write(c_successor_WA)

        times = testing.test_code("code_WA.c")
        assert len(times) == 1 and times[0] == "WA"

        with open("code_IR.c", "w") as file:
            file.write(c_successor_IR)

        times = testing.test_code("code_IR.c")
        assert len(times) == 1 and times[0] == "IR(1)"

        with open("code_TLE.py", "w") as file:
            file.write(sleep_python)

        times = testing.test_code("code_TLE.py")
        assert len(times) == 1 and times[0] == "TLE(>1)"

    finally:
        os.chdir(original_cwd)
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
