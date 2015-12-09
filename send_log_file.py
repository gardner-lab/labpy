import smtplib
from email.mime.text import MIMEText
import os
import sys


def main():
    if len(sys.argv) < 2:
        print('You need to supply an email address to this program!')
        raise new Exception('No Email Supplied')
    else:
        email_address = sys.argv[1]
    if os.path.exists('/tmp/gbf.log'):
        with open('tmp.log', 'r') as f:
            msg = f.read()
            mail = MIMEText(msg)
            mail['Subject'] = 'Today\'s Birdsong Saving Log'
            mail['From'] = 'Gardnerlab Work Computer'
            mail['To'] = email_address
            s = smtplib.SMTP('smtp.bu.edu')
            s.sendmail('work_computer@glab.com', email_address, mail.as_string())
            s.quit()
        os.remove('/tmp/gbf.log')


if __name__ == "__main__":
    main()
