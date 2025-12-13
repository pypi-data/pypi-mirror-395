import json
from pathlib import Path
from typing import Any, Dict, Mapping, cast


class Version:
    """Utility class for managing MONAI Deploy versions"""

    @staticmethod
    def get_version() -> str:
        """Get the current MONAI Deploy version"""
        try:
            version_file = Path(__file__).parent.parent / "_version.py"
            version_info = Version.parse_version_file(version_file)
            return str(version_info.get("version", "unknown"))
        except Exception:
            return "unknown"

    @staticmethod
    def parse_version_file(version_file: Path) -> Dict[str, Any]:
        """Parse version info from _version.py file"""
        if not version_file.exists():
            return {}

        version_text = version_file.read_text()
        try:
            version_json = version_text.split("version_json = '")[1].split("'\n")[0]
        except IndexError:
            return {}
        parsed_version = json.loads(version_json)
        # json.loads returns Any; ensure we always hand back a dictionary
        if not isinstance(parsed_version, Mapping):
            return {}
        return dict(parsed_version)

    @staticmethod
    def get_version_info() -> Dict:
        """Get full version information including git details"""
        try:
            version_file = Path(__file__).parent.parent / "_version.py"
            return Version.parse_version_file(version_file)
        except Exception:
            return {"version": "unknown"}
