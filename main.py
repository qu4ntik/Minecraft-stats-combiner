import os, json

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
stats_folder_path = os.path.join(BASE_DIR, "stats_folder")
stats_combined = {}
player_uuid = ""

def find_stats_folders(folder): #search and find all json files in /saves folder and copy it into the stats_folder

    while "saves" in folder: #debugging possible wrong user input path
        folder = input("Please remove the \"/folder\" at the end of your minecraft path\n>")
    while not ".minecraft" in folder: #debugging possible wrong user input path
        folder = input("Please input a valid minecraft path.\n>")

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
    #print(f"json_stats_combined = {json_stats_combined}")

    json_check = os.listdir(BASE_DIR) #check if there are already a .json generated at the base dir
    count_json = 0 #for loop for counting the number of possible .json files in base_dir. | see (1) | note: json_check.count(".json") doesn't worked
    for file_name in json_check:
        if ".json" in file_name:
            if "-" in file_name:
                count_json += 1

    if not "-" in player_uuid: #if the script didn't got the player UUID:
        filename = "ur_combined_stats"
        if count_json == 0: #if there are already no jsons in the main dir
            with open(os.path.join(BASE_DIR, (filename + ".json")), "w") as f:
                f.write(json_stats_combined)
                print(f"\nur_combined_stats.json has been created, you will have to rename it with your proper UUID.")
        else: #if jsons are already here
            with open(os.path.join(BASE_DIR, (filename + "_" + str(count_json) + ".json")), "w") as f:
                f.write(json_stats_combined)
                print(f"\nYour additional .json has been created, you will have to rename it with your proper UUID.")
    
    else: #if the script sucefully got the player UUID:
        player_uuid_cleared = player_uuid.split(".") #remove .json from player_uuid
        filename = player_uuid_cleared[0]

        if count_json == 0: #if there are already no jsons in the main dir
            with open(os.path.join(BASE_DIR, (filename + ".json")), "w") as f:
                f.write(json_stats_combined)
                print(f"\n{filename}.json has been created.")

        else: #if jsons are already here
            with open(os.path.join(BASE_DIR, (filename + "_" + str(count_json) + ".json")), "w") as f:
                f.write(json_stats_combined)
                print(f"\nYour additional .json has been created.")

    print("\n### The script execution is completed ! ###\nYou can now find a combined stats .json in the same folder as this script.\nYou can use it to fully check your stats or to play with.\n")

    try:
        print(f"You played {round((stats_combined['stats']['minecraft:custom']['minecraft:play_time'] / 600), 1)} hours.")
        print(f"You sneaked {round((stats_combined['stats']['minecraft:custom']['minecraft:sneak_time'] / stats_combined['stats']['minecraft:custom']['minecraft:play_time']) * 100, 2)}% of your total playtime.")
        print(f"You jumped {stats_combined['stats']['minecraft:custom']['minecraft:jump']} times.")
        print(f"You dealt {stats_combined['stats']['minecraft:custom']['minecraft:damage_dealt']} damage while you took {stats_combined['stats']['minecraft:custom']['minecraft:damage_taken']}.")
        print(f"You killed {stats_combined['stats']['minecraft:custom']['minecraft:mob_kills']} mobs.")
        print(f"You opened {stats_combined['stats']['minecraft:custom']['minecraft:open_chest']} chests.")
        print(f"You walked {round((stats_combined['stats']['minecraft:custom']['minecraft:walk_one_cm'] / 100))} meters while you sprinted {round((stats_combined['stats']['minecraft:custom']['minecraft:sprint_one_cm'] / 100))} meters.")
        print(f"You flew {round((stats_combined['stats']['minecraft:custom']['minecraft:fly_one_cm'] / 100))} meters and swimmed {round((stats_combined['stats']['minecraft:custom']['minecraft:swim_one_cm'] / 100))} meters.\n")
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

            if "-" in file: #trying to catch the player UUID
                player_uuid = file

            if stats_combined == {}:
                print(f"{file} was defined as the reference dict.")
                stats_combined = json_buffer
                continue

            for category in json_buffer["stats"]:
                print(f"category type = {type(category)} | category = {category}")

                for stat in json_buffer["stats"][category]:
                    print(f"stat type = {type(stat)} | stat = {stat}")

                    if stats_combined["stats"][category].get(stat) != None: #si il y a match entre les deux dicts
 
                        stats_combined["stats"][category][stat] += json_buffer["stats"][category][stat]
                        print(f"The stat : {stat} is getting combined...")
    
                    else:
                        stats_combined["stats"][category][stat] = json_buffer["stats"][category][stat]

            print(f"{file} was effectively combined.")

print("##### Welcome to my Minecraft stats combiner. #####\nYou can use CTRL+C at any time to stop the script.\n")
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
