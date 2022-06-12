from flask import Blueprint, render_template, request, flash
from flask_login import login_required, current_user
import math
from random import randint, random
from numpy import empty

def generateQuestion(operator, question_level):
    # question_level: 1 is easiest, 3 is hardest. 
    # addition is 3-4 digits
    if operator == '+':
        if question_level == 1:
            x = randint(1, 9)
            y = randint(1, 9)    
        elif question_level == 2:
            x = randint(10, 99)
            y = randint(10, 99)
        else:    
            x = randint(100, 9999)
            y = randint(100, 9999)
        question = []
        question.append(x)
        question.append(y)
        question.append(operator)

        return question
    
    # subtraction is 3-4 digits
    elif operator == '-':
        if question_level == 1:
            x = randint(5, 10)
            y = randint(1, 5)            
        elif question_level == 2:
            y = randint(1, 60)
            x = 0
            while x < y:
                x = randint(30, 100)
        else:
            y = randint(100, 4999)
            x = 0
            while x < y:
                x = randint(1000, 9999)
        question = []
        question.append(x)
        question.append(y)
        question.append(operator)

        return question
    # mutlipication are 3 and then 2 digits
    elif operator == '*':
        if question_level == 1:
            x = randint(1, 10)
            y = randint(1, 10)
        elif question_level == 1:
            x = randint(10, 99)
            y = randint(10, 99)
        else:
            x = randint(100, 999)
            y = randint(11, 99)
        question = []
        question.append(x)
        question.append(y)
        question.append(operator)
        return question
    
    # division are 3 and then 1 digits
    elif operator == '/':
        if question_level == 1:
            x = randint(4, 10)
            y = randint(1, 3)
            while x%y != 0:
                x = randint(4, 10)
        elif question_level == 2:
            x = randint(50, 100)
            y = randint(2, 9)
            while x%y != 0:
                x = randint(50, 100)
        else:
            x = randint(100, 999)
            y = randint(2, 9)
            while x%y != 0:
                x = randint(100, 999)
        question = []
        question.append(x)
        question.append(y)
        question.append(operator)
        return question

def ParseQuestionBank(question_bank_data):
    question_bank_data = question_bank_data.replace('[', '')
    question_bank_data = question_bank_data.replace(']', '')
    question_bank_data = question_bank_data.replace("'", "")
    question_bank_data = question_bank_data.replace(',', '')
    question_bank_list = question_bank_data.split(' ')

    question_bank = []

    for index in range(0, len(question_bank_list), 4):
        currentQuestion = []
        # question format is [x, y, +, index]
        # can ignore index for this
        currentQuestion.append(question_bank_list[index])
        currentQuestion.append(question_bank_list[index+1])
        currentQuestion.append(question_bank_list[index+2])
        question_bank.append(currentQuestion)
    
    return question_bank

def checkAnswer(equation, answerKey):
    x = float(equation[0])
    y = float(equation[1])
    operator = equation[2]
    answer_Key = float(answerKey)
    answer = 0

    if operator == '+':
        answer = x + y
    elif operator == '-':
        answer = x - y
    elif operator == '*':
        answer = x * y
    elif operator == '/':
        answer = x / y
    else:
        print('something went wrong.')
    
    if answer == answer_Key:
        return True
    else:
        return False

mathquiz = Blueprint('mathquiz', __name__)

@mathquiz.route('/mathquiz', methods=['POST', 'GET'])
@login_required
def QuizMe():

    # getting info from selection
    if request.method == 'POST' and "operatorType" in request.form:
        operator = request.form.get('operatorType')
        number_of_questions = request.form.get('numQuestion')
        question_level = int(request.form.get('level'))
        question_bank = []
        question_ID = 0

        if not operator or not number_of_questions or not question_level:
            flash("Please make a valid selection.")
            return render_template("mathquiz.html", user=current_user)
        else:
            number_of_questions = int(number_of_questions)
            for i in range(number_of_questions):
                question = generateQuestion(operator, question_level)
                question.append(question_ID)
                question_bank.append(question)
                question_ID+=1
        
        return render_template("mathquiz.html", user=current_user, questionBank=question_bank)
    
    elif request.method != 'POST':
        return render_template("mathquiz.html", user=current_user)

    else:
        #this is the check answer POST request
        # grabbing all the questions from form
        question_bank_data = request.form.get('allQuestions')
        question_bank = ParseQuestionBank(question_bank_data)
                
        # grabbing all the answers from user input
        user_answers = []
        key='answer'
        keyNum=0
        end_of_answers = False
        #getting all the answers from POST call. 
        while not end_of_answers:
            currentKey=key+str(keyNum)
            data = request.form.get(currentKey)
            if not data:
                end_of_answers = True
            else:
                user_answers.append(data)
                keyNum+=1
        # correctness tracks the right or wrong
        results = []
        correct_answer = 0
        number_of_questions = len(user_answers)
        # checking all answers 
        for i in range(0, number_of_questions):
            if checkAnswer(question_bank[i], user_answers[i]):
                results.append('Correct')
                correct_answer+=1
            else:
                results.append('Wrong')
        
        # give student score
        student_score = int((correct_answer / number_of_questions) * 100)
        
        return render_template("mathquizresults.html", user=current_user, userScore=student_score, questionBank=zip(question_bank, user_answers, results))
    
