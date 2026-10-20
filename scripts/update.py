#!/bin/env python3

import json
import sys
import typing

from pathlib import Path

import requests

VersionDict: typing.TypeAlias = dict[str, dict[str, str]]

REQUIRED_SECTIONS = ("firmware", "keymapTool")
TIMEOUT_SECONDS = 30
VERSION_FILE = Path(__file__).resolve().parent.parent / "version.json"
VERSION_URL = "https://origin.pfultd.com/downloads/hhkb/HHKBVersion.json"


def fetch_versions() -> typing.Any:
    response = requests.get(VERSION_URL, timeout=TIMEOUT_SECONDS)
    response.raise_for_status()

    # Manually decode the response content from UTF-8 BOM.
    decoded_response = response.content.decode("utf-8-sig")

    return json.loads(decoded_response)


def validate(versions: typing.Any) -> VersionDict:
    if not isinstance(versions, dict):
        raise ValueError(f"not a JSON object: {type(versions).__name__}")

    for section in REQUIRED_SECTIONS:
        entries = versions.get(section)
        if not isinstance(entries, dict) or not entries:
            raise ValueError(f"missing or empty section: {section!r}")
        for key, value in entries.items():
            if not isinstance(value, str):
                raise ValueError(f"non-string {section}.{key}: {value!r}")

    return versions


def load_versions(path: Path) -> VersionDict:
    try:
        with open(path, "r", encoding="utf-8") as stream:
            return json.load(stream)
    except FileNotFoundError:
        return {}


def save_versions(path: Path, versions: VersionDict) -> None:
    with open(path, "w", encoding="utf-8") as stream:
        json.dump(versions, stream, indent=2, sort_keys=True)
        stream.write("\n")


def main() -> int:
    try:
        new_json = validate(fetch_versions())
    except (requests.RequestException, ValueError) as error:
        print(f"Not updating {VERSION_FILE.name}: {error}", file=sys.stderr)
        return 1

    if new_json != load_versions(VERSION_FILE):
        save_versions(VERSION_FILE, new_json)

    return 0


if __name__ == "__main__":
    sys.exit(main())
