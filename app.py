import os
from flask import Flask, render_template, request, redirect, session, url_for, flash
import string
import random

app = Flask(__name__)
app.secret_key = "tu6fgjyuo7i65u7rtgwet3y5y6u" # Change this!

# --- 1. CONTENT DATABASE (Add your articles here) ---
blog_data = {
    # JEE Articles
    "math-shortcuts": {
        "title": "Top 10 Mathematics Shortcuts for JEE",
        "content": """
            <p class="lead">Time management is the key to clearing JEE. Here are the essential shortcuts you need for 2026.</p>
            <h3>1. Integration by Parts (DI Method)</h3>
            <p>Don't use the standard formula for repeated integration. Use the DI (Differentiation-Integration) table method to solve integrals of type x^n * e^x in seconds.</p>
            <h3>2. Coordinate Geometry</h3>
            <p>Memorize the condition of tangency for Circle, Parabola, and Ellipse (c = a/m, c^2 = a^2(1+m^2)). This solves 40% of questions directly.</p>
            <h3>3. Matrices</h3>
            <p>For finding the inverse of a 3x3 matrix, use the Cayley-Hamilton theorem shortcut instead of the traditional adjoint method.</p>
        """
    },
    "organic-chemistry": {
        "title": "Mastering Organic Reaction Mechanisms",
        "content": """
            <p>Organic chemistry requires understanding electron flow, not rote memorization.</p>
            <h3>SN1 vs SN2 Reactions</h3>
            <ul>
                <li><strong>SN1:</strong> Two steps, carbocation intermediate, favors polar protic solvents.</li>
                <li><strong>SN2:</strong> Single step, transition state, favors polar aprotic solvents.</li>
            </ul>
            <p>Focus heavily on 'General Organic Chemistry' (GOC) effects like Resonance and Hyperconjugation before starting reactions.</p>
        """
    },
    
    # CDS Articles
    "preparation-strategy": {
        "title": "CDS 2026: Complete 6-Month Strategy",
        "content": """
            <p>The Combined Defence Services exam is about speed and accuracy.</p>
            <h3>English (100 Marks)</h3>
            <p>Focus on Antonyms, Synonyms, and Idioms. Read 'The Hindu' editorial daily to improve comprehension.</p>
            <h3>General Knowledge</h3>
            <p>Do not study everything. Prioritize: 
            <br>1. Modern History (1857-1947)
            <br>2. Physical Geography
            <br>3. Current Affairs (Last 6 months)</p>
        """
    },
    "cds-2026-dates": {
        "title": "CDS 1 2026 Notification & Eligibility",
        "content": """
            <p><strong>Notification Date:</strong> December 2025</p>
            <p><strong>Exam Date:</strong> April 2026</p>
            <h3>Age Limits</h3>
            <ul>
                <li><strong>IMA:</strong> 19-24 Years</li>
                <li><strong>OTA:</strong> 19-25 Years</li>
            </ul>
            <p>Ensure you have your degree certificate or provisional ready before the SSB interview.</p>
        """
    },

    # CAPF Articles
    "paper-2-tips": {
        "title": "How to Score 90+ in CAPF Paper 2",
        "content": """
            <p>Paper 2 is subjective and often the reason candidates fail. Here is the structure for a perfect essay.</p>
            <h3>Essay Structure</h3>
            <ul>
                <li><strong>Introduction:</strong> Start with a quote or a recent statistic.</li>
                <li><strong>Body:</strong> Divide into Social, Economic, and Political aspects.</li>
                <li><strong>Conclusion:</strong> Always end on a futuristic, positive note (Way Forward).</li>
            </ul>
        """
    },

    # SSC Articles
    "cpo-guide": {
        "title": "SSC CPO: Physical & Medical Standards",
        "content": """
            <p>SSC CPO is unique because the Physical Endurance Test (PET) is qualifying but mandatory.</p>
            <h3>Male Candidates</h3>
            <ul>
                <li>1.6 Km Run in 6.5 Minutes</li>
                <li>Long Jump: 3.65 Meters</li>
                <li>High Jump: 1.2 Meters</li>
            </ul>
            <h3>Medical Tips</h3>
            <p>Check for flat foot and knock knees immediately. LASIK surgery is allowed if done 6 months prior.</p>
        """
    },
    
    # Default for generic pages
    "default": {
        "title": "Study Material",
        "content": "<p>This content is currently being updated. Please check back later for detailed notes and PDFs.</p>"
    }
}

# --- EXISTING LOGIC BELOW ---
url_db = {}

def generate_id():
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(6))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/shorten', methods=['POST'])
def shorten():
    long_url = request.json.get('url')
    short_id = generate_id()
    url_db[short_id] = long_url
    return {"short_url": f"{request.host_url}s/{short_id}"}

@app.route('/s/<short_id>')
def start_short_path(short_id):
    if short_id not in url_db:
        return "URL Not Found", 404
    session['step'] = 1
    session['target_id'] = short_id
    return redirect(url_for('interstitial'))

@app.route('/interstitial', methods=['GET', 'POST'])
def interstitial():
    step = session.get('step', 1)
    short_id = session.get('target_id')
    
    if request.method == 'POST':
        user_answer = request.form.get('answer')
        correct_answer = request.form.get('correct')
        
        if user_answer == correct_answer:
            session['step'] = step + 1
            if session['step'] > 5:
                return redirect(url_for('final_page'))
            return redirect(url_for('interstitial'))

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

# --- UPDATED DYNAMIC BLOG ROUTE ---
@app.route('/blog/<category>/<slug>')
def blog_post(category, slug):
    # Fetch data from our dictionary
    data = blog_data.get(slug, blog_data["default"])
    
    # If the title wasn't found in dictionary, use the slug as a fallback title
    title = data["title"] if slug in blog_data else slug.replace('-', ' ').title()
    
    return render_template('blog_template.html', category=category, title=title, content=data["content"])

@app.route('/privacy-policy')
def privacy():
    return render_template('privacy.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        flash("Thank you! Your message has been sent.")
        return render_template('contact.html', success=True)
    return render_template('contact.html')

if __name__ == '__main__':
    app.run(debug=True)
