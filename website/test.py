from flask import Blueprint, render_template, request, flash
from flask_login import login_required, current_user
import math
from random import randint, random
from numpy import empty

test = Blueprint('test', __name__)

@test.route('/test', methods=['POST', 'GET'])
@login_required
def testme():

    # getting info from selection
    if request.method == 'POST':
        data1 = request.form.get('answer5')
        if not data1:
            print('data1 is none')
    
    return render_template("test.html", user=current_user)

@test.route('/test', methods=['POST', 'GET'])
@login_required
def testyou():

    # getting info from selection
    if request.method == 'POST':
        data1 = request.form.get('answer0')
        print('TEST YOUUUUUUUU' + str(data1))
    
    return render_template("test.html", user=current_user)