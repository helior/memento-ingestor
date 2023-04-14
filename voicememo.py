import csv
import datetime
from dateutil import parser
import os
import requests
from signal import SIGABRT
import sqlite3

from src.probe import ffprobe

if __name__ == '__main__':
  # Configuration variables
  db_url = os.path.expanduser("~/Library/Application Support/com.apple.voicememos/Recordings/CloudRecordings.db")
  tracker_file = 'voicememo_db.csv'
  headers = ['~id', '~label', '~path', '~date']
  all_rows = []
  tracked_rows = []
  tracked_ids = []
  pending_rows = []

  # Create an empty file if it doesn't exist
  if not os.path.exists(tracker_file):
    with open(tracker_file, 'w') as f:
      f.write(None)

  # Read tracked records
  with open(tracker_file, 'r') as f:
    reader = csv.DictReader(f, headers)
    for row in reader:
      tracked_ids.append(row['~id'])
      tracked_rows.append(row)
    # Delete the superfluous header row
    if len(tracked_ids):
      del tracked_ids[0]
      del tracked_rows[0]


  # Read from Voicememo DB
  try:
    cx = sqlite3.connect(db_url)
    cu = cx.cursor()
    results = cu.execute('SELECT ZUNIQUEID, ZCUSTOMLABEL, ZPATH, ZDATE FROM "ZCLOUDRECORDING" ORDER BY "ZDATEFORSORTING" ASC')
    for row in results:
      all_rows.append(row)
  except sqlite3.OperationalError as e:
    print("❌💀❌ Sorry!!")
    print(e)
    exit(SIGABRT)

# Compare all_rows with tracked_ids
for row in all_rows:
  id, label, path, date = row
  if id not in tracked_ids:
    # Skip record when file is not yet synchronized.
    if not path:
      print('⚠️ {} is not yet synchronized. Skipping..'.format(id))
      continue

    pending_rows.append({
      '~id': id,
      '~label': label,
      '~path': path,
      '~date': date
    })


print(pending_rows)
print('{} pending items.'.format(len(pending_rows)))

# TODO: Confirm ingestion of X items

# Import records
try:
  for row in pending_rows:
    probe = ffprobe(row['~path'])
    created_time = parser.parse(probe.get('format').get('tags').get('creation_time'))
    duration = probe.get('format').get('duration')
    start_time = created_time - datetime.timedelta(seconds=float(duration))

    data = {
      "label": row['~label'],
      "startTime": start_time,
      "duration": duration,
    }
    files = {'audioFile': open (row['~path'], 'rb')}

    r = requests.post('http://localhost:8000/api/mementooriginalaudio/', files=files, data=data)
    try:
      r.raise_for_status()
      print('✅ {}'.format(row['~id']))

      # On success, add ID to tracked IDs
      tracked_rows.append(row)

    except requests.exceptions.HTTPError as err:
      print('❌ -----')
      print(err)
      print('{} ({})'.format(row['~id'], row['~label']))
      print('❌ -----')

except Exception as e:
  print(e)


# Write
with open(tracker_file, 'w') as f:
  dw = csv.DictWriter(f, headers)
  dw.writeheader()
  dw.writerows(tracked_rows)
