# import pandas as pd

s1_f = pd.read_csv("../temp_data/features/day11_team_out/merged/team_merged_train.csv")
s1_f_test = pd.read_csv("../temp_data/features/day11_team_out/merged/team_merged_test.csv")

xu_train = pd.read_csv("./xu_train.csv")
xu_test = pd.read_csv("./xu_test.csv")


cols = [c for c in xu_train.columns if c not in s1_f.columns or c == 'id' ]
cols = [c for c in cols if 'woe' not in c]
tr = s1_f.merge(xu_train[cols], on = 'id', how = 'left')

cols = [c for c in xu_test.columns if c not in s1_f_test.columns or c == 'id']
cols = [c for c in cols if 'woe' not in c]
tt = s1_f_test.merge(xu_test[cols], on = 'id', how = 'left')


# tr =  pd.read_csv('merge_xu.csv')
# tt =  pd.read_csv('merge_xu_test.csv')

tr_s = pd.read_csv('train_ser.csv')
te_s = pd.read_csv('test_s.csv')

new_train = tr.merge(tr_s, on = 'id', how = 'left')
new_test = tt.merge(te_s, on = 'id', how = 'left')

new_train.to_csv('final_train.csv', index=False)
new_test.to_csv('final_test.csv', index=False)

'''
python TimeSeriesFactor.py --input_path /Users/zhangzekun/Desktop/Files/codes/比赛模拟/初赛B榜数据集/testab/testab_bank_statement.csv --output_path test_s.csv --id_col id --time_col time --direction_col direction --amount_col amount  
把src丢到projects下
project的config，src的space都要改成yaml
init记得注释掉
'''

'''
run里面先做一份特征
raw里的文件名字
testab_bank_statement.csv       
train_bank_statement.csv
testab_with_amount.csv          
train.csv
'''

'''
d.columns.tolist()
19列
'id', 
'title', 
'career',
'zip_code',
'residence',
'loan',
'term',
'interest_rate',
'issue_time',
'syndicated',
'installment',
'record_time',
'history_time',
'total_accounts',
'balance_accounts',
'balance_limit',
'balance',
'level',
'label'
'''

'''
cols = df.columns.tolist()

move_last = ["id", "label"]

new_cols = [c for c in cols if c not in move_last] + move_last
df = df[new_cols]
'''

'''
import json

with open("lasso.json", "w", encoding="utf-8") as f:
    json.dump(list(d.columns), f, ensure_ascii=False, indent=4)

import json

with open("columns.json", "r", encoding="utf-8") as f:
    columns = json.load(f)

print(type(columns))
print(columns)

'''

'''
https://mirrors.aliyun.com/pypi/simple
python3.10 -m pip install wszzk==0.3.0 -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com

python3.10 -m pip show wszzk
'''