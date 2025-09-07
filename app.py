# app.py - Main Flask Application
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import random
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bible_quiz.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Models
class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.Text, nullable=False)
    option_a = db.Column(db.String(255), nullable=False)
    option_b = db.Column(db.String(255), nullable=False)
    option_c = db.Column(db.String(255), nullable=False)
    correct_answer = db.Column(db.String(1), nullable=False)  # 'A', 'B', or 'C'
    explanation = db.Column(db.Text)

class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)

# Blueprints
from blueprints.game import game_bp
from blueprints.admin import admin_bp

app.register_blueprint(game_bp, url_prefix='/')
app.register_blueprint(admin_bp, url_prefix='/admin')

@app.route('/')
def index():
    return render_template('index.html')

def create_sample_data():
    """Create sample questions and admin user"""
    if Question.query.count() == 0:
        sample_questions = [
            {
                'question': 'Who was the first man created by God?',
                'option_a': 'Moses',
                'option_b': 'Adam',
                'option_c': 'Noah',
                'correct_answer': 'B',
                'explanation': 'Adam was the first man created by God in the Garden of Eden (Genesis 2:7).'
            },
            {
                'question': 'How many days did it take God to create the world?',
                'option_a': '6 days',
                'option_b': '7 days',
                'option_c': '8 days',
                'correct_answer': 'A',
                'explanation': 'God created the world in 6 days and rested on the 7th (Genesis 1).'
            },
            {
                'question': 'Who built the ark?',
                'option_a': 'Moses',
                'option_b': 'Abraham',
                'option_c': 'Noah',
                'correct_answer': 'C',
                'explanation': 'Noah built the ark as commanded by God to save his family and animals (Genesis 6-9).'
            },
            {
                'question': 'What did Jesus turn water into?',
                'option_a': 'Wine',
                'option_b': 'Oil',
                'option_c': 'Milk',
                'correct_answer': 'A',
                'explanation': 'Jesus turned water into wine at the wedding in Cana (John 2:1-11).'
            },
            {
                'question': 'How many apostles did Jesus have?',
                'option_a': '10',
                'option_b': '11',
                'option_c': '12',
                'correct_answer': 'C',
                'explanation': 'Jesus chose 12 apostles to be his closest disciples.'
            },
            {
                'question': 'Who betrayed Jesus?',
                'option_a': 'Peter',
                'option_b': 'Judas Iscariot',
                'option_c': 'Thomas',
                'correct_answer': 'B',
                'explanation': 'Judas Iscariot betrayed Jesus for 30 pieces of silver.'
            },
            {
                'question': 'What is the first book of the Bible?',
                'option_a': 'Exodus',
                'option_b': 'Genesis',
                'option_c': 'Leviticus',
                'correct_answer': 'B',
                'explanation': 'Genesis is the first book of the Bible, meaning "beginning".'
            },
            {
                'question': 'Who led the Israelites out of Egypt?',
                'option_a': 'Moses',
                'option_b': 'Aaron',
                'option_c': 'Joshua',
                'correct_answer': 'A',
                'explanation': 'Moses led the Israelites out of slavery in Egypt through the Red Sea.'
            },
            {
                'question': 'How many plagues did God send on Egypt?',
                'option_a': '8',
                'option_b': '9',
                'option_c': '10',
                'correct_answer': 'C',
                'explanation': 'God sent 10 plagues on Egypt before Pharaoh let the Israelites go.'
            },
            {
                'question': 'Who was swallowed by a great fish?',
                'option_a': 'Jonah',
                'option_b': 'Daniel',
                'option_c': 'Elijah',
                'correct_answer': 'A',
                'explanation': 'Jonah was swallowed by a great fish for three days and nights.'
            },
            {
                'question': 'What did David use to defeat Goliath?',
                'option_a': 'Sword',
                'option_b': 'Sling and stone',
                'option_c': 'Spear',
                'correct_answer': 'B',
                'explanation': 'David used a sling and stone to defeat the giant Goliath.'
            },
            {
                'question': 'Who was the strongest man in the Bible?',
                'option_a': 'Samson',
                'option_b': 'David',
                'option_c': 'Solomon',
                'correct_answer': 'A',
                'explanation': 'Samson was blessed with supernatural strength by God.'
            },
            {
                'question': 'What did Jesus multiply to feed 5000 people?',
                'option_a': 'Bread and wine',
                'option_b': 'Loaves and fishes',
                'option_c': 'Fruits and vegetables',
                'correct_answer': 'B',
                'explanation': 'Jesus multiplied 5 loaves and 2 fishes to feed 5000 people.'
            },
            {
                'question': 'On which mountain did Moses receive the Ten Commandments?',
                'option_a': 'Mount Ararat',
                'option_b': 'Mount Sinai',
                'option_c': 'Mount Olive',
                'correct_answer': 'B',
                'explanation': 'Moses received the Ten Commandments on Mount Sinai.'
            },
            {
                'question': 'Who was the wisest king of Israel?',
                'option_a': 'David',
                'option_b': 'Saul',
                'option_c': 'Solomon',
                'correct_answer': 'C',
                'explanation': 'Solomon was known for his great wisdom given by God.'
            },
            {
                'question': 'What happened to Lot\'s wife when she looked back?',
                'option_a': 'She disappeared',
                'option_b': 'She turned to salt',
                'option_c': 'She was struck blind',
                'correct_answer': 'B',
                'explanation': 'Lot\'s wife turned into a pillar of salt when she looked back at Sodom.'
            },
            {
                'question': 'How many books are in the New Testament?',
                'option_a': '25',
                'option_b': '26',
                'option_c': '27',
                'correct_answer': 'C',
                'explanation': 'The New Testament contains 27 books.'
            },
            {
                'question': 'Who baptized Jesus?',
                'option_a': 'John the Baptist',
                'option_b': 'Peter',
                'option_c': 'Paul',
                'correct_answer': 'A',
                'explanation': 'John the Baptist baptized Jesus in the Jordan River.'
            },
            {
                'question': 'What was the name of the garden where Adam and Eve lived?',
                'option_a': 'Garden of Gethsemane',
                'option_b': 'Garden of Eden',
                'option_c': 'Garden of Olives',
                'correct_answer': 'B',
                'explanation': 'Adam and Eve lived in the Garden of Eden before the fall.'
            },
            {
                'question': 'How many days and nights did Jesus fast in the wilderness?',
                'option_a': '30',
                'option_b': '40',
                'option_c': '50',
                'correct_answer': 'B',
                'explanation': 'Jesus fasted for 40 days and nights in the wilderness.'
            },
            {
                'question': 'Who denied Jesus three times?',
                'option_a': 'John',
                'option_b': 'Peter',
                'option_c': 'Thomas',
                'correct_answer': 'B',
                'explanation': 'Peter denied knowing Jesus three times before the rooster crowed.'
            },
            {
                'question': 'What language was most of the New Testament originally written in?',
                'option_a': 'Hebrew',
                'option_b': 'Aramaic',
                'option_c': 'Greek',
                'correct_answer': 'C',
                'explanation': 'Most of the New Testament was originally written in Greek.'
            },
            {
                'question': 'Who was the mother of Jesus?',
                'option_a': 'Martha',
                'option_b': 'Mary',
                'option_c': 'Elizabeth',
                'correct_answer': 'B',
                'explanation': 'Mary was chosen by God to be the mother of Jesus.'
            },
            {
                'question': 'What city was Jesus born in?',
                'option_a': 'Nazareth',
                'option_b': 'Jerusalem',
                'option_c': 'Bethlehem',
                'correct_answer': 'C',
                'explanation': 'Jesus was born in Bethlehem, the city of David.'
            },
            {
                'question': 'Who wrote most of the letters in the New Testament?',
                'option_a': 'Peter',
                'option_b': 'Paul',
                'option_c': 'John',
                'correct_answer': 'B',
                'explanation': 'Paul wrote 13 of the 27 books in the New Testament.'
            }
        ]
        
        for q_data in sample_questions:
            question = Question(**q_data)
            db.session.add(question)
    
    # Create default admin user
    if Admin.query.count() == 0:
        admin = Admin(
            username='admin',
            password_hash=generate_password_hash('admin123')
        )
        db.session.add(admin)
    
    db.session.commit()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        create_sample_data()
    app.run(debug=True)

# ============================================================================
# blueprints/game.py - Game Blueprint
from flask import Blueprint, render_template, request, redirect, url_for, session, flash, jsonify
import random

game_bp = Blueprint('game', __name__)

@game_bp.route('/setup')
def setup():
    return render_template('setup.html')

@game_bp.route('/start_game', methods=['POST'])
def start_game():
    from app import Question, db
    
    num_players = int(request.form['num_players'])
    players = []
    
    for i in range(num_players):
        first_name = request.form[f'player_{i+1}_first']
        last_name = request.form[f'player_{i+1}_last']
        if first_name and last_name:
            players.append({
                'id': i + 1,
                'first_name': first_name,
                'last_name': last_name,
                'score': 0
            })
    
    if len(players) < num_players:
        flash('Please fill in all player names')
        return redirect(url_for('game.setup'))
    
    # Get random 20 questions
    all_questions = Question.query.all()
    if len(all_questions) < 20:
        flash('Not enough questions in database. Need at least 20 questions.')
        return redirect(url_for('game.setup'))
    
    selected_questions = random.sample(all_questions, 20)
    question_ids = [q.id for q in selected_questions]
    
    # Store game data in session
    session['game_active'] = True
    session['players'] = players
    session['question_ids'] = question_ids
    session['current_question'] = 0
    session['current_player'] = 0
    
    return redirect(url_for('game.play'))

@game_bp.route('/play')
def play():
    from app import Question
    
    if not session.get('game_active'):
        return redirect(url_for('index'))
    
    current_q_index = session['current_question']
    current_player_index = session['current_player']
    
    if current_q_index >= 20:
        return redirect(url_for('game.results'))
    
    question_id = session['question_ids'][current_q_index]
    question = Question.query.get(question_id)
    current_player = session['players'][current_player_index]
    
    progress = ((current_q_index) / 20) * 100
    
    return render_template('play.html', 
                         question=question, 
                         current_player=current_player,
                         players=session['players'],
                         question_number=current_q_index + 1,
                         total_questions=20,
                         progress=progress)

@game_bp.route('/answer', methods=['POST'])
def answer():
    from app import Question
    
    if not session.get('game_active'):
        return redirect(url_for('index'))
    
    selected_answer = request.form['answer']
    current_q_index = session['current_question']
    current_player_index = session['current_player']
    
    question_id = session['question_ids'][current_q_index]
    question = Question.query.get(question_id)
    
    is_correct = selected_answer == question.correct_answer
    
    if is_correct:
        session['players'][current_player_index]['score'] += 1
    
    # Move to next player
    session['current_player'] = (current_player_index + 1) % len(session['players'])
    
    # If we've gone through all players for this question, move to next question
    if session['current_player'] == 0:
        session['current_question'] += 1
    
    return render_template('answer_result.html',
                         question=question,
                         selected_answer=selected_answer,
                         is_correct=is_correct,
                         current_player=session['players'][current_player_index],
                         players=session['players'])

@game_bp.route('/next_question')
def next_question():
    if not session.get('game_active'):
        return redirect(url_for('index'))
    
    return redirect(url_for('game.play'))

@game_bp.route('/results')
def results():
    if not session.get('game_active'):
        return redirect(url_for('index'))
    
    players = session['players']
    # Sort players by score (descending)
    players.sort(key=lambda x: x['score'], reverse=True)
    
    # Clear session
    session.pop('game_active', None)
    session.pop('players', None)
    session.pop('question_ids', None)
    session.pop('current_question', None)
    session.pop('current_player', None)
    
    return render_template('results.html', players=players)

# ============================================================================
# blueprints/admin.py - Admin Blueprint
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from werkzeug.security import check_password_hash, generate_password_hash

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    from app import Admin
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        admin = Admin.query.filter_by(username=username).first()
        
        if admin and check_password_hash(admin.password_hash, password):
            session['admin_logged_in'] = True
            session['admin_id'] = admin.id
            flash('Login successful!')
            return redirect(url_for('admin.dashboard'))
        else:
            flash('Invalid username or password')
    
    return render_template('admin/login.html')

@admin_bp.route('/logout')
def logout():
    session.pop('admin_logged_in', None)
    session.pop('admin_id', None)
    flash('Logged out successfully')
    return redirect(url_for('admin.login'))

@admin_bp.route('/dashboard')
def dashboard():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin.login'))
    
    from app import Question, db
    questions = Question.query.all()
    return render_template('admin/dashboard.html', questions=questions)

@admin_bp.route('/add_question', methods=['GET', 'POST'])
def add_question():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin.login'))
    
    from app import Question, db
    
    if request.method == 'POST':
        question = Question(
            question=request.form['question'],
            option_a=request.form['option_a'],
            option_b=request.form['option_b'],
            option_c=request.form['option_c'],
            correct_answer=request.form['correct_answer'],
            explanation=request.form['explanation']
        )
        db.session.add(question)
        db.session.commit()
        flash('Question added successfully!')
        return redirect(url_for('admin.dashboard'))
    
    return render_template('admin/add_question.html')

@admin_bp.route('/edit_question/<int:id>', methods=['GET', 'POST'])
def edit_question(id):
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin.login'))
    
    from app import Question, db
    
    question = Question.query.get_or_404(id)
    
    if request.method == 'POST':
        question.question = request.form['question']
        question.option_a = request.form['option_a']
        question.option_b = request.form['option_b']
        question.option_c = request.form['option_c']
        question.correct_answer = request.form['correct_answer']
        question.explanation = request.form['explanation']
        db.session.commit()
        flash('Question updated successfully!')
        return redirect(url_for('admin.dashboard'))
    
    return render_template('admin/edit_question.html', question=question)

@admin_bp.route('/delete_question/<int:id>')
def delete_question(id):
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin.login'))
    
    from app import Question, db
    
    question = Question.query.get_or_404(id)
    db.session.delete(question)
    db.session.commit()
    flash('Question deleted successfully!')
    return redirect(url_for('admin.dashboard'))

# ============================================================================
# Create the directory structure and required files
import os

# Create directories
os.makedirs('blueprints', exist_ok=True)
os.makedirs('templates', exist_ok=True)
os.makedirs('templates/admin', exist_ok=True)
os.makedirs('static/css', exist_ok=True)

# Create __init__.py files
with open('blueprints/__init__.py', 'w') as f:
    f.write('')

print("Flask Bible Quiz Game created successfully!")
print("\nTo run the application:")
print("1. Make sure you have Flask and Flask-SQLAlchemy installed:")
print("   pip install Flask Flask-SQLAlchemy")
print("2. Run the application:")
print("   python app.py")
print("3. Access the game at http://localhost:5000")
print("4. Admin login: username='admin', password='admin123'")
print("5. Admin dashboard: http://localhost:5000/admin/dashboard")