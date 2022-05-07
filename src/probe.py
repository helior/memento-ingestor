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


# parser = argparse.ArgumentParser(description='View ffprobe output')
# parser.add_argument('-i', '--input', help='File Name', required=True)
# args = parser.parse_args()
# if not Path(args.input).is_file():
#   print("could not read file: " + args.input)
#   exit(1)
# print('File:       {}'.format(args.input))
# ffprobe_result = ffprobe(file_path=args.input))
# if ffprobe_result.return_code == 0:
#   # Print the raw json string
#   print(ffprobe_result.json)

#   # or print a summary of each stream
#   d = json.loads(ffprobe_result.json)
#   streams = d.get("streams", [])
#   for stream in streams:
#     print(f'{stream.get("codec_type", "unknown")}: {stream.get("codec_long_name")}')

# else:
#   print("ERROR")
#   print(ffprobe_result.error, file=sys.stderr)
