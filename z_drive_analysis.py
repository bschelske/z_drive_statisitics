import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Replace 'your_file.csv' with the path to your CSV file.
df = pd.read_csv(r'/20240524_z_drive_path_statistics.csv')
df['Percent Utilzation'] = (df['Folder Size (bytes)'] / df['Folder Size (bytes)'].max()) * 100

DIVISIONS = 30
sorted_df = df.sort_values(by='Folder Size (bytes)', ascending=False).head(DIVISIONS)

sorted_df['Size'] = sorted_df['Folder Size (bytes)']//(1e+9)
sorted_df=sorted_df.sort_values(by='Size')
plt.style.use('ggplot')
fig, ax = plt.subplots()
colors = [plt.cm.RdYlGn(i / DIVISIONS) for i in range(DIVISIONS)]
# bars = sorted_df.plot(kind='barh', y='Size', x='Path', color=colors[::-1])
bars = ax.barh(sorted_df['Path'], sorted_df['Size'], color=colors[::-1])
print(bars)
ax.bar_label(bars)

ax.xaxis.grid(True)
plt.xlabel('Size (gb)')




# Set axis color
plt.gca().tick_params(axis='x')
plt.gca().tick_params(axis='y')

# Set label color
plt.ylabel(None)

#
plt.title('Z-Drive Usage Estimation\n(1 folder depth)')
plt.show()