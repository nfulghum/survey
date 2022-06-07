from flask import Flask, request, flash, render_template, redirect, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)

app.config['SECRET_KEY'] = "itsasecret"
debug = DebugToolbarExtension(app)

responses = []


@app.route('/')
def home():
    return render_template('home.html', survey=survey)


@app.route('/start', methods=["post"])
def start():
    return redirect("/questions/0")


@app.route('/answer', methods=["post"])
def answer():
    choice = request.form['answer']

    responses.append(choice)

    if (len(responses) == len(survey.questions)):
        return redirect('/complete')
    else:
        return redirect(f'/questions/{len(responses)}')


@app.route('/questions/<int:qid>')
def questions(qid):
    if (responses is None):
        return redirect('/')
    if (len(responses) == len(survey.questions)):
        return redirect('/complete')
    if (len(responses) != qid):
        flash(f"Invalid question id: {qid}.")
        return redirect(f'/questions/{len(responses)}')

    question = survey.questions[qid]
    return render_template('questions.html', question_num=qid, question=question)


@app.route('/complete')
def complete():
    return render_template('complete.html')
