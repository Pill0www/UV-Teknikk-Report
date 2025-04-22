import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("converted_log.csv")
plt.plot(df["time"], df["depth"])  # Adjust columns as needed
plt.xlabel("Time")
plt.ylabel("Depth")
plt.title("ROV Depth over Time")
plt.show()
