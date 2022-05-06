import os
import datetime


def main():

    current_date = datetime.date.today()
    current_date = current_date.strftime('%m-%d-%Y')

    report_dir = os.path.abspath('/home/ANT.AMAZON.COM/vernehel/Documents/notes/work') + '/'
    report_daily = f'report_{current_date}.md'

    if not os.path.exists(report_dir + report_daily):
        print(f'File does not exist, creating {report_daily} in {report_dir}')
        rd = open(report_dir + report_daily, 'x')
        rd.write(f'### {current_date}\n')
        rd.close()
    else:
        print(f'File does exist, found {report_daily} in {report_dir[:-1]}')
        print('Exiting')
        exit()


if __name__ == '__main__':
    main()
