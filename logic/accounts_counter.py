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

bbva_accumulator = {}

unique_accounts = set()

count = 0

for record in F170404_list:
    account = record[0:18]
    value_1 = int(record[19:33])
    value_2 = int(record[34:48])
    if account in bbva_accumulator.keys():
        old_value_1 = bbva_accumulator[account][0]
        old_value_2 = bbva_accumulator[account][1]
        new_value_1 = old_value_1 + value_1
        new_value_2 = old_value_2 + value_2
        bbva_accumulator[account] = [new_value_1, new_value_2]
    else:
        bbva_accumulator[account] = [value_1, value_2]
    unique_accounts.add(account)
    count += 1
    print(count)

p_file.write("Total unique accounts: " + str(len(unique_accounts)) + "\n")
p_file.flush()
execution_time = time() - start_time
p_file.write("Accumulation values execution time: " + str(timedelta(seconds=execution_time)) + "\n")
p_file.flush()

path = BBVA_Accounts_root.ROOT_DIR + os.path.sep + 'results' + os.path.sep

result_file = open(path + "BBVA_Accounts-Results.csv", 'a')
good_accounts_file = open(path + "BBVA_Accounts-GoodAccountsResults.csv", 'a')
bad_accounts_file = open(path + "BBVA_Accounts-BadAccountsResults.csv", 'a')

count = 0

good_accounts_count = 0
bad_accounts_count = 0

for account in bbva_accumulator:
    result_file.write(account + ";" + str(bbva_accumulator[account][0]) + ";" + str(bbva_accumulator[account][1]) + "\n")
    result_file.flush()
    if bbva_accumulator[account][0] == bbva_accumulator[account][1]:
        good_accounts_file.write(account + ";" + str(bbva_accumulator[account][0]) + ";" + str(bbva_accumulator[account][1]) + "\n")
        good_accounts_file.flush()
        good_accounts_count += 1
    else:
        bad_accounts_file.write(account + ";" + str(bbva_accumulator[account][0]) + ";" + str(bbva_accumulator[account][1]) + "\n")
        bad_accounts_file.flush()
        bad_accounts_count += 1
    count += 1
    print(count)

p_file.write("Total good accounts: " + str(good_accounts_count) + "\n")
p_file.flush()
p_file.write("Total bad accounts: " + str(bad_accounts_count) + "\n")
p_file.flush()
execution_time = time() - start_time
p_file.write("Results generation execution time: " + str(timedelta(seconds=execution_time)) + "\n")
p_file.flush()
