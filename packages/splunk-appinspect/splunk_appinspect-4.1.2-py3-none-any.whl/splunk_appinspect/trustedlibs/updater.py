import json
import logging
import urllib.parse
import urllib.request
from datetime import datetime
from pathlib import Path, PurePosixPath
from typing import Dict, Optional

import click

from splunk_appinspect.trustedlibs.constants import (
    BUNDLED_TRUSTEDLIBS_DIR,
    DEFAULT_TRUSTEDLIBS_URL,
    FILE_URL_PATHS,
    METADATA_URL_PATH,
)

logger = logging.getLogger(__name__)


class TrustedlibsUpdater:
    def __init__(self, trustedlibs_url: str = DEFAULT_TRUSTEDLIBS_URL, cache_dir: Optional[Path] = None):
        self.cache_dir = cache_dir or BUNDLED_TRUSTEDLIBS_DIR

        self.file_url_mapping = {
            urllib.parse.urljoin(trustedlibs_url, file_url_path): self.cache_dir / PurePosixPath(file_url_path).name
            for file_url_path in FILE_URL_PATHS
        }

        self.metadata_file_url = urllib.parse.urljoin(trustedlibs_url, METADATA_URL_PATH)
        self.metadata_file = self.cache_dir / "metadata.json"

    def update(self) -> None:
        self.cache_dir.mkdir(parents=True, exist_ok=True)

        click.echo("Checking for an update of trusted libraries...")

        if self._check_for_update():
            click.echo("Downloading an update of trusted libraries...")
            self._download_trustedlibs_files()
            self._save_metadata(self._download_metadata())
        else:
            click.echo("Trusted libraries up to date.")

    def _check_for_update(self) -> bool:
        if not self.metadata_file.exists():
            self._save_metadata(self._download_metadata())
            return True

        if not all(path.exists() for path in self.file_url_mapping.values()):
            return True

        try:
            local_metadata = self._load_metadata()
        except Exception:
            self._save_metadata(self._download_metadata())
            return True

        remote_metadata = self._download_metadata()

        return datetime.fromisoformat(remote_metadata["last_updated"]) > datetime.fromisoformat(
            local_metadata["last_updated"]
        )

    def _download_metadata(self) -> Dict[str, str]:
        try:
            with urllib.request.urlopen(self.metadata_file_url) as response:
                return json.loads(response.read())
        except Exception:
            click.echo(click.style("Error while downloading trusted libraries metadata.", fg="yellow"))
            raise

    def _load_metadata(self) -> Dict[str, str]:
        with open(self.metadata_file) as f:
            return json.load(f)

    def _save_metadata(self, metadata: Dict[str, str]) -> None:
        with open(self.metadata_file, "w") as f:
            json.dump(metadata, f)

    def _download_trustedlibs_files(self) -> None:
        try:
            for url, path in self.file_url_mapping.items():
                urllib.request.urlretrieve(url, path)
        except Exception:
            click.echo(click.style("There was an error downloading trusted libraries files.", fg="yellow"))
            raise
