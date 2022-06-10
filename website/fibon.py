from flask import Blueprint, render_template, request, flash
from flask_login import login_required, current_user

fibon = Blueprint('fibon', __name__)

@fibon.route('/fibon', methods=['GET', 'POST'])
@login_required
def fibonacci():
    fibonacci_Nums = [0, 1]
    if request.method == 'POST':
    
        number = int(request.form.get('number'))
        if number < 2:
            flash("Enter a number bigger than 1", category='error')
        elif number > 100:
            flash("Please enter something smaller than 100.", category='error')
        else:
            for i in range(number-2):
                new_number = fibonacci_Nums[i] + fibonacci_Nums[i+1]
                fibonacci_Nums.append(new_number)
    
    return render_template("fibon.html", user=current_user, results=fibonacci_Nums)