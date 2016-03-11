import time
from datetime import datetime


s = '2016-02-27 04:02:00 UTC'
form = '%Y-%m-%d %H:%M:%S %Z'


print('now is:', time.time())
date = datetime.strptime(s, form)
print(date)
ts = time.mktime(date.timetuple())

print('now: ', time.time())
print('parsed: ', ts)
print('diff', (time.time() - ts) / 3600)
