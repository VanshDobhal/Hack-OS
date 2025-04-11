import os
import json
import logging
from datetime import datetime
from flask import Flask, render_template, request, jsonify, session
from models import db, User, GameProgress, HighScore
import gemini_ai

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)

# Set the secret key
app.secret_key = os.environ.get("SESSION_SECRET", "default_secret_key_for_development")

# Configure database
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}
# Initialize database
db.init_app(app)

# Create all tables
with app.app_context():
    db.create_all()

# Import updated levels
from updated_levels import LEVELS

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/storyline')
def storyline():
    return render_template('storyline.html')

@app.route('/high-scores')
def high_scores_page():
    # Get overall top scores across all levels
    overall_scores = db.session.query(
        User.alias, 
        db.func.sum(HighScore.score).label('total_score'),
        db.func.count(HighScore.id).label('levels_completed')
    ).join(User).group_by(User.id).order_by(
        db.desc('total_score')
    ).limit(10).all()

    # Format for template
    formatted_scores = [
        {
            "alias": score[0],
            "score": score[1],
            "levels_completed": score[2]
        } for score in overall_scores
    ]

    # Get level-specific best times
    levels_data = []
    for level_id in range(1, 13):  # Assuming levels 1-12
        level_scores = HighScore.query.filter_by(level=level_id).order_by(
            HighScore.completion_time
        ).limit(3).all()

        if level_scores:
            level_data = {
                "level_id": level_id,
                "title": LEVELS[level_id]["title"],
                "scores": []
            }

            for score in level_scores:
                user = User.query.get(score.user_id)
                level_data["scores"].append({
                    "alias": user.alias if user else "Unknown",
                    "completion_time": score.completion_time,
                    "date": score.date_achieved.strftime("%Y-%m-%d %H:%M:%S")
                })

            levels_data.append(level_data)

    return render_template(
        'high_scores.html',
        overall_scores=formatted_scores,
        levels_data=levels_data
    )

@app.route('/game')
def game():
    # Initialize game state if not exists
    if 'alias' not in session:
        session['alias'] = request.args.get('alias', 'Hacker')

    if 'user_id' not in session:
        # Check if we have a user with this alias
        alias = session['alias']
        user = User.query.filter_by(alias=alias).first()

        if not user:
            # Create a new user with this alias
            user = User(username=f"user_{int(datetime.utcnow().timestamp())}", alias=alias)
            db.session.add(user)
            db.session.commit()

        # Create or get progress for this user
        progress = GameProgress.query.filter_by(user_id=user.id).first()
        if not progress:
            progress = GameProgress(user_id=user.id)
            db.session.add(progress)
            db.session.commit()

        # Store user and progress info in session
        session['user_id'] = user.id
        session['level'] = progress.current_level
        session['completed_levels'] = progress.get_completed_levels()
        session['current_directory'] = progress.current_directory

    # Return game page with user data
    return render_template(
        'game.html', 
        alias=session['alias'],
        current_level=session['level'],
        completed_levels=session['completed_levels']
    )

@app.route('/api/level/<int:level_id>')
def get_level(level_id):
    """Get details about a specific level, omitting solution information"""
    if level_id not in LEVELS:
        return jsonify({"error": "Level not found"}), 404

    # Create a copy of the level data without solution information
    level_data = {k: v for k, v in LEVELS[level_id].items() if k not in ['solution', 'solution_text']}

    return jsonify(level_data)

@app.route('/api/level/<int:level_id>/solution')
def get_level_with_solution(level_id):
    """Get details about a specific level, including solution information"""
    if level_id not in LEVELS:
        return jsonify({"error": "Level not found"}), 404

    # Return the complete level data including solution
    return jsonify(LEVELS[level_id])

@app.route('/api/command', methods=['POST'])
def execute_command():
    """Execute a command in the game's terminal"""
    data = request.json
    command = data.get('command', '').strip()
    current_level = data.get('level', 1)
    current_directory = data.get('directory', '/')

    logger.debug(f"Executing command: {command} for level {current_level} in directory {current_directory}")

    # Store the command in session for context
    if 'command_history' not in session:
        session['command_history'] = []

    # Add the command to history (limit to last 10 commands)
    command_history = session['command_history']
    command_history.append({
        "command": command,
        "timestamp": datetime.utcnow().isoformat(),
        "level": current_level,
        "directory": current_directory
    })
    session['command_history'] = command_history[-10:]  # Keep only the last 10 commands

    # Check if the command is valid for this level
    if current_level not in LEVELS:
        return jsonify({
            "output": "Error: Invalid level",
            "success": False
        })

    level_data = LEVELS[current_level]

    # Check if it's a simple dictionary lookup command
    simple_commands = {
        "help": "Available commands: help, ls, cd, cat, pwd, clear, hint, reset\nSpecialized commands for this level: " + ", ".join(level_data.get("commands", [])),
        "clear": "CLEAR_TERMINAL",
        "hint": "Use the hint button for assistance.",
        "pwd": f"Current directory: {current_directory}"
    }

    if command in simple_commands:
        return jsonify({
            "output": simple_commands[command],
            "success": True
        })

    # Split command into parts first
    command_parts = command.split()
    base_command = command_parts[0] if command_parts else ""

    # Initialize response
    response = {
        "output": "",
        "success": False,
        "level_complete": False,
        "update_directory": None
    }

    # Get level data and available commands
    level_data = LEVELS.get(current_level, {})
    available_commands = level_data.get("commands", [])

    # Special command handling for each level
    if current_level == 4 and base_command == "brute":
        # Brute force password attempt
        password_attempt = command_parts[1] if len(command_parts) > 1 else ""
        if password_attempt == "netron":
            response["success"] = True
            response["output"] = "Password correct! Access granted."
            response["level_complete"] = True
        else:
            response["output"] = f"Password '{password_attempt}' incorrect. Try another combination."
            response["success"] = True

    elif current_level == 5:
        if base_command == "analyze":
            response["output"] = level_data.get("analyze_result", "Log analysis complete. Line 4 is corrupted and needs repair.")
            response["success"] = True
        elif command == "nano corrupt.log":
            # Only completing all objectives should finish the level
            if "fixed_content" in level_data and level_data["fixed_content"] in data.get("file_content", ""):
                response["level_complete"] = True
                response["success"] = True
                response["output"] = "File fixed successfully!"

    elif current_level == 6:
        if base_command == "rules":
            response["output"] = level_data.get("rules_result", "Firewall rules:\nDENY ALL\nALLOW 22 (SSH)\nALLOW 443 (HTTPS)\nALLOW 8080 (Development) - WEAK CONFIGURATION\nDENY EXTERNAL")
            response["success"] = True
        elif base_command == "scan":
            response["output"] = level_data.get("scan_result", "Scanning...\nPorts found: 22, 80, 443, 8080\nPort 8080 appears vulnerable - development configuration detected.")
            response["success"] = True
        elif base_command == "probe":
            port = command_parts[1] if len(command_parts) > 1 else None
            if port == "8080":
                response["output"] = level_data.get("probe_result_8080", "Port 8080 is open and vulnerable. Misconfigured with admin permissions.")
                response["success"] = True
            else:
                response["output"] = f"Port {port} appears secure."
                response["success"] = True

    elif current_level == 7:
        current_files = level_data.get("files", {})
        path_parts = [p for p in current_directory.split("/") if p]
        current_location = current_files
        for part in path_parts:
            if part in current_location and current_location[part]["type"] == "directory":
                current_location = current_location[part].get("content", {})

        if base_command == "chmod":
            file_name = command_parts[2] if len(command_parts) > 2 else None
            if file_name and file_name in current_location:
                response["success"] = True
                response["output"] = f"Changed permissions for {file_name}"
            else:
                response["output"] = f"Error: File '{file_name}' not found."

    elif current_level == 8:
        if base_command == "reverse":
            hex_value = command_parts[1] if len(command_parts) > 1 else ""
            try:
                decoded = bytes.fromhex(hex_value).decode('utf-8')
                response["output"] = f"Decoded value: {decoded}"
                response["success"] = True
            except:
                response["output"] = "Invalid hex value provided."

    elif current_level == 9:
        if base_command == "overflow":
            input_string = command_parts[1] if len(command_parts) > 1 else ""
            if len(input_string) > 30:
                response["output"] = "System error: Buffer overflow detected.\nMemory protection bypass possible at address 0x7ffeab32\nVulnerable entry point identified."
                response["success"] = True
            else:
                response["output"] = "Input processed normally. No vulnerabilities detected."
                response["success"] = True
        elif base_command == "inject":
            if "0x7ffeab32" in command:
                response["success"] = True
                response["level_complete"] = True
                response["output"] = "Injection successful! Memory protection bypassed."

    # Handle common commands
    if base_command == "chmod" and len(command_parts) > 1:
        perm = command_parts[1]
        file_name = command_parts[2] if len(command_parts) > 2 else None

        if not file_name:
            response["output"] = "Usage: chmod [permissions] [filename]"
        else:
            # Find file in current directory
            current_files = level_data.get("files", {})
            if file_name in current_files and current_files[file_name]["type"] == "file":
                response["success"] = True
                response["output"] = f"Changed permissions for {file_name}"
            else:
                response["output"] = f"Error: File '{file_name}' not found."

    # Handle decrypt command
    elif base_command == "decrypt" and len(command_parts) > 1:
        file_name = command_parts[1]

        # Find the file in current directory
        current_files = level_data.get("files", {})
        path_parts = [p for p in current_directory.split("/") if p]

        # Navigate to current directory
        current_location = current_files
        for part in path_parts:
            if part in current_location and current_location[part]["type"] == "directory":
                current_location = current_location[part].get("content", {})
            else:
                current_location = {}
                break
        current_files = current_location

        # Check if file exists and decrypt
        if file_name in current_files and current_files[file_name]["type"] == "file":
            if "decrypted_message" in level_data:
                response["success"] = True
                response["output"] = f"File decrypted successfully. Output saved to {file_name.replace('.enc', '.txt')}"
            else:
                response["output"] = "This file cannot be decrypted."
        else:
            response["output"] = f"Error: File '{file_name}' not found."

    # Handle unrecognized commands
    elif base_command not in level_data.get("commands", []):
        response["output"] = f"Command '{command}' not recognized. Type 'help' for available commands."

    # Process common commands
    base_command = command_parts[0] if command_parts else ""

    # Check if this is a valid command for this level
    valid_commands = level_data.get("commands", [])

    if base_command == "ls":
        # Handle ls command to list files and directories in current directory
        response["success"] = True

        # Find the correct directory structure based on current_directory
        current_files = level_data.get("files", {})
        path_parts = [p for p in current_directory.split("/") if p]

        # Track current directory contents
        current_location = current_files
        for part in path_parts:
            if part in current_location and current_location[part]["type"] == "directory":
                current_location = current_location[part].get("content", {})
            else:
                current_location = {}
                break
        current_files = current_location

        # Build the output for ls command
        if current_files:
            file_list = []
            for name, info in current_files.items():
                if info["type"] == "directory":
                    file_list.append(f"<span class='directory'>{name}/</span>")
                else:
                    file_list.append(name)

            response["output"] = " ".join(file_list) if file_list else "No files found."
        else:
            response["output"] = "No files found."

    elif base_command == "cat" and len(command_parts) > 1:
        # Handle cat command to read file contents
        file_name = command_parts[1]

        # Find the file in the current directory
        current_files = level_data.get("files", {})
        path_parts = [p for p in current_directory.split("/") if p]

        # Navigate to the current directory in the file structure
        current_location = current_files
        for part in path_parts:
            if part in current_location and current_location[part]["type"] == "directory":
                current_location = current_location[part].get("content", {})
            else:
                current_location = {}
                break
        current_files = current_location

        # Check if the file exists and display its contents
        if file_name in current_files and current_files[file_name]["type"] == "file":
            response["success"] = True
            response["output"] = current_files[file_name].get("content", "Empty file.")
        else:
            response["output"] = f"Error: File '{file_name}' not found."

    # Check if this command completes the level
    if command in level_data.get("solution", []):
        # For simplicity, we're just checking if the command is in the solution list
        response["success"] = True
        if not response["output"] or response["output"] == f"Command '{command}' not recognized. Type 'help' for available commands.":
            response["output"] = f"Command executed successfully."

        # Check if this was the final command to complete the level
        if command == level_data["solution"][-1]:
            response["level_complete"] = True
            response["output"] = level_data.get("glitch_success", "Level complete!")

    # Update user's current directory if needed
    if base_command == "cd" and len(command_parts) > 1:
        # Extract the target directory
        target_dir = command_parts[1].strip()

        # Find the file structure for the current directory
        current_files = level_data.get("files", {})
        path_parts = [p for p in current_directory.split("/") if p]

        # Track current directory contents
        current_location = current_files
        for part in path_parts:
            if part in current_location and current_location[part]["type"] == "directory":
                current_location = current_location[part].get("content", {})
            else:
                current_location = {}
                break
        current_files = current_location

        if target_dir == "..":
            # Go up one directory
            if current_directory != "/":
                parent_dir = "/".join(current_directory.split("/")[:-1])
                response["update_directory"] = parent_dir if parent_dir else "/"
                response["success"] = True
                response["output"] = f"Changed directory to {response['update_directory']}"
            else:
                response["success"] = True
                response["output"] = "Already at root directory"
        else:
            # Check if the target directory exists in the current directory
            if target_dir in current_files and current_files[target_dir]["type"] == "directory":
                # Go to the subdirectory
                if current_directory == "/":
                    response["update_directory"] = f"/{target_dir}"
                else:
                    response["update_directory"] = f"{current_directory.rstrip('/')}/{target_dir}"
                response["success"] = True
                response["output"] = f"Changed directory to {response['update_directory']}"
            else:
                response["success"] = False
                response["output"] = f"Directory not found: {target_dir}"

    # Update user's directory in database if needed
    if response.get("update_directory"):
        update_user_directory(response["update_directory"])

    return jsonify(response)

@app.route('/api/complete_level', methods=['POST'])
def complete_level():
    """Mark a level as completed and update high score"""
    data = request.json
    level_id = int(data.get('level_id', 1)) #Fixed line
    completion_time = data.get('completion_time', 0)  # Time in seconds

    if 'user_id' not in session:
        return jsonify({"error": "User not logged in"}), 401

    # Get user and progress
    user_id = session['user_id']
    progress = GameProgress.query.filter_by(user_id=user_id).first()

    if not progress:
        return jsonify({"error": "User progress not found"}), 404

    # Mark level as completed
    completed_levels = progress.get_completed_levels()
    if level_id not in completed_levels:
        progress.add_completed_level(level_id)

        # Update current level if this was the current one
        if progress.current_level == level_id:
            progress.current_level = min(level_id + 1, len(LEVELS))

        # Update session
        session['level'] = progress.current_level
        session['completed_levels'] = progress.get_completed_levels()

        # Create or update high score
        score = 1000  # Base score
        time_penalty = min(completion_time, 300)  # Cap time penalty at 300 seconds
        final_score = max(score - time_penalty, 100)  # Ensure minimum score of 100

        existing_score = HighScore.query.filter_by(
            user_id=user_id, level=level_id
        ).first()

        if existing_score:
            # Update if better time
            if completion_time < existing_score.completion_time:
                existing_score.completion_time = completion_time
                existing_score.score = final_score
                existing_score.date_achieved = datetime.utcnow()
        else:
            # Create new score
            high_score = HighScore(
                user_id=user_id,
                level=level_id,
                score=final_score,
                completion_time=completion_time,
                date_achieved=datetime.utcnow()
            )
            db.session.add(high_score)

        db.session.commit()

    # Return next level data
    next_level = min(level_id + 1, len(LEVELS))
    next_level_data = None

    if next_level in LEVELS and next_level <= len(LEVELS):
        next_level_data = {
            "id": next_level,
            "title": LEVELS[next_level]["title"],
            "description": LEVELS[next_level]["description"]
        }

    return jsonify({
        "success": True,
        "next_level": next_level,
        "next_level_data": next_level_data,
        "game_completed": next_level > len(LEVELS)
    })

@app.route('/api/chat', methods=['POST'])
def chat_with_glitch():
    """Process a chat message to Glitch (the AI assistant) and get a response"""
    data = request.json
    message = data.get('message', '').strip()
    # Accept either 'level_id' or 'level' for backward compatibility
    level_id = data.get('level_id') or data.get('level', 1)

    if not message:
        return jsonify({"error": "Message is required"}), 400

    # Get the level data
    if level_id not in LEVELS:
        return jsonify({"error": "Invalid level ID"}), 400

    level_data = LEVELS[level_id]

    # Get alias if available
    alias = session.get('alias', 'Hacker')

    # Replace [alias] with the actual alias
    level_intro = level_data.get("glitch_intro", "").replace("[alias]", alias)

    # Get command history for context
    command_history = session.get('command_history', [])

    # Try to use Gemini AI for a response
    try:
        # Prepare context for Gemini
        context = {
            "user_message": message,
            "level_data": level_data,
            "current_level": level_id,
            "alias": alias,
            "command_history": command_history
        }

        # Generate response using Gemini
        ai_response = gemini_ai.generate_response(
            message, 
            context=context
        )

        # If successful, return the AI-generated response
        if ai_response:
            return jsonify({
                "response": ai_response,
                "level_intro": level_intro
            })

    except Exception as e:
        logger.error(f"Error using Gemini AI: {str(e)}")
        # Will fall back to static responses below

    # Fallback to static responses
    if "hint" in message.lower() or "help" in message.lower():
        response = level_data.get("glitch_hint", "I can't provide a hint right now.")
    elif "hello" in message.lower() or "hi" in message.lower():
        response = f"Hello, {alias}. Focus on the mission."
    else:
        # Default response
        response = f"I understand you're saying '{message}', but I need to stay focused on helping you with level {level_id}: {level_data['title']}."

    # Replace [alias] with the actual alias
    response = response.replace("[alias]", alias)

    return jsonify({
        "response": response,
        "level_intro": level_intro
    })

def update_user_directory(directory):
    """Update the user's current directory in the database"""
    if 'user_id' in session:
        user_id = session['user_id']
        progress = GameProgress.query.filter_by(user_id=user_id).first()

        if progress:
            progress.current_directory = directory
            db.session.commit()

            # Also update session
            session['current_directory'] = directory
            return True
    return False

@app.route('/api/update_directory', methods=['POST'])
def update_user_directory_endpoint():
    """Update the user's current directory in the database via API"""
    data = request.json
    directory = data.get('directory')

    if 'user_id' not in session:
        return jsonify({"error": "User not logged in"}), 401

    if not directory:
        return jsonify({"error": "No directory provided"}), 400

    success = update_user_directory(directory)

    if success:
        return jsonify({"success": True, "message": "Directory updated"})
    else:
        return jsonify({"error": "Failed to update directory"}), 500

def get_hint_for_level(level_id):
    """Generate a contextual hint for the current level using Gemini AI or fall back to static hints"""
    # Get the level data
    if level_id not in LEVELS:
        return "Invalid level ID"

    level_data = LEVELS[level_id]

    # Get user progress information
    user_progress = None
    if 'user_id' in session:
        user_id = session['user_id']
        user = User.query.get(user_id)
        progress = GameProgress.query.filter_by(user_id=user_id).first()

        if user and progress:
            user_progress = {
                "alias": user.alias,
                "current_level": progress.current_level,
                "completed_levels": progress.get_completed_levels(),
                "command_history": session.get('command_history', [])
            }

    # Try to use Gemini AI for the hint
    try:
        ai_hint = gemini_ai.generate_hint(level_data, user_progress)
        if ai_hint:
            return ai_hint
    except Exception as e:
        logger.error(f"Error generating AI hint: {str(e)}")

    # Fall back to static hint if AI fails
    static_hint = level_data.get("glitch_hint", "No hint available for this level.")

    # Replace [alias] with the actual alias if available
    if user_progress:
        static_hint = static_hint.replace("[alias]", user_progress.get("alias", "Hacker"))

    return static_hint

@app.route('/api/hint/<int:level_id>')
def get_hint(level_id):
    """API endpoint to get a hint for a specific level"""
    hint = get_hint_for_level(level_id)
    return jsonify({"hint": hint})

@app.route('/api/high-scores', methods=['GET'])
def get_high_scores():
    """Get high scores for all levels or a specific level"""
    level_id = request.args.get('level_id')

    if level_id:
        # Get scores for a specific level
        try:
            level_id = int(level_id)
            scores = HighScore.query.filter_by(level=level_id).order_by(
                HighScore.score.desc()
            ).limit(10).all()
        except ValueError:
            return jsonify({"error": "Invalid level ID"}), 400
    else:
        # Get overall top scores
        scores = db.session.query(
            User.alias, 
            db.func.sum(HighScore.score).label('total_score'),
            db.func.count(HighScore.id).label('levels_completed')
        ).join(User).group_by(User.id).order_by(
            db.desc('total_score')
        ).limit(10).all()

        formatted = [
            {
                "alias": s[0],
                "score": s[1],
                "levels_completed": s[2]
            } for s in scores
        ]

        return jsonify({"scores": formatted})

    # Format individual level scores
    formatted = []
    for score in scores:
        user = User.query.get(score.user_id)
        formatted.append({
            "alias": user.alias if user else "Unknown",
            "score": score.score,
            "completion_time": score.completion_time,
            "date": score.date_achieved.strftime("%Y-%m-%d %H:%M:%S")
        })

    return jsonify({"scores": formatted})

@app.route('/api/reset', methods=['POST'])
def reset_game():
    """Reset the game progress for the current user"""
    if 'user_id' not in session:
        return jsonify({"error": "User not logged in"}), 401

    user_id = session['user_id']

    # Reset progress
    progress = GameProgress.query.filter_by(user_id=user_id).first()
    if progress:
        progress.current_level = 1
        progress.completed_levels = ""
        progress.current_directory = "/"
        db.session.commit()

    # Reset session data
    session['level'] = 1
    session['completed_levels'] = []
    session['current_directory'] = "/"
    session['command_history'] = []

    return jsonify({"success": True})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)