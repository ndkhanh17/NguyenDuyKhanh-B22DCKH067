import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import argparse

def radar_chart(data, player1, player2, attributes):
    # Số lượng chỉ số
    num_vars = len(attributes)

    # Tạo một mảng cho mỗi cầu thủ
    player1_values = data[data['Name'] == player1][attributes].values.flatten()
    player2_values = data[data['Name'] == player2][attributes].values.flatten()

    # Tạo một mảng góc cho các chỉ số
    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()

    # Đóng vòng cho biểu đồ
    player1_values = np.concatenate((player1_values, [player1_values[0]]))
    player2_values = np.concatenate((player2_values, [player2_values[0]]))
    angles += angles[:1]

    # Tạo biểu đồ radar
    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))
    ax.fill(angles, player1_values, color='red', alpha=0.25, label=player1)
    ax.fill(angles, player2_values, color='blue', alpha=0.25, label=player2)

    # Thêm các đường kẻ và nhãn
    ax.set_yticklabels([])
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(attributes)

    # Thêm tiêu đề và chú thích
    plt.title(f'Radar Chart Comparison: {player1} vs {player2}')
    plt.legend(loc='upper right', bbox_to_anchor=(0.1, 0.1))
    plt.show()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Compare players using radar chart.')
    parser.add_argument('--p1', type=str, required=True, help='Name of player 1')
    parser.add_argument('--p2', type=str, required=True, help='Name of player 2')
    parser.add_argument('--Attribute', type=str, required=True, help='Comma-separated list of attributes')
    
    args = parser.parse_args()
    
    # Đọc dữ liệu từ file CSV
    data = pd.read_csv('E:workspace/btlPython/results.csv')  # Thay 'results.csv' bằng tên file của bạn

    # Lấy danh sách các chỉ số từ đối số
    attributes = args.Attribute.split(',')

    # Gọi hàm vẽ biểu đồ radar
    radar_chart(data, args.p1, args.p2, attributes)
