import BBVA_Accounts_root
from datetime import timedelta, datetime
from time import time
import os

start_time = time()
date = datetime.today().strftime("%Y_%m_%d-%H_%M_%S")
path_to_file = date + " - BBVA_Accounts_Performance.txt"
p_file = open(path_to_file, 'a')
p_file.write(date + " Accumulation Values - Local Execution \n")
p_file.flush()
p_file.write("Reading file: F170404.txt" + "\n")
p_file.flush()
path = BBVA_Accounts_root.ROOT_DIR + os.path.sep + 'data' + os.path.sep
F170404_file = open(path + "F170404.txt")
F170404_list = F170404_file.read().splitlines()

unique_accounts = set()
bbva_accounts = []

for record in F170404_list:
    account = record[0:18]
    value_1 = int(record[19:33])
    value_2 = int(record[34:48])
    unique_accounts.add(account)
    bbva_accounts.append([account, value_1, value_2])

p_file.write("Total unique accounts: " + str(len(unique_accounts)) + "\n")
p_file.flush()
execution_time = time() - start_time
p_file.write("Read file execution time: " + str(timedelta(seconds=execution_time)) + "\n")
p_file.flush()
p_file.write("Accumulating values ... " + "\n")
p_file.flush()

bbva_accumulator = {}
accumulator_value_1 = 0
accumulator_value_2 = 0

count = 0

for account in unique_accounts:
    for record in bbva_accounts:
        if account == record[0]:
            accumulator_value_1 += record[1]
            accumulator_value_2 += record[2]
    bbva_accumulator[account] = [accumulator_value_1, accumulator_value_2]
    accumulator_value_1 = 0
    accumulator_value_2 = 0
    count += 1
    print(count)

execution_time = time() - start_time
p_file.write("Accumulation values execution time: " + str(timedelta(seconds=execution_time)) + "\n")
p_file.flush()

result_file = open("BBVA_Accounts-Results.csv", 'a')
good_accounts_file = open("BBVA_Accounts-GoodAccountsResults.csv", 'a')
bad_accounts_file = open("BBVA_Accounts-BadAccountsResults.csv", 'a')

count = 0

for account in bbva_accumulator:
    result_file.write(account + ";" + str(bbva_accumulator[account][0]) + ";" + str(bbva_accumulator[account][1]) + "\n")
    result_file.flush()
    if bbva_accumulator[account][0] == bbva_accumulator[account][1]:
        good_accounts_file.write(account + ";" + str(bbva_accumulator[account][0]) + ";" + str(bbva_accumulator[account][1]) + "\n")
        good_accounts_file.flush()
    else:
        bad_accounts_file.write(account + ";" + str(bbva_accumulator[account][0]) + ";" + str(bbva_accumulator[account][1]) + "\n")
        bad_accounts_file.flush()
    count += 1
    print(count)

execution_time = time() - start_time
p_file.write("Results generation execution time: " + str(timedelta(seconds=execution_time)) + "\n")
p_file.flush()
