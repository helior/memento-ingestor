import time
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler

from src.handlers import on_created, on_deleted, on_modified, on_moved


if __name__ == '__main__':
  """
  Main:
  TODO: Load configuration file (from ~/.memento-ingestor.yml) or something
  TODO: On Startup, asyncronously scan existing files from watch folder to process
  ✓ Initialize Watch folder
  """

  # Config for WATCH FOLDER
  patterns = ['*.mp3', '*.mp4', '*.m4a'] # TODO: or from configuration
  ignore_patterns = None
  ignore_directories = False
  case_sensitive = True
  event_handler = PatternMatchingEventHandler(patterns, ignore_patterns, ignore_directories, case_sensitive)

  event_handler.on_created = on_created
  event_handler.on_deleted = on_deleted
  event_handler.on_modified = on_modified
  event_handler.on_moved = on_moved

  watchfolder_path = './watchfolder' # TODO: or from configuration
  go_recursively = False
  observer = Observer()
  observer.schedule(event_handler, watchfolder_path, go_recursively)

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
