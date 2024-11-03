import requests
from bs4 import BeautifulSoup
import sys
import pandas as pd
import time
# Thiết lập mã hóa UTF-8 cho đầu ra
sys.stdout.reconfigure(encoding='utf-8')

# Hàm xử lý dữ liệu cầu thủ
def process_footballer_data(player_row, team_name):
    # Hàm lấy giá trị từ một cột nhất định
    def get_stat(stat):
        cell = player_row.find('td', {'data-stat': stat})
        return cell.get_text(strip=True) if cell.get_text(strip=True) else "N/a"

    # Lấy thông tin cầu thủ từ các cột cần thiết
    player_data = {
        "Player Name": player_row.find('th', {'data-stat': 'player'}).get_text(strip=True),
        "Nationality": player_row.find('td', {'data-stat': 'nationality'}).find('a')['href'].split('/')[-1].replace('-Football', ' ') if player_row.find('td', {'data-stat': 'nationality'}).find('a') else "N/a",
        "Team": team_name,
        "Position": get_stat('position'),
        "Age": get_stat('age'),
        "Games": get_stat('games'),
        "Games Starts": get_stat('games_starts'),
        "Minutes": get_stat('minutes'),
        "Goals (Pens)": get_stat('goals_pens'),
        "Penalties Made": get_stat('pens_made'),
        "Assists": get_stat('assists'),
        "Yellow Cards": get_stat('cards_yellow'),
        "Red Cards": get_stat('cards_red'),
        "xG": get_stat('xg'),
        "npxG": get_stat('npxg'),
        "xAG": get_stat('xg_assist'),
        "Progressive Carries": get_stat('progressive_carries'),
        "Progressive Passes": get_stat('progressive_passes'),
        "Progressive Passes Received": get_stat('progressive_passes_received'),
        "Goals per 90": get_stat('goals_per90'),
        "Assists per 90": get_stat('assists_per90'),
        "Goals + Assists per 90": get_stat('goals_assists_per90'),
        "Goals (Pens) per 90": get_stat('goals_pens_per90'),
        "Goals + Assists (Pens) per 90": get_stat('goals_assists_pens_per90'),
        "xG per 90": get_stat('xg_per90'),
        "xAG per 90": get_stat('xg_assist_per90'),
        "xG + xAG per 90": get_stat('xg_xg_assist_per90'),
        "npxG per 90": get_stat('npxg_per90'),
        "npxG + xAG per 90": get_stat('npxg_xg_assist_per90')
    }
    
    return list(player_data.values())


# Hàm xử lý dữ liệu thủ môn
def process_goalkeeper_data(player):
    # Hàm phụ để lấy giá trị từ các cột
    def get_stat(stat):
        cell = player.find('td', {'data-stat': stat})
        return cell.get_text(strip=True) if cell.get_text(strip=True) else "N/a"
    
    # Lấy dữ liệu cho các chỉ số thủ môn
    goalkeeper_data = [
        get_stat('gk_goals_against'),
        get_stat('gk_goals_against_per90'),
        get_stat('gk_shots_on_target_against'),
        get_stat('gk_saves'),
        get_stat('gk_save_pct'),
        get_stat('gk_wins'),
        get_stat('gk_ties'),
        get_stat('gk_losses'),
        get_stat('gk_clean_sheets'),
        get_stat('gk_clean_sheets_pct'),
        get_stat('gk_pens_att'),
        get_stat('gk_pens_allowed'),
        get_stat('gk_pens_saved'),
        get_stat('gk_pens_missed'),
        get_stat('gk_pens_save_pct')
    ]
    
    return goalkeeper_data

def process_shooting_data(player):
    # Hàm phụ để lấy giá trị từ cột
    def get_stat(stat):
        cell = player.find('td', {'data-stat': stat})
        return cell.get_text(strip=True) if cell.get_text(strip=True) else "N/a"
    
    # Lấy dữ liệu cho các chỉ số về sút bóng
    shooting_data = [
        get_stat('goals'),
        get_stat('shots'),
        get_stat('shots_on_target'),
        get_stat('shots_on_target_pct'),
        get_stat('shots_per90'),
        get_stat('shots_on_target_per90'),
        get_stat('goals_per_shot'),
        get_stat('goals_per_shot_on_target'),
        get_stat('average_shot_distance'),
        get_stat('shots_free_kicks'),
        get_stat('pens_made'),
        get_stat('pens_att'),
        get_stat('xg'),
        get_stat('npxg'),
        get_stat('npxg_per_shot'),
        get_stat('xg_net'),
        get_stat('npxg_net')
    ]
    
    return shooting_data

# Hàm xử lý dữ liệu Passing
def process_passing_data(player):
    def get_stat(stat):
        cell = player.find('td', {'data-stat': stat})
        return cell.get_text(strip=True) if cell.get_text(strip=True) else "N/a"
    
    passing_data = [
        get_stat('passes_completed'),
        get_stat('passes'),
        get_stat('passes_pct'),
        get_stat('passes_total_distance'),
        get_stat('passes_progressive_distance'),
        get_stat('passes_completed_short'),
        get_stat('passes_short'),
        get_stat('passes_pct_short'),
        get_stat('passes_completed_medium'),
        get_stat('passes_medium'),
        get_stat('passes_pct_medium'),
        get_stat('passes_completed_long'),
        get_stat('passes_long'),
        get_stat('passes_pct_long'),
        get_stat('assists'),
        get_stat('xg_assist'),
        get_stat('pass_xa'),
        get_stat('xg_assist_net'),
        get_stat('assisted_shots'),
        get_stat('passes_into_final_third'),
        get_stat('passes_into_penalty_area'),
        get_stat('crosses_into_penalty_area'),
        get_stat('progressive_passes')
    ]
    return passing_data

def process_pass_types_data(player):
    def get_stat(stat):
        cell = player.find('td', {'data-stat': stat})
        return cell.get_text(strip=True) if cell.get_text(strip=True) else "N/a"
    
    pass_types_data = [
        get_stat('passes_live'),
        get_stat('passes_dead'),
        get_stat('passes_free_kicks'),
        get_stat('through_balls'),
        get_stat('passes_switches'),
        get_stat('crosses'),
        get_stat('throw_ins'),
        get_stat('corner_kicks'),
        get_stat('corner_kicks_in'),
        get_stat('corner_kicks_out'),
        get_stat('corner_kicks_straight'),
        get_stat('passes_completed'),
        get_stat('passes_offsides'),
        get_stat('passes_blocked')
    ]
    return pass_types_data

def process_goal_and_shot_creation_data(player):
    def get_stat(stat):
        cell = player.find('td', {'data-stat': stat})
        return cell.get_text(strip=True) if cell.get_text(strip=True) else "N/a"
    
    goal_and_shot_creation_data = [
        get_stat('sca'),
        get_stat('sca_per90'),
        get_stat('sca_passes_live'),
        get_stat('sca_passes_dead'),
        get_stat('sca_take_ons'),
        get_stat('sca_shots'),
        get_stat('sca_fouled'),
        get_stat('sca_defense'),
        get_stat('gca'),
        get_stat('gca_per90'),
        get_stat('gca_passes_live'),
        get_stat('gca_passes_dead'),
        get_stat('gca_take_ons'),
        get_stat('gca_shots'),
        get_stat('gca_fouled'),
        get_stat('gca_defense')
    ]
    return goal_and_shot_creation_data

def process_defensive_actions_data(player):
    def get_stat(stat):
        cell = player.find('td', {'data-stat': stat})
        return cell.get_text(strip=True) if cell.get_text(strip=True) else "N/a"
    
    defensive_actions_data = [
        get_stat('tackles'),
        get_stat('tackles_won'),
        get_stat('tackles_def_3rd'),
        get_stat('tackles_mid_3rd'),
        get_stat('tackles_att_3rd'),
        get_stat('challenge_tackles'),
        get_stat('challenges'),
        get_stat('challenge_tackles_pct'),
        get_stat('challenges_lost'),
        get_stat('blocks'),
        get_stat('blocked_shots'),
        get_stat('blocked_passes'),
        get_stat('interceptions'),
        get_stat('tackles_interceptions'),
        get_stat('clearances'),
        get_stat('errors')
    ]
    return defensive_actions_data

# Hàm xử lý dữ liệu Possession
def process_possession_data(player):
    def get_stat(stat):
        cell = player.find('td', {'data-stat': stat})
        return cell.get_text(strip=True) if cell.get_text(strip=True) else "N/a"
    
    possession_data = [
        get_stat('touches'),
        get_stat('touches_def_pen_area'),
        get_stat('touches_def_3rd'),
        get_stat('touches_mid_3rd'),
        get_stat('touches_att_3rd'),
        get_stat('touches_att_pen_area'),
        get_stat('touches_live_ball'),
        get_stat('take_ons'),
        get_stat('take_ons_won'),
        get_stat('take_ons_won_pct'),
        get_stat('take_ons_tackled'),
        get_stat('take_ons_tackled_pct'),
        get_stat('carries'),
        get_stat('carries_distance'),
        get_stat('carries_progressive_distance'),
        get_stat('progressive_carries'),
        get_stat('carries_into_final_third'),
        get_stat('carries_into_penalty_area'),
        get_stat('miscontrols'),
        get_stat('dispossessed'),
        get_stat('passes_received'),
        get_stat('progressive_passes_received')
    ]
    return possession_data

# Hàm xử lý dữ liệu Playing Time
def process_playing_time_data(player):
    def get_stat(stat):
        cell = player.find('td', {'data-stat': stat})
        return cell.get_text(strip=True) if cell.get_text(strip=True) else "N/a"
    
    playing_time_data = [
        get_stat('games_starts'),
        get_stat('minutes_per_start'),
        get_stat('games_complete'),
        get_stat('games_subs'),
        get_stat('minutes_per_sub'),
        get_stat('unused_subs'),
        get_stat('points_per_game'),
        get_stat('on_goals_for'),
        get_stat('on_goals_against'),
        get_stat('on_xg_for'),
        get_stat('on_xg_against')
    ]
    return playing_time_data

# Hàm xử lý dữ liệu Miscellaneous Stats
def process_miscellaneous_stats_data(player):
    def get_stat(stat):
        cell = player.find('td', {'data-stat': stat})
        return cell.get_text(strip=True) if cell.get_text(strip=True) else "N/a"
    
    miscellaneous_stats_data = [
        get_stat('fouls'),
        get_stat('fouled'),
        get_stat('offsides'),
        get_stat('crosses'),
        get_stat('own_goals'),
        get_stat('ball_recoveries'),
        get_stat('aerials_won'),
        get_stat('aerials_lost'),
        get_stat('aerials_won_pct')
    ]
    return miscellaneous_stats_data



# Hàm cào dữ liệu lấy thông tin cầu thủ của từng đội bóng
def Crawl_Data(players_data, team_data):
    # Lấy thông tin và các chỉ số cầu thủ của mỗi đội
    for team in team_data:
        team_name, team_url = team
    
        print(f"[][][]Đang cào dữ liệu cầu thủ của đội {team_name}..........[][][]")
        
        # Cào url của từng đội bóng
        r_tmp = requests.get(team_url)
        soup_tmp = BeautifulSoup(r_tmp.content, 'html.parser')   

        # Danh sách tạm thời chứa thông tin tất cả cầu thủ của đội bóng hiện tại
        player_data_tmp = []
        mp = {}  # Map ánh xạ đến list chứa thông tin và chỉ số của cầu thủ thông qua key là tên cầu thủ

        # Tìm bảng chứa thông tin các cầu thủ
        player_table = soup_tmp.find('table', {'class': 'stats_table sortable min_width', 'id': 'stats_standard_9'})
        tbody = player_table.find('tbody')
        players = tbody.find_all('tr')

        for player in players:
            player_minutes_matches = player.find('td', {'data-stat': 'minutes'}).get_text(strip=True) if player.find('td', {'data-stat': 'minutes'}).get_text(strip=True) else "N/a"
            # Lọc ra những cầu thủ đã thi đấu ít nhất 90 phút
            if player_minutes_matches == "N/a" or int(player_minutes_matches.replace(',','')) < 90: 
                continue
            player_data_tmp.append(process_footballer_data(player, team_name))


        # Các bảng khác: Goalkeeper, Shooting, Passing, Pass Types, Goal & Shot Creation, Defensive Actions, Possession, Playing Time, Miscellaneous Stats
        data_tables = [
            ('stats_keeper_9', 'process_goalkeeper_data', 15),
            ('stats_shooting_9', 'process_shooting_data', 17),
            ('stats_passing_9', 'process_passing_data', 23),
            ('stats_passing_types_9', 'process_pass_types_data', 14),
            ('stats_gca_9', 'process_goal_and_shot_creation_data', 16),
            ('stats_defense_9', 'process_defensive_actions_data', 16),
            ('stats_possession_9', 'process_possession_data', 22),
            ('stats_playing_time_9', 'process_playing_time_data', 11),
            ('stats_misc_9', 'process_miscellaneous_stats_data', 9)
        ]

        # Duyệt qua từng bảng
        for table_id, process_func_name, missing_data_len in data_tables:
            table = soup_tmp.find('table', {'class': 'stats_table sortable min_width', 'id': table_id})
            tbody = table.find('tbody')
            players = tbody.find_all('tr')
            list_tmp = []

            # Xử lý dữ liệu cho từng bảng
            for player in players:
                player_name = player.find('th', {'data-stat': 'player'}).get_text(strip=True)
                if player_name in mp:
                    # Gọi hàm xử lý tương ứng theo tên hàm
                    process_func = globals()[process_func_name]
                    mp[player_name] += process_func(player)
                    list_tmp.append(player_name)

            # Điền giá trị "N/a" nếu cầu thủ không có dữ liệu từ bảng này
            for player in player_data_tmp:
                if player[0] not in list_tmp:
                    player += ["N/a"] * missing_data_len

        # Thêm dữ liệu các cầu thủ của đội bóng vào danh sách chứa dữ liệu của tất cả các cầu thủ
        players_data += player_data_tmp
        print(f"<<<<<<<<Đã cào xong dữ liệu cầu thủ của đội {team_name}.>>>>>>>")

        # Tạm nghỉ trước khi cào đội tiếp theo
        # break
        time.sleep(10)
        
    return players_data


if __name__ == "__main__":
    # URL to fetch
    url = 'https://fbref.com/en/comps/9/2023-2024/2023-2024-Premier-League-Stats'
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')

    # Tìm bảng chứa thông tin các đội bóng trong mùa giải 2023-2024
    table = soup.find('table', {
        'class': 'stats_table sortable min_width force_mobilize',
        'id': 'results2023-202491_overall'
    })

    #  # Danh sách chứa dữ liệu đội bóng và URL
    team_data = []

    # Tìm thẻ <tbody> trong <table>
    tbody = table.find('tbody')
    teams = tbody.find_all('a', href=True)
    for team in teams:
        if "squads" in team['href']:  # Kiểm tra nếu "squads" có trong href
            team_name = team.get_text(strip=True)
            team_url = "https://fbref.com" + team['href']
            team_data.append([team_name, team_url])

    #  Danh sach chứa từng cầu thủ của đội bóng
    players_data = []
    time.sleep(5)
    players_data = Crawl_Data(players_data, team_data)
    
    # Sắp xếp dữ liệu theo first name và tuổi giảm dần
    players_data = sorted(players_data, key=lambda x: (x[0].split()[0], -int(x[4]) if x[4] != "N/a" else 0))





    # # Chuyển dữ liệu thành DataFrame và lưu thành file CSV
    df_players = pd.DataFrame(players_data, columns=["Player Name", "Nation", "Team", "Position", "Age", "Matches Played", "Starts", "Minutes", "Non-Penalty Goals", "Penalties Made", "Assists", "Yellow Cards", "Red Cards", "xG", "npxG", "xAG", "PrgC", "PrgP", "PrgR","Gls/90", "Ast/90", "G+A/90", "G-PK/90", "G+A-PK/90", "xG/90", "xAG/90","xG+xAG/90", "npxG/90", "npxG+xAG/90",
                                                     "Goalkeeping_GA", "GGoalkeeping_GA90", "Goalkeeping_SoTA", "Goalkeeping_Saves", "Goalkeeping_Save%", "Goalkeeping_W", "Goalkeeping_D", "Goalkeeping_L", "Goalkeeping_CS", "Goalkeeping_CS%", "Goalkeeping_PKatt", "Goalkeeping_PKA", "Goalkeeping_Pksv", "Goalkeeping_PKm", "Goalkeeping_Save%",
                                                     "Shooting_Gls", "Shooting_Sh", "Shooting_SoT", "Shooting_SoT%", "Shooting_Sh/90", "Shooting_SoT/90", "Shooting_G/Sh", "Shooting_G/SoT", "Shooting_Dist", "Shooting_FK", "Shooting_PK", "Shooting_PKatt", "Shooting_xG", "Shooting_npxG", "Shooting_npxG/Sh", "Shooting_G-xG", "Shooting_np:G-xG",
                                                     "Passing_Cmp", "Passing_Att", "Passing_Cmp%", "Passing_ToDist", "Passing_PrgDist", "Passing_Short_Cmp", "Passing_Short_Att", "Passing_Short_Cmp%", "Passing_Med_Cmp", "Passing_Med_Att", "Passing_Med_Cmp%", "Passing_Long_Cmp", "Passing_Long_Att", "Passing_Long_Cmp%", "Passing_Ast", "Passing_xAG", "Passing_xA", "Passing_A-xAG", "Passing_KP", "Passing_1/3", "Passing_PPA", "Passing_CrsPA", "Passing_PrgP",
                                                     "Pass_Types_Live", "Pass_Types_Dead", "Pass_Types_FK", "Pass_Types_TB", "Pass_Types_Sw", "Pass_Types_Crs", "Pass_Types_TI", "Pass_Types_CK", "Pass_Types_In", "Pass_Types_Out", "Pass_Types_Str", "Pass_Types_Gmp", "Pass_Types_Off", "Pass_Types_Blocks",
                                                     "GSCreation_SCA", "GSCreation_SCA90", "GGSCreation_SCA_PassLive", "GSCreation_SCA_PassDead", "GSCreation_SCA_TO", "GSCreation_SCA_Sh", "GSCreation_SCA_Fld", "GSCreation_SCA_Def", "GSCreation_GCA", "GSCreation_GCA90", "GSCreation_GCA_PassLive", "GSCreation_GCA_PassDead", "GSCreation_GCA_TO", "GSCreation_GCA_Sh", "GSCreation_GCA_Fld", "GSCreation_GCA_Def",
                                                     "DActions_Tkl", "DActions_TklW", "DActions_Def3rd", "DActions_Mid3rd", "DActions_Att3rd", "DActions_Challenges_Tkl", "DActions_Challenges_Att", "DActions_Challenges_Tkl%", "DActions_Challenges_Lost", "DActions_Blocks", "DActions_Blocks_Sh", "DActions_Blocks_Pass", "DActions_Int", "DActions_Tkl+Int", "DActions_Clr", "DActions_Err",
                                                     "Possession_Touches", "Possession_Def Pen", "Possession_Def 3rd", "Possession_Mid 3rd", "Possession_Att 3rd", "Possession_Att Pen", "Possession_Live", "Possession_Att", "Possession_Succ", "Possession_Succ%", "Possession_Tkld", "Possession_Tkld%", "Possession_Carries", "Possession_TotDist", "Possession_PrgDist", "Possession_PrgC", "Possession_1/3", "Possession_CPA", "Possession_Mis", "Possession_Dis", "Possession_Rec", "Possession_PrgR",
                                                     "PTime_Starts", "PTime_Mn/Start", "PTime_Compl", "PTime_Subs", "PTime_Mn/Sub", "PTime_unSub", "PTime_PPM", "PTime_onG", "PTime_onGA", "PTime_onxG", "PTime_onxGA",
                                                     "MStats_Fls", "MStats_Fld", "MStats_Off", "MStats_Crs", "MStats_OG", "MStats_Recov", "MStats_Won", "MStats_Lost", "MStats_Won%"
                                                     ])
    df_players.to_csv("results.csv", index=False, encoding='utf-8-sig')
    print("Đã lưu thông tin các cầu thủ vào file results.csv!")