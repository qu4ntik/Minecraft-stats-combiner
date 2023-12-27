import os
import json

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
stats_folder_path = os.path.join(BASE_DIR, "stats_folder")
#final_json_path = os.path.join(BASE_DIR, "ur_combined_stats")

#X 1. Demander a l'utilisateur si il prefère import ses fichiers stats (1) ou si il pref donner le chemin vers son dossier minecraft (2)
#X 1.1 Si (2) : Lui demander d'input le chemin vers son dossier minecraft
#X 2.Importer tous les fichiers JSON du fichier DATA et les input dans une function qui va return un DICT
# 3. 

#'clear', 'copy', 'fromkeys', 'get', 'items', 'keys', 'pop', 'popitem', 'setdefault', 'update', 'values']
    
#folder = folder_path_input
def combine_stats(folder):

    files = os.listdir(folder)
    stats_combined = {}

    for file in files:

        print(f"Actual file = {file}")
        folder_path = os.path.join(folder, file)
        
        if file.endswith('.json'): #si le fichier se termine bien par .JSON...
            with open(folder_path, 'r') as f:

                try:
                    json_buffer = json.load(f)
                except json.decoder.JSONDecodeError:
                    continue

                try: #si ce n'est pas un fichier stats, passer a la prochain iteration...
                    if json_buffer.get("stats") == None:
                        continue
                except KeyError:
                    continue
                except TypeError:
                    continue
                except AttributeError:
                    continue

                if stats_combined == {}: #si c'est le premier alors...
                    print(f"stats_combined = {file}")
                    stats_combined = json_buffer
                    continue

###################################################################################################################
                for category in json_buffer["stats"]:
                    print(f"category type = {type(category)} | category = {category}")

                    for stat in json_buffer["stats"][category]:
                        print(f"stat type = {type(stat)} | stat = {stat}")

                        if stats_combined["stats"][category].get(stat) != None: #si il y a match entre les deux dicts
                            print(f"The stat : {stat} is getting combined...")
                            stats_combined["stats"][category][stat] += json_buffer["stats"][category][stat]
                        
                        else:
                            stats_combined["stats"][category][stat] = json_buffer["stats"][category][stat]

    stats_combined["stats"]['minecraft:custom']["minecraft:time_since_death"] = 0
    stats_combined["stats"]['minecraft:custom']["minecraft:time_since_rest"] = 0
    json_stats_combined = json.dumps(stats_combined)
    with open(os.path.join(BASE_DIR, "ur_combined_stats.json"), "w") as f:
        f.write(json_stats_combined)

    print("\nThe script execution is completed.\nYou can now find a combined stats .json in the same folder as this script.")

    try:
        print(f"\nYou played {round((stats_combined['stats']['minecraft:custom']['minecraft:play_time'] / 600), 1)} hours.")
        print(f"You sneaked {round((stats_combined['stats']['minecraft:custom']['minecraft:sneak_time'] / stats_combined['stats']['minecraft:custom']['minecraft:play_time']) * 100, 2)}% of your total playtime.")
        print(f"You jumped {stats_combined['stats']['minecraft:custom']['minecraft:jump']} times.")
        print(f"You dealt {stats_combined['stats']['minecraft:custom']['minecraft:damage_dealt']} damage while you took {stats_combined['stats']['minecraft:custom']['minecraft:damage_taken']}.")
        print(f"You killed {stats_combined['stats']['minecraft:custom']['minecraft:mob_kills']} mobs.")
        print(f"You opened {stats_combined['stats']['minecraft:custom']['minecraft:open_chest']} chests.")
        print(f"You walked {round((stats_combined['stats']['minecraft:custom']['minecraft:walk_one_cm'] / 100))} meters while you sprinted {round((stats_combined['stats']['minecraft:custom']['minecraft:sprint_one_cm'] / 100))} meters.")
        print(f"You flew {round((stats_combined['stats']['minecraft:custom']['minecraft:fly_one_cm'] / 100))} meters and swimmed {round((stats_combined['stats']['minecraft:custom']['minecraft:swim_one_cm'] / 100))} meters.")

        print("\nYou can now rename your combined file and replace it in a world to fully check your stats or to play with.")

    except KeyError:
        pass
###################################################################################################################
                

if __name__ == "__main__":
    
    print("##### Welcome to my Minecraft stats combiner. #####\n")
    print("How are you importing the stats files ?")
    main_input = input("Please enter 1 if you put them in the stats_folder, enter 2 if you want to import your minecraft folder.\n>")

    while main_input not in "12":
        print("Please enter a valid number.")
        main_input = input(">")
        print(f"main_input = {main_input}")
    
    if main_input == "1":
        print("1!")

        if os.listdir(stats_folder_path) == []:
            print("\nYour stats_folder is empty.")

        combine_stats(stats_folder_path)

    if main_input == "2":
        print("2!")

        minecraft_map_folder_path = input("\nPlease enter your minecraft or curseforge folder path.\nYou have to right click to use copy/paste here.\n>")

        while os.path.exists(minecraft_map_folder_path) == False:
            minecraft_map_folder_path = input("Your path is incorrect.\n>")

        if not "saves" in minecraft_map_folder_path: #rajouter /saves au path si il n'y est pas
            minecraft_map_folder_path =  os.path.join(minecraft_map_folder_path, "saves")

        combine_stats(minecraft_map_folder_path)
