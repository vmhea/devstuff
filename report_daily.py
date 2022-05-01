import os.path
import datetime


def main():

    current_date = datetime.date.today()
    current_date = current_date.strftime('%m-%d-%Y')

    report_dir = os.path.abspath('C:/Users/Heath/PycharmProjects/workReporter') + '/'
    report_daily = 'report_' + current_date + '.md'

    if not os.path.exists(report_dir + report_daily):
        print(f'File does not exist, creating {report_daily} in {report_dir}')
        rd = open(report_dir + report_daily, 'x')
        rd.write('### ' + current_date + '\n')
        rd.close()
    else:
        print('File does exist, found ' + report_daily + 'in ' + report_dir[:-1])
        print('Exiting')
        exit()


if __name__ == '__main__':
    main()