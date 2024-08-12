import requests
from bs4 import BeautifulSoup
import csv

def skimmer(address,tag):
    print(f'Fetching relevant entries from {tag}:')
    
    #grabbing webpage
    page = requests.get(address)

    #creating parsable object
    soup = BeautifulSoup(page.text, 'html.parser')

    abstracts = soup.find_all('p', class_ = "mathjax")
    titles = soup.find_all('div',class_="list-title mathjax")

    abstracts_list = []
    titles_list = []

    keyword_list = [['dark',10],['matter',10]]
    #set score threshold at minimum of one instance of each keyword (25 atm)
    
    for abstract in abstracts:
        #print(abstract.contents[0])
        abstracts_list.append(str(abstract.contents[0]))

    for title in titles:
        #print(title.contents[1])
        titles_list.append(str(title.contents[1]))

    for i in range(len(abstracts_list)):
        abs_word_list = abstracts_list[i].split(" ")
        title_word_list = titles_list[i].split(" ")
        del abs_word_list[0:10]
        del abs_word_list[(len(abs_word_list) - 8):len(abs_word_list)]
        del title_word_list[0:10]
        del title_word_list[(len(title_word_list) - 8):len(title_word_list)]
        score = 0
        for keyword in keyword_list:
            for word in abs_word_list:
                if word.lower() == keyword[0].lower():
                    score += 1*keyword[1]
        if True == True: #placeholder for additional filter
            if score >= 20:
                print(f'{titles_list[i]} -> score  = {score}\n')

def url_merge(tag):
    return('https://arxiv.org/list/'+ f'{tag}/new')

def main():
    tags = ['hep-ex','hep-th']
    for tag in tags:
        skimmer((url_merge(tag)),tag)

main()


    
    


 

