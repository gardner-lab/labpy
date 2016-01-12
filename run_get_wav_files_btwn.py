import datetime
import subprocess

def main():
    print('Format: year.month.day')
    from_date = raw_input('From: ')
    to_date = raw_input('To: ')
    bird = raw_input('Bird: ')
    ch = raw_input('Channel: ')
    from_dt = datetime.datetime.strptime(from_date, '%Y.%m.%d')
    to_dt = datetime.datetime.strptime(to_date, '%Y.%m.%d')
    for day in range((to_dt-from_dt).days):
        print('In this loop')
        d = from_dt + datetime.timedelta(days=day)
        day_format = d.strftime('%Y.%m.%d')
        print(day_format)
        print(bird)
        print(ch)
        # TODO: make the file location work on all computers
        subprocess.call(['/Users/wgillis/py/labPy/get_todays_wav_files.py',
                        '-l', '-b', bird, '-c', ch, '-d', '/Volumes/Untitled/winSongData/',
                        '--day', day_format])

if __name__ == '__main__':
    main()
