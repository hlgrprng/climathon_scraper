from summa import summarizer
from summa import keywords
import csv
import re


with open('summeries.csv', 'wb') as csvfile:
    challengewriter = csv.writer(csvfile, delimiter=';',
                            quotechar='"', quoting=csv.QUOTE_MINIMAL)
    challengewriter.writerow(['id', 'city', 'title', 'question', 'theme', 'keywords', 'summary', 'challenge_text_main', 'challenge_url' ])
    with open('challenges.csv', 'rb') as csvfile:

        challenges = csv.reader(csvfile, delimiter=';', quotechar='"')
        line_count = 1
        for row in challenges:
            challenge_id = row[0]
            city = row[1]
            title = row[2]
            question = row[3]
            theme = row[4]
            challenge_description = row[5]
            link = row[6]

            challenge_description = re.sub(r'[\t\r\n]', ' ', challenge_description)
            summary = summarizer.summarize(challenge_description, words=50)
            print summary

            words = keywords.keywords(challenge_description)
            words = re.sub(r'[\t\r\n]', '|', words)
            print words

            challengewriter.writerow([challenge_id, city, title, question, theme, words.encode('utf-8'), summary, challenge_description, link])
