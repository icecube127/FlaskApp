from flask import Blueprint, render_template, request, flash
from flask_login import login_required, current_user
import math

mortgage = Blueprint('mortgage', __name__)

@mortgage.route('/mortgage', methods=['GET', 'POST'])
@login_required
def calc_mortgage():
    results = []    

    if request.method == 'POST':
        loan_amount = float(request.form.get('loan'))
        year_of_mortgage = int(request.form.get('year'))
        interest = float(request.form.get('interest'))
        
        '''
        For example, say you borrowed $265,000 on a 15-year mortgage at 4.32 percent. 
        #1 Start by dividing 0.0432 by 12 to find that the monthly rate equals 0.0036. 
        #2 add 1 to 0.0036 to get 1.0036. 
        #3, multiply 15 years by 12 payments per year to find that your loan consists of 180 monthly payments. 
        #4, raise 1.0036 to the negative 180th power to get 0.5237. 
        #5, subtract 0.5237 from 1 to get 0.4763. 
        #6, divide 0.0036 by 0.4763 to get 0.00755826. 
        #7, multiply 0.00755826 by $265,000 to find your monthly payment will be $2,002.93.
        '''
        #1
        interest = ((interest / 100) / 12)
        #2
        rate = 1 + interest
        #3
        num_of_payments = year_of_mortgage * 12
        #4
        rate = rate ** (-1 * num_of_payments)
        #5
        rate = 1 - rate
        #6
        rate = interest / rate
        #7
        monthly_payment = loan_amount * rate
        monthly_payment_str = "{:.2f}".format(monthly_payment)
        # return results: [0] is monthly payemnt [1] is number of payments
        results.append(monthly_payment_str)
        results.append(num_of_payments)
        return render_template("mortgage.html", user=current_user, result=results)

    return render_template("mortgage.html", user=current_user)