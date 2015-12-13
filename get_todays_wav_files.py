import datetime
import os
import subprocess
import glob
import shutil
import smtplib
from email.mime.text import MIMEText
import argparse
import time
import sys

__author__ = 'Winthrop Gillis'

def find_matlab():
    '''Returns the most recent MATLAB in the Applications folder'''
    #Right now only runs on MacOS
    if sys.platform == 'darwin':
        matlabs = sorted(glob.glob('/Applications/MATLAB*'), reverse=True)
    else:
        # TODO: add compatibility for windows OS
        pass
    return matlabs[0]


def main():
    start = time.time()
    parser = argparse.ArgumentParser()
    parser.add_argument('-b', type=str)
    parser.add_argument('-d', type=str)
    parser.add_argument('-c', type=str)
    parser.add_argument('--day', type=str)
    parser.add_argument('-l', action='store_true', help='Appends output to a log file')
    args = parser.parse_args()
    channel_number = args.c
    bird_name = args.b
    matlab_path = os.path.join(find_matlab(), 'bin', 'matlab')
    # assumes you run this in the main directory you want to store your data
    directory = args.d
    if args.day:
        y, m, d = args.day.split('.')
        day = datetime.date(year=int(y), month=int(m), day=int(d))
    else:
        day = datetime.date.today()
    file_filter = day.strftime('%Y.%m.%d')
    print(file_filter)
    # makes a new folder for every day
    folder_path = os.path.join(directory, bird_name, day.isoformat())
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    # move files one by one to new folder
    recording_folder = os.path.join('/Volumes', 'recording', '{0}-WAV'.format(channel_number))
    images_folder = os.path.join('/Volumes', 'recording', '{0}-IMG'.format(channel_number))
    wavfiles = glob.glob(os.path.join(recording_folder, '*{0}*.wav'.format(file_filter)))
    print('Moving files')
    for file in wavfiles:
        shutil.move(file, folder_path)

    if wavfiles:
        files = glob.glob(os.path.join(images_folder, '*{0}*.jpg'.format(file_filter)))
        print('Removing Images')
        for file in files:
            os.remove(file)
    # run matlab script on files for song detection
    os.chdir(folder_path)
    if wavfiles:
        print('Running Matlab')
        subprocess.check_output([matlab_path, '-nodesktop', '-nosplash', '-r',
                    "zftftb_song_chop(pwd, 'song_duration', 0.65, 'audio_pad', 0.5, 'song_ratio', 2.8, 'song_thresh', 0.2); exit"])
    # remove all 40 second snippets
        files = glob.glob(os.path.join(folder_path, '*.wav'))
        for file in files:
            os.remove(file)
        if args.l:
            with open('/tmp/gbf.log', 'a') as f:
                msg = 'Bird: {0}\nChannel: {1}\nDate: {2}\nSaved path: {3}\n{4}\n'
                msg = msg.format(bird_name, channel_number, file_filter, folder_path, '-'*10)
                f.write(msg)
            # add iformation to log file and have the user invoke another script
            # to send the file over email
        else:
            message = ''.join(['Sound files for {0} in recording box {1} have been moved to {2}',
                                '\n\nIf you are not recording from {0} any more please remove',
                                'the line:\n\n"python get_todays_wav_files.py -b {0} -c {1} -d {3}"\n',
                                'from your crontab with "crontab -e"']).format(bird_name, channel_number, folder_path, directory)

            msg = MIMEText(message)
            msg['Subject'] = '{0}\'s recording has been saved'.format(bird_name)
            msg['From'] = 'Winthrop Gillis (work computer)'
            msg['To'] = 'wgillis@bu.edu'
            s = smtplib.SMTP('smtp.bu.edu')
            s.sendmail('win_work_computer@glab.com', 'wgillis@bu.edu', msg.as_string())
            s.quit()
    elif args.l:
        with open('/tmp/gbf.log', 'a') as f:
            msg = 'No wav files found for bird {0} on {1}'
            msg = msg.format(bird_name, file_filter)
            f.write(msg)
    else:
        print('No wav files found')

    # send email of summary and disk usage
    end = time.time()
    print('Done. Finished in {} seconds'.format(end-start))

if __name__ == '__main__':
    main()
