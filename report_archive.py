import os
import datetime
import pyperclip


# issues:
# no checking if a current day report exists in report_archive
# this can lead to duplicate entries if the script is run more than once
# read lines and terminate if entry matching date is found
# potentially find next date entry and just update entry instead of exiting


def main():

    daily_list = []
    archive_list = []

    current_date = datetime.date.today()
    current_date = current_date.strftime('%m-%d-%Y')

    report_dir = os.path.abspath('C:/Users/Heath/PycharmProjects/workReporter') + '/'
    report_daily = 'report_' + current_date + '.md'
    report_archive = 'hog_archive.md'

    # if exists read daily report file
    if os.path.exists(report_dir + report_daily):
        print(f'Found daily report: {report_daily} in {report_dir[:-1]}')

        with open(report_dir + report_daily, 'r') as rd:
            lines = rd.readlines()
            for line in lines:
                daily_list.append(line)

            # is daily report generated but not filled out?
            if daily_list != 'f[### {current_date}\n]':
                print('Daily report is not empty')
                print(f'"Prepending" {report_daily} to {report_archive}')

                # if report archive doesn't exist create it
                if not os.path.exists(report_dir + report_archive):
                    ra = open(report_dir + report_archive, 'x')
                    ra.write('# HOG Report Archive\n\n')
                    ra.close()

                # read report archive
                with open(report_dir + report_archive, 'r') as ra:
                    lines = ra.readlines()
                    for line in lines:
                        archive_list.append(line)

                # write to temp report archive
                with open(report_dir + report_archive + '.tmp', 'w') as new_file:

                    # split markdown title
                    new_file.write(''.join(archive_list[:2]))
                    new_file.write('\n')

                    # write daily report
                    new_file.write(''.join(daily_list))

                    # write report archive
                    new_file.write(''.join(archive_list[1:]))

                # copy to clipboard
                pyperclip.copy(''.join(daily_list[1:])[:-2])
                print(f'{report_daily} copied to clipboard')

                # delete original report_archive, rename new one to replace old
                os.remove(f'{report_dir}{report_archive}')
                os.rename(f'{report_dir}{report_archive}.tmp', f'{report_dir}{report_archive}')
                print(f'{report_archive} updated with report')

            else:
                print(f'ERROR: {report_daily} is empty')
                print('Exiting')
                exit()
    else:
        print(f'ERROR: {report_daily} not found')
        print('Exiting')
        exit()


if __name__ == '__main__':
    main()
