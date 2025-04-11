import os
import google.generativeai as genai
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configure the Gemini API
API_KEY = os.environ.get("GEMINI_API_KEY")

if not API_KEY:
    logger.warning("GEMINI_API_KEY not found in environment variables. AI functionality will not work properly.")
else:
    genai.configure(api_key=API_KEY)

def generate_response(prompt, context=None, model="gemini-1.5-pro"):
    """
    Generate a response using the Gemini AI model
    
    Args:
        prompt (str): The prompt to send to Gemini
        context (dict, optional): Context information about the current game state
        model (str, optional): The model to use (default: gemini-1.5-pro)
        
    Returns:
        str: The generated response, or an error message if generation fails
    """
    if not API_KEY:
        return "I'm experiencing technical difficulties. Try using the hint or solution buttons instead."
    
    try:
        # Create a more detailed system prompt with the context
        system_prompt = create_system_prompt(context)
        
        # Create the full prompt
        full_prompt = f"{system_prompt}\n\nUser: {prompt}"
        
        # Generate response
        model = genai.GenerativeModel(model)
        response = model.generate_content(full_prompt)
        
        # Return the response text
        return response.text
    
    except Exception as e:
        logger.error(f"Error generating response: {e}")
        return "I'm experiencing technical difficulties. Try using the hint or solution buttons instead."

def create_system_prompt(context):
    """
    Create a system prompt with the provided context
    
    Args:
        context (dict): Context information about the current game state
        
    Returns:
        str: The system prompt
    """
    # Default system prompt
    system_prompt = "You are Glitch, a rogue AI assistant helping a hacker navigate through a cybersecurity challenge. Be concise, helpful, and stay in character. Provide useful technical advice without giving away complete solutions."
    
    # Add context if available
    if context:
        current_level = context.get("level", 1)
        level_data = context.get("level_data", {})
        user_alias = context.get("user_alias", "Hacker")
        
        # Add level-specific context
        if level_data:
            level_title = level_data.get("title", "Unknown Level")
            level_goal = level_data.get("goal", "Unknown Goal")
            level_commands = level_data.get("commands", [])
            
            system_prompt += f"\n\nCurrent state:" 
            system_prompt += f"\n- The user (alias: {user_alias}) is on Level {current_level}: {level_title}"
            system_prompt += f"\n- The goal is to: {level_goal}"
            system_prompt += f"\n- Available commands: {', '.join(level_commands)}"
            
            # Add previous user actions if available
            user_actions = context.get("user_actions", [])
            if user_actions:
                system_prompt += f"\n\nRecent user actions: {', '.join(user_actions[-3:])}"
    
    return system_prompt

def generate_hint(level_data, user_progress=None):
    """
    Generate a contextual hint for the current level
    
    Args:
        level_data (dict): Data for the current level
        user_progress (dict, optional): Information about the user's progress
        
    Returns:
        str: A generated hint
    """
    if not API_KEY:
        # Fallback to static hints if no API key
        return level_data.get("glitch_hint", "I don't have a specific hint for this level yet.")
    
    try:
        level_number = level_data.get("level_number", 1)
        level_title = level_data.get("title", "Unknown Level")
        level_goal = level_data.get("goal", "Unknown Goal")
        level_commands = level_data.get("commands", [])
        
        # Create hint prompt
        hint_prompt = f"""
        Generate a helpful hint for Level {level_number}: {level_title}.
        
        Level goal: {level_goal}
        Available commands: {', '.join(level_commands)}
        
        The hint should:
        1. Not reveal the complete solution
        2. Guide the user in the right direction
        3. Be concise (max 1-2 sentences)
        4. Be in character as Glitch, a rogue AI helping the user
        """
        
        # Add user progress context if available
        if user_progress:
            attempted_commands = user_progress.get("attempted_commands", [])
            if attempted_commands:
                hint_prompt += f"\n\nUser has already tried: {', '.join(attempted_commands[-3:])}"
        
        # Generate the hint
        model = genai.GenerativeModel("gemini-1.5-pro")
        response = model.generate_content(hint_prompt)
        
        return response.text.strip()
    
    except Exception as e:
        logger.error(f"Error generating hint: {e}")
        # Fallback to static hint
        return level_data.get("glitch_hint", "I don't have a specific hint for this level yet.")