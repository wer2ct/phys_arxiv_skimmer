import requests
from bs4 import BeautifulSoup
import csv

def skimmer(address,tag):
    print("-------------------------------------")
    print(f'Fetching relevant entries from {tag}:')
    
    #grabbing webpage
    page = requests.get(address)

    #creating parsable object
    soup = BeautifulSoup(page.text, 'html.parser')

    abstracts = soup.find_all('p', class_ = "mathjax")
    titles = soup.find_all('div',class_="list-title mathjax")

    links = soup.css.select('a[id^="pdf-"]')

    
    abstracts_list = []
    titles_list = []
    links_list = []

    keyword_list = [['Riemann',10],['hypothesis',10]]
    
    for abstract in abstracts:
        #print(abstract.contents[0])
        abstracts_list.append(str(abstract.contents[0]))

    for title in titles:
        #print(title.contents[1])
        titles_list.append(str(title.contents[1]))
    for link in links:
        links_list.append(('https://arxiv.org' + str(link).split('"')[3]))

    for i in range(len(abstracts_list)):
        abs_word_list = abstracts_list[i].split(" ")
        title_word_list = titles_list[i].split(" ")
        del abs_word_list[0:10]
        del abs_word_list[(len(abs_word_list) - 8):len(abs_word_list)]
        del title_word_list[0:10]
        del title_word_list[(len(title_word_list) - 8):len(title_word_list)]
        for i in range(len(titles_list)):
            titles_list[i] = titles_list[i].strip()
        score = 0
        for keyword in keyword_list:
            for word in abs_word_list:
                if word.lower() == keyword[0].lower():
                    score += 1*keyword[1]
        if True == True: #placeholder for additional filter
            if score >= 20:
                print(f'\n{titles_list[i]} \nscore  = {score} \nlink = {links_list[i]}\n')

def url_merge(tag):
    return('https://arxiv.org/list/'+ f'{tag}/new')

def main():
    tags = ['math']
    for tag in tags:
        skimmer((url_merge(tag)),tag)

main()


    
    


 

