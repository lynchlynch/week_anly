import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

data = {
    'China': [2, 1200, 1300, 1400, 1500, 1600, 1700, 1800, 1900, 2500],
    'America': [1200, 1300, 1400, 1500, 1600, 1700, 1800, 1900, 2000, 2100],
    'Britain': [1000, 1200, 1300, 1400, 1500, 1600, 1700, 1800, 1900, 2000],
    "Russia": [800, 1000, 1200, 1300, 1400, 1500, 1600, 1700, 1800, 1900]
}
df = pd.DataFrame(data)

# df.plot.box(title="Consumer spending in each country", vert=False)
df.plot.box(title="Consumer spending in each country")

plt.grid(linestyle="--", alpha=0.3)
plt.show()