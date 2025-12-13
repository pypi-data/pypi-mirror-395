try:
    from functools import cached_property
except ImportError:
    from cached_property import cached_property
import json
import logging
from pathlib import Path
from appdirs import user_config_dir
import master_mind.install as mm_install


class Configuration:
    def __init__(self):
        logging.info(f"Reading configuration from {self.path}")
        config = {}
        if self.path.exists():
            with self.path.open("r") as fp:
                config = json.load(fp)

        self.courses = set()
        for course in config.get("courses", []):

            if getattr(mm_install, course, None) is not None:
                self.courses.add(course)
            else:
                logging.warning("Course '%s' does not exit – removing", course)

    def save(self):
        self.path.parent.mkdir(exist_ok=True, parents=True)
        s = json.dumps({"courses": [c for c in self.courses]})
        self.path.write_text(s)
        logging.info("Wrote configuration in %s", self.path)

    @cached_property
    def path(self) -> Path:
        return Path(user_config_dir("master-mind", "isir")) / "config.json"
