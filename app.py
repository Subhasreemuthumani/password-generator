from flask import Flask, render_template, request
import re

app = Flask(__name__)

def evaluate_password(password):
    length = len(password) >= 8
    upper = re.search(r'[A-Z]', password)
    lower = re.search(r'[a-z]', password)
    digit = re.search(r'\d', password)
    special = re.search(r'[!@#$%^&*(),.?":{}|<>]', password)

    score = sum([length, bool(upper), bool(lower), bool(digit), bool(special)])

    if score == 5:
        strength = 'Strong'
        color = 'green'
    elif score >= 3:
        strength = 'Moderate'
        color = 'orange'
    else:
        strength = 'Weak'
        color = 'red'

    return strength, color, {
        "Length ≥ 8": length,
        "Uppercase": bool(upper),
        "Lowercase": bool(lower),
        "Number": bool(digit),
        "Special char": bool(special)
    }

@app.route('/', methods=['GET', 'POST'])
def index():
    strength = None
    color = None
    criteria = {}
    password = ''

    if request.method == 'POST':
        password = request.form['password']
        strength, color, criteria = evaluate_password(password)

    return render_template('index.html', strength=strength, color=color, criteria=criteria, password=password)

if __name__ == '__main__':
    app.run(debug=True)
