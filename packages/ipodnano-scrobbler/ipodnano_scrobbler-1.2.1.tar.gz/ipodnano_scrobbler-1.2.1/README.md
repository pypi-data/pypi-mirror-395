# iPod Nano scrobbler

Upload your iPod music listening stats on last.fm.

Tested on the iPod Nano 6th gen. Previous generations probably won't work, the 7th generation might.

```
usage: ipodnano_scrobble [-h] --ipod_path IPOD_PATH [--skipcount SKIPCOUNT] [--days DAYS]

options:
  -h, --help            show this help message and exit
  --ipod_path IPOD_PATH
                        Path to the iPod's 'iTunes Library.itlp' folder
  --skipcount SKIPCOUNT
                        Skip songs with this or more recent plays
  --days DAYS           Skip playcounts older than this
```