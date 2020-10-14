# Stim2.RESP and Stim3.RESP need to be combined. I counted the last answer.
# If no response for S2, take S3; if S2 and S3 given, take last S3; if S2 response only, take last S2; otherwise 0. 
# =IF(LEN(O2)<1,R2,IF(AND(LEN(O2)=1, LEN(R2)>=1), RIGHT(R2,1), IF(LEN(O2)>=1, RIGHT(O2,1), 0)))

# Fix accuracies using new responses
# =IF(Corr.ans=Resp.fix,1,0)

# Categorize the responses depending on whether the trial was a Target, a Lure, or a Foil, and whether the answer was correct or not.
# =IF(ObjectType="T",IF(Acc.fix=1, "REM", "FRGT"), IF(ObjectType="L", IF(Acc.fix=1, "CR", "FA"), "BLANK"))

# Run the following code:

import pandas as pd
import itertools
import xlrd

def divide_chunks(l, n): 
    for i in range(0, len(l), n):  
        yield l[i:i + n]
		
def orig_order_set(seq):
    seen = set()
    seen_add = seen.add
    return [x for x in seq if not (x in seen or seen_add(x))]

workbook = xlrd.open_workbook('Merged0730.xlsx')
worksheet = workbook.sheet_by_name('Sheet1')

# Your order of columns may vary; sub - subject IDs, dprime - categorized responses
sub = worksheet.col_values(7)[1:]
subset = orig_order_set(sub)
sub_enc = [list(itertools.repeat(i, 128)) for i in subset]
sub_enc = [item for sublist in sub_enc for item in sublist]

stim_enc = ["096","127","069","066","169","005","082","041","180","134",
            "146","108","192","018","140","030","061","086","152","002",
            "021","013","168","040","166","177","068","143","138","036",
            "015","028","044","029","048","060","183","155","073","010",
            "099","190","090","022","072","049","008","131","117","113",
            "055","111","027","035","098","175","070","053","058","123",
            "085","017","120","023","122","182","189","084","149","042",
            "114","172","144","119","051","150","185","025","178","170",
            "012","091","083","067","095","087","191","043","080","109",
            "124","137","129","133","112","103","094","065","132","148",
            "007","050","163","141","009","161","079","016","088","076",
            "037","142","116","089","139","184","032","047","167","006",
            "081","100","174","173","156","145","125","045"]
stim_ret = ["174","113","016","099","152","053","041","159","172","123",
            "163","051","050","160","105","060","034","076","007","049",
            "125","098","085","038","079","191","121","141","177","145",
            "109","161","059","033","017","036","081","169","176","071",
            "140","035","186","069","064","086","162","180","115","181",
            "047","129","006","028","090","063","150","065","073","132",
            "075","102","005","082","156","062","119","178","143","093",
            "021","091","111","158","106","025","103","012","104","084",
            "061","137","185","146","022","133","153","167","144","154",
            "097","187","151","020","039","157","018","095","013","037",
            "008","189","100","149","014","184","088","165","116","175",
            "057","055","080","046","164","077","015","030","166","114",
            "148","124","002","042","010","131","182","168","108","078",
            "027","092","054","074","130","134","138","024","043","026",
            "112","001","147","070","118","094","122","190","048","040",
            "058","056","004","192","171","072","173","044","101","126",
            "142","188","009","083","089","179","096","087","068","110",
            "170","183","067","135","136","117","045","003","032","011",
            "029","031","127","052","066","019","023","155","128","107",
            "120","139"]
rts = stim_ret*len(subset)

onset = worksheet.col_values(4)[1:129]
onsets = onset*len(subset) 

dprime = worksheet.col_values(18)[1:]
dps = list(divide_chunks(dprime, 192)) 

dict_ret = [dict(zip(stim_ret, dps[i])) for i in range(len(dps))]
rec = {k : v1 for k,v1 in zip(subset, dict_ret)}
res = [rec[j][i] for j in rec for i in stim_enc if i in rec[j]]

df = pd.DataFrame(list(zip(sub_enc, res, onsets)))
df.columns = ['sub', 'cond', "onset"]
df['display'] = '4'
df['weight'] = '1'

REM = df[df['cond'] == "REM"]
MISS = df[df['cond'] == "FRGT"]
CR = df[df['cond'] == "CR"]
FA = df[df['cond'] == "FA"]

cond_list = [REM, MISS, CR, FA]
by_sub = [j[j['sub'] == i].sort_values('onset') for i in subset for j in cond_list]

columns_needed = ["onset", "display", "weight"]
for i in by_sub:
    i.to_csv(str(int(i.iloc[0,0])) + "_" + str(i.iloc[0,1]) + ".txt", header=False, columns=columns_needed, index=False, sep="\t")