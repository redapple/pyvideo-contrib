from datetime import datetime
import pprint
import re

with open('video_durations.txt') as f:
   lines = f.readlines()

file_re = re.compile(r'Processing (.+)', re.I)
duration_re = re.compile(r'Duration: ([\d:]+)')

fmt = '%H:%M:%S'
durations = [{"video_file": file_re.search(lines[i]).group(1),
              "duration": datetime.strptime(duration_re.search(lines[i+1]).group(1), fmt) \
                - datetime.strptime('00:00:00', fmt)}
              for i in xrange(0, len(lines), 3)]
pprint.pprint(durations)
