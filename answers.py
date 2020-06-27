from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import csv

QUIZ_URL  = 'https://www.proprofs.com/quiz-school/story.php?title=mtg1njq3oa7yte'
FILE_NAME = 'Answers.csv'

navigation_js = '''
buttons = document.querySelectorAll('[class="dropdown_icon_more t_wo"],[id="cardshowflash"],[name="mySubmit"]')
buttons.forEach(button => {
    button.click()
});

document.querySelector('#fctbleview').click()
table = document.querySelector('table[id="flashTable"')
rows = [...table.rows]

rows.forEach(function (row, index){
    var question = index +'. '+row.cells[0].innerText
    var answer  = row.cells[1].innerText
    console.log(index +'. '+row.cells[0].innerText)
    console.log(row.cells[1].innerText)
});
'''


def get_page():
    print('Getting Page...')
    options = Options()
    options.headless = True
    #driver = webdriver.Chrome(r'D:\Salesforce Workspace\SalesforceScripts\webdriver\chromedriver.exe',options=options)
    driver = webdriver.Chrome('./webdriver/chromedriver.exe',options=options)
    driver.get(QUIZ_URL)
    driver.execute_script(navigation_js)
    page =  driver.find_element_by_xpath("//body").get_attribute('outerHTML')
    driver.quit()
    return page

def parse_page(page):
    print('Parsing the page...')
    solutions = []
    soup = BeautifulSoup(page, 'html.parser')
    table = soup.find('table', id='flashTable')
    for index,row in enumerate(soup.find_all('tr', id='row')):
        cells = row.find_all('td')
        if len(cells) > 0:
            solutions.append({
                'Q No.':index,
                'Question':cells[0].text.strip(),
                'Answer':cells[1].text.strip()
            })
    return solutions


def write_to_csv(solutions):
    with open(FILE_NAME, 'w', encoding='utf8', newline='') as output_file:
        fc = csv.DictWriter(output_file, fieldnames=solutions[0].keys(), )
        fc.writeheader()
        fc.writerows(solutions)


if __name__ == '__main__':
    page = get_page()
    solutions = parse_page(page)
    write_to_csv(solutions)



