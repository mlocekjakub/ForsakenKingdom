from main import BOSS_ICON,BODY_BOSS_ICON
from util import clear_screen
import engine


def display_message(message, new_lines=0,filler = 4):
    new_lines = "\n"*new_lines
    print(f"{new_lines}{filler*' '}{message}")

def display_error_message(message,new_lines=2,filler=4):
    new_lines = "\n"*new_lines
    print(f"{new_lines}{filler*' '}{message}")

def display_title(title,new_lines=2,filler=4):
    new_lines = "\n"*new_lines
    print(f"{new_lines}{filler*' '}{title}")

def display_board(board):
    '''
    Displays complete game board on the screen

    Returns:
    Nothing
    '''
    print("\n")
    for i in range(len(board)):
        row = "    " + "".join(board[i])
        row = row.replace("O", " ")
        print(row)

def display_dark_board(board,player):
    torch_range = 4
    print("\n")
    for i in range(len(board)):
        for j in range(len(board[0])):
            if j > player["player_location"][1]-torch_range and j <player["player_location"][1]+ torch_range and i > player["player_location"][0] - torch_range and i < player["player_location"][0] + torch_range:
                if board[i][j] =="O":
                    print(" ",end="")
                elif board[i][j] != " ":
                    print(board[i][j],end="")
                else:
                    print(".",end="")
            else:
                print(" ",end="")
        print()

def display_boss_board(board):
    boss_range = 3
    boss_location = engine.get_boss_location(board,BOSS_ICON)
    boss_design = [BODY_BOSS_ICON] * 6 +["Q"," ","Q"]+[BODY_BOSS_ICON] * 2+[" ",BOSS_ICON," ",]+[BODY_BOSS_ICON] * 2+["V"]*3+[BODY_BOSS_ICON] * 6
    index_of_boss_design = 0
    if boss_location[0]:
        for i in range(len(board)):
            for j in range(len(board[0])):
                if j > boss_location[1] - boss_range and j < boss_location[1]+ boss_range and i > boss_location[0] - boss_range and i < boss_location[0] + boss_range:
                    board[i][j] = boss_design[index_of_boss_design]
                    index_of_boss_design += 1
                else:
                    if board[i][j] == BODY_BOSS_ICON:
                        board[i][j] =" "                  
                # print(board[i][j],end="")
            # print()
    print("\n")
    for i in range(len(board)):
        row = "".join(board[i])
        row = row.replace("O", " ")
        print(f"{row}".center(119))

def display_equipment(player):
    # display_title("Your Equipment".center(119),3,0)
    equipment = player["equipment"]
    equipment_headers = ["Head: ","Chest: ","Legs: ","Shoes: ","Weapons: "]
    display_inventory(equipment,"Your Equipment\n",equipment_headers)
    # for i in range(len(equipment_headers)):
    #     print(f"\n\n    {equipment_headers[i]} : {equipment[i]['name']}   {equipment[i]['type']}= {equipment[i]['value']}")

def display_stats(player_stats,new_lines=0, divider = ", the ", cut = 7):
    """
    player_stats.keys() = {"name", "race", "health", "lvl", "exp", 
                        "attack", "armor", "player_location", "player_icon", "inventory"}
    """

    stats = list(player_stats.items())
    #removing "player_location" and "player_icon" and "inventory"
    stats = [stats[i] for i in range(len(stats)) if i <cut]

    for i in range(len(stats)):
        if i <2:
            stats[i] = stats[i][1]
        else:
            stats[i] = (stats[i][0] + ": " + str(stats[i][1])).title()

    longest_word = 0
    for i in range(2,len(stats)):
        if len(str(stats[i])) > longest_word:
            longest_word = len(str(stats[i]))

    stats_to_display = [[],[]]
    stats_to_display[0] = [stats[x] for x in range(len(stats)) if x <5]
    stats_to_display[1] = [stats[x] for x in range(len(stats)) if x >4]
    
    first_row = f"{stats_to_display[0][0]}{divider}{stats_to_display[0][1]} "
    for i in range(2,len(stats_to_display[0])):
        first_row += "| " + stats_to_display[0][i] + " "
    second_row = ""
    for i in range(len(stats_to_display[1])):
        second_row += stats_to_display[1][i] + " | "
    new_lines = "\n" * new_lines
    print(new_lines)
    print(f"{first_row}".center(119+3))
    print()
    print(f"{second_row[:-2]}".center(119+6))

def display_menu(title, list_options):
    longest_option_lenght = len(max(list_options, key=len))
    display_title(f"{title}\n\n".center(119),4,0)
    list_of_indieces = list(range(1,len(list_options)))
    list_of_indieces.append(0)
    for i in list_of_indieces:
        option_lenght = len(list_options[i])
        filler = (longest_option_lenght - option_lenght) * " "
        print(f"({i}) {list_options[i]}{filler}\n".center(119))

def display_race_choices(races):
    clear_screen()
    longest_race = len(races[0]["race"])
    longest_value = len(str(races[0]["health"]))
    for i in range(len(races)):
        if len(races[i]["race"]) > longest_race:
            longest_race = len(races[i]["race"])
        if len(str(races[i]["health"])) > longest_value:
            longest_value = len(str(races[i]["health"]))
        if len(str(races[i]["attack"])) > longest_value:
            longest_value = len(str(races[i]["attack"]))
        if len(str(races[i]["armor"])) > longest_value:
            longest_value = len(str(races[i]["armor"]))
    
    display_title("Choose your characters race:".center(119),4,0)
    print("\n\n")
    for i in range(len(races)):
        race_length = len(races[i]["race"])
        filler_race = (longest_race-race_length) * " "
        health_lenght = len(str(races[i]["health"]))
        attack_lenght = len(str(races[i]["attack"]))
        armor_lenght = len(str(races[i]["armor"]))
        filler_health = (longest_value-health_lenght) * " " 
        filler_attack = (longest_value-attack_lenght) * " "
        filler_armor = (longest_value-armor_lenght) * " "
        print(f'{longest_race*" "}   Health  =  {races[i]["health"]}{filler_health}'.center(119))
        print(f'{races[i]["race"]}{filler_race} : Attack  =  {races[i]["attack"]}{filler_attack}'.center(119))
        print(f'{longest_race*" "}   Armor   =  {races[i]["armor"]}{filler_armor}'.center(119))
        if i < len(races)-1:
            display_message("============================".center(119),1,0)
            print()
            
def display_inventory(inventory, lable = "Inventory:\n",header = None):
    # inventory = [{'type': str, 'name': str, 'value': int}, ...]
    inventory = sorted(inventory, key=lambda x: x["type"])
    longest_name = len(inventory[0]["name"])
    longest_type = len(inventory[0]["type"])
    longest_value = len(str(inventory[0]["value"]))
    is_gold_in_inventory = False
    if len(inventory) > 1:
        for i in range(len(inventory)):
            if len(inventory[i]["name"]) > longest_name:
                longest_name = len(inventory[i]["name"])
            elif len(inventory[i]["type"]) > longest_type:
                longest_type = len(inventory[i]["type"])
            elif len(str(inventory[i]["value"])) > longest_value:
                longest_value = len(str(inventory[i]["value"]))
    else:
        longest_name = len(inventory[0]["name"])
        longest_type = len(inventory[0]["type"])
        longest_value = len(str(inventory[0]["value"]))

    clear_screen()
    display_title(f"{lable}".center(119),3,filler=0)
    for i in range(len(inventory)):
        name_lenght = len(inventory[i]["name"])
        type_lenght = len(inventory[i]["type"])
        value_lenght = len(str(inventory[i]["value"]))
        filler_name = (longest_name - name_lenght + 2)*" "
        filler_type = (longest_type - type_lenght + 2)*" "
        filler_value = (longest_value - value_lenght + 2)*" "
        if header:
            display_message(f"{header[i]}{inventory[i]['name']}{filler_name}:  {inventory[i]['type']}{filler_type}=  {inventory[i]['value']}{filler_value}".center(119),1,filler=0)
        elif inventory[i]["name"] != "Gold" and not header:
            display_message(f"{inventory[i]['name']}{filler_name}:  {inventory[i]['type']}{filler_type}=  {inventory[i]['value']}{filler_value}".center(119),1,filler=0)
        else:
            is_gold_in_inventory = True
            gold = inventory[i]
    if is_gold_in_inventory:
        gold_filler_name = (longest_name + 2)*" "
        gold_filler_type = (longest_type - len(gold["type"]) + 2)*" "
        gold_filler_value = (longest_value - len(str(gold["value"])) + 2)*" "
        print()
        display_message(f"{gold_filler_name}   {gold['type']}{gold_filler_type}=  {gold['value']}{gold_filler_value}".center(119),1,filler=0)


"""ASCI ART"""

def display_menu_art():
    art = """  _____                               _                       _  __  _                       _                     
 |  ___|  ___    _ __   ___    __ _  | | __   ___   _ __     | |/ / (_)  _ __     __ _    __| |   ___    _ __ ___  
 | |_    / _ \  | '__| / __|  / _` | | |/ /  / _ \ | '_ \    | ' /  | | | '_ \   / _` |  / _` |  / _ \  | '_ ` _ \ 
 |  _|  | (_) | | |    \__ \ | (_| | |   <  |  __/ | | | |   | . \  | | | | | | | (_| | | (_| | | (_) | | | | | | |
 |_|     \___/  |_|    |___/  \__,_| |_|\_\  \___| |_| |_|   |_|\_\ |_| |_| |_|  \__, |  \__,_|  \___/  |_| |_| |_|
                                                                                 |___/                             """
    print("\n\n\n")
    art = art.split("\n")
    longest_row_length = len(max(art))
    for i in range(len(art)):
        row_lenght = len(art[i])
        filler = (longest_row_length - row_lenght) * " "
        print(f"{art[i]}{filler}".center(119))

def display_fight_art():
    art = """   |\                     /)
 /\_\\\__               (_//
|   `>\-`     _._       //`)
 \ /` \\\  _.-`:::`-._  //
  `    \|`    :::    `|/
        |     :::     |
        |.....:::.....|
        |:::::::::::::|
        |     :::     |
        \     :::     /
         \    :::    /
          `-. ::: .-'
           //`:::`\\\\
          //   '   \\\\
         //         \\\\"""
    art = art.split("\n")
    longest_row_length = len(max(art))
    for i in range(len(art)):
        row_lenght = len(art[i])
        filler = (longest_row_length - row_lenght) * " "
        print(f"{art[i]}{filler}".center(119))