import os
import datetime
import pyperclip


# issues:
# no checking if a current day report exists in report_archive
# this can lead to duplicate entries if the script is run more than once
# read lines and terminate if entry matching date is found
# potentially find next date entry and just update entry instead of exiting
# * will not work for night shift due to date changing before end of shift


def access_file(file_path, file_in_out, file_mode):
    if file_mode == 'r':
        # Read mode
        with open(file_path, 'r') as fr:
            lines = fr.readlines()
            for line in lines:
                file_in_out.append(line)
            fr.close()

    elif file_mode == 'x':
        # Write mode
        with open(file_path, 'x') as fw:
            fw.write(file_in_out)
            fw.close()


def main():
    daily_list = []
    archive_list = []

    current_date = datetime.date.today()
    current_date = current_date.strftime('%m-%d-%Y')

    previous_date = datetime.date.today() - datetime.timedelta(days=1)
    previous_date = previous_date.strftime('%m-%d-%Y')

    report_dir = os.path.abspath('/home/ANT.AMAZON.COM/vernehel/Documents/notes/work') + '/'

    report_daily_name = f'report_{previous_date}.md'
    report_daily_file = report_dir + report_daily_name

    report_archive_name = 'hog_archive.md'
    report_archive_file = report_dir + report_archive_name

    # if exists read daily report file
    if os.path.exists(report_daily_file):
        print(f'Found daily report: {report_daily_name} in {report_dir[:-1]}')
        access_file(report_daily_file, daily_list, 'r')

        # is daily report generated but not filled out?
        if daily_list != [f'### {previous_date}\n']:
            print('Daily report is not empty')
            print(f'"Prepending" {report_daily_name} to {report_archive_name}')

            # if report archive doesn't exist create it
            if not os.path.exists(report_archive_file):
                access_file(report_archive_file, '# HOG Report Archive\n\n', 'x')

            # read report archive
            access_file(report_archive_file, archive_list, 'r')

            # write to temp report archive
            i = ''.join(archive_list[:2]) + '\n' + ''.join(daily_list) + ''.join(archive_list[1:])
            access_file(report_archive_file[:-3] + '.tmp', i, 'x')

            # copy to clipboard
            pyperclip.copy(''.join(daily_list[1:])[:-2])
            print(f'{report_daily_name} copied to clipboard')

            # delete daily report and original report_archive, rename new one to replace old
            os.remove(report_archive_file)
            os.rename(report_archive_file[:-3] + '.tmp', report_archive_file)
            os.remove(report_daily_file)
            print(f'{report_archive_name} updated with report')

        else:
            print(f'ERROR: {report_daily_name} is empty')
            print('Exiting')
            exit()

    else:
        print(f'ERROR: {report_daily_name} not found')
        print('Exiting')
        exit()


if __name__ == '__main__':
    main()
