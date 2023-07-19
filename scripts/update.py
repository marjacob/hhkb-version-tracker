#!/bin/env python3

import json
import typing
import requests

VersionDict: typing.TypeAlias = dict[dict[str, str]]

VERSION_FILE = "version.json"
VERSION_URL = "https://origin.pfultd.com/downloads/hhkb/HHKBVersion.json"

response = requests.get(VERSION_URL)
response.raise_for_status()

# Manually decode the response content from UTF-8 BOM.
decoded_response = response.content.decode("utf-8-sig")

new_json: VersionDict = json.loads(decoded_response)
old_json: VersionDict = {}

try:
    with open(VERSION_FILE, "r") as stream:
        old_json = json.load(stream)
except FileNotFoundError:
    pass

if new_json != old_json:
    with open(VERSION_FILE, "w") as stream:
        json.dump(new_json, stream, indent=2, sort_keys=True)
