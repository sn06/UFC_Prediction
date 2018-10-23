# -*- coding: utf-8 -*-
"""
Created on Sun Oct 14 11:59:13 2018

@author: sn06
"""

import urllib3
from bs4 import BeautifulSoup
import time
import numpy as np
import pandas as pd

http = urllib3.PoolManager()

df = pd.DataFrame(columns=['Events',
                          'Fighter1',
                          'Fighter2',
                          'Winner',
                          'fighter1_odds',
                          'fighter2_odds',
                          'F1 or F2',
                          'Label',
                          'Combine',
                          'Favourite',
                          'Underdog'])

for j in range(332,391):
    url = 'https://www.betmma.tips/free_ufc_betting_tips.php?Event=' + str(j)
    response = http.request('GET',url)
    soup = BeautifulSoup(response.data)
    
    event = soup.find('h1').text
    
    odds = []
    address = soup.find_all('td')
    for i in range(len(address)):
        if address[i].get_text().startswith(' @'):
            odds.append(float(address[i].get_text()[2:]))
            
    fighters_list = []
    address = soup.find_all('a')
    for i in range(len(address)):
        if ' vs ' in address[i].get_text():
            if address[i-1].get_text()!= 'MMA Betting Blog':
                fighters_list.append(address[i-1].get_text())
            if address[i+1].get_text()!= 'In Depth UFC Fight Stats':
                fighters_list.append(address[i+1].get_text())
            if len(fighters_list)!=0:
                print(fighters_list[len(fighters_list)-1])
    
    results = []
    address = soup.find_all('td')
    for i in range(len(address)):
        if address[i].get_text().startswith(' @'):
            if address[i].get('bgcolor') == '#A2FC98':
                results.append(1)
            else:
                results.append(2)
    if len(fighters_list)!=0:
        for i in range(len(fighters_list)):
            if i % 2 == 0:
                if results[i] == 1:
                    winner = fighters_list[i]
                    if odds[i] <= odds[i+1]:
                        lab = 'Favourite'
                        fav = fighters_list[i]
                        und = fighters_list[i+1]
                    else:
                        lab = 'Underdog'
                        fav = fighters_list[i+1]
                        und = fighters_list[i]
                else:
                    winner = fighters_list[i+1]
                    if odds[i+1] <= odds[i]:
                        lab = 'Favourite'
                        fav = fighters_list[i+1]
                        und = fighters_list[i]
                    else:
                        lab = 'Underdog'
                        fav = fighters_list[i]
                        und = fighters_list[i+1]
                combine = lab + ' ' + str(results[i])
                z = pd.DataFrame([[event,
                     fighters_list[i],
                     fighters_list[i+1],
                     winner,
                     odds[i],
                     odds[i+1],
                     results[i],
                     lab,
                     combine,
                     fav,
                     und
                     ]],columns=['Events',
                                  'Fighter1',
                                  'Fighter2',
                                  'Winner',
                                  'fighter1_odds',
                                  'fighter2_odds',
                                  'F1 or F2',
                                  'Label',
                                  'Combine',
                                  'Favourite',
                                  'Underdog'])
                df = df.append(z,ignore_index=True)

    timedelay = np.random.randint(15,30)
    print('%s--%s' % (j,timedelay))
    time.sleep(timedelay)