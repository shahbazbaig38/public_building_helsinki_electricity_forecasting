import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_json('data/raw/energy_data.json')
# print(df.head())
# print(df.info())

plt.figure(figsize=(12, 6))
plt.plot(df['timestamp'], df['value'])
plt.show()