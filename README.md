# Gardner Lab python scripts

## A collection of python scripts people in the lab use to extract audio form recording room computers, and distribute these recordings to a users local computer for analysis.

----

### Pieces:

- get_todays_wav_files
  - Python script that grabs recording files from our recording room computer, moves them to the user's computer, and extracts portions of the file that contain bird calls and songs.

    #### How to install:
      1. Make sure you have MATLAB also installed on your computer. This script assumes MATLAB is located at '/Applications/MATLAB_R2015a.app/bin'
      2. Download Jeff Markowitz's song extraction code [here](https://github.com/jmarkow/). Repos needed are:
        - markolab
        - zftftb
        - robofinch
      3. Make sure the recording computer's 'recording' folder is mounted on your computer using `cmd+shift+k` if you use a mac, and search for recording computer 2
