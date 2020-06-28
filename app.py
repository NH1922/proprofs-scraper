from flask import Flask, request, jsonify,send_file
import json
import questions
import answers
from zipfile import ZipFile
app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def get_file():
    # with open('questions.txt','w') as questionfile:
    #     questionfile.write('lol')
    #     questionfile.write('one more line')
    #     questionfile.write('another line')
    # file = open('questions.txt','rb')
    # file.seek(0)
    content = request.get_json()
    url = content['url']

    # Get questions
    page = questions.get_quiz(url)
    questions.scrape_quiz(page)

    # Get answers
    page = answers.get_page(url)
    solutions = answers.parse_page(page)
    answers.write_to_csv(solutions)


    with ZipFile('Quiz.zip','w') as zip:
        zip.write('questions.txt')
        zip.write('Answers.csv')
    file = open('Quiz.zip', 'rb')
    file.seek(0)
    # file = open('questions.txt','rb')
    # file.seek(0)
    # return send_file(file,mimetype='text/plain',attachment_filename='question.txt', as_attachment=True)
    return send_file(file, mimetype='application/zip', attachment_filename='question.txt', as_attachment=True)


@app.route("/add")
def add_manga():
    global manhwas
    manhwa_name = request.args.get('name')
    chapters = request.args.get('chapters')
    manhwas[manhwa_name] = chapters
    print(manhwas)
    return jsonify(manhwas)


if __name__ == '__main__':
    app.run(debug=True)