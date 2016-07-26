# Scripts Used By the Gardner Lab

A collection of python scripts people in the lab use to extract audio form
recording room computers, and distribute these recordings to a users local
computer for analysis.

**Important:** some of these scripts rely on the OSX file structure and may
not work as intended on a Windows machine (for instance: Matlab install dir).

The mose useful file is:

## get_todays_wav_files.py

This is a python script that copies audio files from our recording room computer,
moves them to the user's computer, and extracts only the segments of the file
that contain bird calls and songs. It can be run as an executable.

### Installation Prerequisites:

  1. Make sure you have MATLAB also installed on your computer. This script assumes MATLAB is located in your `/Applications` folder
  1. Download Jeff Markowitz's song extraction code [jmarkow](https://github.com/jmarkow/). Repos needed are:
      - [markolab](https://github.com/jmarkow/markolab)
      - [zftftb](https://github.com/jmarkow/zftftb)
      - [robofinch](https://github.com/jmarkow/robofinch)
  1. Make sure the recording computer's 'recording' folder is mounted on your computer using 
  `cmd+shift+k` in finder on your mac, and search for Recording Computer 2
      - It should be mounted at `/Volumes/recording`, because the script assumes this path.
  1. To set up to run daily, open up your terminal and type (`crontab -e`). Then refer to [the set-up](#crontab-set-up)
      - To edit the crontab in nano, type:
        ```bash
        env EDITOR=nano crontab -e
        ```
      - (Or use emacs and become a wizard like Ben :zap:)

## Use a configuration file

Store all the information you need in this simple json format shown below.
You can configure the recording channels to copy over, the bird names, and
the output directories for each bird (or all the birds if you choose).

```json
{
  "output": "/Volumes/Untitled/winSongData/", // default savepath
  "birds": [
    {"name": "lny29-post",
    "channel": "11"},
    {"name": "lny29-post",
    "channel": "11",
    "output": "/Volumes/Untitled/winSongData/"} // override the default savepath for specific birds
  ]
}
```

### Crontab set-up
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
