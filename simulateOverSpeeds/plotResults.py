import matplotlib.pyplot as plt
import pandas as pd

data = pd.read_csv("./results.csv")
print(data)

plt.plot(data["speed"], data["CD"])

plt.show()
