import datetime
from dateutil import parser

created_time = "2017-11-03T02:40:55.000000Z"
duration = 4.597551

ct = parser.parse(created_time)
st = ct - datetime.timedelta(seconds=duration)

print("{}: {}".format('created', ct))
print("{}: {}".format('duration', duration))
print("{}: {}".format('started', st))
