#!/usr/bin/env python
# -*- coding: utf-8 -*-
import mechanicalsoup
import time
import json
import pygsheets
from enum import Enum
from datetime import datetime

URL='https://secure.runescape.com/m=hiscore_oldschool_ultimate/overall?table='
HISCORES_ID = 'contentHiscores'
NEXT_PAGE_BUTTON_CLASS = 'personal-hiscores__pagination-arrow--down'
PREV_PAGE_BUTTON_CLASS = 'personal-hiscores__pagination-arrow--up'
HTML_TAG_CONTAINING_USERNAME = 'a'
KNOWN_TD_TAGS_TO_IGNORE = 4
KNOWN_MAX_ITEMS_PER_PAGE = 25
MAX_LEVEL = 99
OVERALL_MAX_LEVEL = 2277 
LEVEL_CONTAINER_TAG = 'td'
PAGE_FILTER_QUERY = '&page='

class Skill(Enum):
    OVERALL = '0'
    ATTACK = '1'
    DEFENCE = '2'
    STRENGTH = '3'
    HITPOINTS = '4'
    RANGED = '5'
    PRAYER = '6'
    MAGIC = '7'
    COOKING = '8'
    WOODCUTTING = '9'
    FLETCHING = '10'
    FISHING = '11'
    FIREMAKING = '12'
    CRAFTING = '13'
    SMITHING = '14'
    MINING = '15'
    HERBLORE = '16'
    AGILITY = '17'
    THIEVING = '18'
    SLAYER = '19'
    FARMING = '20'
    RUNECRAFT = '21'
    HUNTER = '22'
    CONSTRUCTION = '23'
    
def ceilDivision(dividend,divisor): return -(dividend//-divisor)
        
def levelToCheck(skillname): return OVERALL_MAX_LEVEL if skillname == "OVERALL" else MAX_LEVEL
    
def countFromStart(browser):
    maxedUIMCount = {}
    for skill in Skill:
        print(skill.name)
        browser.open(URL+skill.value)
        foundAll99s = False
        total99s = 0
        while not foundAll99s:
            listOfSkillLevelsOnPage = list(int(userLevel.get_text().replace(',', '')) for userLevel in browser.page.find(id=HISCORES_ID).find_all(name=LEVEL_CONTAINER_TAG,class_=None)[KNOWN_TD_TAGS_TO_IGNORE:])
            ninetyNinesOnPage = sum(1 for userLevel in listOfSkillLevelsOnPage if userLevel == levelToCheck(skill.name))
            total99s += ninetyNinesOnPage
            print(total99s)
            browser.follow_link(class_=NEXT_PAGE_BUTTON_CLASS)
            time.sleep(2)
            if ninetyNinesOnPage < KNOWN_MAX_ITEMS_PER_PAGE:
                maxedUIMCount[skill.name] = total99s
                foundAll99s = True
    return maxedUIMCount

def countFromLast(browser,lastCount):
    maxedUIMCount = {}
    for skill in Skill:
        print(skill.name)
        startPage = ceilDivision(lastCount[skill.name],KNOWN_MAX_ITEMS_PER_PAGE)
        browser.open(URL+skill.value+PAGE_FILTER_QUERY+str(startPage))
        
        
        #Check the total has not somehow decreased (e.g. via bot busting) by confirming first item on page is a 99
        ninetyNinesConfirmed = False
        while not ninetyNinesConfirmed:
            firstLevelOnPage = int(browser.page.find(id=HISCORES_ID).find_all(name=LEVEL_CONTAINER_TAG,class_=None)[KNOWN_TD_TAGS_TO_IGNORE:][0].contents[0].replace(',', ''))
            if firstLevelOnPage == levelToCheck(skill.name):
                ninetyNinesConfirmed = True
            else:
                browser.follow_link(class_=PREV_PAGE_BUTTON_CLASS)
                time.sleep(2)
                startPage -= 1
        
        foundAll99s = False
        total99s = (startPage-1)*KNOWN_MAX_ITEMS_PER_PAGE
        while not foundAll99s:
            listOfSkillLevelsOnPage = list(int(userLevel.get_text().replace(',', '')) for userLevel in browser.page.find(id=HISCORES_ID).find_all(name=LEVEL_CONTAINER_TAG,class_=None)[KNOWN_TD_TAGS_TO_IGNORE:])
            ninetyNinesOnPage = sum(1 for userLevel in listOfSkillLevelsOnPage if userLevel == levelToCheck(skill.name))
            total99s += ninetyNinesOnPage
            print(total99s)
            browser.follow_link(class_=NEXT_PAGE_BUTTON_CLASS)
            time.sleep(2)
            if ninetyNinesOnPage < KNOWN_MAX_ITEMS_PER_PAGE:
                maxedUIMCount[skill.name] = total99s
                foundAll99s = True
    return maxedUIMCount



if __name__ == '__main__':
    browser = mechanicalsoup.StatefulBrowser()
    try:
        with open('lastCount.json','r') as jsonFile:
            lastCount = json.loads(jsonFile.read())
    except FileNotFoundError:
        lastCount = False
    
    if lastCount:
        maxedUIMCount = countFromLast(browser,lastCount)
    else:
        maxedUIMCount = countFromStart(browser)
    
    with open('lastCount.json','w') as f:
        f.write(json.dumps(maxedUIMCount))
        
    with open('tablePositions.json','r') as f:
        tablePositions = json.loads(f.read())
        
    pygsheetsClient = pygsheets.authorize(service_file="service_file.json")
    sheet = pygsheetsClient.open('UIM 99s')
    worksheet = sheet.sheet1
    for key in tablePositions:
        if key == 'DATEFIELD':
            worksheet.update_value(tablePositions[key],datetime.now().isoformat())
            print(datetime.now().isoformat())
        else:
            worksheet.update_value(tablePositions[key],str(maxedUIMCount[key]))
            
    
    
