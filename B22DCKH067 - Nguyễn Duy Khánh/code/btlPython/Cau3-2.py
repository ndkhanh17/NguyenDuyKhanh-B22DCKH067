import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import argparse

def enhanced_radar_chart(data, player1, player2, attributes):
    # Số lượng các thuộc tính
    num_attributes = len(attributes)

    # Trích xuất dữ liệu cho hai cầu thủ
    values1 = data[data['Player Name'] == player1][attributes].values.flatten()
    values2 = data[data['Player Name'] == player2][attributes].values.flatten()

    # Góc cho mỗi trục trong biểu đồ radar
    angles = np.linspace(0, 2 * np.pi, num_attributes, endpoint=False).tolist()

    # Đóng vòng dữ liệu
    values1 = np.concatenate((values1, [values1[0]]))
    values2 = np.concatenate((values2, [values2[0]]))
    angles += angles[:1]

    # Khởi tạo biểu đồ radar
    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))
    ax.plot(angles, values1, 'o-', linewidth=2, label=player1, color='red', markersize=10, markerfacecolor='yellow')
    ax.fill(angles, values1, alpha=0.1, color='red')
    ax.plot(angles, values2, 'd-', linewidth=2, label=player2, color='blue', markersize=10, markerfacecolor='lightblue')
    ax.fill(angles, values2, alpha=0.1, color='blue')

    # Cài đặt nhãn cho mỗi trục, cải tiến với font chữ lớn hơn
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(attributes, fontsize=14, fontweight='bold')

    # Thêm đường lưới để cải thiện tính rõ ràng
    ax.yaxis.grid(True)
    ax.xaxis.grid(True)

    # Thêm tiêu đề và chú thích
    plt.title('So sánh Giá Trị Cầu Thủ qua Biểu Đồ Radar', size=18, color='purple', y=1.1)
    plt.legend(loc='upper right', bbox_to_anchor=(0.1, 0.1))

    plt.show()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='So sánh hai cầu thủ bằng biểu đồ radar.')
    parser.add_argument('--p1', type=str, required=True, help='Tên cầu thủ thứ nhất')
    parser.add_argument('--p2', type=str, required=True, help='Tên cầu thủ thứ hai')
    parser.add_argument('--Attribute', type=str, required=True, help='Danh sách các thuộc tính cách nhau bằng dấu phẩy')
    
    args = parser.parse_args()
    
    data = pd.read_csv('results.csv')  # Đổi đường dẫn file dữ liệu
    attributes = args.Attribute.split(',')

    enhanced_radar_chart(data, args.p1, args.p2, attributes)
