"""
Taken from https://stackoverflow.com/questions/9896644/getting-ffprobe-information-with-python
"""
import argparse
import subprocess
import sys
from pathlib import Path
from typing import NamedTuple
import json

class FFProbeResult(NamedTuple):
  return_code: int
  json: str
  error: str


def ffprobe(file_path) -> FFProbeResult:
  # TODO: check if ffprobe exists on system
  # TODO: Add ffprobe to docker container
  command_array = ["ffprobe",
                  "-v", "quiet",
                  "-print_format", "json",
                  "-show_format",
                  "-show_streams",
                  file_path]
  command_results = subprocess.run(command_array, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
  results = FFProbeResult(return_code=command_results.returncode,
                        json=command_results.stdout,
                        error=command_results.stderr)

  if results.return_code != 0:
    print('ERROR: {} - {}'.format(results.error, sys.stderr))

  return json.loads(results.json)
