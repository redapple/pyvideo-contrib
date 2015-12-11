Uses:

- scrapy
- dateparser
- html2text
- prettytable
- fuzzywuzzy

```
cd ./pyconfr2015
scrapy crawl paullavideos -o videos.json
scrapy crawl pyconfrtalks -o talks.json
```


## Using  ffprobe to get durations

```
sh ffprobe_duration.sh > video_durations.txt
python parse_ffprobe.py > video_durations.json
```

