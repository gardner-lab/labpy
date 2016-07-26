import datetime
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed

def main():
    print('Format: year.month.day')
    from_date = raw_input('From: ')
    to_date = raw_input('To: ')
    bird = raw_input('Bird: ')
    ch = raw_input('Channel: ')
    from_dt = datetime.datetime.strptime(from_date, '%Y.%m.%d')
    to_dt = datetime.datetime.strptime(to_date, '%Y.%m.%d')
    def call_matlab(date):
        d = from_dt + datetime.timedelta(date)
        dstr = d.strftime('%Y.%m.%d')
        subprocess.call(['/Users/wgillis/py/labPy/get_todays_wav_files.py',
                        '--config',
                        '/Users/wgillis/py/labPy/win_recording_room_config.json', '--day', dstr])

    def make_date(d):
        return (from_dt + datetime.timedelta(d)).strftime('%Y.%m.%d')

    days = range((to_dt-from_dt).days)
    with ThreadPoolExecutor(max_workers=4) as executor:
        future_to_result = {executor.submit(call_matlab, d): d for d in days}
        for future in as_completed(future_to_result):
            print(make_date(future_to_result[future]))

if __name__ == '__main__':
    main()
