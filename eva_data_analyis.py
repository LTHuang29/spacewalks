import matplotlib.pyplot as plt
import pandas as pd

# https://data.nasa.gov/resource/eva.json (with modifications)
input_file= open('./eva_data.json', 'r', encoding='ascii')
output_file = open('./eva_data.csv','w', encoding='utf-8')
graph_file = './cumulative_eva_graph.png'

print("--Start--")
print("Reading data from JSON file {input_file}")
#read the data from a JSON file into a Pandas dataframe
eva_df = pd.read_json(input_file, convert_dates=['date'], encoding='ascii')
eva_df['eva'] = eva_df['eva'].astype(float)
#Clean the data by removing any rows where duration is missing or date is missing
eva_df.dropna(axis=0, subset=['duration','date'], inplace=True)

print(f'Saving to CSV file {output_file}')
#save dataframe to CSV file for later analysis
eva_df.to_csv(output_file, index=False, encoding='utf-8')

#sort dataframe by date ready to be plotted (date values are on x-axis)
eva_df.sort_values('date', inplace=True)
eva_df['cumulative_time'] = eva_df['duration_hours'].cumsum()

#plot cumulative time spent in space over years
plt.plot(eva_df['date'], eva_df['cumulative_time'], 'ko-')
plt.xlabel('Year')
plt.ylabel('Total time spent in space to date (hours)')
plt.tight_layout()
plt.savefig(graph_file)
plt.show()
print("--END--")
