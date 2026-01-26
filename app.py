import os
import json
import base64
import requests
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify, Response  # Added Response here
from functools import wraps
from bs4 import BeautifulSoup # Added for HTML filtering

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

# --- NEW: ROUTE TO SERVE IMAGES THROUGH YOUR DOMAIN ---
@app.route('/uploads/<filename>')
def serve_image(filename):
    """Fetches the image from GitHub and serves it through your domain."""
    github_raw_url = f"https://raw.githubusercontent.com/{REPO_OWNER}/{REPO_NAME}/{BRANCH}/static/uploads/{filename}"
    res = requests.get(github_raw_url)
    if res.status_code == 200:
        return Response(res.content, mimetype=res.headers.get('Content-Type'))
    return "Image not found", 404

# --- UPDATED GITHUB IMAGE UPLOAD ---
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
    if r.status_code in [201, 200]:
        # Return a relative path served by our new route
        return f"/uploads/{filename}"
    return None

@app.route('/sitemap.xml', methods=['GET'])
def sitemap():
    """Generates a sitemap.xml dynamically."""
    pages = []
    # Static pages
    for rule in app.url_map.iter_rules():
        if "GET" in rule.methods and len(rule.arguments) == 0:
            pages.append(["https://subodhpgcollege.site" + str(rule.rule), "2026-01-26"])

    # Dynamic Blog Posts from posts.json
    posts, _ = get_github_file(POSTS_FILE_PATH)
    for post in posts:
        url = "https://subodhpgcollege.site/blog/" + post['slug']
        pages.append([url, "2026-01-26"])

    sitemap_xml = render_template('sitemap_template.xml', pages=pages)
    response = make_response(sitemap_xml)
    response.headers["Content-Type"] = "application/xml"
    return response

# --- UPDATED INDEX ROUTE WITH PAGINATION ---
@app.route('/')
def index():
    # Get current page from URL (default is 1)
    page = request.args.get('page', 1, type=int)
    per_page = 12
    
    posts, _ = get_github_file(POSTS_FILE_PATH)
    
    # Calculate pagination
    total_posts = len(posts)
    total_pages = (total_posts + per_page - 1) // per_page
    
    start = (page - 1) * per_page
    end = start + per_page
    paginated_posts = posts[start:end]
    
    return render_template('index.html', 
                           posts=paginated_posts, 
                           page=page, 
                           total_pages=total_pages)

# --- NEW SEARCH ROUTE ---
@app.route('/search')
def search():
    query = request.args.get('q', '').strip().lower()
    posts, _ = get_github_file(POSTS_FILE_PATH)
    
    if query:
        # Filter posts by title or category matching the query
        filtered_posts = [
            p for p in posts 
            if query in p['title'].lower() or query in p['category'].lower()
        ]
    else:
        filtered_posts = []
        
    return render_template('index.html', 
                           posts=filtered_posts, 
                           search_query=query)

@app.route('/blog/<slug>')
def blog_post(slug):
    posts, _ = get_github_file(POSTS_FILE_PATH)
    # Find the current post
    post = next((p for p in posts if p['slug'] == slug), None)
    
    if not post:
        return "Post not found", 404
    
    # Logic for Similar Posts: Filter by category, exclude current post, limit to 3
    similar_posts = [p for p in posts if p['category'] == post['category'] and p['slug'] != slug][:3]
    
    return render_template('blog_post.html', post=post, similar_posts=similar_posts)

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

# --- UPDATED ADMIN ADD ROUTE WITH FILTERING ---
@app.route('/admin/add', methods=['POST'])
@login_required
def add_post():
    posts, sha = get_github_file(POSTS_FILE_PATH)
    image_url = ""
    
    if 'image' in request.files:
        file = request.files['image']
        if file.filename != '':
            image_url = upload_github_image(file.filename, file.read())

    raw_content = request.form.get('content', '')

    # 1. Replace "Vidya Rays" with "Vidya Subodh"
    processed_content = raw_content.replace("Vidya Rays", "Vidya Subodh")
    processed_content = processed_content.replace("vidyarays", "vidyasubodh")

    # 2. Filter HTML: Extract only <p> and <table> tags
    soup = BeautifulSoup(processed_content, "html.parser")
    tags_to_keep = ['p', 'table', 'thead', 'tbody', 'tr', 'th', 'td', 'h2', 'h3', 'ul', 'li']
    
    # Extract only the allowed tags and their content
    clean_html_parts = []
    for element in soup.find_all(tags_to_keep):
        # Prevent nesting issues by only taking top-level allowed elements
        if element.parent.name not in tags_to_keep:
            clean_html_parts.append(str(element))
    
    final_content = "".join(clean_html_parts) if clean_html_parts else processed_content

    new_post = {
        "title": request.form.get('title'),
        "slug": request.form.get('slug'),
        "category": request.form.get('category'),
        "image": image_url,
        "content": final_content,
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

@app.route('/robots.txt')
def static_from_root():
    return send_from_directory(app.static_folder, request.path[1:])

if __name__ == '__main__':
    app.run(debug=True)
