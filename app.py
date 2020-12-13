from flask import Flask, request, jsonify,send_file,render_template
import flask
import json
import questions
import answers
import os
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
    # content = request.get_json()
    # url = content['url']

    if request.method == 'POST':
        url = flask.request.values.get('quizurl')
        title = url.split('?title=')[1]
        output_file_name = 'Quiz_'+title+'.zip'
        print(url)
        # Get questions
        question_list = []
        page = questions.get_quiz(url)
        if page != 'error':
            question_list = questions.scrape_quiz(page)
        else:
            return 'Invalid URL'

        # Get answers
        page = answers.get_page(url)
        solutions = answers.parse_page(page,question_list)
        answers.write_to_csv(solutions)


        with ZipFile(output_file_name,'w') as zip:
            zip.write('questions.txt')
            zip.write('Answers.csv')
        file = open(output_file_name, 'rb')
        file.seek(0)
        # file = open('questions.txt','rb')
        # file.seek(0)
        # return send_file(file,mimetype='text/plain',attachment_filename='question.txt', as_attachment=True)
        return send_file(file, mimetype='application/zip', attachment_filename=output_file_name, as_attachment=True)
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug = True)
