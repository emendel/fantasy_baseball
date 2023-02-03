import time
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
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


dic = {}
lis = []
products = []
search = []
b = init('https://www.rotochamp.com/default.aspx')
time.sleep(3)
cnt = 0
for x in range(1, 2):
    with open("../b_draft_value.csv".format(x), "r") as inf,  \
            open('../b_atc_value.csv'.format(x), 'w', newline='') as outf:
        csvreader = csv.DictReader(inf)
        # Add column name to beginning.
        fieldnames = ["Name", "FVAL"]
        csvwriter = csv.DictWriter(outf, fieldnames)
        csvwriter.writeheader()
        for row in csvreader:
            card = {
                "Name": row["Name"],
                # "HR": row["HR"],
                # "R": row["R"],
                # "RBI": row["RBI"],
                # "SB": row["SB"],
                # "OPS": row["OPS"],
                # "AB": row["AB"],
                "FVAL": row["FVAL"]
                # "QS": row["QS"],
                # "SV": row["SV"],
                # "SO": row["SO"]
            }
            query = card["Name"]
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
                ab = pos.find_element(
                    by=By.XPATH, value="./following-sibling::td")
                # print(ab.text)
                runs = ab.find_element(
                    by=By.XPATH, value="./following-sibling::td")
                # print(runs.text)
                hr = runs.find_element(
                    by=By.XPATH, value="./following-sibling::td")
                # print(hr.text)
                rbi = hr.find_element(
                    by=By.XPATH, value="./following-sibling::td")
                # print(rbi.text)
                sb = rbi.find_element(
                    by=By.XPATH, value="./following-sibling::td")
                # print(sb.text)
                avg = sb.find_element(
                    by=By.XPATH, value="./following-sibling::td")
                # print(avg.text)
                obp = avg.find_element(
                    by=By.XPATH, value="./following-sibling::td")
                # print(obp.text)
                slg = obp.find_element(
                    by=By.XPATH, value="./following-sibling::td")
                # print(slg.text)
                ops = slg.find_element(
                    by=By.XPATH, value="./following-sibling::td")
                # print(ops.text)
                bb = ops.find_element(
                    by=By.XPATH, value="./following-sibling::td")
                # print(bb.text)
                k = bb.find_element(
                    by=By.XPATH, value="./following-sibling::td")
                # print(k.text)
                fval = k.find_element(
                    by=By.XPATH, value="./following-sibling::td")
                fval = fval.text.replace('$', '')
                fval = fval.replace('(', '-')
                fval = fval.replace(')', '')
                # print(fval)
                # card["HR"] = int(hr.text)
                # card["R"] = int(runs.text)
                # card["RBI"] = int(rbi.text)
                # card["SB"] = int(sb.text)
                # card["OPS"] = float(ops.text)
                # card["AB"] = int(ab.text)
                card["FVAL"] = float(fval)
                # card["QS"] = median
                # card["SV"] = float(composite)
                # card["SO"] = float(past)

            except Exception as e:
                print(e)
                continue

            # print(query + "===" + str(median))
            csvwriter.writerow(card)
