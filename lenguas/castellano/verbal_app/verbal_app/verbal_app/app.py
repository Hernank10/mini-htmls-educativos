from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash
from functools import wraps
import json, os, hashlib, uuid
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = 'verbal2025_secret_key_x9z'

DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
USERS_FILE = os.path.join(DATA_DIR, 'users.json')
SCORES_FILE = os.path.join(DATA_DIR, 'scores.json')
FLASHCARDS_FILE = os.path.join(DATA_DIR, 'flashcards.json')
EXERCISES_FILE = os.path.join(DATA_DIR, 'exercises.json')

# ── helpers ──────────────────────────────────────────────────────────────────
def load_json(path, default):
    if os.path.exists(path):
        with open(path) as f:
            return json.load(f)
    return default

def save_json(path, data):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def hash_pw(pw): return hashlib.sha256(pw.encode()).hexdigest()

def get_users(): return load_json(USERS_FILE, {})
def save_users(u): save_json(USERS_FILE, u)
def get_scores(): return load_json(SCORES_FILE, {})
def save_scores(s): save_json(SCORES_FILE, s)

MEDALS = [
    {'name':'Bronce',   'min':0,   'icon':'🥉','color':'#cd7f32'},
    {'name':'Plata',    'min':200, 'icon':'🥈','color':'#C0C0C0'},
    {'name':'Oro',      'min':500, 'icon':'🥇','color':'#FFD700'},
    {'name':'Platino',  'min':1000,'icon':'💎','color':'#E5E4E2'},
    {'name':'Diamante', 'min':2000,'icon':'💠','color':'#b9f2ff'},
]
LEVELS = [
    {'level':1,'name':'Principiante','min':0},
    {'level':2,'name':'Básico','min':100},
    {'level':3,'name':'Intermedio','min':300},
    {'level':4,'name':'Avanzado','min':600},
    {'level':5,'name':'Experto','min':1000},
    {'level':6,'name':'Maestro','min':1800},
]

def get_medal(pts):
    m = MEDALS[0]
    for x in MEDALS:
        if pts >= x['min']: m = x
    return m

def get_level(pts):
    lv = LEVELS[0]
    for x in LEVELS:
        if pts >= x['min']: lv = x
    return lv

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated

def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        users = get_users()
        if not users.get(session['user_id'], {}).get('is_admin'):
            return redirect(url_for('dashboard'))
        return f(*args, **kwargs)
    return decorated

def user_score(uid):
    scores = get_scores()
    return scores.get(uid, {'total':0,'correct':0,'attempted':0,'by_lang':{},'history':[]})

def update_score(uid, pts, correct, lang):
    scores = get_scores()
    s = scores.get(uid, {'total':0,'correct':0,'attempted':0,'by_lang':{},'history':[]})
    s['total'] += pts; s['attempted'] += 1
    if correct: s['correct'] += 1
    bl = s.setdefault('by_lang', {})
    bl.setdefault(lang, {'pts':0,'correct':0,'attempted':0})
    bl[lang]['pts'] += pts; bl[lang]['attempted'] += 1
    if correct: bl[lang]['correct'] += 1
    s.setdefault('history', []).append({'ts':datetime.now().isoformat(),'pts':pts,'lang':lang,'correct':correct})
    if len(s['history']) > 200: s['history'] = s['history'][-200:]
    scores[uid] = s
    save_scores(scores)

# ── AUTH ──────────────────────────────────────────────────────────────────────
@app.route('/')
def index():
    if 'user_id' in session: return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        d = request.get_json() or request.form
        username = str(d.get('username','')).strip()
        email    = str(d.get('email','')).strip()
        password = str(d.get('password','')).strip()
        if not username or not email or not password:
            return jsonify({'ok':False,'msg':'Todos los campos son requeridos'}), 400
        users = get_users()
        if any(u['username']==username or u['email']==email for u in users.values()):
            return jsonify({'ok':False,'msg':'Usuario o email ya registrado'}), 400
        uid = str(uuid.uuid4())
        users[uid] = {
            'uid':uid,'username':username,'email':email,
            'password':hash_pw(password),'is_admin':len(users)==0,
            'created':datetime.now().isoformat(),'avatar':username[0].upper()
        }
        save_users(users)
        session['user_id'] = uid
        session['username'] = username
        return jsonify({'ok':True,'redirect': url_for('dashboard')})
    return render_template('register.html')

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        d = request.get_json() or request.form
        username = str(d.get('username','')).strip()
        password = str(d.get('password','')).strip()
        users = get_users()
        uid = next((k for k,v in users.items() if v['username']==username and v['password']==hash_pw(password)), None)
        if not uid:
            return jsonify({'ok':False,'msg':'Credenciales incorrectas'}), 401
        session['user_id'] = uid
        session['username'] = users[uid]['username']
        return jsonify({'ok':True,'redirect': url_for('dashboard')})
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# ── DASHBOARD ─────────────────────────────────────────────────────────────────
@app.route('/dashboard')
@login_required
def dashboard():
    uid = session['user_id']
    users = get_users()
    user = users[uid]
    sc = user_score(uid)
    medal = get_medal(sc['total'])
    level = get_level(sc['total'])
    next_lvl = next((x for x in LEVELS if x['min'] > sc['total']), None)
    progress = 0
    if next_lvl:
        span = next_lvl['min'] - level['min']
        progress = int(((sc['total'] - level['min']) / span) * 100) if span else 100
    # leaderboard top 5
    scores = get_scores()
    board = sorted([{'uid':k,'pts':v['total'],'user':users.get(k,{}).get('username','?')} for k,v in scores.items()], key=lambda x:-x['pts'])[:5]
    return render_template('dashboard.html', user=user, sc=sc, medal=medal, level=level, next_lvl=next_lvl, progress=progress, board=board)

# ── PROFILE ───────────────────────────────────────────────────────────────────
@app.route('/profile')
@login_required
def profile():
    uid = session['user_id']
    users = get_users()
    user = users[uid]
    sc = user_score(uid)
    medal = get_medal(sc['total'])
    level = get_level(sc['total'])
    history = sc.get('history', [])[-20:][::-1]
    earned_medals = [m for m in MEDALS if sc['total'] >= m['min']]
    return render_template('profile.html', user=user, sc=sc, medal=medal, level=level, history=history, earned_medals=earned_medals, all_medals=MEDALS, all_levels=LEVELS)

@app.route('/profile/update', methods=['POST'])
@login_required
def profile_update():
    uid = session['user_id']
    d = request.get_json()
    users = get_users()
    if d.get('email'): users[uid]['email'] = d['email']
    if d.get('password'): users[uid]['password'] = hash_pw(d['password'])
    save_users(users)
    return jsonify({'ok':True})

# ── FLASHCARDS ────────────────────────────────────────────────────────────────
@app.route('/flashcards')
@login_required
def flashcards():
    cards = load_json(FLASHCARDS_FILE, [])
    langs = sorted(set(c['lang'] for c in cards))
    return render_template('flashcards.html', total=len(cards), langs=langs)

@app.route('/api/flashcards')
@login_required
def api_flashcards():
    cards = load_json(FLASHCARDS_FILE, [])
    lang = request.args.get('lang','all')
    if lang != 'all': cards = [c for c in cards if c['lang']==lang]
    import random; random.shuffle(cards)
    return jsonify(cards)

# ── EXERCISES ─────────────────────────────────────────────────────────────────
@app.route('/exercises')
@login_required
def exercises():
    exs = load_json(EXERCISES_FILE, [])
    langs = sorted(set(e['lang'] for e in exs))
    return render_template('exercises.html', total=len(exs), langs=langs)

@app.route('/api/exercises')
@login_required
def api_exercises():
    exs = load_json(EXERCISES_FILE, [])
    lang = request.args.get('lang','all')
    if lang != 'all': exs = [e for e in exs if e['lang']==lang]
    import random; random.shuffle(exs)
    return jsonify(exs)

@app.route('/api/submit', methods=['POST'])
@login_required
def api_submit():
    uid = session['user_id']
    d = request.get_json()
    answer = str(d.get('answer','')).lower()
    keywords = [k.lower() for k in d.get('keywords',[])]
    lang = d.get('lang','es')
    pts = 0; correct = False
    if keywords:
        hits = sum(1 for k in keywords if k in answer)
        ratio = hits / len(keywords)
        if ratio >= 0.35: pts = 10; correct = True
        elif ratio >= 0.15: pts = 5
    update_score(uid, pts, correct, lang)
    sc = user_score(uid)
    return jsonify({'ok':True,'pts':pts,'correct':correct,'total':sc['total'],'medal':get_medal(sc['total']),'level':get_level(sc['total'])})

# ── EXAM ──────────────────────────────────────────────────────────────────────
@app.route('/exam')
@login_required
def exam():
    return render_template('exam.html')

@app.route('/api/exam/start', methods=['POST'])
@login_required
def exam_start():
    d = request.get_json()
    lang = d.get('lang','all')
    count = int(d.get('count', 20))
    exs = load_json(EXERCISES_FILE, [])
    if lang != 'all': exs = [e for e in exs if e['lang']==lang]
    import random; random.shuffle(exs)
    session['exam'] = {'items': [e['id'] for e in exs[:count]], 'lang':lang, 'count':count, 'started': datetime.now().isoformat()}
    return jsonify({'ok':True,'count':len(exs[:count])})

# ── ADMIN ─────────────────────────────────────────────────────────────────────
@app.route('/admin')
@admin_required
def admin():
    users = get_users()
    scores = get_scores()
    exs = load_json(EXERCISES_FILE, [])
    cards = load_json(FLASHCARDS_FILE, [])
    stats = {'users': len(users), 'exercises': len(exs), 'flashcards': len(cards),
             'total_attempts': sum(v.get('attempted',0) for v in scores.values())}
    user_list = []
    for uid, u in users.items():
        sc = scores.get(uid, {'total':0,'correct':0,'attempted':0})
        medal = get_medal(sc['total'])
        level = get_level(sc['total'])
        user_list.append({**u, 'score': sc['total'], 'medal': medal, 'level': level})
    user_list.sort(key=lambda x: -x['score'])
    return render_template('admin.html', stats=stats, users=user_list)

@app.route('/admin/user/<uid>/toggle_admin', methods=['POST'])
@admin_required
def toggle_admin(uid):
    users = get_users()
    if uid in users:
        users[uid]['is_admin'] = not users[uid].get('is_admin', False)
        save_users(users)
    return jsonify({'ok':True})

@app.route('/admin/user/<uid>/delete', methods=['POST'])
@admin_required
def delete_user(uid):
    users = get_users()
    if uid in users and uid != session['user_id']:
        del users[uid]
        save_users(users)
    return jsonify({'ok':True})

@app.route('/api/leaderboard')
def leaderboard():
    users = get_users()
    scores = get_scores()
    board = []
    for uid, sc in scores.items():
        u = users.get(uid, {})
        if not u: continue
        board.append({'username': u['username'], 'pts': sc['total'],
                      'medal': get_medal(sc['total']), 'level': get_level(sc['total']),
                      'correct': sc.get('correct',0), 'attempted': sc.get('attempted',0)})
    board.sort(key=lambda x: -x['pts'])
    return jsonify(board[:20])

if __name__ == '__main__':
    os.makedirs(DATA_DIR, exist_ok=True)
    app.run(debug=True, port=5000)

# Add enumerate filter for Jinja2
@app.template_filter('enumerate')
def jinja_enumerate(iterable, start=0):
    return enumerate(iterable, start=start)
