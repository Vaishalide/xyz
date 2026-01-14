import os
from flask import Flask, render_template, request, redirect, session, url_for
import string
import random

app = Flask(__name__)
app.secret_key = "super_secret_key_for_session" # Change this!

# Database-like storage (For Heroku, use Redis or PostgreSQL for persistence)
url_db = {}

def generate_id():
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(6))

# --- ROUTE: THE BLOG (For AdSense Approval) ---
@app.route('/')
def index():
    # Render your blog content here
    return render_template('index.html')

# --- ROUTE: API TO SHORTEN (For you to use) ---
@app.route('/api/shorten', methods=['POST'])
def shorten():
    long_url = request.json.get('url')
    short_id = generate_id()
    url_db[short_id] = long_url
    return {"short_url": f"{request.host_url}s/{short_id}"}

# --- ROUTE: THE REDIRECT LOGIC ---
@app.route('/s/<short_id>')
def start_short_path(short_id):
    if short_id not in url_db:
        return "URL Not Found", 404
    
    # Reset progression session
    session['step'] = 1
    session['target_id'] = short_id
    return redirect(url_for('interstitial'))

@app.route('/interstitial', methods=['GET', 'POST'])
def interstitial():
    step = session.get('step', 1)
    short_id = session.get('target_id')
    
    if request.method == 'POST':
        # Logic to check math answer
        user_answer = request.form.get('answer')
        correct_answer = request.form.get('correct')
        
        if user_answer == correct_answer:
            session['step'] = step + 1
            if session['step'] > 5:
                return redirect(url_for('final_page'))
            return redirect(url_for('interstitial'))

    # Generate a simple math question
    num1, num2 = random.randint(1, 10), random.randint(1, 10)
    correct = num1 + num2
    options = [correct, correct + 2, correct - 1]
    random.shuffle(options)

    return render_template('quiz_page.html', step=step, n1=num1, n2=num2, correct=correct, options=options)

@app.route('/final')
def final_page():
    short_id = session.get('target_id')
    final_url = url_db.get(short_id)
    return render_template('final_page.html', final_url=final_url)

if __name__ == '__main__':
    app.run(debug=True)
