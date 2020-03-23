import csv
import sys
import os
import math
from datetime import datetime
from pytz import timezone

# with open('eggs.csv', newline='') as csvfile:
#     spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
#     for row in spamreader:
#         print(', '.join(row))
#
# with open('names.csv', 'w', newline='') as csvfile:
#     fieldnames = ['first_name', 'last_name']
#     writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
#
#     writer.writeheader()
#     writer.writerow({'first_name': 'Baked', 'last_name': 'Beans'})
#     writer.writerow({'first_name': 'Lovely', 'last_name': 'Spam'})
#     writer.writerow({'first_name': 'Wonderful', 'last_name': 'Spam'})

fieldnames = [  'rounds', 'condition', 'investment', 'investment x 3',
                '% returned', 'amount returned', 'PPT round profit', 'RA round profit',
                'PPT block total profit', 'RA block total profit', 'date', 'time', 'P_id', 'RA_id']

def round(num):
    rounding = num - math.floor(num)
    if rounding >= 0.5:
        return math.ceil(num)
    else:
        return math.floor(num)

def extractData(reader, participant_id):

    start = False
    with open(participant_id + '.csv', 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        # writer.writerow({ 'rounds': 1, 'condition': 1 })

        roundNum = 1
        condition = None
        investment = None
        returnPercentage = None
        returnValue = None
        ppt_round_profit = None
        ra_round_profit = None
        ppt_total_profit = 0
        ra_total_profit = 0
        date = None
        time = None
        p_id = None
        ra_id = None

        for num, row in enumerate(reader):
            if (row['player.participant_number'] == participant_id):

                condition = row['player.condition_number']
                p_id = row['player.participant_number']

                date_data = row['participant.time_started']
                datetime_object = datetime.strptime(date_data, '%Y-%m-%d %H:%M:%S.%f%z')
                datetime_central = datetime_object.astimezone(timezone('US/Central'))

                date = datetime_central.strftime("%m/%d/%Y")
                time = datetime_central.strftime("%I:%M:%S %p")

                start = True
            if start:
                lineRoundNum = int(row['subsession.round_number'])

                if(roundNum != lineRoundNum):
                    writer.writerow({   'rounds': roundNum, 'condition': condition,
                                        'investment': investment, 'investment x 3': (investment * 3),
                                        '% returned': returnPercentage, 'amount returned': returnValue,
                                        'PPT round profit': ppt_round_profit, 'RA round profit': ra_round_profit,
                                        'PPT block total profit': ppt_total_profit, 'RA block total profit': ra_total_profit,
                                         'date': date, 'time': time, 'P_id': p_id, 'RA_id': ra_id})
                    if(roundNum == 40):
                        print('Exported file: \'', csvfile.name, '\'', sep='')
                        return
                    else:
                        roundNum += 1
                        if (roundNum - 1) % 10 == 0:
                            ppt_total_profit = 0
                            ra_total_profit = 0

                if row['group.invest'] == '':
                    investment = 0
                else:
                    investment = round(float(row['group.invest']))
                if row['group.reciprocate'] == '':
                    returnPercentage = 0
                else:
                    returnPercentage = float(row['group.reciprocate'])

                returnValue = round(investment * 3 * returnPercentage)
                if row['player.id_in_group'] == '1':
                    ppt_round_profit = math.floor((10 - investment) + returnValue)
                    ppt_total_profit += ppt_round_profit
                else:
                    ra_round_profit = math.floor((investment * 3) - returnValue)
                    ra_total_profit += ra_round_profit
                    if ra_id == None:
                        ra_id = row['player.participant_number']
    if not start:
        os.remove(participant_id + '.csv')
        print('Participant ID \'' + participant_id + '\' does not exist!')


def printFormated(reader):
    for row in reader:
        print(row['participant.code'], row['session.code'])

if __name__== "__main__":

    if(len(sys.argv) < 3):
        print('Error: Please enter file name and participant id!')
        print('Usage: \'python3 data_processor.py <data_file_name.csv> <participant_id>\'')
        quit()

    print('Running Jaye\'s OTREE Data Processor...')
    with open(sys.argv[1], newline='') as csvfile:
        reader = csv.DictReader(csvfile);
        data = extractData(reader, sys.argv[2])

# sys.argv
