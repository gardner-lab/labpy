# Gardner Lab python scripts

## A collection of python scripts people in the lab use to extract audio form recording room computers, and distribute these recordings to a users local computer for analysis.

----

## get_todays_wav_files

- Python script that grabs recording files from our recording room computer, moves them to the user's computer, and extracts portions of the file that contain bird calls and songs.

#### How to install:
  1. Make sure you have MATLAB also installed on your computer. This script looks for any MATLAB installation in the Applications folder on your Mac.
  2. Download Jeff Markowitz's song extraction code [here](https://github.com/jmarkow/). Repos needed are:
    - [markolab](https://github.com/jmarkow/markolab)
    - [zftftb](https://github.com/jmarkow/zftftb)
    - [robofinch](https://github.com/jmarkow/robofinch)
  3. Make sure the recording computer's 'recording' folder is mounted on your computer using `cmd+shift+k` if you use a mac, and search for Recording Computer 2
    - It should be mounted at `/Volumes/recording`. The script assumes this path.
  4. To set up to run daily, set up a crontab in terminal (`crontab -e`). To edit the crontab in nano, type:
  ```bash
  env EDITOR=nano crontab -e
  ```

# New and Improved, use a configurable file instead of populating a crontab!
Example:
```json
{
  "output": "/Volumes/Untitled/winSongData/",
  "birds": [
    {"name": "lny29-post",
    "channel": "11"},
    {"name": "lny29-post",
    "channel": "11",
    "output": "/Volumes/Untitled/winSongData/"}
  ]
}
```
And add this to your crontab:

`0 21 * * * python PATH/get_todays_wav_files.py --config PATH_TO_CONFIG`

and:

`59 23 * * * python PY_PATH/send_log_file.py example@gmail.com`

# Otherwise, use the old method:

To run every day, (for each bird) at 10PM:
```bash
0 21 * * * python PY_PATH/get_todays_wav_files.py -l -b BIRDID -c BOXID -d DESTINATION_PATH
```

Where...
```
PY_PATH = the full path to where you saved labPy

BIRDID = the bird's ID/name

BOXID = the box ID i.e. the recording channel

DESTINATION PATH = the path where you want to save the processed data
```

Each bird should be entered in on a different line, separated by ~20 minutes, to assure the network where the files copy through does not choke.

You can choose to send an email with a summary of all birds copied over, using the `-l` flag, or per bird which is the default. To send the summary email, a second script needs to be run, after all the others:

```bash
59 23 * * * python PY_PATH/send_log_file.py example@gmail.com
```

You need to supply an email for this script, or else it will throw an exception.
