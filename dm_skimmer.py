import requests
from bs4 import BeautifulSoup
import csv
from datetime import date

def skimmer(address,tag): #function takes web address and arxiv tag, currently works best for 'new' pages 

    today=date.today()

    #grabbing webpage
    page = requests.get(address)

    #creating parsable object in BeautifulSoup
    soup = BeautifulSoup(page.text, 'html.parser')
    
    #Finding abstracts, titles, and links on a given arxiv page
    abstracts = soup.find_all('p', class_ = "mathjax")
    titles = soup.find_all('div',class_="list-title mathjax")
    links = soup.css.select('a[id^="pdf-"]')

    #creating lists for abstracts, titles, and links
    abstracts_list = []
    titles_list = []
    links_list = []

    #weighted keyword list. First entry in list is keyword (capitalization doesn't matter), second is weight
    keyword_list = [['dark',10],['matter',10]]

    #List that will store the results
    results_list = []

    #Parsing to create a filled results list
    for abstract in abstracts:
        abstracts_list.append(str(abstract.contents[0]))

    for title in titles:
        titles_list.append(str(title.contents[1]))
        
    for i in range(len(titles_list)):
        titles_list[i] = titles_list[i].strip()
    
    for link in links:
        links_list.append(('https://arxiv.org' + str(link).split('"')[3]))

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
        if score >= 20:
            results_list.append([today,tag,titles_list[i],score,links_list[i]])

    return(results_list)

def url_merge(tag): #function takes tag and returns a link to the new page
    return('https://arxiv.org/list/'+ f'{tag}/new')

def main(): #main function
    tags = ['hep-ex','hep-th'] #declare the tags to parse
    with open('articles_dm.csv','a') as file: #opening existing output file to append
        writer = csv.writer(file)
        writer.writerow(["Date","Section","Title","Score","URL"])
        for tag in tags:
            article_returns = ((skimmer((url_merge(tag)),tag))) #calling skimmer for every tag
            for i in range(len(article_returns)): #writing results
                writer.writerow(article_returns[i])

main()


    
    


 




 

