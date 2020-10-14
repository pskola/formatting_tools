import xlrd
import itertools
import pandas as pd

def orig_order_set(seq):
    seen = set()
    seen_add = seen.add
    return [x for x in seq if not (x in seen or seen_add(x))]

book = xlrd.open_workbook('C:\\Users\\pauli\\Downloads\\ForPaulina\\BETTER_TS\\MergeV2.xlsx')
sheet = book.sheet_by_name('MergeV2')

# To easily find column the numbers: Excel> File> Options> Formulas> Change reference style to R1C1
# Just remember to subtract 1.
subs = sheet.col_values(1)[1:]
acc = sheet.col_values(65)[1:]
comp = sheet.col_values(70)[1:]
ons = sheet.col_values(71)[1:]
sub_list = subset = orig_order_set(subs)

data = pd.DataFrame(list(zip(subs, acc, comp, ons)))
data.columns = ['sub', 'acc', 'comp', 'onset']
data['display'] = '1.5'
data['weight'] = '1'

data["cond"] = ""
data.loc[(data.acc == 0) | (data.comp == 9), "cond"] = "Err"
data.loc[(data.acc == 1) & (data.comp == 0), "cond"] = "Single"
data.loc[(data.acc == 1) & (data.comp == 1), "cond"] = "NS_comp"
data.loc[(data.acc == 1) & (data.comp == 2), "cond"] = "NS_incomp"
data.loc[(data.acc == 1) & (data.comp == 3), "cond"] = "SW_comp"
data.loc[(data.acc == 1) & (data.comp == 4), "cond"] = "SW_incomp"

Err = data[(data.acc == 0) | (data.comp == 9)]
Single = data[(data.acc == 1) & (data.comp == 0)]
NS_comp = data[(data.acc == 1) & (data.comp == 1)]
NS_incomp = data[(data.acc == 1) & (data.comp == 2)]
SW_comp = data[(data.acc == 1) & (data.comp == 3)]
SW_incomp = data[(data.acc == 1) & (data.comp == 4)]

cond_list = [Err, Single, NS_comp, NS_incomp, SW_comp, SW_incomp]
by_sub = [j[j['sub'] == i] for i in sub_list for j in cond_list]
columns_needed = ["onset", "display", "weight"]

for i in by_sub:
    i.to_csv(str(int(i.iloc[0,0])) + "_" + str(i.iloc[0,6]) + "V2.txt", header=False, columns=columns_needed, index=False, sep="\t")