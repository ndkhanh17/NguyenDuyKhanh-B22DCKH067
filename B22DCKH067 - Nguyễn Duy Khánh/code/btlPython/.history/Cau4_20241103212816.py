import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import sys

# Đảm bảo đầu ra sử dụng mã hóa UTF-8
sys.stdout.reconfigure(encoding='utf-8')

def fetch_teams(base_url):
    # Lấy danh sách các đội từ trang web
    response = requests.get(base_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Tìm bảng dữ liệu đội bóng
    teams_table = soup.find('table', {'class': 'table table-striped table-hover leaguetable mvp-table ranking-table mb-0'})
    teams_list = []

    if teams_table:
        for team in teams_table.select('tbody a[href]'):
            teams_list.append({
                'name': team.get_text(strip=True),
                'url': team['href']
            })
        print("Hoàn thành lấy dữ liệu các đội bóng.")
    else:
        print("Không tìm thấy bảng dữ liệu các đội.")
    
    return teams_list

def fetch_players(team):
    # Lấy thông tin cầu thủ của từng đội
    response = requests.get(team['url'])
    soup = BeautifulSoup(response.text, 'html.parser')
    
    players = []
    players_table = soup.find('table', {'class': 'table table-striped-rowspan ft-table mb-0'})

    if players_table:
        for player_row in players_table.select('tbody tr'):
            if any(cls in player_row.get('class', []) for cls in ['odd', 'even']):
                name = player_row.find('th').find('span').get_text(strip=True)
                cost = player_row.find_all('td')[-1].get_text(strip=True)
                players.append({'name': name, 'team': team['name'], 'cost': cost})
        
        print(f"Đã lấy thông tin cầu thủ của đội: {team['name']}")
    else:
        print(f"Không tìm thấy bảng dữ liệu cầu thủ của đội: {team['name']}")
    
    return players

if __name__ == "__main__":
    url = 'https://www.footballtransfers.com/us/leagues-cups/national/uk/premier-league/2023-2024'
    
    # Lấy danh sách các đội bóng
    teams = fetch_teams(url)
    
    # Lấy thông tin cầu thủ từ từng đội
    all_players = []
    for team in teams:
        team_players = fetch_players(team)
        all_players.extend(team_players)
        time.sleep(3)  # Tạm dừng để tránh quá tải yêu cầu

    # Lưu dữ liệu vào file CSV
    players_df = pd.DataFrame(all_players)
    players_df.to_csv("results4.csv", index=False, encoding='utf-8-sig')
    print("Đã lưu thông tin giá cầu thủ vào file results4.csv")
