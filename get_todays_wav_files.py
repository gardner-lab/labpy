#!/usr/bin/env python
import datetime
import os
from os.path import join
import subprocess
import glob
import shutil
import smtplib
from email.mime.text import MIMEText
import argparse
import time
import sys
import json

__author__ = 'Winthrop Gillis'

def find_matlab():
    '''Returns the most recent installed MATLAB in the Applications folder'''
    #Right now only runs on MacOS
    if sys.platform == 'darwin':
        matlabs = sorted(glob.glob('/Applications/MATLAB*'), reverse=True)
    else:
        # TODO: add compatibility for windows OS
        raise OSError('Script optimized for MacOS')
    return join(matlabs[0], 'bin', 'matlab')

def get_recording_path():
    path = '/Volumes'
    if os.path.exists(join(path, 'recording')):
        return join(path, 'recording')
    elif os.path.exists(join(path, 'raid1', 'recording')):
        return join(path, 'raid1', 'recording')
    else:
        raise OSError('Recording path does not exist! Please mount drive')

def get_date(args=None):
    '''Returns a datetime given the arguments'''
    if args and args.day:
        y, m, d = args.day.split('.')
        day = datetime.date(year=int(y), month=int(m), day=int(d))
    else:
        day = datetime.date.today()
    return day

def make_day_folder(path, bird_name, day):
    '''Returns the path where new files will be saved'''
    folder_path = join(path, bird_name, day.isoformat())
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    return folder_path

def get_file_filter(day):
    file_filter = day.strftime('%Y.%m.%d')
    return file_filter

def get_input_folders(file_filter, channel_number):
    recording_path = get_recording_path()
    recording_folder = join(recording_path, '{0}-WAV'.format(channel_number))
    images_folder = join(recording_path, '{0}-IMG'.format(channel_number))
    return recording_folder, images_folder

def get_wavfiles(path, file_filter):
    return glob.glob(join(path, '*{0}*.wav'.format(file_filter)))

def get_imagefiles(path, file_filter):
    return glob.glob(join(path, '*{0}*.jpg'.format(file_filter)))

def transfer_files(files, path):
    for f in files:
        try:
            shutil.move(f, path)
        except Exception as e:
            print(e)
    return

def remove_files(files):
    for f in files:
        os.remove(f)
    return

def run_matlab():
    print('Running Matlab')
    subprocess.check_output([find_matlab(), '-nodesktop', '-nosplash', '-r',
                "zftftb_song_chop(pwd, 'song_duration', 0.65, 'audio_pad', 0.5, 'song_ratio', 2.8, 'song_thresh', 0.2); exit"])
    return

def cli(args):
    channel_number = args.c
    bird_name = args.b
    directory = args.d

    day = get_date(args)

    file_filter = get_file_filter(day)
    # the following line for debugging purposes
    # print(file_filter)

    # makes a new folder for every day
    folder_path = make_day_folder(directory, bird_name, day)

    # move files one by one to new folder
    recording_folder, images_folder = get_input_folders(file_filter, channel_number)

    wavfiles = get_wavfiles(recording_folder, file_filter)

    # For debugging
    # print('Moving files')

    if wavfiles:
        transfer_files(wavfiles, folder_path)
        img_files = get_imagefiles(images_folder, file_filter)
        # for debugging
        # print('Removing Images')
        remove_files(img_files)

    # run matlab script on files for song detection
    os.chdir(folder_path)

    if wavfiles:
        run_matlab()

        # remove all 40 second snippets
        files = glob.glob(join(folder_path, '*.wav'))
        remove_files(files)

        with open('/tmp/gbf.log', 'a') as f:
            msg = 'Bird: {0}\nChannel: {1}\nDate: {2}\nSaved path: {3}\n{4}\n'
            msg = msg.format(bird_name, channel_number, file_filter, folder_path, '-'*10)
            f.write(msg)

    else:
        with open('/tmp/gbf.log', 'a') as f:
            msg = 'No wav files found for bird {0} on {1}\n{2}\n'
            msg = msg.format(bird_name, file_filter, '-'*10)
            f.write(msg)


def config(args):
    with open(args.config, 'r') as f:
        birds = json.load(f)
    day = get_date(args)
    file_filter = get_file_filter(day)

    # birds is an array of config variables
    for bird in birds['birds']:
        output = bird.get('output', birds['output'])
        save_path = make_day_folder(output, bird['name'], day)
        rec_folder, img_folder = get_input_folders(file_filter, bird['channel'])
        wav = get_wavfiles(rec_folder, file_filter)
        if wav:
            transfer_files(wav, save_path)
            img = get_imagefiles(img_folder, file_filter)
            remove_files(img)
            os.chdir(save_path)

            run_matlab()

            files = glob.glob(join(save_path, '*.wav'))
            remove_files(files)

            with open('/tmp/gbf.log', 'a') as f:
                msg = 'Bird: {0}\nChannel: {1}\nDate: {2}\nSaved path: {3}\n{4}\n'
                msg = msg.format(bird['name'], bird['channel'], file_filter, save_path, '-'*10)
                f.write(msg)
        else:
            with open('/tmp/gbf.log', 'a') as f:
                msg = 'No wav files found for bird {0} on {1}\n{2}\n'
                msg = msg.format(bird['name'], file_filter, '-'*10)
                f.write(msg)




def main():
    start = time.time()
    parser = argparse.ArgumentParser()
    parser.add_argument('-b', type=str)
    parser.add_argument('-d', type=str)
    parser.add_argument('-c', type=str)
    parser.add_argument('--day', type=str)
    parser.add_argument('--config', type=str, help='Path to config file')
    # parser.add_argument('-l', action='store_true', help='Appends output to a log file')
    args = parser.parse_args()

    if args.config:
        config(args)
    else:
        cli(args)

    end = time.time()
    print('Done. Finished in {} seconds'.format(end-start))


if __name__ == '__main__':
    main()
