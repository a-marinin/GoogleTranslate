"""
PLEASE NOTICE:
This script was written just for training.
Using following code for something more than just practicing of Python breaks Google's terms of service.
"""

import bs4 as bs
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# Translate list of words from ENG to RUS through Google Translate using Senenium.
def translate(word):
    print("Working on following word: " + str(word))
    link = 'https://translate.google.com.ar/#en/ru/{}'.format(word)

    # Run Chrome in headless mode
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')  # Last I checked this was necessary.
    driver = webdriver.Chrome('C:\\Python\\Webdrivers\\chromedriver.exe', chrome_options=options)
    driver.get(link)

    # Get the page source and parse it with BeautifullSoup
    html = driver.page_source
    soup = bs.BeautifulSoup(html, 'lxml')

    # Empty lists for Common, Uncommon and Rare translations respectively
    listCommon = []
    listUncommon = []
    listRare = []

    # Common translation / Traducción común
    for i in soup.select('div[title*="Traducción común"]'):
        # print(i.get_text)
        commonTranslations = i.findNext().findNext()
        # print(commonTranslations.text)
        listCommon.append(commonTranslations.text)

    # Uncommon translation / Traducción poco común
    for i in soup.select('div[title*="Traducción poco común"]'):
        uncommonTranslations = i.findNext().findNext()
        listUncommon.append(uncommonTranslations.text)

    # Rare translation / Traducción rara
    for i in soup.select('div[title*="Traducción rara"]'):
        rareTranslations = i.findNext().findNext()
        listRare.append(rareTranslations.text)

    # Put the translations into appropriate list and clean it up
    commonStr = str(listCommon).replace('[','').replace(']','').replace("'","")
    uncommonStr = str(listUncommon).replace('[','').replace(']','').replace("'","")
    rareStr = str(listRare).replace('[','').replace(']','').replace("'","")

    # Constructing DataFrame from the lists
    df = pd.DataFrame(
        {'word': word,
         'common': commonStr,
         'uncommon': uncommonStr,
         'rare': rareStr
        }, index=[0])

    # Return DataFrame
    return df

# List of words to translate
words_list= ['cat', 'bat', 'rat', 'hat']

df_temp = [translate(i) for i in words_list]
df = pd.concat(df_temp, ignore_index=True)
df.to_excel('translations.xlsx')