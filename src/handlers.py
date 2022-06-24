import datetime
from dateutil import parser
import requests
import os

from src.probe import ffprobe

def on_created(event):
  """
  On Create:
  TODO: info log a new file (event.ingestor.fileDetected, path)
  """
  print(f"Created: {event.src_path} ")
  # TODO: Log event

  if event.is_directory:
    print('!!Is directory!')

  try:
    # Probe
    probe = ffprobe(event.src_path)

    #Pre-process
    created_time = parser.parse(probe.get('format').get('tags').get('creation_time'))
    duration = probe.get('format').get('duration')
    start_time = created_time - datetime.timedelta(seconds=float(duration))
    basename = os.path.basename(event.src_path)

    # Save.
    data = {
      "label": basename,
      "startTime": start_time,
      "duration": duration,
    }
    files = {'audioFile': open (event.src_path, 'rb')}
    r = requests.post('http://localhost:8000/api/momentoriginalaudio/', files=files, data=data)

    # Log: Sucessful upload.
    print(probe)
    print(r.json())

    # Move.
    processed_path = './processed' # TODO: or from configuration
    destination_path = os.path.abspath(os.path.join(processed_path, basename))
    os.rename(event.src_path, destination_path)
    # os.remove(event.src_path) # TODO: remove files instead, but only after you've detected duplicates

  except Exception as e:
    print(e)

def on_deleted(event):
  """
  On Delete:
  TODO: info log manual deletion of a file (event.ingestor.fileDeleted, path)
  """
  print(f"Deleted: {event.src_path} ")

def on_modified(event):

  print(f"Modified: {event.src_path} ")

def on_moved(event):
  """
  On Move:
  - TODO: info log event (event.ingestor.fileMoved, path, MID)
  """
  print(f"Moved: {event.src_path} → {event.dest_path} ")
