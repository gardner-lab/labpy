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

### Script summary

When run with the proper commandline arguments, this script will move
files from the GardnerLab Recording Room Computer. These files are only
associated with the recording channel(s) and the date of recording
that you specify.

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

`0 21 * * * python [path to this script]/get_todays_wav_files.py --config [path to config file]`

`0 21 * * *` means it will run this script every day at 21:00 (or 11:00 PM).


and:

`0 8 * * * python [path to this script]/send_log_file.py example@gmail.com`

The second script will send an email to example@gmail.com at 8:00 AM
to give a status update from the script. It will send you information
on which audio files were copied over, and if the script could not find
any new files for the day.

### The Old Method

This method was the first implementation, and still works, put is not
recommended to use, because it is tedious to write the following code
for each bird that needs files copied. It allowed for more errors.

To run every day, (for each bird) at 10PM:

```bash
0 21 * * * python PY_PATH/get_todays_wav_files.py -b BIRDID -c BOXID -d DESTINATION_PATH
```

Where...
```
PY_PATH = the full path to where you saved labPy

BIRDID = the bird's ID/name

BOXID = the box ID i.e. the recording channel

DESTINATION PATH = the path where you want to save the processed data
```

Each bird should be entered in on a different line, separated by ~20 minutes, to assure the network where the files copy through does not choke.

The same summary email as above can be sent with the same command:

```bash
0 8 * * * python PY_PATH/send_log_file.py example@gmail.com
```

You need to supply an email for this script, or else it will throw an exception.
