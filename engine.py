from os import closerange
import random
import util
import ui
from time import sleep
from importlib import reload

def create_board(width, height):
    board = [[" " for x in range(width)]for y in range(height)]
    for i in range(len(board)):
        board[i].insert(0, "|")
        board[i].append("|")
    horizontal_top_board_line = ["=" for x in range(len(board[0]))]
    horizontal_bottom_board_line = ["=" for x in range(len(board[0]))]
    board.insert(0,horizontal_top_board_line)
    board.append(horizontal_bottom_board_line)
    return board

def create_player(player_start_row, player_start_col, player_icon):
    nothing_armor_item = {
        "name":"Nothing",
        "type":"Armor",
        "value":0
    }
    nothing_weapon_item = {
        "name":"Nothing",
        "type":"Attack",
        "value":0
    }
    start_gold ={
        "name":"Gold",
        "type":"Gold",
        "value":0
    }
    equipment = [nothing_armor_item,nothing_armor_item,nothing_armor_item,nothing_armor_item,nothing_weapon_item]
    while True:
        ui.clear_screen()
        ui.display_title("Create your hero!\n".center(119),4,0)
        ui.display_message("Your hero's name:".center(119),2,0)
        print("\n")
        player_stats = {"name":input("".rjust(119//2-3)).title()}
        if player_stats["name"] == "Admin":
            player_stats.update({"race":"God" ,"health":1000000,"lvl":1000000,"exp":0,"attack":1000000,
                                "armor":1000000,"player_location": [player_start_row,player_start_col],"player_icon":player_icon, "inventory":[start_gold],"equipment": equipment})
            return player_stats
        while True:        
            orc = {"race":"Orc" ,"health":125,"lvl":1,"exp":0,"attack":7,"armor":20}
            human = {"race":"Human","health":100,"lvl":1,"exp":0,"attack":10,"armor":10}
            dwarf = {"race":"Dwarf","health":75,"lvl":1,"exp":0,"attack":10,"armor":20} 
            elf = {"race":"Elf","health":75,"lvl":1,"exp":0,"attack":13,"armor":10}
            ui.display_race_choices([orc,human,dwarf,elf])

            player_race = util.get_input("Race",3,0,True).lower()
            if player_race == "human":
                player_stats.update(human)
                break
            elif player_race == "dwarf":
                player_stats.update(dwarf)
                break
            elif player_race == "elf":
                player_stats.update(elf)
                break
            elif player_race == "orc":
                player_stats.update(orc)
                break
            else:
                util.clear_screen()
                ui.display_error_message("Incorect race name.".center(119),4,0)
                util.press_any_button(2,0,True) 
        player_stats.update({"player_location": [player_start_row,player_start_col],
                                "player_icon":player_icon, "inventory": [start_gold],"equipment": equipment})

        ui.clear_screen()
        ui.display_message(f'You have created {player_stats["name"]}, the {player_stats["race"]}'.center(119),4,0)
        ui.display_message(f"Do you want to play as {player_stats['name']}? (yes/no)".center(119),2,0)
        if util.get_confirmation("",0):
            break
    return player_stats

def save_game(player, boards, board_level,escaped_cave):
    with open("saved_games.py","w",encoding="utf-8") as save_file:
        save_file.write(f"player = {player}\nboards = {boards}\nboard_level = {board_level[0]}\nescaped_cave = {escaped_cave}")

def load_game(player, boards, board_level,escaped_cave):
    try:
        import saved_games
        reload(saved_games)
        player.update(saved_games.player)
        boards[:] = saved_games.boards
        board_level[0] = saved_games.board_level
        escaped_cave[0] = saved_games.escaped_cave[0]
        return True
    except:
        util.clear_screen()
        ui.display_error_message("There are no saved games".center(119),3,0)
        util.press_any_button(2,0,True)
        util.clear_screen()
        return False

def cheats(lumos_on):
    util.clear_screen()
    ui.display_message("Input your cheat code:".center(119),3,0)
    print()
    cheat_code = input("".rjust(119//2)).lower()
    if cheat_code == "lumos":
        lumos_on[0] = 1

def create_pause_menu(sound_one):
    options = ["Exit Game",
               "Resume Game",
               "Save Game",
               "Load Game",
               "Main Menu",
               "Cheats"]
    if sound_one == [1]:
        options.insert(4,"Mute Sound")
    else:
        options.insert(4,"Unmute Sound")
    ui.display_menu("Game paused", options)

def pause_menu(player, boards, board_level, sound_on,unmuted,lumos_on,escaped_cave):
    while True:
        create_pause_menu(sound_on)
        try:
            option = int(util.get_input("Select option".rjust(130//2),1,0))
            if option == 0:
                return "exit_game"
            elif option == 1:
                return
            elif option == 2:
                return save_game(player, boards, board_level,escaped_cave)
            elif option == 3:
                load_game(player, boards, board_level,escaped_cave)
                return "load_game"
            elif option == 4:
                if sound_on == [1]:
                    sound_on[0] = 0
                    unmuted[0] = 0
                else:
                    sound_on[0] = 1
                    unmuted[0] = 1
                return
            elif option == 5:
                return "back_to_menu"
            elif option == 6:
                cheats(lumos_on)
                return
            else:
                raise KeyError
        except KeyError:
            util.clear_screen()
            ui.display_error_message("There is no such option!".center(119),3,0)
            util.press_any_button(2,0,True)
            util.clear_screen()
            
        except ValueError:
            util.clear_screen()
            ui.display_error_message("Please enter a number!\n".center(119),3,0)
            util.press_any_button(2,0,True)
            util.clear_screen()

def is_unoccupied(board,row,col):
    return board[row][col] == " " or board[row][col] == "O"
    # return True

def is_not_wall(board, row, col):
    return (board[row][col] != "=" and board[row][col] != "|")
    # return True

def get_player_placement(board, player_icon):
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == player_icon:
                return i,j

def put_player_on_board(board, player,player_icon):
    cords = get_player_placement(board, player_icon)
    if cords:
        board[cords[0]][cords[1]] = " "
    player_row, player_col, player_icon = player["player_location"][0],player["player_location"][1], player["player_icon"]
    board[player_row][player_col] = player_icon

def player_location_after_door(board,player_location_row,player_location_col):
    if player_location_row == 0:
        player_location_row = len(board)-2
    elif player_location_row == len(board)-1:
        player_location_row = 1
    elif player_location_col == 0:
        player_location_col = len(board[0])-2
    elif player_location_col == len(board[0])-1:
        player_location_col = 1
    return [player_location_row,player_location_col]
    
def get_next_level_old_door_location(board,row,col):
    if row == 0:
        row = len(board)-1
    elif row == len(board)-1:
        row = 0
    elif col == 0:
        col = len(board[0])-1
    elif col == len(board[0])-1:
        col = 0
    return [row,col]

def put_door_on_board(boards,door_icon):
    enter_door_row = random.randint(0, len(boards[0])-1)
    if enter_door_row in [0, len(boards[0])-1]:
        enter_door_col = random.choice([1,len(boards[0][0])-2])
    else:
        enter_door_col = random.choice([0, len(boards[0][0])-1])

    for i in range(len(boards)):
        if i == 0:
            boards[0][enter_door_row][enter_door_col] = door_icon
        elif i == 1:
            boards[1][0][58] = door_icon
            exit_door_row, exit_door_col = get_next_level_old_door_location(boards[0], enter_door_row, enter_door_col)
            boards[1][exit_door_row][exit_door_col] = "O" #open door
        elif i == 2:
            enter_door_row = 0
            enter_door_col = 58
            boards[2][enter_door_row][enter_door_col] = door_icon
            exit_door_row = 31
            exit_door_col = 58
            boards[2][exit_door_row][exit_door_col] = "O"
        else:
            pass

def find_the_door(board):
    for row in range(len(board)):
        for col in range(len(board[0])):
            if board[row][col] == "X":
                return row,col

def delete_key_from_inventory(inventory):
    for index in range(len(inventory)):
        if inventory[index]["type"] == "Key":
            break
    del inventory[index]       

def open_the_door(board,player):
    enter_door_row,enter_door_col = find_the_door(board)
    if have_key_in_inventory(player["inventory"]):
        board[enter_door_row][enter_door_col] =" "
        delete_key_from_inventory(player["inventory"])
    else:
        util.clear_screen()
        ui.display_message("You do not have a key. Maybe someone can help you...".center(119),3,0)
        util.press_any_button(2,0,True)
        
def is_next_to_player(enemy_row,enemy_col,player):
    player_row, player_col = player["player_location"]
    if enemy_row + 1 == player_row and enemy_col == player_col:
        return True
    elif enemy_row - 1 == player_row and enemy_col == player_col:
        return True
    elif enemy_row == player_row and enemy_col + 1 == player_col:
        return True
    elif enemy_row == player_row and enemy_col - 1 == player_col:
        return True
    return False

def put_npc_quest_on_board(boards,npc_quest_icon):
    boards[0][6][38] = npc_quest_icon
    boards[1][12][21] = npc_quest_icon
    boards[2][26][105] = npc_quest_icon

def put_npc_shop_on_board(board,npc_shop_icon):
    for i in range(len(board)):
        npc_row = random.randint(1, len(board[i])-2)
        npc_col = random.randint(1, len(board[i][0])-2)
        while not is_unoccupied(board[i],npc_row,npc_col):
            npc_row = random.randint(1, len(board[i])-2)
            npc_col = random.randint(1, len(board[i][0])-2)
        board[i][npc_row][npc_col] = npc_shop_icon

def put_item_on_board(board,item_icon):
    for i in range(len(board)):
        item_row = random.randint(1, len(board[i])-2)
        item_col = random.randint(1, len(board[i][0])-2)
        for x in range (0,11):
            while not is_unoccupied(board[i],item_row,item_col):
                item_row = random.randint(1, len(board[i])-2)
                item_col = random.randint(1, len(board[i][0])-2)
                x-=1
            board[i][item_row][item_col] = item_icon
def put_treasure_on_board(boards,treasure_icon):
    boards[0][7][69] = treasure_icon

    boards[1][11][32] = treasure_icon
    boards[1][20][23] = treasure_icon

    boards[2][30][4] = treasure_icon
    boards[2][14][106] = treasure_icon
    boards[2][8][84] = treasure_icon

def put_enemy_on_board(board,enemy_icon):
    for i in range(len(board)):
        number_of_enemies = random.randint(10,15)
        while number_of_enemies > 0:
            enemy_row = random.randint(1, len(board[i])-2)
            enemy_col = random.randint(1, len(board[i][0])-2)
            while not is_unoccupied(board[i],enemy_row,enemy_col):
                enemy_row = random.randint(1, len(board[i])-2)
                enemy_col = random.randint(1, len(board[i][0])-2)
            board[i][enemy_row][enemy_col] = enemy_icon
            number_of_enemies -= 1

def put_boss_on_board(board,boss_icon):
    enemy_row = 20
    enemy_col = 20
    board[enemy_row][enemy_col] = boss_icon

def random_item_name(type,type_description):
    item = random.choice(type)
    description_item = random.choice(type_description)
    return (description_item+" "+item).strip()

def create_item(is_shop=False):
    MIN_ATTACK_VALUE = 1
    MAX_ATTACK_VALUE = 10
    MIN_ARMOR_VALUE = 1
    MAX_ARMOR_VALUE = 10
    MIN_GOLD_VALUE = 1
    MAX_GOLD_VALUE = 17
    MIN_CONSUMABLE_VALUE = 10
    MAX_CONSUMABLE_VALUE = 50

    item_stats = dict()
    weapons = ["Bow","Warglaive","Staff","Wand","Axe","Sword","Mace","Dagger","Fist","Crossbow"]
    weapons_description = ["Bloody","Blessed", "Cursed","Doom","Big", "Metal" ,"War","Elvies","Small","Holy","Enchantend",""]
    armor = ["Helmet", "Chest", "Trousers", "Shoes"]
    armor_description = ["Plate","Leather","Mail","Cloth"]
    consumable = ["Ham","Cheese","Elixir","Bread","Water"]
    consumable_description = ["Stinky","Tasty","Godlike"]
    if not is_shop:
        type = ["Weapons","Weapons","Armor","Armor","Health","Gold","Gold","Gold"]
    else:
        type = ["Weapons","Weapons","Weapons","Armor","Armor","Health","Health"]

    randomized_type = random.choice(type)
    item_stats["type"] = randomized_type
    if randomized_type == "Weapons":
        item_stats["name"] = random_item_name(weapons,weapons_description)
        item_stats["type"] = "Attack"
        item_stats["value"] = random.randint(MIN_ATTACK_VALUE,MAX_ATTACK_VALUE)
    elif randomized_type == "Armor":
        item_stats["name"] = random_item_name(armor,armor_description)
        item_stats["value"] = random.randint(MIN_ARMOR_VALUE,MAX_ARMOR_VALUE)
    elif randomized_type == "Health":
        item_stats["name"] = random_item_name(consumable,consumable_description)
        item_stats["value"] = random.randint(MIN_CONSUMABLE_VALUE,MAX_CONSUMABLE_VALUE)
    else:
        item_stats["name"] = "Gold"
        item_stats["value"] = random.randint(MIN_GOLD_VALUE,MAX_GOLD_VALUE)
    return item_stats

def authors():
    crew = [
        "Kordian Płusa     : Full-Stack Developer          ",
        "Kewin Gregorczyk  : Back-end Developer | Audio    ",
        "Dawid Kuropka     : Back-end Developer | Marketing",
        "Jakub Młocek      : Back-end Leader    | Story    ",
        "Dominik Berniak   : Front-end Leader   | Back-end "]
    x = 0
    i = 0
    while x in range(len(crew)*2):
        ui.clear_screen()
        ui.display_title("Game authors:".center(119),4,0)
        if x == 0:
            crew_display = crew[i].center(119)
        elif x%2 != 0:
            crew_display = "\n" + crew_display
            i+=1
        else:
            crew_display = crew[i].center(119) + "\n" + crew_display
        ui.display_message(f"{crew_display}".center(119),2,filler=0)
        sleep(0.2)
        x+=1
    util.press_any_button(3,0,True)
    util.clear_screen()

def story(filename,player):
    with open(filename,"r") as file:
        story = file.readlines()
    x = 0
    i = 0
    while x in range(len(story)*2):
        ui.clear_screen()
        if x == 0:
            story_display = story[i].center(119)
        elif x%2 != 0:
            story_display = "\n" + story_display
            i+=1
        else:
            story_display = story[i].center(119) + story_display
        ui.display_message(f"{story_display}".replace("NAME",player["name"].upper()).center(119),4,0)
        sleep(0.8)
        x+=1
    util.press_any_button(2,0,True)
    util.clear_screen()

def instruction():
    ui.clear_screen()
    information = """Preparation for the game:
First you need to create a character. Choose the races responsibly!
Each race has different stats. The character is moved by W/S/A/D.
Objective:
The main goal is to defeat the final boss,
but before you get to this stage, you have to kill a lot of enemies.
During your adventure you will meet shop npcs with whom you can trade.
You will also meet quest npcs who will give you riddles to solve.
Legend:
@ - You         X - Gate
$ - Shop        ? - Quest
T - Monster     & - Item 
% - Treasure
"""
    
    information = information.split("\n")
    longest_row_lenght = len(max(information,key=len))
    for i in range(len(information)):
        filler = (longest_row_lenght-len(information[i]))*" "
        if i != 0 and i !=3 and i!=8:
            ui.display_message(f"{information[i]}{filler}".center(119),1,0)
        else:
            ui.display_message(f"{information[i]}{filler}".center(119),3,0)
    util.press_any_button(1,0,True)
    util.clear_screen()

def hall_of_fame(mode,player_level=0, current_exp = 0, player_name=""):
    if mode == "result":
        try:
            HOF_scores = open(r"hall_of_fame.txt", "a+")
            HOF_scores.write(f"{player_name}|{100 * player_level + current_exp}\n")
        except:
            ui.display_message("Program encountered critical error! (error type: missing file)")
    elif mode == "scoreboard":
        scoreboard = []
        try:
            HOF_scores = open(r"hall_of_fame.txt", "r")
        except:
            HOF_scores = open(r"hall_of_fame.txt", "a+")
        for line in HOF_scores.readlines():
            line = line.split("|")
            line[1] = int(line[1])
            scoreboard.append(line)
        sorted_score = sorted(scoreboard, key=lambda x: x[1])[:10]
        util.clear_screen()
        print("\n")
        longest_name_lenght = len(sorted_score[0][0])
        longest_score_length = len(str(sorted_score[0][1]))
        for i in range(len(sorted_score)):
            if len(sorted_score[i][0]) > longest_name_lenght:
                longest_name_lenght = len(sorted_score[i][0])

            if len(str(sorted_score[i][1])) > longest_score_length:
                longest_score_length = len(str(sorted_score[i][1]))

        ui.display_title("Hall of Fame\n".center(119),2,0)
        for count,score in enumerate(sorted_score, start=1):
            name_lenght = len(score[0])
            score_length = len(str(score[1]))
            filler_name = (longest_name_lenght-name_lenght)* " "
            filler_score = (longest_score_length - score_length)* " "

            ui.display_message(f"{count}. {score[0]}{filler_name}  : score = {int(score[1])}{filler_score}".center(119),1,0)
        util.press_any_button(3,0,True)
        util.clear_screen()

def create_menu():
    options = ["Exit game", 
               "New Game",
               "Load Game",
               "Hall of Fame",
               "Authors",
               "Instruction"]
    ui.display_menu("Main menu", options)

def load_module(option):
    if option == 1:
        return "start_game"
    elif option == 2:
        return "load_game"
    elif option == 3:
        hall_of_fame("scoreboard")
    elif option == 4:
        authors()
    elif option == 5:
        instruction()
    elif option == 0:
        return "quit"
    else:
        raise KeyError()

def menu():
    while True:
        create_menu()
        try:
            option = util.get_input("Select option".rjust(130//2),1,0)
            option = load_module(int(option))
            if option == "start_game" or option == "quit" or option == "load_game":
                return option

        except KeyError:
            util.clear_screen()
            ui.display_error_message("There is no such option!".center(119),3,0)
            util.press_any_button(2,0,True)
            util.clear_screen()
            
        except ValueError:
            util.clear_screen()
            ui.display_error_message("Please enter a number!".center(119),3,0)
            util.press_any_button(2,0,True)
            util.clear_screen()

def create_npc(name,cost_item,amount_items_in_shop):
    list_items_in_shop = []
    for i in range(amount_items_in_shop):
        list_items_in_shop.append(create_item(True))
    npc = {
        "icon": "$",
        "name": name,
        "cost_item": cost_item,
        "shop": list_items_in_shop
    }
    return npc

def create_torch():
    torch = {
        "type" : "Key",
        "name" : "Torch",
        "value": 1
    }
    return torch

def create_key():
    torch = {
        "type" : "Key",
        "name" : "Key",
        "value": 1
    }
    return torch

def create_peter():
    peter = {
        "icon": "?",
        "name":"Peter Iscoming",
        "quest_description": "You have to correctly answer my question",
        "quest":"What is the name of a command that adds one or more files to the staging area?",
        "answer": "git add",
        "reward": create_torch(),
        "is_done": False
    }
    return peter

def create_kate():
    kate = {
        "icon": "?",
        "name": "Kate Antlish",
        "quest_description": "You have to correctly answer my question",
        "quest": "How to reverse a string with variable name: \"word?\"",
        "answer":"word[::-1]",
        "reward":create_key(),
        "is_done": False
    }
    return kate

def create_adalbert():
    adalbert = {
        "icon":"?",
        "name": "Adalbert Gribbs",
        "quest_description": "You have to correctly answer my question",
        "quest": "What is StackOverflow? ",
        "answer":"i dont know",
        "reward":create_key(),
        "is_done": False
    }
    return adalbert

def have_key_in_inventory(inventory):
    for index in range(len(inventory)):
        if inventory[index]["type"] == "Key":
            return True
    return False

def do_quest(player,board_lvl):
    if board_lvl == 0:
        npc = create_kate()
    elif board_lvl == 1:
        npc = create_peter()
    else:
        npc = create_adalbert()
    if not have_key_in_inventory(player["inventory"]) or npc["is_done"]:
        util.clear_screen()
        ui.display_message(f"{npc['name']} : {npc['quest_description']}".center(119),3,0)
        ui.display_message(f"{npc['name']} : {npc['quest']}".center(119),3,0)
        print("\n")
        answer = input("".rjust(119//2)).lower()
        reward = npc["reward"]

        if answer == npc["answer"]:
            util.clear_screen()
            ui.display_message(f"{npc['name']} : Correct. Here is your key".center(119),3,0)
            add_to_inventory(player,reward)
        else:
            util.clear_screen()
            ui.display_message(f"{npc['name']} : Wrong answer".center(119),3,0)
    else:
        util.clear_screen()
        ui.display_message(f"{npc['name']} : You have the key already".center(119),3,0)    
    util.press_any_button(2,0,True)

def add_to_inventory(player, added_items):
    inventory = player["inventory"]
    is_in_inventory = False
    for items in inventory:
        if items["name"] == added_items["name"]:
            items["value"] += added_items["value"]
            is_in_inventory = True
    if not is_in_inventory:
        inventory.append(added_items)

def update_gold_in_inventory(inventory,amount_of_gold):
    for index in range(len(inventory)):
        if inventory[index]["name"] == "Gold":
            if inventory[index]["value"] + amount_of_gold < 0:
                raise ValueError
            else:
                inventory[index]["value"] += amount_of_gold

def create_boss():
    boss = {
        "adjective":"Demon",
        "name":"Yoshi",
        "health":200,
        "attack":35,
        "armor":20,
        "exp":0
    }
    return boss

def create_enemy(player):
    skeleton = {"adjective": "","name":"Skeleton","health":[5,20],"attack": 10,"armor":5, "exp": 10}
    ghoul = {"adjective": "","name":"Ghoul","health":[15,30],"attack": 20,"armor":0, "exp": 15}
    boar = {"adjective": "","name":"Boar","health":[10,30],"attack": 10,"armor":2, "exp": 25}
    spider = {"adjective": "","name":"Spider","health":[3,17],"attack": 15,"armor":0, "exp": 15}
    ghost = {"adjective": "","name":"Ghost","health":[1,8],"attack": 7,"armor":0, "exp": 5}
    ogre = {"adjective": "","name":"Ogre","health":[20,60],"attack": 25,"armor":10, "exp": 75}
    enemy = random.choice([skeleton, ghoul, boar, spider, ghost, ogre])

    enemy_adjectives = ["Mighty", "Fearless", "Powerful", "Deadly", "Ferocious", "Horrifying", "Frightening", "Spooky", "Ghostly"]
    enemy_adjective = random.choice(enemy_adjectives)
    if enemy["name"] == "Skeleton":
        enemy_adjective = random.choice([enemy_adjective, "Scary Spooky"])
    enemy["adjective"] = enemy_adjective
    
    player_level = player["lvl"]
    if player_level < 5: 
        enemy["health"][1] = enemy["health"][1]//2
        enemy["armor"] = enemy["armor"]//2
    enemy["health"] = random.randint(enemy["health"][0],enemy["health"][1])

    return enemy

def sell_from_inventory(player):
    unsold_items = ["gold","torch","key"]
    while True:
        if len(player["inventory"]) < 2:
            util.clear_screen()
            ui.display_message("You don't have anything to sell".center(119),3,0)
            util.press_any_button(2,0,True)
            break
        ui.display_inventory(player["inventory"])
        ui.display_message("What do you want to sell?".center(119),3,0)
        print("\n")
        name_item_to_sell = input("".rjust(119//2)).lower()
        index = 0
        if name_item_to_sell in ["return",""]:
            break
        if name_item_to_sell in unsold_items:
            continue
        for item in player["inventory"]:
            if name_item_to_sell == item["name"].lower():
                break
            index += 1
        try:
            del player["inventory"][index]
            update_gold_in_inventory(player["inventory"],10)
            util.clear_screen()
            if len(player["inventory"])>0:
                ui.display_inventory(player["inventory"])
            else:
                util.clear_screen()
                ui.display_message("Your inventory is empty.".center(119),3,0)
            util.press_any_button(3,0,True)

        except IndexError:
            util.clear_screen()
            ui.display_error_message(f"You don't have {name_item_to_sell.title()}".center(119),3,0)
            util.press_any_button(3,0,True)
        
        util.clear_screen()
        if util.get_confirmation("Wanna sell somthing else?".center(119),3):
            util.clear_screen()
        else:
            break

def buy_from_shop(player,npc):
    shop = npc["shop"]
    while True:
        ui.display_inventory(shop)
        index = 0
        ui.display_message("What do you want to buy?".center(119),2,0)
        print("\n")
        name_item_to_buy = input("".rjust(119//2)).lower()
        if name_item_to_buy in ["return",""]:
            break
        for item in shop:
            if name_item_to_buy == item["name"].lower():
                break
            index += 1
        try:
            update_gold_in_inventory(player["inventory"],-(npc["cost_item"]))
            add_to_inventory(player,shop[index])
            del shop[index]
            util.clear_screen()
            if len(player["inventory"])>0:
                    ui.display_inventory(player["inventory"])
            else:
                util.clear_screen()
                ui.display_message("Your inventory is empty.".center(119),3,0)
            util.press_any_button(4,0,True)

        except IndexError:
            util.clear_screen()
            ui.display_error_message(f"I don't have {name_item_to_buy.title()}".center(119),3,0)
            util.press_any_button(4,0,True)
        except ValueError:
            util.clear_screen()
            ui.display_error_message(f"You don't have money to buy this".center(119),3,0)
            util.press_any_button(4,0,True)
        util.clear_screen()
        if util.get_confirmation("Wanna buy something else?".center(119),3):
            util.clear_screen()
        else:
            break

def filter_items(inventory,type,part_of_armor=""):
    filtred_inventory = []
    if type == "Armor":
        for item in inventory:
            item_name = item["name"].split(" ")
            if part_of_armor in item_name:
                filtred_inventory.append(item)
    elif type == "Attack":
        for item in inventory:
            if item["type"] == type:
                filtred_inventory.append(item)
    return filtred_inventory

def choose_item_to_wear(filtred_inventory,player,number_of_part_equipment):
    while True:
        util.clear_screen()
        if len(filtred_inventory)>0:
            ui.display_inventory(filtred_inventory)
            ui.display_message("Choose item to wear".center(119),3,0)
            print()
            item_from_inventory = input("".rjust(119//2)).lower()
            for item in filtred_inventory:
                if item["name"].lower() == item_from_inventory:
                    return item
            if item_from_inventory in ["return", ""]:
                return player["equipment"][number_of_part_equipment]
            util.clear_screen()
            ui.display_error_message(f"You do not have {item_from_inventory.title()} in your inventory".center(119),3,0)
            util.press_any_button(2,0,True)
        else:
            util.clear_screen()
            ui.display_message("Your inventory is empty.".center(119),3,0)
            util.press_any_button(2,0,True)
            return player["equipment"][number_of_part_equipment]
        
def wear_equipment(player):
    while True:
        util.clear_screen()
        ui.display_equipment(player)
        equipment = player["equipment"]
        ui.display_message("Choose your part of equipment: ".center(119),2,0)
        print()
        part_of_equipment = input("".rjust(119//2)).title()
        if part_of_equipment == "Head":
            filtred_item = filter_items(player["inventory"],"Armor","Helmet")
            player["armor"] -= equipment[0]["value"]
            equipment[0] = choose_item_to_wear(filtred_item,player,0)
            player["armor"] += equipment[0]["value"]
        elif part_of_equipment == "Chest":
            filtred_item = filter_items(player["inventory"],"Armor","Chest")
            player["armor"] -= equipment[1]["value"]
            equipment[1] = choose_item_to_wear(filtred_item,player,1)
            player["armor"] += equipment[1]["value"]
        elif part_of_equipment == "Legs":
            filtred_item = filter_items(player["inventory"],"Armor","Trousers")
            player["armor"] -= equipment[2]["value"]
            equipment[2] = choose_item_to_wear(filtred_item,player,2)
            player["armor"] += equipment[2]["value"]
        elif part_of_equipment == "Shoes":
            filtred_item = filter_items(player["inventory"],"Armor","Shoes")
            player["armor"] -= equipment[3]["value"]
            equipment[3] = choose_item_to_wear(filtred_item,player,3)
            player["armor"] += equipment[3]["value"]
        elif part_of_equipment == "Weapons":
            filtred_item = filter_items(player["inventory"],"Attack")
            player["attack"] -= equipment[4]["value"]
            equipment[4] = choose_item_to_wear(filtred_item,player,4)
            player["attack"] += equipment[4]["value"]
        elif part_of_equipment in ["", "Return"]:
            return "pressed_enter"
        else:
            util.clear_screen()
            ui.display_error_message("No such part of equipement".center(119),3,0)
            util.press_any_button(2,0,True)
    
def use_item(player):
    inventory = list(player["inventory"])
    inventory_to_display = [inventory[i] for i in range(len(inventory)) if inventory[i]["type"] == "Health"]
    if len(inventory_to_display)>0:
        while True:
            util.clear_screen()
            ui.display_inventory(inventory_to_display,"Consumables:\n")
            was_item_used = False
            ui.display_message("What do you want to use?".center(119),4,filler=0)
            ui.display_message("(name of item / return)\n".center(120),1,filler=0)
            player_input = input("".rjust(119//2)).title()
            if player_input == "Return":
                return False
            for i in range(len(inventory)):
                if inventory[i]["name"] == player_input:
                    player["health"] += inventory[i]["value"]
                    player["inventory"].pop(i)
                    was_item_used = True
                    break
            if was_item_used:
                return was_item_used
            else:
                ui.display_error_message("No such item in your inventory".center(119), 4,0)
                util.press_any_button(2,center=True)
    else:
        util.clear_screen()
        ui.display_error_message("There are no consumables in your inventory".center(119),4,0)
        util.press_any_button(2,center=True)
        return False

def add_random_item_to_inventory(player, is_treasure=False):
    if not is_treasure:
        random_item = create_item()
    else:
        random_item = {"type": "Gold", "name": "Gold", "value": 20}
    if random_item["type"] == "Gold":
        added_gold = False
        for i in range(len(player["inventory"])):
            if player["inventory"][i]["type"] == "Gold":
                player["inventory"][i]["value"] += random_item["value"]
                added_gold = True
        if not added_gold:
            player["inventory"].append(random_item)
    else:
        player["inventory"].append(random_item)
    return random_item

def fight_enemy(player,is_boss=False):
    if is_boss:
        enemy = create_boss()
    else:
        enemy = create_enemy(player)
    enemy_turn = "Enemy"
    player_turn = "Player"
    turn = random.choice([enemy_turn,player_turn])

    util.clear_screen()
    if is_boss:
        ui.display_title(f'You have encountered {enemy["adjective"]} {enemy["name"]}.'.center(119),3,0)
    else:
        ui.display_title(f'You have encountered the {enemy["adjective"]} {enemy["name"]}.'.center(119),3,0)
    util.press_any_button(2,0,True)
    while True:
        util.clear_screen()
        ui.display_stats(enemy,1," ",5)
        ui.display_fight_art()
        ui.display_stats(player,1)

        #enemy turn
        if turn == enemy_turn:
            ui.display_message(f"It's {turn.lower()}'s turn to attack".center(119),2,0)
            sleep(1)
            enemy_max_damage = (enemy["attack"] - player["armor"])
            if enemy_max_damage > 0:
                enemy_damage = random.randint(1,enemy_max_damage)
                player["health"] -= enemy_damage
            else:
                enemy_damage = 0
            ui.display_message(f"{enemy['name']} did {enemy_damage} damage".center(119),2,filler=0)
            util.press_any_button(1,0,True)
            util.clear_screen()
            turn = player_turn

        #player turn
        else:
            ui.display_message(f"It's your turn to attack".center(119),4,0)
            ui.display_message("Attack | Use Item\n".center(119),2,0)
            player_input = input("".rjust(119//2)).lower().replace(" ", "")
            if player_input in ["useitem", "u", "i"]:
                did_use_item = use_item(player)
                if did_use_item:
                    turn = enemy_turn
            else:
                player_max_damage = (player["attack"] - enemy["armor"])
                if player_max_damage > 0:
                    player_damage = random.randint(1,player_max_damage)
                    enemy["health"] -= player_damage + player["lvl"]
                else:
                    player_damage = 0
                if enemy["health"] > 0:
                    ui.display_message(f"You did {player_damage} damage".center(119),2,filler=0)
                    util.press_any_button(1,0,True)
                    util.clear_screen()
                    turn = enemy_turn

        if enemy["health"]<=0 or player["health"]<=0:
            break

    if enemy["health"] <= 0:
        player["exp"] += enemy["exp"]
        if player["exp"] >= 100:
            while True:
                player["lvl"] += 1
                player["exp"] -= 100
                if player["exp"] < 100:
                    break
        dropped_item = add_random_item_to_inventory(player)
        util.clear_screen()
        if dropped_item["name"] != "Gold":
            ui.display_message(f"You have killed the {enemy['adjective']} {enemy['name']}, have gained {enemy['exp']} exp and have picked up {dropped_item['name']}".center(119),4,0)
        else:
            ui.display_message(f"You have killed the {enemy['adjective']} {enemy['name']}, have gained {enemy['exp']} exp and have picked up {dropped_item['value']} {dropped_item['name']}".center(119),4,0)
        util.press_any_button(1,0,True)
        return "victory"
    else:
        return "defeat"

def interaction_with_traders(player,board_level):
    shop_level_1 = create_npc("Dominic Passivniac",10,8) # panowie sory musiałem XD
    shop_level_2 = create_npc("Kevin Gregorish",10,8)
    shop_level_3 = create_npc("Jacob Hamer",10,8)
    npcs = [shop_level_1,shop_level_2,shop_level_3]
    while True:
        ui.clear_screen()
        ui.display_message(f"{npcs[board_level]['name']}: Do you want to buy or sell something?".center(119),3,0)
        print("\n")
        sell_or_buy = input("".rjust(119//2)).lower()
        if sell_or_buy == "sell":
            sell_from_inventory(player)
        elif sell_or_buy == "buy":
            buy_from_shop(player,npcs[board_level])
        elif sell_or_buy in ["return", ""]:
            return
        else:
            util.clear_screen()
            ui.display_error_message(f"{npcs[board_level]['name']}: I don't understand. See you later!".center(119),3,0)
            util.press_any_button(2,0,True)
            break

def get_boss_location(board,boss_icon):
    for row in range(len(board)):
        for col in range(len(board[0])):
            if board[row][col] == boss_icon:
                return [row,col]
    return [False]

def encounter(board, player, player_row, player_col,quest_icon,shop_icon,enemy_icon,item_icon,board_level,door_icon,treasure_icon,boss_icon):
    if board[player_row][player_col] == quest_icon:
        do_quest(player,board_level)
        return [0]
    elif board[player_row][player_col] == shop_icon:
        interaction_with_traders(player,board_level)
        return [0]
    elif board[player_row][player_col] == enemy_icon:
        result = fight_enemy(player)
        if result == "victory":
            return [1]
        elif result == "defeat":
            return [0,"defeat"]
    elif board[player_row][player_col] == boss_icon:
        result = fight_enemy(player,True)
        if result == "victory":
            return [0,"final_victory"]
        elif result == "defeat":
            return [0,"defeat"]
    elif board[player_row][player_col] == door_icon:
        open_the_door(board, player)
        return [0]
    elif board[player_row][player_col] == item_icon:
        item = add_random_item_to_inventory(player)
        util.clear_screen()
        if item["name"] != "Gold":
            ui.display_message(f"You have picked up {item['name']}.".center(119),3,0)
        else:
            ui.display_message(f"You have picked up {item['value']} {item['name'].lower()}.".center(119),3,0)
        util.press_any_button(1,0,True)
        util.clear_screen()
        return [1]
    elif board[player_row][player_col] == treasure_icon:
        util.clear_screen()
        ui.display_message(f"You have found a treasure. You have picked up 20 gold.".center(119),3,0)
        util.press_any_button(1,0,True)
        add_random_item_to_inventory(player,is_treasure=True)
        return [1]

def move_enemies_randomly(board,enemy_icon,player,is_boss = False):
    if is_boss:
        range_of_enemy = 3
    else:
        range_of_enemy = 0

    enemy_cords = []
    for x in range(len(board)):
        for y in range(len(board[0])):
            if board[x][y] == enemy_icon:
                enemy_cords.append([x,y])        

    i = 0
    while i < len(enemy_cords):
        enemy_current_row = enemy_cords[i][0]
        enemy_current_col = enemy_cords[i][1]
        if is_next_to_player(enemy_current_row,enemy_current_col,player):
            board[enemy_current_row][enemy_current_col] = " "
            if is_boss:
                return fight_enemy(player,True)
            else:
                return fight_enemy(player)
        
        random_row_move = random.choice([-1,0,0,0,0,0,1])
        if random_row_move in [-1,1]:
            random_col_move = 0
        else:
            random_col_move = random.choice([-1,0,0,0,0,0,1])
        if is_unoccupied(board,enemy_current_row+random_row_move+range_of_enemy,enemy_current_col+random_col_move+range_of_enemy):
            board[enemy_current_row][enemy_current_col] = " "
            board[enemy_current_row+random_row_move][enemy_current_col+random_col_move] = enemy_icon
            i+=1
        else:
            i+=1

