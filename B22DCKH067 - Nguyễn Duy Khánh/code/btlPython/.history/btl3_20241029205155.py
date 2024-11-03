import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

# Đọc dữ liệu từ file CSV
data = pd.read_csv('results.csv')  # Thay 'results.csv' bằng tên file của bạn

# Chọn các chỉ số để phân cụm
features = ['Age', 'matches played', 'minutes', 'Assists', 'non-Penalty Goals', 'Yellow Cards', 'Red Cards']

# Tiêu chuẩn hóa dữ liệu
scaler = StandardScaler()
data_scaled = scaler.fit_transform(data[features])

# Áp dụng K-means
kmeans = KMeans(n_clusters=5, random_state=0)  # Số lượng nhóm là 5
data['Cluster'] = kmeans.fit_predict(data_scaled)

# Sử dụng PCA để giảm số chiều xuống 2
pca = PCA(n_components=2)
data_pca = pca.fit_transform(data_scaled)

# Thêm các thông tin PCA vào DataFrame
data['PCA1'] = data_pca[:, 0]
data['PCA2'] = data_pca[:, 1]

# Tạo lưới để tô màu các vùng
x_min, x_max = data['PCA1'].min() - 1, data['PCA1'].max() + 1
y_min, y_max = data['PCA2'].min() - 1, data['PCA2'].max() + 1
xx, yy = np.meshgrid(np.arange(x_min, x_max, 0.01),
                     np.arange(y_min, y_max, 0.01))

# Dự đoán nhãn cho từng điểm trong lưới
Z = kmeans.predict(pca.inverse_transform(np.c_[xx.ravel(), yy.ravel()]))
Z = Z.reshape(xx.shape)

# Vẽ vùng màu
plt.figure(figsize=(12, 8))
plt.contourf(xx, yy, Z, alpha=0.5, cmap='viridis')

# Vẽ các điểm dữ liệu
sns.scatterplot(x='PCA1', y='PCA2', hue='Cluster', data=data, palette='viridis', s=100, edgecolor='k')
plt.title('K-means Clustering of Football Players')
plt.xlabel('PCA 1')
plt.ylabel('PCA 2')
plt.legend(title='Cluster')
plt.show()
