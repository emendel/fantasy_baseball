import time
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium import webdriver
import csv


def init(link):
    options = Options()
    ua = UserAgent()
    user_agent = ua.random
    options.add_argument(f'user-agent={user_agent}')

    browser = webdriver.Firefox()
    browser.get(link)
    time.sleep(2)
    return browser


b = init('https://www.rotochamp.com/default.aspx')
time.sleep(3)
cnt = 0
for x in range(0, 1):
    with open("../p_draft_value.csv".format(x), "r") as inf,  \
            open('../p_atc_value.csv'.format(x), 'w', newline='') as outf:
        csvreader = csv.DictReader(inf)
        # Add column name to beginning.
        fieldnames = ["Name", "FVAL"]
        csvwriter = csv.DictWriter(outf, fieldnames)
        csvwriter.writeheader()
        for row in csvreader:
            card = {
                "Name": row["Name"],
                "FVAL": row["FVAL"]
                # "QS": row["QS"],
                # "SV": row["SV"],
                # "SO": row["SO"]
            }
            query = card["Name"]
            print(query)
            searchbar = b.find_element(by=By.ID, value="inputPlayerSearch")
            searchbar.click()
            action = ActionChains(b)
            action2 = ActionChains(b)
            action.send_keys(query)
            time.sleep(1)
            action.perform()
            time.sleep(1)
            action2.send_keys(Keys.DOWN, Keys.ENTER)
            time.sleep(1)
            action2.perform()
            time.sleep(2)
            dollars = []
            cnt = 0
            composite = ''
            past = ''
            try:
                values = []
                atc = b.find_element(
                    by=By.XPATH, value="//*[@data-stattype='ATC']")
                team = atc.find_element(
                    by=By.XPATH, value="../following-sibling::td")
                team_name = team.find_element(by=By.TAG_NAME, value="a").text
                # print(team_name)
                pos = team.find_element(
                    by=By.XPATH, value="./following-sibling::td")
                pos_name = pos.find_element(by=By.TAG_NAME, value="a").text
                # print(pos_name)
                ip = pos.find_element(
                    by=By.XPATH, value="./following-sibling::td")
                # print(ab.text)
                ws = ip.find_element(
                    by=By.XPATH, value="./following-sibling::td")
                # print(runs.text)
                ls = ws.find_element(
                    by=By.XPATH, value="./following-sibling::td")
                # print(hr.text)
                era = ls.find_element(
                    by=By.XPATH, value="./following-sibling::td")
                # print(rbi.text)
                whip = era.find_element(
                    by=By.XPATH, value="./following-sibling::td")
                # print(sb.text)
                k = whip.find_element(
                    by=By.XPATH, value="./following-sibling::td")
                # print(avg.text)
                bb = k.find_element(
                    by=By.XPATH, value="./following-sibling::td")
                # print(obp.text)
                sv = bb.find_element(
                    by=By.XPATH, value="./following-sibling::td")
                # print(slg.text)
                fval = sv.find_element(
                    by=By.XPATH, value="./following-sibling::td")
                fval = fval.text.replace('$', '')
                fval = fval.replace('(', '-')
                fval = fval.replace(')', '')
                # print(fval)
                # card["QS"] = int(int(ls.text)/2) + int(ws.text)
                # card["SV"] = int(sv.text)
                # card["K"] = int(k.text)
                # card["ERA"] = float(era.text)
                # card["WHIP"] = float(whip.text)
                # card["IP"] = int(ip.text)
                card["FVAL"] = float(fval)

            except Exception as e:
                print(e)
                continue

            # print(query + "===" + str(median))
            csvwriter.writerow(card)
