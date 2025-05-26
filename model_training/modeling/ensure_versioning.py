"""Utility for ensuring version files exist and are up to date."""

from pathlib import Path

import yaml


class Ensurance:
    """Class to ensure version files exist and provide version info."""

    def ensure_version_file_exists(self):
        """Create params.yaml with version before any DVC commands run."""
        version_file = Path("dynamic_version.txt")
        params_file = Path("params.yaml")

        # Priority: dynamic_version.txt > VERSION.txt
        if version_file.exists():
            with open(version_file, encoding="utf-8") as f:
                version = f.read().strip()
        else:
            with open("VERSION.txt", encoding="utf-8") as f:
                version = f.read().strip()

        # Write params.yaml immediately
        with open(params_file, "w", encoding="utf-8") as f:
            yaml.dump({"version": version}, f)

        return version

    def return_version(self):
        """Return the version for needy functions."""
        version_file = Path("dynamic_version.txt")

        # Priority: dynamic_version.txt > VERSION.txt
        if version_file.exists():
            with open(version_file, encoding="utf-8") as f:
                version = f.read().strip()
        else:
            with open("VERSION.txt", encoding="utf-8") as f:
                version = f.read().strip()

        return version


if __name__ == "__main__":
    ensurance = Ensurance()
    ensurance.ensure_version_file_exists()
