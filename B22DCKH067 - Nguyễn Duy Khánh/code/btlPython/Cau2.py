import sys
sys.stdout.reconfigure(encoding='utf-8')
import pandas as pd
import numpy as np
from tabulate import tabulate
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
import os
import time

def write_top3(df, performance_metrics, output_file="Top3ChiSo.txt"):
    with open(output_file, "w", encoding="utf-8") as file:
        for column in performance_metrics:
            # Ghi kết quả Top 3 cao nhất
            file.write(f"\nTop 3 cầu thủ cao nhất cho chỉ số '{column}':\n")
            top_highest = df.nlargest(3, column)[['Player Name', 'Team', column]]
            file.write(tabulate(top_highest, headers='keys', tablefmt='fancy_grid') + "\n")
            
            # Ghi kết quả Top 3 thấp nhất
            file.write(f"\nTop 3 cầu thủ thấp nhất cho chỉ số '{column}':\n")
            top_lowest = df.nsmallest(3, column)[['Player Name', 'Team', column]]
            file.write(tabulate(top_lowest, headers='keys', tablefmt='fancy_grid') + "\n")
    
    print(f"Đã ghi kết quả Top 3 cao nhất và thấp nhất vào file {output_file}")

def export_team_statistics(df, performance_metrics, output_file="results2.csv"):
    # Tạo một hàm phụ để tính toán và định dạng kết quả cho từng nhóm (toàn giải hoặc từng đội)
    def calculate_stats(data, label, idx):
        stats = {'STT': idx, 'Team': label}
        for col in performance_metrics:
            stats[f'Median of {col}'] = round(data[col].median(), 2)
            stats[f'Mean of {col}'] = round(data[col].mean(), 2)
            stats[f'Std of {col}'] = round(data[col].std(), 2)
        return stats

    # Tính toán cho toàn giải và thêm vào danh sách kết quả
    results = [calculate_stats(df, 'all', 0)]

    # Tính toán cho từng đội và thêm vào danh sách kết quả
    for idx, (team, group) in enumerate(df.groupby('Team'), start=1):
        results.append(calculate_stats(group, team, idx))

    # Chuyển danh sách kết quả thành DataFrame và xuất ra file CSV
    final_df = pd.DataFrame(results)
    final_df.to_csv(output_file, index=False, encoding='utf-8-sig')
    print(f"<<<<<<<<Đã xuất kết quả ra file {output_file}>>>>>>>>")

def generate_histograms(df, performance_metrics):
    # Tạo thư mục cho toàn giải
    all_teams_folder = "histograms_all"
    os.makedirs(all_teams_folder, exist_ok=True)

    # Vẽ biểu đồ cho toàn giải
    for col in performance_metrics:
        plt.figure(figsize=(8, 6))
        sns.histplot(df[col], bins=20, kde=True, color='yellow')
        plt.title(f'Histogram of {col} - Toàn Giải')
        plt.xlabel(col)
        plt.ylabel('Số lượng cầu thủ (Người)')
        plt.grid(True, linestyle='--', alpha=0.5)
        plt.savefig(os.path.join(all_teams_folder, f"{col}_all.png"))
        plt.close()
    
    print("Đã vẽ xong biểu đồ cho toàn giải")

    # Tạo thư mục cho từng đội
    teams_folder = "histograms_teams"
    os.makedirs(teams_folder, exist_ok=True)

    # Vẽ biểu đồ cho từng đội
    for team in df['Team'].unique():
        team_folder = os.path.join(teams_folder, team)
        os.makedirs(team_folder, exist_ok=True)

        print("Vui lòng chờ.......")
        team_data = df[df['Team'] == team]
        for col in performance_metrics:
            plt.figure(figsize=(8, 6))
            sns.histplot(team_data[col], bins=20, kde=True, color='red')
            plt.title(f'Histogram of {col} - {team}')
            plt.xlabel(col)
            plt.ylabel('Số lượng cầu thủ (Người)')
            plt.grid(True, linestyle='--', alpha=0.5)
            plt.savefig(os.path.join(team_folder, f"{df.columns.get_loc(col)}_{team}.png"))
            plt.close()
        
        print(f"Đã vẽ xong biểu đồ cho đội {team}")
        time.sleep(1)

def identify_best_teams(df, performance_metrics):
    # Chuyển đổi các cột chỉ số thành dạng số nếu cần thiết
    df[performance_metrics] = df[performance_metrics].apply(pd.to_numeric, errors='coerce')

    # Tính giá trị trung bình của mỗi chỉ số cho từng đội
    team_averages = df.groupby('Team')[performance_metrics].mean()

    # Tìm đội có giá trị cao nhất cho mỗi chỉ số
    best_teams = [
        [stat, team_averages[stat].idxmax(), team_averages[stat].max()]
        for stat in performance_metrics
    ]

    # Hiển thị bảng kết quả chỉ số cao nhất cho mỗi chỉ số
    headers = ["Chỉ số", "Team", "Giá trị"]
    print(tabulate(best_teams, headers=headers, tablefmt="grid"))

    # Tính toán tần suất xuất hiện của từng đội trong các chỉ số cao nhất
    team_frequency = Counter(team for _, team, _ in best_teams)
    sorted_frequency = sorted(team_frequency.items(), key=lambda x: x[1], reverse=True)

    # Hiển thị bảng tần suất của các đội
    print("\nTần suất của từng đội bóng:")
    print(tabulate(sorted_frequency, headers=["Team", "Số lần"], tablefmt="grid"))

    # Xác định đội có phong độ tốt nhất dựa trên tần suất cao nhất
    best_team = sorted_frequency[0]
    print(f"\nĐội có phong độ tốt nhất: {best_team[0]} với số lần là: {best_team[1]}")

if __name__ == "__main__":
    df = pd.read_csv("results.csv")
    performance_metrics = df.columns[4:]
    df[performance_metrics] = df[performance_metrics].apply(pd.to_numeric, errors='coerce')
    
    write_top3(df, performance_metrics)
    export_team_statistics(df, performance_metrics)
    generate_histograms(df, performance_metrics)
    identify_best_teams(df, df.columns[8:])
    
