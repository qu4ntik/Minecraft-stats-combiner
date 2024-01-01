import os, json

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
stats_folder_path = os.path.join(BASE_DIR, "stats_folder")
stats_combined = {}
#final_json_path = os.path.join(BASE_DIR, "ur_combined_stats")

def find_stats_folders(folder): #search and find all json files in /saves folder and copy it into the stats_folder
 #   folder = os.path.join(folder, "saves") #C:\Users\jerem\AppData\Roaming\.minecraft\saves
    file = os.listdir(folder)
    print(f"map folders = {file}")

    for root, dirs, files in os.walk(folder): #directory tree generator | root = directory path (folder) | 
        #print(f"root = {root}\ndirs = {dirs}\nfiles = {files}")
        for file in files:

            if "stats" not in root:
                continue
   
            #print(f"root = {root}\ndirs = {dirs}\nfile = {file}")
            combine_stats(root)

def final_exec():

        stats_combined["stats"]['minecraft:custom']["minecraft:time_since_death"] = 0 
        stats_combined["stats"]['minecraft:custom']["minecraft:time_since_rest"] = 0
        json_stats_combined = json.dumps(stats_combined)

        if not "-" in player_uuid: #simple check if the file name contain the user UUID
            with open(os.path.join(BASE_DIR, "ur_combined_stats.json"), "w") as f:
                f.write(json_stats_combined)
                print(f"ur_combined_stats.json has been created, you will have to rename it with your proper UUID.")
        
        json_check = os.listdir(BASE_DIR) #check if there are already a .json generated at the base dir

        count_json = 0 #for loop for counting the number of possible .json files in base_dir. | note: json_check.count(".json") doesn't worked
        for file_name in json_check:
            if ".json" in file_name:
                count_json += 1

        duplicate_player_uuid_file_name = ""
        print(f"count_json = {count_json}")
        print(f"json_check = {json_check}")

        for json_type in json_check: #
            if ".json" in json_type:
                duplicate_player_uuid_file_name = player_uuid + str(count_json)
                with open(os.path.join(BASE_DIR, duplicate_player_uuid_file_name), "w") as f:
                    json_check = os.listdir(BASE_DIR)
                    f.write(json_stats_combined)
                    print(f"\n{duplicate_player_uuid_file_name} has been written and the file name should be your minecraft UUID.")
                break

            else:     
                with open(os.path.join(BASE_DIR, player_uuid), "w") as f:
                    json_check = os.listdir(BASE_DIR)
                    f.write(json_stats_combined)
                    print(f"\n{player_uuid} has been written and the file name should be your minecraft UUID.")

        print("\n### The script execution is completed ! ###\nYou can now find a combined stats .json in the same folder as this script.\nYou can use it to fully check your stats or to play with.\n")

        try:
            print(f"You played {round((stats_combined['stats']['minecraft:custom']['minecraft:play_time'] / 600), 1)} hours.")
            print(f"You sneaked {round((stats_combined['stats']['minecraft:custom']['minecraft:sneak_time'] / stats_combined['stats']['minecraft:custom']['minecraft:play_time']) * 100, 2)}% of your total playtime.")
            print(f"You jumped {stats_combined['stats']['minecraft:custom']['minecraft:jump']} times.")
            print(f"You dealt {stats_combined['stats']['minecraft:custom']['minecraft:damage_dealt']} damage while you took {stats_combined['stats']['minecraft:custom']['minecraft:damage_taken']}.")
            print(f"You killed {stats_combined['stats']['minecraft:custom']['minecraft:mob_kills']} mobs.")
            print(f"You opened {stats_combined['stats']['minecraft:custom']['minecraft:open_chest']} chests.")
            print(f"You walked {round((stats_combined['stats']['minecraft:custom']['minecraft:walk_one_cm'] / 100))} meters while you sprinted {round((stats_combined['stats']['minecraft:custom']['minecraft:sprint_one_cm'] / 100))} meters.")
            print(f"You flew {round((stats_combined['stats']['minecraft:custom']['minecraft:fly_one_cm'] / 100))} meters and swimmed {round((stats_combined['stats']['minecraft:custom']['minecraft:swim_one_cm'] / 100))} meters.")
        except Exception:
            pass

def combine_stats(folder):

    global stats_combined
    global player_uuid
    files = os.listdir(folder)
    for file in files:

        print(f"Actual file = {file}")
        folder_path = os.path.join(folder, file)

        if file.endswith('.json'): #.JSON CHECK
            with open(folder_path, 'r') as f:

                try:
                    json_buffer = json.load(f)
                except Exception:
                    continue
            #----------- fin du WITH OPEN -------------
            try: #STATS FILE CHECK
                if json_buffer.get("stats") == None:
                    print(f"{file} is not a minecraft stats file. Skipping.")
                    continue
            except Exception:
                continue

            if stats_combined == {}:
                print(f"{file} was defined as the reference dict.")
                player_uuid = file
                stats_combined = json_buffer
                continue

            for category in json_buffer["stats"]:
                #print(f"category type = {type(category)} | category = {category}")

                for stat in json_buffer["stats"][category]:
                    #print(f"stat type = {type(stat)} | stat = {stat}")

                    if stats_combined["stats"][category].get(stat) != None: #si il y a match entre les deux dicts
                        #print(f"The stat : {stat} is getting combined...")
                        stats_combined["stats"][category][stat] += json_buffer["stats"][category][stat]
                    
                    else:
                        stats_combined["stats"][category][stat] = json_buffer["stats"][category][stat]
            print(f"{file} was effectively combined.")





print("##### Welcome to my Minecraft stats combiner. #####\n")
print("How are you importing the stats files ?")
main_input = input("Please enter 1 if you put them in the stats_folder, enter 2 if you want to import your minecraft folder.\n>")

while main_input not in "12":
    print("Please enter a valid number.")
    main_input = input(">")
    print(f"main_input = {main_input}")

if main_input == "1":

    if os.listdir(stats_folder_path) == []:
        print("\nYour stats_folder is empty.")

    combine_stats(stats_folder_path)

if main_input == "2":

    minecraft_map_folder_path = input("\nPlease enter your minecraft or curseforge folder path.\nYou have to right click to use copy/paste here.\n>")

    while os.path.exists(minecraft_map_folder_path) == False:
        minecraft_map_folder_path = input("Your path is incorrect.\n>")

    find_stats_folders(minecraft_map_folder_path)

final_exec() #final execution once all the functions worked well
