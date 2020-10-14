# check for reverse coding and multiple responses - fix manually in excel, then generate new accuracies. I counted the last response given, changed no response to 0.
# For reverse coding: =IF(CELL=1,4,IF(CELL=3,2,IF(CELL=4,1,IF(CELL=2,3,0))))
# For multiple responses: =VALUE(IF(ISBLANK(CELL), 0, IF(LEN(CELL>1),RIGHT(CELL,1),CELL)))

# Get onset time - copy from the template. TS should start at 30, then add 1.5 and ntimes. And add 30 second every 30 trials (in miliseconds).

# After preparing the data, run the code below. You need python installed, along with the packages (pandas and xlrd; use e.g., pip install pandas).

import xlrd
import itertools
import pandas as pd

def orig_order_set(seq):
    seen = set()
    seen_add = seen.add
    return [x for x in seq if not (x in seen or seen_add(x))]

book = xlrd.open_workbook('Merge_TS_edit.xlsx')
sheet = book.sheet_by_name('Merge_TS')

# Your order of columns may vary; subs - subject IDs, acc - fixed accuracy, switch - task condition (0,1,2), ons - onset time  
subs = sheet.col_values(1)[1:]
acc = sheet.col_values(64)[1:]
switch = sheet.col_values(67)[1:]
ons = sheet.col_values(69)[1:]

sub_list = subset = orig_order_set(subs)

data = pd.DataFrame(list(zip(subs, acc, switch, ons)))
data.columns = ['sub', 'acc', 'switch', 'onset']
#data = data[data.switch != 9]
data['display'] = '1.5'
data['weight'] = '1'

data["cond"] = ""
data.loc[(data.acc == 0) | (data.switch == 9), "cond"] = "Err"
data.loc[(data.acc == 1) & (data.switch == 0), "cond"] = "Single"
data.loc[(data.acc == 1) & (data.switch == 1), "cond"] = "DualNS"
data.loc[(data.acc == 1) & (data.switch == 2), "cond"] = "DualSW"

Err = data[(data.acc == 0) | (data.switch == 9)]
Single = data[(data.acc == 1) & (data.switch == 0)]
DualNS = data[(data.acc == 1) & (data.switch == 1)]
DualSW = data[(data.acc == 1) & (data.switch == 2)]

cond_list = [Err, Single, DualNS, DualSW]
by_sub = [j[j['sub'] == i] for i in sub_list for j in cond_list]
columns_needed = ["onset", "display", "weight"]

for i in by_sub:
    i.to_csv(str(int(i.iloc[0,0])) + "_" + str(i.iloc[0,6]) + ".txt", header=False, columns=columns_needed, index=False, sep="\t")