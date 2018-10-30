from bs4 import BeautifulSoup
from bs4 import Comment
import urllib2
import requests
import csv
import re
import codecs


number = "1"
url = "https://climathon.climate-kic.org/en/"
url2 = "https://climathon.climate-kic.org"
with open('challenges.csv', 'wb') as csvfile:
    challengewriter = csv.writer(csvfile, delimiter=';',
                            quotechar='"', quoting=csv.QUOTE_MINIMAL)
    challengewriter.writerow(['id', 'city', 'title', 'question', 'theme', 'challenge_text_main', 'challenge_url'])
    with open('cities.csv', 'rb') as csvfile:

        cities = csv.reader(csvfile, delimiter=';', quotechar='"')
        for row in cities:
            #print ', '.join(row)
            cityid = url.join(row)
            load_city = url + cityid
            print load_city

            soup_cities = urllib2.urlopen(load_city).read()
            #Html_file= open("cities/" + cityid + ".html","w")
            #Html_file.write(soup_cities)
            #Html_file.close()

            #soup = BeautifulSoup(soup_cities,"html.parser")
            soup = BeautifulSoup(open('cities/' + cityid + '.html'),"html.parser")
            #soup = BeautifulSoup(open('cities/toledo.html'),"html.parser")
            [x.extract() for x in soup.find_all('div',{'class':'tab-pane fade'})]
            [x.extract() for x in soup.find_all('div',{'class':'mod-aesir-item mod-aesir-item-default'})]

            title = soup.find_all('h1',attrs={'class':'title'})
            print title[0].text
            city = title[0].text.encode('utf-8')

            n = 0
            data = soup.findAll('div',attrs={'class':'text'})
            for div in data:
                links = div.findAll('a')
                for a in links:
                    n += 1
                    link = url2 + a['href']

                    theme = re.sub(r'/en/challenges/', '', a['href'])
                    theme = theme.split('/', 1)[0]
                    #print theme
                    challenge_description = ""
                    #soup_challenge = BeautifulSoup(open('challenge.html'),"html.parser")
                    soup_challenge_text = urllib2.urlopen(link).read()
                    soup_challenge = BeautifulSoup(soup_challenge_text,"html.parser")
                    #soup_challenge = BeautifulSoup(open(link),"html.parser")
                    challenge_id = cityid+"0"+str(n)
                    print n
                    print challenge_id
                    challenge_id = challenge_id.encode('utf-8')

                    Html_file= open("challenges/" + challenge_id + ".html","w")
                    Html_file.write(soup_challenge_text)
                    Html_file.close()

                    challenge_title = soup_challenge.find_all('h1',attrs={'class':'title'})
                    title = ""
                    try:
                        title = challenge_title[0].text.encode('utf-8')
                    except:
                        print "No title!"
                    print title
                    intro_text = soup_challenge.find_all('div',attrs={'class':'introText'})
                    question = intro_text[0].h3.text.encode('utf-8')
                    if title == "":
                        title = question
                    intro_text = intro_text[0].p.text.encode('utf-8')
                    [x.extract() for x in soup_challenge.find_all('h3')]
                    description = soup_challenge.find_all('div',attrs={'class':'description'})
                    for each in description:
                        print each.getText()
                        challenge_description += each.getText() + " "
                    challenge_description = re.sub(r'[\t\r\n]', ' ', challenge_description)
                    challenge_description = challenge_description.encode('utf-8')
                    challenge_description = intro_text + " " + challenge_description


                    #print challenge_description
                    #description = soup_challenge.find_next('div',attrs={'class':'description'})
                    #print description[0].p.text
                    #challengewriter.writerow(['id', city, url + a['href'], title, question, theme, challenge_description])
                    challengewriter.writerow([challenge_id, city, title, question, theme, challenge_description, link])



        #r = requests.get(url)
        #soup = BeautifulSoup(r.content)
        #price = soup.find_all("div",{"class":"property-card-price-container"})
        #address = soup.find_all("div",{"class":"property-card-subtitle"})
