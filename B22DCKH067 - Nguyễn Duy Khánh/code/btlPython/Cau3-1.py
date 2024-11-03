import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt

def initialize_data():
    # Đọc và chuẩn bị dữ liệu
    df = pd.read_csv('results.csv')
    df = df.select_dtypes(exclude=['object'])
    df = df.fillna(df.mean())
    return df

def scale_and_reduce(df):
    # Chuẩn hóa và giảm chiều dữ liệu
    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(df)
    pca = PCA(n_components=2)
    return pca.fit_transform(scaled_data)


def perform_kmeans(data, num_clusters=5, max_iter=100):
    # Chuyển đổi dữ liệu thành mảng NumPy nếu là DataFrame
    if isinstance(data, pd.DataFrame):
        data = data.values
    
    # Khởi tạo ngẫu nhiên các tâm cụm
    centroids = data[np.random.choice(data.shape[0], num_clusters, replace=False)]
    
    for step in range(max_iter):
        # Tính khoảng cách từ mỗi điểm đến tất cả tâm cụm và gán cụm
        distances = np.linalg.norm(data[:, np.newaxis] - centroids, axis=2)
        clusters = np.argmin(distances, axis=1)
        
        # Tính tâm cụm mới bằng cách lấy trung bình cộng của các điểm trong mỗi cụm
        new_centroids = np.array([data[clusters == i].mean(axis=0) for i in range(num_clusters)])
        
        # Kiểm tra sự hội tụ: nếu tâm cụm không thay đổi thì dừng lặp
        if np.allclose(centroids, new_centroids):
            break
        
        centroids = new_centroids

    return centroids, clusters

def visualize_clusters(data, centroids, clusters):
    # Vẽ biểu đồ các cụm với phong cách khác
    plt.figure(figsize=(10, 8))
    unique_clusters = np.unique(clusters)
    colors = plt.cm.get_cmap('tab10', len(unique_clusters))  # Sử dụng bảng màu 'tab10' cho đa dạng màu sắc

    # Vẽ điểm dữ liệu với màu sắc và nhãn tương ứng với từng cụm
    for i, color in zip(unique_clusters, colors.colors):
        cluster_data = data[clusters == i]
        plt.scatter(cluster_data[:, 0], cluster_data[:, 1], color=color, label=f'Cluster {i}', alpha=0.6, edgecolor='w')

    # Vẽ các tâm cụm với ký hiệu và màu đậm hơn
    for idx, centroid in enumerate(centroids):
        plt.scatter(*centroid, color='black', marker='X', s=250, edgecolor='w', linewidth=2)
        plt.text(centroid[0], centroid[1], f'Center {idx}', fontsize=12, weight='bold', ha='center')

    plt.title('Enhanced Visualization of K-means Clustering')
    plt.xlabel('Principal Component 1')
    plt.ylabel('Principal Component 2')
    plt.legend(title='Cluster ID')
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    df = initialize_data()
    data = scale_and_reduce(df)
    centroids, clusters = perform_kmeans(data)
    visualize_clusters(data, centroids, clusters)
