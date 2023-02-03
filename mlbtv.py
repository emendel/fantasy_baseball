import time
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

watch_list = [
    "Logan Webb", "Kevin Gausman", "Shohei Ohtani", "Kyle Tucker", "George Springer", "Josh Bell", "Corey Seager",
    "Sonny Gray", "Pablo Lopez", "Ranger Suarez", "Jordan Romano", "Taylor Rogers", "Andrew Kittrege", "Alex Bregman",
    "Joe Barlow", "Jo Adell", "Andrew McCutchen", "Charlie Blackmon", "sus Sanchez",  "Keibert Ruiz", "Jean Segura", "Carlos Santana", "Miles Mikolas", "Brandon Crawford"
]


def init(link):
    options = Options()
    ua = UserAgent()
    user_agent = ua.random
    options.add_argument(f'user-agent={user_agent}')

    browser = webdriver.Firefox()
    browser.get(link)
    time.sleep(2)
    return browser


def get_mlb_tv_browser_session():
    browser = init(
        'https://www.mlb.com/login?campaignCode=mp5&redirectUri=/tv')
    time.sleep(2)
    removed_cookies = ActionChains(browser)
    removed_cookies.send_keys(Keys.TAB, Keys.TAB, Keys.ENTER)
    removed_cookies.perform()
    time.sleep(0.5)
    action = ActionChains(browser)
    action.send_keys("ezra.mendelson", Keys.TAB)
    action.perform()
    time.sleep(1)

    action2 = ActionChains(browser)
    action2.send_keys("baseball", Keys.ENTER)
    action2.perform()
    time.sleep(5)
    return browser


def check_and_watch_games(browser):
    while True:
        browser.switch_to.window(browser.window_handles[1])
        time.sleep(2)
        for name in watch_list:
            first_name = name.split(" ")[1]

            try:
                game = browser.find_element(
                    by=By.PARTIAL_LINK_TEXT, value=first_name)
                game.click()
                browser.switch_to.window(browser.window_handles[0])
                browser.close()

                watching(name, browser)
                # browser.execute_script("window.open('');")
                # browser.switch_to.window(browser.window_handles[1])
                # Switch to the new window and open new URL
                browser.get("https://www.mlb.tv")
                break
            except Exception as e:
                print(e)
                continue
        browser.switch_to.window(browser.window_handles[0])
        time.sleep(30)


def new_guy(browser):
    browser.execute_script("window.open('');")
    browser.switch_to.window(browser.window_handles[1])
    browser.get("https://www.mlb.com/tv")
    check_and_watch_games(browser)


def watching(name, browser):
    while True:
        time.sleep(25)
        try:
            active = browser.find_element(
                by=By.PARTIAL_LINK_TEXT, value=name)
        except Exception as e:
            print(e)
            new_guy(browser)
            return


def check_games(browser):
    time.sleep(5)

    active = 0
    # String strUrl = driver.getCurrentUrl();
    time.sleep(3)
    while True:
        for name in watch_list:
            first_name = name.split(" ")[1]

            try:
                game = browser.find_element(
                    by=By.PARTIAL_LINK_TEXT, value=first_name)
                game.click()
                watching(name, browser)
                # browser.execute_script("window.open('');")
                # browser.switch_to.window(browser.window_handles[1])
                # Switch to the new window and open new URL
                browser.get("https://www.mlb.tv")
                break
            except Exception as e:
                print(e)
                continue
        time.sleep(5)

    return []


b = get_mlb_tv_browser_session()
time.sleep(5)
check_games(b)
