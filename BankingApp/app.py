from flask import Flask, request, render_template, redirect, url_for, session, flash
import bcrypt

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Dummy user database simulation
users = {
    'Abdullah': bcrypt.hashpw('pass123'.encode(), bcrypt.gensalt()),
    'user2': bcrypt.hashpw('abc@123'.encode(), bcrypt.gensalt())
}

# Initial setup for the balance and transaction log
balance = 0
transaction_log = []

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and bcrypt.checkpw(password.encode(), users[username]):
            session['username'] = username
            return redirect(url_for('home'))
        else:
            return 'Login Failed'
    return render_template('login.html')

@app.route('/home')
def home():
    if 'username' in session:
        return render_template('home.html', username=session['username'], balance=balance)
    return redirect(url_for('login'))

@app.route('/deposit', methods=['POST'])
def deposit():
    global balance
    amount = float(request.form['amount'])
    if amount > 0:
        balance += amount
        transaction_log.append(('Deposit', amount))
        flash(f'Successfully deposited ${amount:.2f}')
    else:
        flash('Invalid amount for deposit')
    return redirect(url_for('home'))

@app.route('/withdraw', methods=['POST'])
def withdraw():
    global balance
    amount = float(request.form['amount'])
    if amount > 0 and amount <= balance:
        balance -= amount
        transaction_log.append(('Withdrawal', amount))
        flash(f'Successfully withdrew ${amount:.2f}')
    else:
        flash('Invalid amount or insufficient funds for withdrawal')
    return redirect(url_for('home'))

@app.route('/transactions')
def transactions():
    if 'username' in session:
        return render_template('transactions.html', transactions=transaction_log)
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(debug=True)
