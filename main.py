import datetime
import time
import os
from dateutil import parser
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
import requests
from src.probe import ffprobe



def on_created(event):
  """
  On Create:
  TODO: info log a new file (event.ingestor.fileDetected, path)
  TODO: Move file to organize location
  - ❓Optional into Cloud Storage directory (Is this automatic?)
  - origin
  -- Year number
  --- Week number
  TODO:Save "Memento" record in DB
  - SQLite + Cloud Storage (iCloud, Dropbox, etc.)
  - Data Model:
      mID (memento ID)
      startTime
      endTime
      duration
      filePath
      tags[]
  """
  print(f"Created: {event.src_path} ")
  # TODO: Log event

  try:
    # Probe
    probe = ffprobe(event.src_path)

    #Process
    created_time = parser.parse(probe.get('format').get('tags').get('creation_time'))
    duration = probe.get('format').get('duration')
    start_time = created_time - datetime.timedelta(seconds=float(duration))

    # Move
    os.rename(event.src_path, "{}".format(event.src_path))

    # Save
    data = {
      "label": probe.get('format').get('filename').rsplit('/', 1)[1],
      "startTime": start_time,
      "duration": duration,
    }
    files = {'media': open (event.src_path, 'rb')}
    r = requests.post('http://localhost:8000/api/momentoriginalaudio/', files=files, data=data)

    # Log successful completion
    print(probe)
    print(r.json())
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


if __name__ == '__main__':
  """
  Main:
  TODO: Load configuration file (from ~/.memento-ingestor.yml) or something
  TODO: On Startup, asyncronously scan existing files from watch folder to process
  ✓ Initialize Watch folder
  """

  # Config for WATCH FOLDER
  patterns = ['*.mp3', '*.mp4', '*.m4a']
  ignore_patterns = None
  ignore_directories = False
  case_sensitive = True
  event_handler = PatternMatchingEventHandler(patterns, ignore_patterns, ignore_directories, case_sensitive)

  event_handler.on_created = on_created
  event_handler.on_deleted = on_deleted
  event_handler.on_modified = on_modified
  event_handler.on_moved = on_moved

  path = '.'
  go_recursively = True
  observer = Observer()
  observer.schedule(event_handler, path, go_recursively)

  # Begin watching..
  print('event.app.start')
  observer.start()

  # Do nothing infinitely, unless interrupted
  # TODO: except KILLSIG??
  try:
    while True:
      time.sleep(1)
  except KeyboardInterrupt:
    observer.stop()
    observer.join()
