from cputils import samples
from cputils.config import config


import os
import tempfile
import shutil


original_cwd = os.getcwd()


def test_samples_kattis():
    config.config["source"] = "kattis"
    try:
        temp_dir = tempfile.mkdtemp(prefix="cputils_test_kattis_")

        os.chdir(temp_dir)

        samples.get_samples("99problems")

        for n in [1,2,3]:
            for e in ["in", "ans"]:
                f=f"99problems/samples/{n}.{e}"
                assert os.path.isfile(f) and os.path.getsize(f) > 0

    finally:
        os.chdir(original_cwd)
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)


def test_samples_aceptaelreto():
    config.config["source"] = "aceptaelreto"
    try:
        temp_dir = tempfile.mkdtemp(prefix="cputils_test_aer_")

        os.chdir(temp_dir)

        samples.get_samples("100")

        for n in [1]:
            for e in ["in", "ans"]:
                f=f"100/samples/{n}.{e}"
                assert os.path.isfile(f) and os.path.getsize(f) > 0

    finally:
        os.chdir(original_cwd)
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
