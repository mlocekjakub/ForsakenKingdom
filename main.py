import util
import engine
import ui
from time import sleep
import winsound
from boards import level_1, level_2, level_3

PLAYER_ICON = '@'
CLOSED_DOOR_ICON = 'X'
OPEN_EXIT_DOOR_ICON = 'O'
NPC_SHOP_ICON = '$'
NPC_QUEST_ICON = "?"
ENEMY_ICON = 'T'
ITEM_ICON = '&'
TREASURE_ICON = "%"
BOSS_ICON = 'B'
BODY_BOSS_ICON ='+'

PLAYER_START_ROW = 30
PLAYER_START_COL = 58

BOARD_WIDTH = 115
BOARD_HEIGHT = 30
BOSS_BOARD_WIDTH = 60
BOSS_BOARD_HEIGHT = 30

CAVE_LEVEL = 2
BOSS_LEVEL = 3

def player_dead(player):
    util.clear_screen()
    ui.display_title("You are dead")
    ui.display_message(f"You have achieved {player['lvl']} level.",2)
    util.press_any_button(4)
    return main()

def player_win(player):
    util.clear_screen()
    engine.story("end_story.txt",player)
    ui.display_title("You win".center(119),3,0)
    engine.hall_of_fame("result",player['lvl'],player['exp'], player['name'])
    ui.display_message(f"You have achieved {player['lvl']} level.".center(119),2,0)
    util.press_any_button(3,0,True)
    return main()

def quit():
    ui.clear_screen()
    ui.display_message("Thank you for playing. Goodbye!".center(119),4,0)
    sleep(2)
    ui.clear_screen()

def main():
    winsound.PlaySound("sounds/menu.wav",winsound.SND_ASYNC)
    util.clear_screen()
    ui.display_menu_art()
    option = engine.menu()
    if option == "start_game" or option == "load_game":
        if option == "start_game":
            util.clear_screen()
            player = engine.create_player(PLAYER_START_ROW,PLAYER_START_COL,PLAYER_ICON)
            if player["name"] != "Admin":
                engine.story("begin_story.txt",player)    
                ui.display_message("You are entering the Forsaken Kingdom".center(119),4,0)
                util.press_any_button(2,0,True)
                util.clear_screen()
        boards = [level_1,level_2,level_3]
        board_level = [0]
        sound_on = [1]
        unmuted = [0]
        lumos_on = [0]
        escaped_cave = [False]
        engine.put_npc_shop_on_board(boards,NPC_SHOP_ICON)
        engine.put_npc_quest_on_board(boards,NPC_QUEST_ICON)
        engine.put_treasure_on_board(boards,TREASURE_ICON)
        engine.put_enemy_on_board(boards,ENEMY_ICON)
        engine.put_item_on_board(boards,ITEM_ICON)
        engine.put_door_on_board(boards,CLOSED_DOOR_ICON)
        boss_level = engine.create_board(BOSS_BOARD_WIDTH,BOSS_BOARD_HEIGHT)
        boards.append(boss_level)
        engine.put_boss_on_board(boards[BOSS_LEVEL],BOSS_ICON)
        if option == "load_game":
            player = {}
            was_load_successful = engine.load_game(player, boards, board_level, escaped_cave)
            if not was_load_successful:
                return main()
        if sound_on == [1]:
            winsound.PlaySound("sounds/first_map.wav",winsound.SND_ASYNC)

        while True:
            if sound_on == [0]:
               winsound.PlaySound(None,winsound.SND_ASYNC) 
            elif sound_on == [1] and unmuted == [1]:
                if board_level[0] == 0:
                     winsound.PlaySound("sounds/first_map.wav",winsound.SND_ASYNC)
                elif board_level[0] == 1:
                     winsound.PlaySound("sounds/second_map.wav",winsound.SND_ASYNC)
                elif board_level[0] == 2:
                     winsound.PlaySound("sounds/cave.wav",winsound.SND_ASYNC)
                elif board_level[0] == 3:
                     winsound.PlaySound("sounds/boss.wav",winsound.SND_ASYNC)
                unmuted[0] = 0
            
            util.clear_screen()
            engine.put_player_on_board(boards[board_level[0]], player, PLAYER_ICON)
            if board_level[0] == 2:
                if lumos_on == [0]:
                    ui.display_dark_board(boards[2],player)
                else:
                    ui.display_board(boards[board_level[0]])
            elif board_level[0] == 3:
                ui.display_boss_board(boards[board_level[0]])
            else:
                ui.display_board(boards[board_level[0]])
            ui.display_stats(player,2)
            player_location_row, player_location_col = player["player_location"]

            key = util.key_pressed()
            if key == "`":
                ui.clear_screen()
                pause_option = engine.pause_menu(player, boards, board_level,sound_on, unmuted,lumos_on,escaped_cave)
                if pause_option == "exit_game":
                    util.clear_screen()
                    if util.get_confirmation("Do you really want to quit the game? (yes/no)"):
                        return quit()
                elif pause_option == "back_to_menu":
                    return main()
                elif pause_option == "load_game":
                    if board_level[0] == 0:
                        winsound.PlaySound("sounds/first_map.wav",winsound.SND_ASYNC)
                    elif board_level[0] == 1:
                        winsound.PlaySound("sounds/second_map.wav",winsound.SND_ASYNC)
                    elif board_level[0] == 2:
                        winsound.PlaySound("sounds/cave.wav",winsound.SND_ASYNC)
                    elif board_level[0] == 3:
                        winsound.PlaySound("sounds/boss.wav",winsound.SND_ASYNC)


            elif key == "w" and engine.is_not_wall(boards[board_level[0]], player_location_row-1, player_location_col):
                if engine.is_unoccupied(boards[board_level[0]],player_location_row-1,player_location_col):
                    player["player_location"][0] -= 1
                    if sound_on == [1]:
                        winsound.Beep(300,2)
                    engine.move_enemies_randomly(boards[board_level[0]],ENEMY_ICON,player)
                    engine.move_enemies_randomly(boards[board_level[0]],BOSS_ICON,player,True)
                else:
                    player_encounter = engine.encounter(boards[board_level[0]], player,player_location_row-1,player_location_col,NPC_QUEST_ICON,NPC_SHOP_ICON,ENEMY_ICON,ITEM_ICON,board_level[0],CLOSED_DOOR_ICON,TREASURE_ICON,BODY_BOSS_ICON)
                    player["player_location"][0] -= player_encounter[0]
                    if len(player_encounter) > 1 and player_encounter[1] == "defeat":
                        return player_dead(player)
                    elif len(player_encounter) > 1 and player_encounter[1] == "final_victory":
                        return player_win(player)

            elif key == "s" and engine.is_not_wall(boards[board_level[0]], player_location_row+1, player_location_col):
                if engine.is_unoccupied(boards[board_level[0]],player_location_row+1,player_location_col):
                    player["player_location"][0] += 1
                    if sound_on == [1]:
                        winsound.Beep(300,2)
                    engine.move_enemies_randomly(boards[board_level[0]],ENEMY_ICON,player)
                    engine.move_enemies_randomly(boards[board_level[0]],BOSS_ICON,player,True)
                else:
                    player_encounter = engine.encounter(boards[board_level[0]], player,player_location_row+1, player_location_col,NPC_QUEST_ICON,NPC_SHOP_ICON,ENEMY_ICON,ITEM_ICON,board_level[0],CLOSED_DOOR_ICON,TREASURE_ICON,BODY_BOSS_ICON)
                    player["player_location"][0] += player_encounter[0]
                    if len(player_encounter) > 1 and player_encounter[1] == "defeat":
                        return player_dead(player)
                    elif len(player_encounter) > 1 and player_encounter[1] == "final_victory":
                        return player_win(player)

            elif key == "a" and engine.is_not_wall(boards[board_level[0]], player_location_row, player_location_col-1):
                if engine.is_unoccupied(boards[board_level[0]],player_location_row,player_location_col-1):
                    player["player_location"][1] -= 1
                    if sound_on == [1]:
                        winsound.Beep(300,2)
                    engine.move_enemies_randomly(boards[board_level[0]],ENEMY_ICON,player)
                    engine.move_enemies_randomly(boards[board_level[0]],BOSS_ICON,player,True)
                else:
                    player_encounter = engine.encounter(boards[board_level[0]], player,player_location_row,player_location_col-1,NPC_QUEST_ICON,NPC_SHOP_ICON,ENEMY_ICON,ITEM_ICON,board_level[0],CLOSED_DOOR_ICON,TREASURE_ICON,BODY_BOSS_ICON) 
                    player["player_location"][1] -= player_encounter[0]
                    if len(player_encounter) > 1 and player_encounter[1] == "defeat":
                        return player_dead(player)
                    elif len(player_encounter) > 1 and player_encounter[1] == "final_victory":
                        return player_win(player)

            elif key == "d" and engine.is_not_wall(boards[board_level[0]], player_location_row, player_location_col+1):
                if engine.is_unoccupied(boards[board_level[0]],player_location_row,player_location_col+1):
                    player["player_location"][1] += 1 
                    if sound_on == [1]:
                        winsound.Beep(300,2)
                    engine.move_enemies_randomly(boards[board_level[0]],ENEMY_ICON,player)
                    engine.move_enemies_randomly(boards[board_level[0]],BOSS_ICON,player,True)
                else:
                    player_encounter = engine.encounter(boards[board_level[0]], player,player_location_row,player_location_col+1,NPC_QUEST_ICON,NPC_SHOP_ICON,ENEMY_ICON,ITEM_ICON,board_level[0],CLOSED_DOOR_ICON,TREASURE_ICON,BODY_BOSS_ICON) 
                    player["player_location"][1] += player_encounter[0]
                    if len(player_encounter) > 1 and player_encounter[1] == "defeat":
                        return player_dead(player)
                    elif len(player_encounter) > 1 and player_encounter[1] == "final_victory":
                        return player_win(player)
                        
            elif key == "i":
                if (len(player["inventory"]) == 1 and player["inventory"][0]["value"] == 0) or len(player["inventory"]) == 0:
                    util.clear_screen()
                    ui.display_message("Your inventory is empty.".center(119),3,0)
                elif len(player["inventory"])>0:
                    ui.display_inventory(player["inventory"])
                util.press_any_button(4,0,True)

            elif key =="b":
                user_input = engine.wear_equipment(player)
                if user_input != "pressed_enter":
                    util.press_any_button(2 ,0,True)

            #Changing board level
            player_location_row, player_location_col = player["player_location"]
            board_walls = {"rows": [0, len(boards[board_level[0]])-1], "cols": [0, len(boards[board_level[0]][0])-1]}
            if player_location_row in board_walls["rows"] or player_location_col in board_walls["cols"]:
                if board_level[0] == 0:
                    player["player_location"] = engine.player_location_after_door(boards[board_level[0]],player_location_row,player_location_col)
                    board_level[0] = 1
                    if sound_on == [1]:
                        winsound.PlaySound("sounds/second_map.wav",winsound.SND_ASYNC)                 
                elif board_level[0] == 2:
                    if boards[board_level[0]][player_location_row][player_location_col] == OPEN_EXIT_DOOR_ICON:
                        player["player_location"] = [1,58]
                        board_level[0] = 1
                    else:
                        player["player_location"] = [28,3]
                        board_level[0] = 3
                        if sound_on == [1]:
                            winsound.PlaySound("sounds/boss.wav",winsound.SND_ASYNC)
                else:
                    if boards[board_level[0]][player_location_row][player_location_col] == OPEN_EXIT_DOOR_ICON and not escaped_cave[0]:
                        player["player_location"] = engine.player_location_after_door(boards[board_level[0]],player_location_row,player_location_col)
                        board_level[0] -= 1
                        if board_level[0] == 0 and sound_on == [1]:
                            winsound.PlaySound("sounds/first_map.wav",winsound.SND_ASYNC) 
                        if board_level[0] == 1 and sound_on == [1]:
                            winsound.PlaySound("sounds/second_map.wav",winsound.SND_ASYNC)
                    elif board_level[0] == 1 and escaped_cave[0]: #reentering cave
                        player["player_location"] = [30,58]
                        board_level[0] += 1
                        if sound_on == [1]:
                            winsound.PlaySound("sounds/cave.wav",winsound.SND_ASYNC) 
                    else:
                        if board_level[0] != 1:
                            player["player_location"] = engine.player_location_after_door(boards[board_level[0]],player_location_row,player_location_col)
                        else: #entering cave
                            player["player_location"] = [15,58]
                            if not escaped_cave[0]:
                                util.clear_screen()
                                if  sound_on == [1]:
                                    winsound.PlaySound("sounds/cave.wav",winsound.SND_ASYNC)
                                ui.display_message("You have fallen into the cave".center(119),3,0)
                                util.press_any_button(2,0,True)
                                escaped_cave[0] = True
                        board_level[0] += 1
    elif option == "quit":
        quit()

if __name__ == '__main__':
    main()