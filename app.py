import os
import redis
from flask import Flask, render_template, request, redirect, session, url_for, flash
import string
import random

app = Flask(__name__)
app.secret_key = "tu6fgjyuo7i65u7rtgwet3y5y6u" 

# --- REDIS SETUP ---
# Heroku provides the Redis URL via the REDIS_URL environment variable
redis_url = os.getenv('REDIS_URL', 'redis://localhost:6379')

# Use connection_pool to specify SSL settings if the URL starts with 'rediss://'
if redis_url.startswith("rediss://"):
    db = redis.from_url(
        redis_url, 
        decode_responses=True, 
        ssl_cert_reqs=None # This line disables SSL verification
    )
else:
    db = redis.from_url(redis_url, decode_responses=True)

# --- 1. CONTENT DATABASE ---
blog_data = {
    # JEE Articles
    "math-shortcuts": {
        "title": "Top 10 Mathematics Shortcuts for JEE",
        "content": """
            <p class="lead">Time management is the key to clearing JEE. Here are the essential shortcuts you need for 2026.</p>
            <h3>1. Integration by Parts (DI Method)</h3>
            <p>Don't use the standard formula for repeated integration. Use the DI (Differentiation-Integration) table method.</p>
            <h3>2. Coordinate Geometry</h3>
            <p>Memorize the condition of tangency for Circle, Parabola, and Ellipse. This solves 40% of questions directly.</p>
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
        """
    },
    
    # NEET Articles
    "neet-biology": {
        "title": "How to Score 340+ in NEET Biology",
        "content": """
            <p>Biology constitutes 50% of the NEET paper. Neglecting NCERT is the biggest mistake students make.</p>
            <h3>The NCERT Strategy</h3>
            <p>Every line of the NCERT Biology textbooks (Class 11 & 12) is a potential MCQ. Focus on:</p>
            <ul>
                <li><strong>Genetics & Evolution:</strong> High weightage unit.</li>
                <li><strong>Human Physiology:</strong> Diagram-based questions.</li>
                <li><strong>Ecology:</strong> Often ignored but very scoring.</li>
            </ul>
        """
    },
    "neet-physics": {
        "title": "Physics for Medical Students: The Fear Factor",
        "content": """
            <p>Medical students often struggle with Physics calculations. The key is to focus on modern physics and mechanics.</p>
            <h3>Priority Chapters</h3>
            <p>Semiconductors, Atoms & Nuclei, and Dual Nature of Matter are high-scoring and calculation-light.</p>
        """
    },

    # CA Articles
    "ca-roadmap": {
        "title": "Chartered Accountancy: Foundation to Final",
        "content": """
            <p>The CA course is a marathon, not a sprint. It tests your perseverance more than your intelligence.</p>
            <h3>1. CA Foundation</h3>
            <p>The entry-level test. Focus heavily on Accounting and Business Law.</p>
            <h3>2. Intermediate</h3>
            <p>The real filter. Group 1 (Accounting, Law, Costing, Tax) requires consistent daily practice of 8-10 hours.</p>
        """
    },

    # Teaching Exam Articles
    "ctet-cdp": {
        "title": "CTET: Child Development & Pedagogy (CDP)",
        "content": """
            <p>To clear CTET or any State TET, mastering CDP is non-negotiable as it covers 30 marks directly and influences pedagogy in other subjects.</p>
            <h3>Key Theorists</h3>
            <ul>
                <li><strong>Piaget:</strong> Cognitive Development Stages.</li>
                <li><strong>Vygotsky:</strong> Socio-Cultural Theory (ZPD).</li>
                <li><strong>Kohlberg:</strong> Moral Development.</li>
            </ul>
        """
    },

    # Defense Articles
    "preparation-strategy": {
        "title": "CDS 2026: Complete 6-Month Strategy",
        "content": "<p>Focus on Antonyms, Synonyms, and Idioms. Read 'The Hindu' editorial daily.</p>"
    },
    "cds-2026-dates": {
        "title": "CDS 1 2026 Notification & Eligibility",
        "content": "<p><strong>Exam Date:</strong> April 2026. <br><strong>Age Limit:</strong> 19-25 Years.</p>"
    },
    "paper-2-tips": {
        "title": "How to Score 90+ in CAPF Paper 2",
        "content": "<p>Paper 2 is subjective. Start with a quote or a recent statistic in your essay.</p>"
    },
    "cpo-guide": {
        "title": "SSC CPO: Physical & Medical Standards",
        "content": "<p>SSC CPO is unique because the Physical Endurance Test (PET) is qualifying but mandatory.</p>"
    },
    
    # Default
    "default": {
        "title": "Study Material",
        "content": "<p>This content is currently being updated. Please check back later for detailed notes and PDFs.</p>"
    }
}

# --- EXISTING LOGIC ---
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
    
    # Store in Redis: key is short_id, value is long_url
    db.set(short_id, long_url)
    
    return {"short_url": f"{request.host_url}s/{short_id}"}


@app.route('/s/<short_id>')
def start_short_path(short_id):
    # Retrieve from Redis
    if not db.exists(short_id):
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
    # Retrieve the final URL from Redis using the stored ID
    final_url = db.get(short_id)
    return render_template('final_page.html', final_url=final_url)

@app.route('/blog/<category>/<slug>')
def blog_post(category, slug):
    data = blog_data.get(slug, blog_data["default"])
    title = data["title"] if slug in blog_data else slug.replace('-', ' ').title()
    return render_template('blog_template.html', category=category, title=title, content=data["content"])

@app.route('/privacy-policy')
def privacy():
    return render_template('privacy.html')

# --- NEW ROUTE FOR TERMS ---
@app.route('/terms')
def terms():
    return render_template('terms.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        flash("Thank you! Your message has been sent.")
        return render_template('contact.html', success=True)
    return render_template('contact.html')

if __name__ == '__main__':
    app.run(debug=True)
