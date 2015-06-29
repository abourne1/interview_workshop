from flask import render_template, redirect, url_for, request, flash
from .models import Topic, Question
from flaskext.mail import Message
from sqlalchemy import desc
from app import app, db, mail

@app.route('/')
def index():
    return render_template(
        'index.html',
        topics=db.session.query(Topic).all(),
        questions=db.session.query(Question).all(),
        difficulties={
            1: "brogrammer",
            2: "application developer",
            3: "library writer",
            4: "language creator",
            5: "linus torvalds"
        }
    )

@app.route('/new', methods=['POST'])
def new():
    new_question = Question(
        author=request.form['author'],
        topic_id=request.form['topic_id'],
        difficulty=request.form['difficulty'],
        text=request.form['question'],
        hint=request.form['hint'],
        answer=request.form['answer']
    )
    db.session.add(new_question)
    db.session.commit()
    flash('Question added to database!')
    msg = Message(
        "New Question",
        sender="from@example.com",
        recipients=[app.config['EMAIL_ADDR']]
    )
    msg.body("A new question has been submitted:\n" +
             request.form['question'] + "\n" +
             request.form['hint']
             )
    mail.send(msg)
    return redirect(url_for('index'))

@app.route('/call', methods=['POST'])
def call():
    render_template(
        'record.xml',
        topics=db.session.query(Topic).all()
    )

@app.route('/query', methods=['POST'])
def query():
    resp = twilio.twiml.Response()
    question = request.form['question']
    if question:
        digit_pressed = request.values.get('Digits', None)
        if digit_pressed == "1":
            resp.say(question.text)
        elif digit_pressed == "2":
            resp.say(question.hint)
        elif digit_pressed == "3":
            questions = request.form['questions']
            question = questions[0]
            questions = questions[1:]
        elif digit_pressed == "4":
            resp.say(question.answer)

    else:
        text = request.form['TranscriptionText']
        difficulties = {"easy":[1,2], "medium":[2,3,4], "hard":[4,5]
        chosen_diffs = set(difficulties.keys()).intersection(text)
        diff_ints = set(sum([difficulties[diff] for diff in chosen_diffs], []))
        topics = [topic.name for topic in db.session.query(Topic).all()]
        chosen_topics = set(topics).intersection(text)

        questions = db.session.query(Question).filter(
            db.session.query(Topic).get(Question.topic_id).name in chosen_topics,
            Question.difficulty in diff_ints
        ).order_by(Question.popularity.desc())
        question = questions[0]
        
    # pass questions[1:] to next url call
    with resp.gather(numDigits=1, action="/query", method="POST") as g:
        g.say(q.question)
        g.say(
            "Press 1 to repeat the question.\
            Press 2 for a hint. \
            Press 3 to skip question \
            Press 4 to hear answer"
            )




