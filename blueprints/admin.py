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
