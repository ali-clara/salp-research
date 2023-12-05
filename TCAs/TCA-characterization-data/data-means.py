# run from /force_data

import graphing_data
import pandas as pd

data_names = ["load-cell-data_1.csv", 
              "load-cell-data_2.csv", 
              "load-cell-data_3.csv"]

power_input = ["1W", "2W", "3W", "4W"]

avg_force_list = []
time_list = []
stdv_list = []

for power in power_input:
    raw_force_data, t, input_data = graphing_data.force_preprocessing(data_names, "force_data/"+power+"/")
    data_avg, data_stdv = graphing_data.find_data_avg(raw_force_data)

    avg_force_list.append(data_avg)
    time_list.append(t)
    stdv_list.append(data_stdv)

# print(avg_force_list)
# print("----------------------")
# print(time_list)
# print("----------------------")
# print(stdv_list)

force_data_formatted = list(zip(*[t,
                             avg_force_list[0], # 1W
                             stdv_list[0],
                             avg_force_list[1], # 2W
                             stdv_list[1],
                             avg_force_list[2], # 3W
                             stdv_list[2],
                             avg_force_list[3], # 4W
                             stdv_list[3],
                             ]))

column_titles = ["t (sec)", 
                 "1W force (mN)", "1W st dev",
                 "2W force (mN)", "2W st dev",
                 "3W force (mN)", "3W st dev",
                 "4W force (mN)", "4W st dev",
                 ]

df = pd.DataFrame(force_data_formatted, columns=column_titles)

print(df)

df.to_csv("force_data/averages.csv", index=False)



