# Bible Quiz Game Requirements
1. Ask how many players will be playing the game
2. The scoreboard should be based on the number of players
3. The questions will be stored in SQLite database
4. There will be 3 questions per options, when the player choses the wrong question the answer should be shown to the player.
5. The questions will be randomized for the number of players
6. There will be twenty questions for each game.
7. Player will only provide their first and lastname to be able to access the dashboard, no need for login.
8. There will be a login requirement for the admin route so the admin can manage the tables in the SQLite Database
9. This game logic will be coded using Flask Python module
10. I need a stylish UI for the game using CSS.
11. All views will inherit from base.html template.
12. Use Blueprint Python Module
13. Score board should be shown as the game progresses.
14. Progress bar should be shown letting the user know how many questions have been done and how many is left. 
# ============================================================================
# requirements.txt
Flask==2.3.3
Flask-SQLAlchemy==3.0.5
Werkzeug==2.3.7

# ============================================================================
# README.md
# Bible Quiz Game

A comprehensive Flask-based Bible quiz game with multiplayer support, admin management, and a modern UI.

## Features

✅ **All Requirements Implemented:**

1. **Multiple Players**: Ask for number of players and create scoreboard
2. **Dynamic Scoreboard**: Updates based on number of players
3. **SQLite Database**: Questions stored in database with full CRUD operations
4. **Three Options Per Question**: A, B, C format with explanations
5. **Randomized Questions**: 20 random questions per game
6. **Player Management**: First and last name input
7. **Admin Authentication**: Secure login for database management
8. **Flask Framework**: Built with Flask and Blueprints
9. **Modern UI**: Stylish CSS with responsive design
10. **Template Inheritance**: All views extend base.html
11. **Blueprint Architecture**: Organized code structure
12. **Live Scoreboard**: Updates during gameplay
13. **Progress Tracking**: Visual progress bar

## Additional Features

- **Responsive Design**: Works on desktop and mobile
- **Animations**: Smooth transitions and hover effects
- **Flash Messages**: User feedback system
- **Error Handling**: Comprehensive error management
- **Sample Data**: Pre-loaded with 25 Bible questions

## Installation & Setup

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Application**:
   ```bash
   python app.py
   ```

3. **Access the Game**:
   - Main Game: http://localhost:5000
   - Admin Panel: http://localhost:5000/admin/login

## Default Admin Credentials

- **Username**: admin
- **Password**: admin123

## File Structure

```
bible_quiz_game/
├── app.py                 # Main Flask application
├── requirements.txt       # Dependencies
├── blueprints/
│   ├── __init__.py
│   ├── game.py           # Game routes
│   └── admin.py          # Admin routes
├── templates/
│   ├── base.html         # Base template
│   ├── index.html        # Home page
│   ├── setup.html        # Game setup
│   ├── play.html         # Gameplay
│   ├── answer_result.html # Answer feedback
│   ├── results.html      # Final results
│   └── admin/
│       ├── login.html    # Admin login
│       ├── dashboard.html # Admin dashboard
│       ├── add_question.html
│       └── edit_question.html
├── static/
│   └── css/
│       └── style.css     # Comprehensive styles
└── bible_quiz.db         # SQLite database (created on first run)
```

## How to Play

1. **Start Game**: Click "Start New Game" on homepage
2. **Setup Players**: Select number of players (1-6) and enter names
3. **Play**: Each player answers 20 randomized questions
4. **View Results**: See final scores and rankings
5. **Play Again**: Start a new game anytime

## Admin Features

- **Question Management**: Add, edit, delete questions
- **Database Overview**: View total questions
- **Secure Access**: Login-protected admin area
- **Bulk Operations**: Manage multiple questions efficiently

## Technical Details

- **Framework**: Flask 2.3.3
- **Database**: SQLite with SQLAlchemy ORM
- **Architecture**: Blueprint-based modular design
- **Frontend**: Modern CSS with animations
- **Session Management**: Secure game state handling
- **Security**: Password hashing with Werkzeug

## Game Flow

1. **Home** → **Setup** → **Play** → **Answer** → **Results**
2. **Admin**: Login → Dashboard → Manage Questions
3. **Multiplayer**: Rotates through players for each question
4. **Scoring**: Real-time updates with final leaderboard

## Customization

- Add more questions via admin panel
- Modify game length (currently 20 questions)
- Customize styling in `static/css/style.css`
- Add new features via blueprints

Enjoy testing your Bible knowledge! 📖✨
