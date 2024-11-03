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

def get_top3(df, columns_to_analyze):
    # Ghi kết quả Top 3 cao nhất
    with open("Top3NguoiChiSoCaoNhat.txt", "w", encoding="utf-8") as file:
        for column in columns_to_analyze:
            file.write(f"\nTop 3 cầu thủ cao nhất cho chỉ số '{column}':\n")
            top_highest = df.nlargest(3, column)[['Player Name', 'Team', column]]
            file.write(tabulate(top_highest, headers='keys', tablefmt='fancy_grid') + "\n")
        print("Đã ghi kết quả Top 3 cao nhất vào file Top3NguoiChiSoCaoNhat.txt")

    # Ghi kết quả Top 3 thấp nhất
    with open("Top3NguoiChiSoThapNhat.txt", "w", encoding="utf-8") as file:
        for column in columns_to_analyze:
            file.write(f"\nTop 3 cầu thủ thấp nhất cho chỉ số '{column}':\n")
            top_lowest = df.nsmallest(3, column)[['Player Name', 'Team', column]]
            file.write(tabulate(top_lowest, headers='keys', tablefmt='fancy_grid') + "\n")
        print("Đã ghi kết quả Top 3 thấp nhất vào file Top3NguoiChiSoThapNhat.txt")

def get_statistics(df, columns_to_analyze):
    # Tính trung vị, trung bình và độ lệch chuẩn
    median_all = df[columns_to_analyze].median().round(2)
    mean_all = df[columns_to_analyze].mean().round(2)
    std_all = df[columns_to_analyze].std().round(2)

    overall_df = pd.DataFrame({
        'STT': [0],
        'Team': ['all'],
        **{f'Median of {col}': [median_all[col]] for col in columns_to_analyze},
        **{f'Mean of {col}': [mean_all[col]] for col in columns_to_analyze},
        **{f'Std of {col}': [std_all[col]] for col in columns_to_analyze}
    })

    median_team = df.groupby('Team')[columns_to_analyze].median().round(2)
    mean_team = df.groupby('Team')[columns_to_analyze].mean().round(2)
    std_team = df.groupby('Team')[columns_to_analyze].std().round(2)

    team_df = pd.DataFrame({
        'STT': range(1, len(median_team) + 1),
        'Team': median_team.index,
        **{f'Median of {col}': median_team[col].values for col in columns_to_analyze},
        **{f'Mean of {col}': mean_team[col].values for col in columns_to_analyze},
        **{f'Std of {col}': std_team[col].values for col in columns_to_analyze}
    })

    final_df = pd.concat([overall_df, team_df], ignore_index=True)
    final_df.to_csv('results2.csv', index=False, encoding='utf-8-sig')
    print("Đã xuất kết quả ra file results2.csv")

def print_histogram(df, columns_to_analyze):
    output_folder_1 = "histograms_all"
    if not os.path.exists(output_folder_1):
        os.makedirs(output_folder_1)

    for col in columns_to_analyze:
        plt.figure(figsize=(8, 6))
        sns.histplot(df[col], bins=20, kde=True, color='blue')
        plt.title(f'Histogram of {col} - Toàn Giải')
        plt.xlabel(col)
        plt.ylabel('Số lượng cầu thủ (Người)')
        plt.grid(True, linestyle='--', alpha=0.5)
        plt.savefig(os.path.join(output_folder_1, f"{df.columns.get_loc(col)}.png"))
        plt.close()

    print("Đã vẽ xong biểu đồ cho toàn giải")

    output_folder_2 = "histograms_teams"
    if not os.path.exists(output_folder_2):
        os.makedirs(output_folder_2)

    teams = df['Team'].unique()
    for team in teams:
        team_folder = os.path.join(output_folder_2, team)
        if not os.path.exists(team_folder):
            os.makedirs(team_folder)

        team_data = df[df['Team'] == team]
        for col in columns_to_analyze:
            plt.figure(figsize=(8, 6))
            sns.histplot(team_data[col], bins=20, kde=True, color='green')
            plt.title(f'Histogram of {col} - {team}')
            plt.xlabel(col)
            plt.ylabel('Số lượng cầu thủ (Người)')
            plt.grid(True, linestyle='--', alpha=0.5)
            plt.savefig(os.path.join(team_folder, f"{df.columns.get_loc(col)}.png"))
            plt.close()
        
        print(f"Đã vẽ xong biểu đồ cho đội {team}")
        time.sleep(3)

def get_best_team(df, columns_to_analyze):
    columns_to_analyze = df.columns[8:]
    df[columns_to_analyze] = df[columns_to_analyze].apply(pd.to_numeric, errors='coerce')

    team_summary = df.groupby('Team')[columns_to_analyze].mean()
    results = []

    for column in columns_to_analyze:
        best_team = team_summary[column].idxmax()
        max_value = team_summary[column].max()
        results.append([column, best_team, max_value])

    headers = ["Chỉ số", "Team", "Giá trị"]
    print(tabulate(results, headers=headers, tablefmt="grid"))

    team_counts = Counter([row[1] for row in results])
    frequency_table = [[team, count] for team, count in team_counts.items()]
    frequency_table.sort(key=lambda x: x[1], reverse=True)

    print("\nTần suất của từng đội bóng:")
    print(tabulate(frequency_table, headers=["Team", "Số lần"], tablefmt="grid"))
    print("Đội có phong độ tốt nhất: " + str(frequency_table[0][0]) + " với số lần là: " + str(frequency_table[0][1]))

if __name__ == "__main__":
    df = pd.read_csv("results.csv")
    columns_to_analyze = df.columns[4:]
    df[columns_to_analyze] = df[columns_to_analyze].apply(pd.to_numeric, errors='coerce')

    print("Chọn chức năng muốn thực hiện: ")
    print("1. Tìm Top 3 người có chỉ số cao nhất và thấp nhất")
    print("2. Tính trung vị, trung bình và độ lệch chuẩn")
    print("3. Vẽ biểu đồ histogram")
    print("4. Tìm đội có giá trị cao nhất ở từng chỉ số")
    print("5. Thoát chương trình")

    while True:
        choice = int(input("Nhập lựa chọn của bạn: "))
        if choice == 1:
            get_top3(df, columns_to_analyze)
        elif choice == 2:
            get_statistics(df, columns_to_analyze)
        elif choice == 3:
            print_histogram(df, columns_to_analyze)
        elif choice == 4:
            get_best_team(df, columns_to_analyze)
        else:
            break
