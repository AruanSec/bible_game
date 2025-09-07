# blueprints/game.py
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
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
# blueprints/admin.py
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from werkzeug.security import check_password_hash

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