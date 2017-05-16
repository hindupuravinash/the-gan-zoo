import re
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

readme = open("README.md").read()

data_string = re.findall("\*.*arxiv.org\/abs\/(\d{2})(\d{2})", readme)
data = np.array([2000 + int(year) + int(month) / 12 for year, month in data_string])

plt.hist(data, 100, cumulative="True")
plt.xticks(range(2014, 2018))
plt.yticks(np.arange(0,100, 10))
plt.title("Cumulative number of GAN papers by year")
plt.xlabel("Year")
plt.ylabel("Total number of papers")
plt.show()
