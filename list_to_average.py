#lists cards as the average of lowest 20 on the market. Doesn't check for BCX or anything so either add that or only use with 1bcx cards.

from beem import Steem
from beem.instance import set_shared_steem_instance
from beem.nodelist import NodeList
import time
import requests
import json
import sys

nodes = NodeList()
nodes.update_nodes()
steem = Steem(node=nodes.get_nodes())
set_shared_steem_instance(steem)
steem.wallet.unlock("BEEM PASSWORD HERE")
listing_account = "ACCOUNT NAME HERE"

def send_cards(sender, user, cardlist):
        while len(cardlist) > 50:
                newlist = cardlist[:50]
                steem.custom_json('sm_gift_cards', {'to': user, 'cards': newlist}, required_auths=[sender])

def sell_cards(account, card_id, price):
        steem.custom_json("sm_sell_cards", [{"cards": [card_id], "currency": "USD", "price": price, "fee_pct": 500}], required_auths = [account])

def get_cards(account):
        cnt = 0
        response = ""
        while str(response) != '<Response [200]>' and cnt < 10:
                response = requests.get("https://steemmonsters.com/cards/collection/%s" % account)
                if str(response) != '<Response [200]>':
                        time.sleep(2)
                cnt += 1
        if cnt == 10:
                print "No API response"
                return 0
        details = response.json()
        print "got cards for %s" % account
        return details['cards']     

def get_market():
        cnt = 0
        response = ""
        while str(response) != '<Response [200]>' and cnt < 10:
                response = requests.get("https://steemmonsters.com/market/for_sale")
                if str(response) != '<Response [200]>':
                        time.sleep(2)
                cnt += 1
        if cnt == 10:
                print "No API response"
                return 0
        market = response.json()
        return market

def get_average_price(card_id, gold, num_cards, market):
        prices = []
        if not gold:
                for card in market:
                        if card["card_detail_id"] == card_id and not card["gold"]:
                                prices.append(float(card["buy_price"]))
        else:
                for card in market:
                        if card["card_detail_id"] == card_id and card["gold"]:
                                prices.append(float(card["buy_price"]))
        prices.sort()
        prices = prices[:num_cards]
        total = 0
        for price in prices:
                total += float(price)
        average = float("%.3f" % (total/num_cards))
        return average

def list_cards(account, gold):
        market = get_market()
        cardlist = get_cards(account)
        for card in cardlist:
                if card["market_id"] != None:
                        continue
                if not gold and card["gold"]:
                        continue
                card_price = get_average_price(card["card_detail_id"], card["gold"], 20, market)
                sell_cards(account, card["uid"], card_price)
                time.sleep(1)


list_cards(listing_account, True)


