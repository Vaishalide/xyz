import os
import json
import base64
import requests
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from functools import wraps

app = Flask(__name__)

# --- SECURE CONFIGURATION (Load from Heroku Config Vars) ---
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "default_fallback_key_for_local")
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
REPO_OWNER = os.environ.get("GITHUB_OWNER")
REPO_NAME = os.environ.get("GITHUB_REPO")
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD")
BRANCH = os.environ.get("GITHUB_BRANCH", "main")
POSTS_FILE_PATH = "posts.json"

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# --- GITHUB API HELPERS ---
def get_github_file(path):
    if not all([GITHUB_TOKEN, REPO_OWNER, REPO_NAME]):
        return [], None
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/{path}?ref={BRANCH}"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    r = requests.get(url, headers=headers)
    if r.status_code == 200:
        content = r.json()
        decoded_data = base64.b64decode(content['content']).decode('utf-8')
        return json.loads(decoded_data), content['sha']
    return [], None

def update_github_file(path, data, sha, message):
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/{path}"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    content_encoded = base64.b64encode(json.dumps(data, indent=4).encode('utf-8')).decode('utf-8')
    payload = {
        "message": message,
        "content": content_encoded,
        "sha": sha,
        "branch": BRANCH
    }
    r = requests.put(url, json=payload, headers=headers)
    return r.status_code

def upload_github_image(filename, file_data):
    path = f"static/uploads/{filename}"
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/{path}"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    content_encoded = base64.b64encode(file_data).decode('utf-8')
    payload = {
        "message": f"Upload image: {filename}",
        "content": content_encoded,
        "branch": BRANCH
    }
    r = requests.put(url, json=payload, headers=headers)
    if r.status_code == 201:
        return f"https://raw.githubusercontent.com/{REPO_OWNER}/{REPO_NAME}/{BRANCH}/{path}"
    return None

# --- ROUTES ---
@app.route('/')
def index():
    posts, _ = get_github_file(POSTS_FILE_PATH)
    return render_template('index.html', posts=posts)

@app.route('/blog/<slug>')
def blog_post(slug):
    posts, _ = get_github_file(POSTS_FILE_PATH)
    post = next((p for p in posts if p['slug'] == slug), None)
    if not post:
        return "Post not found", 404
    return render_template('blog_post.html', post=post)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form.get('password') == ADMIN_PASSWORD:
            session['logged_in'] = True
            return redirect(url_for('admin_dashboard'))
        flash("Invalid credentials")
    return render_template('login.html')

@app.route('/admin')
@login_required
def admin_dashboard():
    posts, _ = get_github_file(POSTS_FILE_PATH)
    return render_template('admin.html', posts=posts)

@app.route('/admin/add', methods=['POST'])
@login_required
def add_post():
    posts, sha = get_github_file(POSTS_FILE_PATH)
    image_url = ""
    if 'image' in request.files:
        file = request.files['image']
        if file.filename != '':
            image_url = upload_github_image(file.filename, file.read())

    new_post = {
        "title": request.form.get('title'),
        "slug": request.form.get('slug'),
        "category": request.form.get('category'),
        "image": image_url,
        "content": request.form.get('content'),
        "date": "January 2026"
    }
    posts.insert(0, new_post)
    update_github_file(POSTS_FILE_PATH, posts, sha, "Add new post via admin")
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/delete/<slug>')
@login_required
def delete_post(slug):
    posts, sha = get_github_file(POSTS_FILE_PATH)
    posts = [p for p in posts if p['slug'] != slug]
    update_github_file(POSTS_FILE_PATH, posts, sha, f"Delete post: {slug}")
    return redirect(url_for('admin_dashboard'))

# Standard AdSense required routes
@app.route('/privacy-policy')
def privacy(): return render_template('privacy.html')

@app.route('/terms')
def terms(): return render_template('terms.html')

@app.route('/disclaimer')
def disclaimer(): return render_template('disclaimer.html')

@app.route('/contact')
def contact(): return render_template('contact.html')

@app.route('/about')
def about(): return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True)
