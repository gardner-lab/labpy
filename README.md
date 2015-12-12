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
      4. to set up to run daily, set up a crontab in terminal. To do this in nano,, type:
      ```bash
      env EDITOR=nano crontab -e
      ```
        To run every day,( for each bird) at 10PM:
        ```bash
        % 0 21  * * * python /'PY_PATH'/lappy/get_todays_wav_files.py -l -b BIRDID -c BOXID -d /DESTINATION_PATH
        ```

        Where...
```
        PY_PATH = the path to the dir containing the python scripts

        BIRDID = the bird ID

        BOXID = the box ID

        DESTINATION PATH = the path where the data is pumped out
```
        Each bird should be entered in on a different line, separated by ~20 minutes, to assure jobs don't accumulate in the cue.

        A log file, to be emailed daily right before midnight, can be exported as well:
 		```bash
  		59 23 * * * python /PY_PATh/lappy/send_log_file.py example@example.edu
 		```
