import json, steamwebapi, time
import logging
from steamwebapi.api import ISteamUser, IPlayerService, ISteamUserStats

class SteamAchievementDataMiner():
    # Constructor
    def __init__(self, username, stats_file_name=None):
        self.key, self.domain = self.get_key_and_domain()
        self.steamuserinfo = ISteamUser(steam_api_key=self.key)
        self.steamstatsinfo = ISteamUserStats(steam_api_key=self.key)
        self.steamplayerinfo = IPlayerService(steam_api_key=self.key)
        self.steamid = self.getSteamID(username)
        self.stats_file_name = stats_file_name
        self.gameList = None
        self.achievementList = None
        logging.basicConfig(filename='example.log', level=logging.DEBUG)

    # GetSteamID
    def getSteamID(self, username):
        steamprofile = self.steamuserinfo.resolve_vanity_url(username)
        logging.debug("!!! DEBUG: - STEAM PROFILE DATA - for username %s" %username)
        logging.debug(steamprofile)
        return steamprofile['response']['steamid']

    # getGameList
    def getGameList(self):
        self.gameList =  self.steamplayerinfo.get_owned_games(self.steamid)['response']['games']
        logging.debug("!!! DEBUG: - STEAM GAME LIST FROM PROFILE")
        logging.debug(self.gameList)
        return self.gameList

    # getAchievements from gamelist
    def getAchievements(self, game_list):
        achievement_list = []
        csvRow = ""
        for game in game_list:
            appid, title = game['appid'], game['name']
            csvRow += ("appid: %s , Title: %s , " % (appid, title))

            try:
                achievements = self.steamstatsinfo.get_player_achievements(self.steamid, appid)
                achievement_list.append(achievements)
                csvRow += ("achievements available: %i \n" %len(achievement_list))# !!!!! LAST FIELD IN CSV HAS NO TRAILING COMMA
            except:
                csvRow += ("achievements available: NA \n") # !!!!! LAST FIELD IN CSV HAS NO TRAILING COMMA
                pass
                # This is incase there are no achievements for a given
                # game, or if there is an error due to rate limiting
            self.writeStatsRow(csvRow)

        self.achievementList = achievement_list
        return achievement_list


    def writeStatsRow(self, data_to_try_to_write):
        if self.stats_file_name != None:
            with open(self.stats_file_name,'a') as file_appender:
                file_appender.write(data_to_try_to_write)
        else:
            print(data_to_try_to_write)

    @staticmethod
    def get_key_and_domain():
        with open('api-config.json','r') as configurationFile:
            config = json.loads(configurationFile.read())
        return config['key'],config['domain']

    @staticmethod
    def dumpToFile(fileName, dataToWrite):
        with open(fileName,'w') as outputFile:
            outputFile.write(json.dumps(dataToWrite +"\n"))



def myMainCodeVersionOne():
    # Starting time for this run to compare process time and performance.

    steamAPI = SteamAchievementDataMiner('adamclmns', stats_file_name='statsFile.csv')
    achievement_list = steamAPI.getAchievements(steamAPI.getGameList())
    #steamAPI.dumpToFile('output.json',achievement_list)

    for achievement in achievement_list:
        print(achievement['playerstats']['gameName'])

def mySampleTestCode():
    # Just prints out one game so you can see the structure of the game stats.
    with open('api-config.json', 'r') as configurationFile:
        config = json.loads(configurationFile.read())
    key, domain =  config['key'], config['domain']
    steamuserinfo = ISteamUser(steam_api_key=key)
    steamstatsinfo = ISteamUserStats(steam_api_key=key)
    steamplayerinfo = IPlayerService(steam_api_key=key)

    steamprofile = steamuserinfo.resolve_vanity_url('adamclmns')
    steamid = steamprofile['response']['steamid']

    print(" STEAM PROFILE DATA SAMPLE:")
    print(steamid)
    print("\n\n")



    print(" GAME DATA FOR FALLOUT 4 ")
    print()
    print("\n\n")

if __name__=='__main__':
    myMainCodeVersionOne()



