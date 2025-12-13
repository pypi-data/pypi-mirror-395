from functools import lru_cache
import logging
import re
import shutil
import subprocess
from typing import Set
import sys
from packaging.version import parse as parse_version, Version
from packaging.requirements import Requirement
import easypip

try:
    from importlib.resources import files as resources_files
except Exception:
    from importlib_resources import files as resources_files


@lru_cache()
def cuda_version() -> Version:
    try:
        re_cuda = re.compile(rb".*CUDA version: ([\d\.]+)", re.IGNORECASE)
        out = subprocess.check_output("nvidia-smi")
        for line in out.splitlines():
            m = re_cuda.match(line)
            if m:
                return parse_version(m.group(1).decode("utf-8"))
    except Exception:
        pass
    logging.info("No CUDA detected")


def install_package(requirement: Requirement):
    if easypip.has_requirement(requirement):
        logging.info("Package %s is already installed", requirement)
        return

    easypip.install(requirement)


def install(name: str, processed: Set[str]):
    if name in processed:
        return

    path = resources_files("master_mind") / "requirements" / f"{name}.txt"

    for value in easypip.parse_requirements(path.read_text()):
        if not value.marker or value.marker.evaluate():
            install_package(value)
        else:
            logging.info("Skipping %s", value)

    processed.add(name)


def rl(processed: Set[str]):
    # Check that swig is installed
    if sys.platform == "win32":
        has_swig = shutil.which("swig.exe")
    else:
        has_swig = shutil.which("swig")

    if not has_swig:
        logging.error(
            "swig n'est pas installé: sous linux utilisez le "
            "gestionnaire de paquets:\n - sous windows/conda : "
            "conda install swig\n - sous ubuntu: sudo apt install swig"
        )
        sys.exit(1)

    install("deep", processed)
    install("rl", processed)


def deepl(processed: Set[str]):
    install("deep", processed)
    install("deepl", processed)


def adl(processed: Set[str]):
    install("deep", processed)
    install("adl", processed)


def llm(processed: Set[str]):
    install("deep", processed)
    install("llm", processed)


def rital(processed: Set[str]):
    install("deep", processed)
    install("rital", processed)
