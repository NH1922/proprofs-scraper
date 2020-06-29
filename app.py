from flask import Flask, request, jsonify,send_file,render_template
import flask
import json
import questions
import answers
from zipfile import ZipFile
app = Flask(__name__)


@app.route('/handle',methods=['POST'])
def handle_form():
    url = request.form['quizurl']
    print(url)
    return 'post complete'

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
        print(url)
        # Get questions
        page = questions.get_quiz(url)
        if page != 'error':
            questions.scrape_quiz(page)
        else:
            return 'Invalid URL'

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
        return send_file(file, mimetype='application/zip', attachment_filename='Quiz.zip', as_attachment=True)
    return render_template('index.html')


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