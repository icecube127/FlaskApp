from flask import Blueprint, render_template, request, flash
from flask_login import login_required, current_user
import math

changemachine = Blueprint('changemachine', __name__)

@changemachine.route('/changemachine', methods=['GET', 'POST'])
@login_required
def givechange():
    
    if request.method == 'POST':
        charge = float(request.form.get('charge'))
        money = float(request.form.get('money'))
        data = request.form.get('unknown')
        
        if money < charge:
            flash("You did not give me enough money.")
            
        else:
            billsDict = {'bill100': 0, 'bill20' : 0, 'bill10': 0, 'bill5' : 0, 'bill1': 0}
            coinsDict = {'quarter': 0, 'dime': 0,'nickle': 0,'penny': 0,}

            dollar_bills = 0
            coins = 0

            #this finds out how many dollars need to be returned    
            dollar_bills = math.floor(money - charge)
            
            charge = int(charge * 100)
            money = int(money * 100)

            coins = (money - charge) - (dollar_bills * 100)
            money_left = dollar_bills + coins/100
            
            #below is to calculate bills
            while dollar_bills >= 100:
                dollar_bills -= 100
                billsDict['bill100'] += 1

            while dollar_bills >= 20:
                dollar_bills -= 20
                billsDict['bill20'] += 1

            while dollar_bills >= 10:
                dollar_bills -= 10
                billsDict['bill10'] += 1

            while dollar_bills >= 5:
                dollar_bills -= 5
                billsDict['bill5'] += 1
            
            billsDict['bill1'] = dollar_bills

            # below is to calculate coins
            while coins >= 25:
                coins -= 25
                coinsDict['quarter'] += 1
            
            while coins >= 10:
                coins -= 10
                coinsDict['dime'] += 1

            while coins >= 5:
                coins -= 5
                coinsDict['nickle'] += 1

            coinsDict['penny'] = coins
        
            return render_template("changemachine.html", user=current_user, bills=billsDict, coins=coinsDict, money_left=money_left)
    return render_template("changemachine.html", user=current_user)