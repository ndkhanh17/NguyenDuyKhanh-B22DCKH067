import pandas as pd
import numpy as np
from tabulate import tabulate
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
import os
import time

def save_top3_players(df, columns, file_name, order='desc'):
    with open(file_name, "w", encoding="utf-8") as file:
        for col in columns:
            file.write(f"\nTop 3 cầu thủ {'cao' if order == 'desc' else 'thấp'} nhất cho chỉ số '{col}':\n")
            top_players = df.nlargest(3, col) if order == 'desc' else df.nsmallest(3, col)
            top_players = top_players[['Player Name', 'Team', col]]
            file.write(tabulate(top_players, headers='keys', tablefmt='fancy_grid') + "\n")
    
    print(f"<<<< Đã ghi kết quả tìm kiếm Top3 {'cao' if order == 'desc' else 'thấp'} nhất vào file {file_name} >>>>")

def calculate_statistics(df, columns):
    stats = {
        'median': df[columns].median().round(2),
        'mean': df[columns].mean().round(2),
        'std': df[columns].std().round(2)
    }
    overall_stats = pd.DataFrame({
        'STT': [0], 'Team': ['all'],
        **{f'{k.capitalize()} of {col}': [v[col]] for k, v in stats.items() for col in columns}
    })
    
    team_stats = df.groupby('Team')[columns].agg(['median', 'mean', 'std']).round(2)
    team_stats.columns = [f'{agg.capitalize()} of {col}' for col, agg in team_stats.columns]
    team_stats.reset_index(inplace=True)
    team_stats.insert(0, 'STT', range(1, len(team_stats) + 1))
    
    final_stats = pd.concat([overall_stats, team_stats], ignore_index=True)
    final_stats.to_csv('results2.csv', index=False, encoding='utf-8-sig')
    print("<<<< Đã xuất kết quả ra file results2.csv >>>>")

def plot_histograms(df, columns):
    for col in columns:
        plot_histogram(df, col, "histograms_all")
        
    for team, team_df in df.groupby('Team'):
        team_folder = os.path.join("histograms_teams", team)
        os.makedirs(team_folder, exist_ok=True)
        for col in columns:
            plot_histogram(team_df, col, team_folder)
            time.sleep(3)

    print("<<<< Đã vẽ xong biểu đồ cho toàn giải và từng đội >>>>")

def plot_histogram(df, col, folder):
    os.makedirs(folder, exist_ok=True)
    plt.figure(figsize=(8, 6))
    sns.histplot(df[col], bins=20, kde=True)
    plt.title(f'Histogram of {col}')
    plt.xlabel(col)
    plt.ylabel('Số lượng cầu thủ (Người)')
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.savefig(os.path.join(folder, f"{col}.png"))
    plt.close()

def analyze_best_team(df, columns):
    team_summary = df.groupby('Team')[columns].mean()
    results = [[col, team_summary[col].idxmax(), team_summary[col].max()] for col in columns]
    
    print(tabulate(results, headers=["Chỉ số", "Team", "Giá trị"], tablefmt="grid"))
    team_counts = Counter([row[1] for row in results])
    frequency_table = sorted(team_counts.items(), key=lambda x: x[1], reverse=True)
    
    print("\nTần suất của từng đội bóng:")
    print(tabulate(frequency_table, headers=["Team", "Số lần"], tablefmt="grid"))
    print(f"Đội có phong độ tốt nhất giải: {frequency_table[0][0]} với số lần cao nhất: {frequency_table[0][1]}")

if __name__ == "__main__":
    df = pd.read_csv("results.csv")
    columns_to_analyze = df.columns[4:]
    df[columns_to_analyze] = df[columns_to_analyze].apply(pd.to_numeric, errors='coerce')
    
    print("Chọn chức năng muốn thực hiện:")
    print("1. Tìm Top 3 người có chỉ số cao nhất và thấp nhất")
    print("2. Tính trung vị, trung bình và độ lệch chuẩn của các chỉ số")
    print("3. Vẽ biểu đồ histogram")
    print("4. Tìm đội có giá trị cao nhất và tần suất của từng đội")
    print("5. Thoát chương trình")

    while True:
        choice = int(input("Nhập lựa chọn của bạn: "))
        if choice == 1:
            save_top3_players(df, columns_to_analyze, "Top3NguoiChiSoCaoNhat.txt", 'desc')
            save_top3_players(df, columns_to_analyze, "Top3NguoiChiSoThapNhat.txt", 'asc')
        elif choice == 2:
            calculate_statistics(df, columns_to_analyze)
        elif choice == 3:
            plot_histograms(df, columns_to_analyze)
        elif choice == 4:
            analyze_best_team(df, columns_to_analyze)
        elif choice == 5:
            break
        else:
            print("Lựa chọn không hợp lệ. Vui lòng thử lại.")
