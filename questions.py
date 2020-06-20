from bs4 import BeautifulSoup
import requests

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
    questions_list = soup.find('ul', class_='questions-list')
    questions = soup.find_all('li', class_='ques_marg')
    question_texts = soup.find_all('div', class_='question-text')
    answers = soup.find_all('ul', class_='answers-list')

    for i in range(len(question_texts)):
        print('{}. {}'.format(i+1,question_texts[i].text))
        options = answers[i].find_all('li')
        for option in options :
            option_no = option.find('div', class_='questonnopt').text.strip()
            option_text = option.find('div', class_='opt_text').text.strip()
            print(option_no + '' + option_text )
        print('\n')


if __name__ == '__main__':
    question_page = get_quiz(BASE_URL)
    if question_page != 'error':
        scrape_quiz(question_page)