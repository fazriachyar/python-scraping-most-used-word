from selenium import webdriver
from bs4 import BeautifulSoup
import operator
from collections import Counter
import pandas as pd

driver = webdriver.Chrome("/home/fazriachyar/.wdm/drivers/chromedriver/linux64/100.0.4896.60/chromedriver")

def main(url):
    wordbank = []
    driver.get(url)
    pagesource = driver.page_source
    soup = BeautifulSoup(pagesource)
    for a in soup.findAll ('div', {'class': 'detail__body-text itp_bodycontent'}):
        comment = a.find_all('p')
        # for i in range(len(comment)):
        #     if i % 2 == 0:
        #      print(comment[i].text)
        as_string = str(comment)
        words = as_string.lower().split()
        for each_word in words:
            wordbank.append(each_word)
        clean_wordbank(wordbank)
        df = pd.DataFrame({'Extracted Data':wordbank})
        df.to_csv('results.csv', index=False, encoding='utf-8')
        

def clean_wordbank(wordbank):
    clean_list = []
    for word in wordbank:
        symbols = "!@#$%^&*()_-+={[}]|\;:\"<>?/., "
        for i in range(len(symbols)):
            word = word.replace(symbols[i], '')
        if len(word) > 0:
            clean_list.append(word)

def create_dict(clean_list):
    word_count = {}
    for word in clean_list:
        if word in word_count:
            word_count[word] += 1
        else:
            word_count[word] = 1
    c = Counter(word_count)
    top = c.most_common(20)
    print(top)

if __name__ != '__main__':
    pass
else:
    url = "https://news.detik.com/berita/d-6120547/kasus-corona-10-juni-tembus-627-orang"
    main(url)


