import subprocess
import os

def check_for_changes():
    if os.path.exists('.git'):
        output = subprocess.check_output(['git', 'status'])
        if 'not staged' in str(output):
            print('You have made changes to this repo, please commit them before running this')
            raise Exception('You have git changes! Please commit!')
    else:
        print('Not a git repository, folder probably downloaded')

def main():
    dirpath = os.path.dirname(os.path.realpath(__file__))
    print('Adding this directory to your bash profile...')
    with open(os.path.expanduser('~') + '.bash_profile', 'a') as f:
        f.write('\n\n#Added by add_to_bin.py from the labpy github directory\n')
        f.write('export PATH="$PATH:{}"\n\n'.format(dirpath))
    print('Making get_todays_wav_files an executable...')
    subprocess.call(['chmod', '+x', 'get_todays_wav_files.py'])
    print('Prepending your python path to that file...')
    with open('get_todays_wav_files.py', 'r+') as f:
        contents = f.read()
        contents = '#!' + contents

if __name__=='__main__':
    check_for_changes()
