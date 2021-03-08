import numpy as np
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt

# 两个样本数据密度分布图
# 多个密度图

rs1 = np.random.RandomState(2)  
rs2 = np.random.RandomState(5)
df1 = pd.DataFrame(rs1.randn(100,2)+2,columns = ['A','B'])
print(df1)
# df2 = pd.DataFrame(rs2.randn(100,2)-2,columns = ['A','B'])
# 创建数据

sns.kdeplot(df1['A'],df1['B'],cmap = 'Greens',
            shade = True,shade_lowest=False)
# sns.kdeplot(df2['A'],df2['B'],cmap = 'Blues',
#             shade = True,shade_lowest=False)
plt.show()