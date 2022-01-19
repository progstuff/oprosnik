#-------------------------------------------------------------------------------
# Name:        module2
# Purpose:
#
# Author:      Андрей
#
# Created:     23.03.2018
# Copyright:   (c) Андрей 2018
# Licence:     <your licence>
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Андрей
#
# Created:     11.03.2018
# Copyright:   (c) Андрей 2018
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import math
import requests
import time
import datetime
import smtplib
import json
import ssl
import re
import vk_api
import dota2api


def getMatches():
    payload = {
        "Host": "betting-public-graphql.gin.bet",
        "Connection": "keep-alive",
        "Content-Length": "2253",
        "Accept": "*/*",
        "X-Auth-Token": "NrfKJzTQJ1F6iOTpuMbt62IeHRXkgNFefr4BoufPSTnP42q9dImNE6V_uZ3ouGDi_KgPB8pYSgJI3OjjWtyPIWSY3lkaIpot5r_C1CAOUo9utiGZ2XPXW3JNrJS2_Fjtck-HqUO8Er_6",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.162 Safari/537.36",
        "Origin": "https://gg11.bet",
        "Content-Type": "application/json",
        "Referer": "https://gg11.bet/ru/betting/",
        "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
        "Accept-Encoding": "gzip, deflate, br"
    }

    data = [
            {
                "query":"query GetMatchesByFilters($offset: Int!, $limit: Int!, $searchString: String, $dateFrom: String, $dateTo: String, $providerIds: [Int!], $matchStatuses: [SportEventStatus!], $sportIds: [String!], $tournamentIds: [String!], $competitorIds: [String!], $marketStatuses: [MarketStatus!], $marketLimit: Int = 1, $dateSortAscending: Boolean, $sportEventTypes: [SportEventType!], $withMarketsCount: Boolean = true) {\n  matches: sportEventsByFilters(offset: $offset, limit: $limit, searchString: $searchString, dateFrom: $dateFrom, dateTo: $dateTo, providerIds: $providerIds, matchStatuses: $matchStatuses, sportIds: $sportIds, tournamentIds: $tournamentIds, competitorIds: $competitorIds, marketStatuses: $marketStatuses, sportEventTypes: $sportEventTypes, dateSortAscending: $dateSortAscending, marketLimit: $marketLimit) {\n    ...Match\n    marketsCount @include(if: $withMarketsCount)\n  }\n}\n\nfragment Match on SportEvent {\n  id\n  disabled\n  providerId\n  hasMatchLog\n  fixture {\n    ...MatchFixture\n  }\n  markets {\n    id\n    name\n    status\n    typeId\n    priority\n    specifiers {\n      name\n      value\n    }\n    odds {\n      id\n      name\n      value\n      isActive\n      status\n      competitorId\n    }\n  }\n}\n\nfragment MatchFixture on SportEventFixture {\n  score\n  title\n  status\n  type\n  startTime\n  sportId\n  liveCoverage\n  streams {\n    id\n    locale\n    url\n  }\n  tournament {\n    id\n    name\n    masterId\n    logo\n  }\n  competitors {\n    id: masterId\n    name\n    type\n    homeAway\n    logo\n    templatePosition\n  }\n}\n",
                "variables":{
                    "offset":0,
                    "limit":33,
                    "sportIds":[
                        "esports_call_of_duty",
                        "esports_counter_strike",
                        "esports_dota_2",
                        "esports_starcraft",
                        "esports_starcraft_1",
                        "esports_world_of_tanks",
                        "esports_hearthstone",
                        "esports_heroes_of_the_storm",
                        "esports_league_of_legends",
                        "esports_overwatch",
                        "esports_battlegrounds",
                        "esports_vainglory",
                        "esports_warcraft_3",
                        "esports_rainbow_six",
                        "esports_rocket_league",
                        "esports_smite",
                        "esports_soccer_mythical",
                        "esports_halo",
                        "esports_crossfire",
                        "esports_fifa",
                        "esports_street_fighter_5",
                        "esports_king_of_glory"
                    ],
                    "matchStatuses":[
                        "NOT_STARTED",
                        "SUSPENDED",
                        "LIVE"
                    ],
                    "marketStatuses":[
                        "ACTIVE",
                        "SUSPENDED"
                    ],
                    "sportEventTypes":[
                        "MATCH"
                    ]
                }
            }
        ]

    r = requests.post('http://betting-public-graphql.gin.bet/graphql', json = data, headers = payload)
    if(len(r.json()) > 0 and r.json() != None):
        matches = r.json()[0]["data"]["matches"];
        liveMatches = []
        for i in range(0,len(matches)):
            if(matches[i]["fixture"]["status"] == 'LIVE' and matches[i]["fixture"]["sportId"] == 'esports_dota_2'):
                liveMatches.append(matches[i])
        return liveMatches
    else:
        return []

def matchData(id):
    payload = {
            "Host": "betting-public-graphql.gin.bet",
            "Connection": "keep-alive",
            "Content-Length": "1053",
            "Accept": "*/*",
            "X-Auth-Token": "NrfKJzTQJ1F6iOTpuMbt62IeHRXkgNFefr4BoufPSTnP42q9dImNE6V_uZ3ouGDi_KgPB8pYSgJI3OjjWtyPIWSY3lkaIpot5r_C1CAOUo9utiGZ2XPXW3JNrJS2_Fjtck-HqUO8Er_6",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.162 Safari/537.36",
            "Origin": "https://gg11.bet",
            "Content-Type": "application/json",
            "Referer": "https://gg11.bet/ru/betting/match/"+id,
            "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
            "Accept-Encoding": "gzip, deflate, br"
        }
    data = [{"query":"query GetMatch($matchId: String!, $marketLimit: Int, $marketStatuses: [MarketStatus] = [ACTIVE, SUSPENDED, RESULTED]) {\n  match: sportEvent(eventId: $matchId, marketLimit: $marketLimit, marketStatuses: $marketStatuses) {\n    ...Match\n  }\n}\n\nfragment Match on SportEvent {\n  id\n  disabled\n  providerId\n  hasMatchLog\n  fixture {\n    ...MatchFixture\n  }\n  markets {\n    id\n    name\n    status\n    typeId\n    priority\n    specifiers {\n      name\n      value\n    }\n    odds {\n      id\n      name\n      value\n      isActive\n      status\n      competitorId\n    }\n  }\n}\n\nfragment MatchFixture on SportEventFixture {\n  score\n  title\n  status\n  type\n  startTime\n  sportId\n  liveCoverage\n  streams {\n    id\n    locale\n    url\n  }\n  tournament {\n    id\n    name\n    masterId\n    logo\n  }\n  competitors {\n    id: masterId\n    name\n    type\n    homeAway\n    logo\n    templatePosition\n  }\n}\n","variables":{"matchId":id,"marketStatuses":["ACTIVE","DEACTIVATED","SUSPENDED","RESULTED"]}}]
    r = requests.post('http://betting-public-graphql.gin.bet/graphql', json = data, headers = payload)
    match = r.json()[0]["data"]["match"];

    return match;

def writeMessage(user_id,s):
    vk.method('messages.send',{'user_id':user_id, 'message':s})

def getHeroIconUrl(hero_id, heroesInfo):
    for i in range(0,len(heroesInfo["heroes"])):
        if(hero_id == heroesInfo["heroes"][i]["id"]):
            return heroesInfo["heroes"][i]

def getHeroLocalisedName(hero_id, heroesInfo):
    for i in range(0,len(heroesInfo["heroes"])):
        if(hero_id == heroesInfo["heroes"][i]["id"]):
            return heroesInfo["heroes"][i]["localized_name"]

def createTable(match,heroesInfo):
    table = []
    if("scoreboard" in match):
        if("dire" in match["scoreboard"] and "radiant" in match["scoreboard"]):
            if("players" in match["scoreboard"]["radiant"] and "players" in match["scoreboard"]["dire"]):
                if(len(match["scoreboard"]["radiant"]["players"]) == 5 and len(match["scoreboard"]["dire"]["players"]) == 5):
                    for i in range(0,5):
                        hero = match["scoreboard"]["radiant"]["players"][i]["hero_id"]
                        if(hero != 0):
                            net_worth = match["scoreboard"]["radiant"]["players"][i]["net_worth"]
                            kills = match["scoreboard"]["radiant"]["players"][i]["kills"]
                            death = match["scoreboard"]["radiant"]["players"][i]["death"]
                            assists = match["scoreboard"]["radiant"]["players"][i]["assists"]
                            heroInfo = getHeroIconUrl(hero, heroesInfo)
                            table.append([hero,heroInfo,net_worth,kills,death,assists,"radiant"])
                        else:
                            return []
                    for i in range(0,5):
                        hero = match["scoreboard"]["dire"]["players"][i]["hero_id"]
                        if(hero != 0):
                            net_worth = match["scoreboard"]["dire"]["players"][i]["net_worth"]
                            kills = match["scoreboard"]["dire"]["players"][i]["kills"]
                            death = match["scoreboard"]["dire"]["players"][i]["death"]
                            assists = match["scoreboard"]["dire"]["players"][i]["assists"]
                            heroInfo = getHeroIconUrl(hero, heroesInfo)
                            table.append([hero,heroInfo,net_worth,kills,death,assists,"dire"])
                        else:
                            return []
    return table

def getLastPick(match,heroesInfo):
    heroId = match["scoreboard"]["radiant"]["picks"][4]["hero_id"]
    heroName = getHeroLocalisedName(heroId, heroesInfo)
    teamName = match["radiant_team"]["team_name"]
    return [teamName,heroName]

def getPicks(match,heroesInfo):
    heroes = []
    for i in range(0,5):
        heroId = match["scoreboard"]["radiant"]["picks"][i]["hero_id"]
        heroName = getHeroLocalisedName(heroId, heroesInfo)
        heroes.append(heroName)
    teamName = match["radiant_team"]["team_name"]
    radiant = [teamName,heroes]

    heroes = []
    for i in range(0,5):
        heroId = match["scoreboard"]["dire"]["picks"][i]["hero_id"]
        heroName = getHeroLocalisedName(heroId, heroesInfo)
        heroes.append(heroName)
    teamName = match["dire_team"]["team_name"]
    dire = [teamName,heroes]


    return [radiant,dire]

def lineWithSpaces(word1,word2,maxWordSize):
    lineSize = maxWordSize*2 + 1
    line = ''
    l = len(word1) + len(word2)
    p = lineSize - l
    prob = ''
    for i in range(0,p):
        prob = prob + '-'
    line = word1 + prob + word2
    return line

def createTextTable(matchData):
    maxLen = 0
    if(maxLen < len(matchData[0][0])):
          maxLen = len(matchData[0][0])
    if(maxLen < len(matchData[1][0])):
        maxLen = len(matchData[1][0])
    for i in range(0,len(matchData)):
        for j in range(0,5):
            if(maxLen < len(matchData[i][1][j])):
                maxLen = len(matchData[i][1][j])
    line = lineWithSpaces(matchData[0][0],matchData[1][0],maxLen)
    mes = line + '\n'
    for i in range(0,5):
        line = lineWithSpaces(matchData[0][1][i],matchData[1][1][i],maxLen)
        mes = mes + line + '\n'
    return mes

def getMatchLineInfo(id):
   matchDetails = matchData(id)
   score = matchDetails["fixture"]["score"]
   i = score.find(":")
   mapNumber = float(score[0:i]) + float(score[i+1:len(score)]) + 1
   betName = ''
   mapName = ''
   if(mapNumber == 1):
    betName = '1st map - winner'
    mapName = 'карта №1'
   elif(mapNumber == 2):
    betName = '2nd map - winner'
    mapName = 'карта №2'
   elif(mapNumber == 3):
    betName = '3rd map - winner'
    mapName = 'карта №3'
   elif(mapNumber == 4):
    betName = '4th map - winner'
    mapName = 'карта №4'
   elif(mapNumber == 5):
    betName = '5th map - winner'
    mapName = 'карта №5'
   markets = matchDetails["markets"]
   line = ''
   for i in range(0,len(markets)):
    if(markets[i]["name"] == betName):
        line = mapName + ' '
        line = line + markets[i]["odds"][0]["name"] + ' ('+str(markets[i]["odds"][0]["value"]) + ')'
        line = line + ' vs '
        line = line + markets[i]["odds"][1]["name"] + ' ('+str(markets[i]["odds"][1]["value"]) + ')\n'
        line = line + ' текущий счёт по картам ' + score + '\n'
        break
   return line

def getGoldGraph(dotaAPI,wantedMatchId):
    games = dotaAPI.get_top_live_games();
    games = games["game_list"];
    for i in range(0,len(games)):
        ssi = games[i]["server_steam_id"]
        r = requests.get('https://api.steampowered.com/IDOTA2MatchStats_570/GetRealtimeStats/v1?key=DBEFFFE8A6BD380AB2BA816A057C3E20&server_steam_id='+ssi)
        game = r.json()
        if(game["match"]["matchid"] == wantedMatchId):
            gameTime = game["match"]["game_time"]
            gold = game["graph_data"]["graph_gold"]
            return [gameTime,gold]
    return [-1,0]

def getGoldLine(gold_data,matchData):
   gameTime = gold_data[0]
   if(gameTime != -1):
    gold = gold_data[1][127]
    line = 'игровое время: ' +  str(math.floor(gameTime/60)) + ':' + str(gameTime - math.floor(gameTime/60)*60) + '\n'
    if(gold > 0):
        line = line + 'команда ' + matchData[0][0] + ' имеет преимущество по золоту в размере ' + str(gold)
    elif(gold < 0):
        line = line +'команда ' + matchData[1][0] + ' имеет преимущество по золоту в размере ' + str(-gold)
    else:
        line = line +'ни одна команда не имеет преимущества по золоту'
    return line
   else:
    return ''



vk = vk_api.VkApi(token = 'b1466ecde89532fd12d536660f591ce028ab4d260f63c104b2f7d16015b7093af9ad328834f039fc13e3f')
api = dota2api.Initialise("DBEFFFE8A6BD380AB2BA816A057C3E20")
heroesInfo = api.get_heroes()
prevgames = []
cnt = 0

mes = 'сервер включен (автоматическаяя рассылка)'
writeMessage(175424382,mes)
#writeMessage(254212222,mes)


#for l in range(0,1):
while(1):
    try:
        dotaMatches = api.get_live_league_games()
        ggmatches = getMatches();
        if(ggmatches != []):
            teams = []
            for i in range(0,len(ggmatches)):
                teams.append([ggmatches[i]["fixture"]["competitors"][0]["name"],ggmatches[i]["fixture"]["competitors"][1]["name"],ggmatches[i]["id"]])

            curgames = []
            gamestates = []
            lastPicks = []
            picks = []
            gold_data = []
            for i in range(0,len(dotaMatches["games"])):
                match = dotaMatches["games"][i]
                if("scoreboard" in match):
                    if("dire_team" in match and "radiant_team" in match):
                        if("team_name" in match["dire_team"] and "team_name" in match["radiant_team"]):
                            if(match["scoreboard"]["duration"] >= 540 and match["scoreboard"]["duration"] <= 700):
                                ti1 = match["dire_team"]["team_name"]
                                ti2 = match["radiant_team"]["team_name"]
                                for j in range(0,len(teams)):
                                    tj1 = teams[j][0]
                                    tj2 = teams[j][1]
                                    if(ti1.find(tj1) >= 0 or ti1.find(tj2) >= 0 or ti2.find(tj1) >= 0 or ti2.find(tj2) >= 0 or tj1.find(ti1) >= 0 or tj1.find(ti2) >= 0 or tj2.find(ti1) >= 0 or tj2.find(ti2) >= 0):
                                      table = createTable(match,heroesInfo)
                                      if(table != []):
                                        curgames.append(teams[j])
                                        gamestates.append(table)
                                        lastPicks.append(getLastPick(match,heroesInfo))
                                        picks.append(getPicks(match,heroesInfo))

                                        wantedMatchId = str(match["match_id"]);
                                        gameTime,gold = getGoldGraph(api,wantedMatchId)
                                        gold_data.append([gameTime,gold])
            mes = ''
            for i in range(0,len(curgames)):
                finded = False
                for j in range(0,len(prevgames)):
                    if(prevgames[j] == curgames[i]):
                        finded = True
                if(finded == False):
                    line = getMatchLineInfo(curgames[i][2])
                    if(line == ''):
                        mes = mes + "прошло более 10 минут матча \n" + curgames[i][0] +" vs "+ curgames[i][1] + "\n команда " + lastPicks[i][0] + " выбирала последней " + lastPicks[i][1] + "\n"
                    else:
                        mes = mes + "прошло более 10 минут\n" + line + "\n команда " + lastPicks[i][0] + " выбирала последней " + lastPicks[i][1] + "\n"
                    mes = mes + "\n составы команд \n"+createTextTable(picks[i])

                    dopMes = getGoldLine(gold_data[i],picks[i])
                    if(dopMes != ''):
                        mes = mes + dopMes + '\n'

                    mes = mes + " \nссылка на ggbet\n https://gg11.bet/ru/betting/match/" + curgames[i][2] + '\n\n'


            prevgames = curgames

            if(mes != ''):
                writeMessage(175424382,mes)
                #writeMessage(254212222,mes)
        cnt = cnt + 1
        print(str(cnt))
        time.sleep(20)
    except:
        print("error\n")















