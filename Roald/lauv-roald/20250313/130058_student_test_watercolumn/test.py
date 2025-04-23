import re
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# Parse log data
log_entries = []
with open('Roald/lauv-roald/20250313/130058_student_test_watercolumn/Output.txt', 'r') as f:
    for line in f:
        entry = {}
        # Extract timestamp
        timestamp_str = re.search(r'\[(.*?)\]', line).group(1)
        entry['timestamp'] = datetime.strptime(timestamp_str, '%Y/%m/%d %H:%M:%S')
        
        # Extract log level and component
        parts = line.split('] - ')
        log_info = parts[1].split(' >> ')[0]
        log_level = log_info.split(' ')[0]
        component = log_info.split('[')[-1].replace(']', '')
        
        entry['level'] = log_level
        entry['component'] = component
        entry['message'] = parts[1].split(' >> ')[-1].strip()
        
        log_entries.append(entry)

df = pd.DataFrame(log_entries)

# 1. Fuel Warnings Over Time (updated resampling)
fuel_df = df[df['message'] == 'fuel is running low']
fuel_counts = fuel_df.resample('1min', on='timestamp').size()  # Changed '1T' to '1min'

plt.figure(figsize=(12, 6))
fuel_counts.plot(title='Fuel Warnings Over Time', color='red')
plt.ylabel('Warnings per Minute')
plt.grid(True)
plt.tight_layout()
# plt.savefig('fuel_warnings.png')
# plt.close()

# Rest of the script remains the same...