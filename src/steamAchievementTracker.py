import json, steamwebapi, time
from steamwebapi.api import ISteamUser, IPlayerService, ISteamUserStats

# Starting time for this run to compare process time and performance.
t0 = time.time()

class SteamAchievementDataMiner():
    def __init__(self, username):
        self.key, self.domain = self.get_key_and_domain()
        self.steamuserinfo = ISteamUser(steam_api_key=self.key)
        self.steamstatsinfo = ISteamUserStats(steam_api_key=self.key)
        self.steamplayerinfo = IPlayerService(steam_api_key=self.key)
        self.steamid = self.getSteamID(username)


    def getSteamID(self, username):
        return self.steamuserinfo.resolve_vanity_url(username)['response']['steamid']

    def getGameList(self):
        return self.steamplayerinfo.get_owned_games(self.steamid)['response']['games']

    def getAchievements(self, game_list):
        achievement_list = []
        for game in game_list:
            appid, title = game['appid'], game['name']
            # print("appid: %s | Title: %s" % (appid, title))
            try:
                achievements = self.steamstatsinfo.get_player_achievements(self.steamid, appid)
                achievement_list.append(achievements)
            except:
                pass #This is incase there are no achievements for a given game, or if there is an error due to rate limiting

        return achievement_list


    @staticmethod
    def get_key_and_domain():
        with open('api-config.json','r') as configurationFile:
            config = json.loads(configurationFile.read())
        return config['key'],config['domain']

    @staticmethod
    def dumpToFile(fileName, dataToWrite):
        with open(fileName,'w') as outputFile:
            outputFile.write(json.dumps(dataToWrite))


if __name__=='__main__':
    # Starting time for this run to compare process time and performance.
    t0 = time.time()

    #Loading achievements from file
    with open('output.json','r') as outputJson:
        achievement_list = json.loads(outputJson.read())


    #dumpToFile('output.json',achievement_list)
    for achievement in achievement_list:

    print("Execution time: %f" %(time.time() - t0))print(achievement['playerstats']['gameName'])
completed = 0
total = 0
percentage = 0.0
try:
    for item in achievement['playerstats']['achievements']:
        # print(item)
        if item['achieved'] == 1:
            completed += 1
            total += 1
        else:
            total += 1
except:
    pass
if total != 0:
    percentage = float(completed / total) * 100.0

print("%f Complete | %i of %i achievements completed" % (percentage, completed, total))
