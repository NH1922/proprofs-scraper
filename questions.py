from bs4 import BeautifulSoup
import requests
import os

BASE_URL = 'https://www.proprofs.com/quiz-school/story.php?title=mtg1njq3oa7yte'
ANSWER_URL = 'https://www.proprofs.com/quiz-school/cardshow.php?title=platform-developer-1-pd1&q=1'


def get_quiz(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        return 'error'


def scrape_quiz(page):
    soup = BeautifulSoup(page, 'html.parser')
    question_list = []
    questions_list = soup.find('ul', class_='questions-list')
    questions = soup.find_all('li', class_='ques_marg')
    question_texts = soup.find_all('div', class_='question-text')
    answers = soup.find_all('ul', class_='answers-list')
    question_list = []
    with open('questions.txt','w') as fp:
        for i in range(len(question_texts)):
            question_list.append(question_texts[i].text.strip())
            print('{}. {}'.format(i+1,question_texts[i].text))
            fp.write('{}. {}'.format(i+1,question_texts[i].text) + '\n')
            options = answers[i].find_all('li')
            for option in options :
                option_no = option.find('div', class_='questonnopt').text.strip()
                option_text = option.find('div', class_='opt_text').text.strip()
                print(option_no + '' + option_text )
                fp.write(option_no + '' + option_text+'\n')
            print('\n')
            fp.write('\n')


if __name__ == '__main__':
    question_page = get_quiz(BASE_URL)
    if question_page != 'error':
        scrape_quiz(question_page)
