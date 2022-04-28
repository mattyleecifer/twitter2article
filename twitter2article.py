from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import re, os, time, sys
import unicodedata


address = sys.argv[1]

def addarticles(driver):
    set = []
    articles = driver.find_elements_by_css_selector('div[style*="transform"]')
    for i in range(0, len(articles)):
        try:
            innertext = articles[i].find_element_by_css_selector('div[lang="en"]').text
            innertext = re.sub("\d?\d/", "", innertext)
            innertext = re.sub("\\n\\n", ". ", innertext)
            innertext = re.sub("^\. ", "", innertext)
            innertext = re.sub("\.\.", ".", innertext)
            innertext = re.sub("\\n@", "@", innertext)
            innertext = re.sub("\\n,", ",", innertext)
            innertext = re.sub("\\n ", " ", innertext)
            innertext = re.sub("(\\n. )$", ".", innertext)
            innertext = re.sub(" \. ", "", innertext)
            innertext = re.sub("^(\.\.+)", "", innertext) # Remove elipses front
            innertext = re.sub("(\.\.+)$", ".", innertext) # Remove elipses behind
            # print(innertext)
            set.append(innertext)
        except:
            pass
    return set

def getarticles(driver):

    complete = []
    setbase = 69420

    while True:
        set = addarticles(driver)
        if set[0] == setbase:
            complete.append(set[0])
            break
        else:
            setbase = set[0]
            for i in range(len(set)-1, 0, -1):
                if set[i] in complete:
                    pass
                else:
                    complete.append(set[i])
            time.sleep(1)
            driver.execute_script("window.scrollBy(0,-2000)", "") #scrolls up
    driver.close()
    return complete

def converthtml(data):
    html = ""
    for i in range(len(data) - 1, 0, -1):
        html = html + data[i] + "<p>"
    print(unicodedata.normalize('NFKD', html).encode('ascii', 'ignore'))
    return html

def main():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(address)
    time.sleep(5)
    data = getarticles(driver)
    converthtml(data)

main()

# unicodedata.normalize('NFKD', innertext).encode('ascii', 'ignore')
