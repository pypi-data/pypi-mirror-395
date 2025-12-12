import subprocess
import sys
from typing import List, Optional
import requests
from packaging.version import parse as parse_version
import json
import logging
from importlib.metadata import version
from easypip import parse_requirements
from .install import install_package


def last_version(package: str):
    """Check if last version"""
    url = f"""https://pypi.org/pypi/{package}/json"""  # noqa: E231
    req = requests.get(url)
    version = parse_version("0")
    if req.status_code == requests.codes.ok:
        j = json.loads(req.text.encode(req.encoding))
        releases = j.get("releases", [])
        for release in releases:
            ver = parse_version(release)
            if not ver.is_prerelease:
                version = max(version, ver)
    return version


def check_last(package: str) -> Optional[str]:
    pypi = last_version(package)
    current = parse_version(version(package))
    if pypi > current:
        return pypi


def check_last_mastermind(args: List[str]):
    better_version = check_last("su_master_mind")

    if better_version:
        logging.info("Updating the package")
        (requirement,) = parse_requirements(f"su_master_mind=={better_version}")
        install_package(requirement)
        logging.info("Updating")
        subprocess.check_call(args)
        sys.exit()
