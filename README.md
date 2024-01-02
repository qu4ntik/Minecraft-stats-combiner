# Minecraft-stats-combiner
Python script to combine every one of your minecraft stats files into a merged one.

I decided to create it because I realized I couldn't find one.

Can maybe be a bit buggy but the main fonctionality is working fine (locally at least)

#################################### How it's working ####################################

- Install Python if it is not already done (If you try to run the script, it will sugest you to install it from windows store, at least on W11)
- Download the latest release [here](https://github.com/qu4ntik/Minecraft-stats-combiner/releases).
- Launch main.py and follow the instructions.

You can use two differents methods to combine your stats :

(EASY) You can copy and paste your minecraft or curseforge path folder and the script will automatically import and export data from all your stats files.

(ADVANCED) You have to regroup your stats files into "stats_folder", theses files are located in the stats folder of any maps.

######################################## Features ########################################

- Automatically detect your player UUID and rename the combined file with it.
- Automatically detect if you already have generated a .json and will adapt the combined stats file name.
- Supports stats files from modded maps. (care if you load the .json on a unmodded minecraft, didn't tested.)
- Print out some important stats at the end of the script execution.
- Combine all your stats file into one which can be used to play with.
- Support stats files from server maps.
- Server owner can use the script to generate a global stat file of every player who played on his server.

Example :

![Capture d'écran 2024-01-02 121449](https://github.com/qu4ntik/Minecraft-stats-combiner/assets/113895291/020e5021-73a9-44ea-9f12-8640bd75bc0e)

########################### How to combine severals folders ##############################

1. Use the advanced (2) method to generate a .json for every one of your minecraft/curseforge folder.
2. Put theses files in stats_folder.
3. Run the easy (1) method.

##########################################################################################
