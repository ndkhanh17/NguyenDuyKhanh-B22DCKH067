import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

# Đọc dữ liệu từ file CSV
df = pd.read_csv('results.csv')

# Lọc dữ liệu chỉ gồm các cột dạng số
num_data = df.select_dtypes(include=['number']).dropna(axis=1)

# Chuẩn hóa dữ liệu
scaler = StandardScaler()
scaled_data = scaler.fit_transform(num_data)

# Sử dụng phương pháp Elbow để xác định số lượng cluster tối ưu
inertias = []
k_range = range(1, 11)

for k in k_range:
    model = KMeans(n_clusters=k, random_state=42)
    model.fit(scaled_data)
    inertias.append(model.inertia_)

# Vẽ đồ thị Elbow
plt.figure(figsize=(8, 5))
plt.plot(k_range, inertias, 'bo-', markersize=8, linewidth=2)
plt.title('Optimal Number of Clusters Using Elbow Method')
plt.xlabel('Number of Clusters (K)')
plt.ylabel('Inertia')
plt.grid(True)
plt.show()
