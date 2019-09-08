from datetime import datetime
from datetime import timedelta

timeFormat = '%Y-%m-%dT%H:%M:%S.%fZ'
wait_time = timedelta(minutes=1382) #23 hours for quest plus 2 for server lag

def get_quest_time(account):
        response = api.get_player_quests(account)
        response = response[0]
        quest_time = datetime.strptime(response["created_date"], timeFormat)
        new_quest_time = quest_time + wait_time
        return new_quest_time

def get_quest_color(account):
        response = api.get_player_quests(account)[0]
        quest_name = response["name"]
        if quest_name == "Rising Dead":
                return "Death"
        if quest_name == "Lyanna's Call":
                return "Earth"
        if quest_name == "Pirate Attacks":
                return "Water"
        if quest_name == "Stir the Volcano":
                return "Fire"
        if quest_name == "Defend the Borders":
                return "Life"
        print "Error: quest not found"
        return 0

def is_quest_finished(account):
        response = api.get_player_quests(account)
        response = response[0]
        quest_status = response["claim_date"]
        if quest_status == None:
                return False
        else:
                return True
