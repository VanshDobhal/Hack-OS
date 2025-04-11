// Main JavaScript file for the game

document.addEventListener('DOMContentLoaded', function() {
    const gameContainer = document.getElementById('gameContainer');
    const bootAnimation = document.getElementById('bootAnimation');
    
    // Show boot animation and then reveal game
    showBootAnimation().then(() => {
        bootAnimation.style.display = 'none';
        gameContainer.style.display = 'flex';
        
        // Initialize the game components
        initializeTerminal();
        initializeGlitch();
        loadCurrentLevel();
        
        // Set up modals
        setupModals();
    });
    
    // Register event listeners
    document.getElementById('helpButton').addEventListener('click', () => {
        new bootstrap.Modal(document.getElementById('helpModal')).show();
    });
    
    document.getElementById('settingsButton').addEventListener('click', () => {
        new bootstrap.Modal(document.getElementById('settingsModal')).show();
    });
    
    document.getElementById('resetGameButton').addEventListener('click', () => {
        resetGame();
    });
    
    // Add event listener for the hint button
    document.getElementById('getHintButton').addEventListener('click', () => {
        getHint();
        // Open the chat modal to show the hint
        new bootstrap.Modal(document.getElementById('glitchChatModal')).show();
    });

    // Add event listener for skip storyline button if it exists
    const skipStorylineButton = document.getElementById('skipStorylineButton');
    if (skipStorylineButton) {
        skipStorylineButton.addEventListener('click', () => {
            // Navigate directly to the game page
            window.location.href = '/game';
        });
    }
});

/**
 * Gets a hint for the current level and displays it via Glitch
 */
function getHint() {
    // Get the current level
    const levelId = document.getElementById('currentLevel').textContent;
    
    // Call the backend to get the hint for this level
    fetch(`/api/hint/${levelId}`)
        .then(response => response.json())
        .then(data => {
            // Add the hint to Glitch's message queue
            addGlitchMessage(data.hint);
        })
        .catch(error => {
            console.error('Error fetching hint:', error);
            addGlitchMessage("I'm having trouble generating a hint right now. Try again?");
        });
}

/**
 * Shows the solution for the current level
 */
function showSolution() {
    // Get the current level
    const levelId = document.getElementById('currentLevel').textContent;
    
    // Call the backend to get the solution for this level
    fetch(`/api/level/${levelId}/solution`)
        .then(response => response.json())
        .then(data => {
            if (data.solution_text) {
                addGlitchMessage(data.solution_text);
            } else {
                addGlitchMessage("I don't have the solution for this level yet. Keep trying!");
            }
        })
        .catch(error => {
            console.error('Error fetching solution:', error);
            addGlitchMessage("Sorry, I couldn't retrieve the solution right now. Try again later.");
        });
}

// Add event listener for the solution button
document.addEventListener('DOMContentLoaded', function() {
    const showSolutionButton = document.getElementById('showSolutionButton');
    if (showSolutionButton) {
        showSolutionButton.addEventListener('click', () => {
            showSolution();
            // Open the chat modal to show the solution
            new bootstrap.Modal(document.getElementById('glitchChatModal')).show();
        });
    }
});

/**
 * Shows the boot animation in sequence
 * @returns {Promise} - Resolves when boot animation is complete
 */
function showBootAnimation() {
    return new Promise((resolve) => {
        const bootLines = document.querySelectorAll('.boot-line');
        const bootAnimation = document.getElementById('bootAnimation');
        
        bootAnimation.style.display = 'flex';
        
        // Reveal each line with a delay
        bootLines.forEach((line, index) => {
            setTimeout(() => {
                line.classList.add('visible');
                
                // If this is the last line, wait and then resolve
                if (index === bootLines.length - 1) {
                    setTimeout(resolve, 1500);
                }
            }, index * 800);
        });
    });
}

/**
 * Loads current level data
 */
function loadCurrentLevel() {
    const currentLevel = document.getElementById('currentLevel').textContent;
    
    // Initialize level start time
    window.levelStartTime = new Date().getTime();
    
    // Get level details
    fetch(`/api/level/${currentLevel}`)
        .then(response => response.json())
        .then(data => {
            // Update level title and description
            const levelTitle = document.getElementById('levelTitle');
            levelTitle.textContent = `Level ${currentLevel}: ${data.title}`;
            levelTitle.dataset.levelId = currentLevel; // Store level ID here
            
            document.getElementById('levelDescription').textContent = data.description;
            document.getElementById('levelGoal').textContent = data.goal;
            
            // Update objectives if they exist
            const objectivesList = document.getElementById('levelObjectives');
            if (objectivesList) {
                // Clear existing objectives
                objectivesList.innerHTML = '';
                
                // Add default objective if no objectives array exists
                if (!data.objectives || !Array.isArray(data.objectives)) {
                    const li = document.createElement('li');
                    li.textContent = data.goal || 'Complete the level objective';
                    objectivesList.appendChild(li);
                } else {
                    // Add each objective from the array
                    data.objectives.forEach(objective => {
                        const li = document.createElement('li');
                        li.textContent = objective;
                        objectivesList.appendChild(li);
                    });
                }
            }
            
            // Initialize level start time for scoring
            window.levelStartTime = new Date().getTime();
            
            // Set terminal directory if needed
            const savedDirectory = data.starting_directory || '/';
            updateTerminalPrompt(savedDirectory);
        })
        .catch(error => {
            console.error('Error loading level data:', error);
        });
}

/**
 * Sets up modal behaviors
 */
function setupModals() {
    // Level complete modal behavior
    const levelCompleteModal = document.getElementById('levelCompleteModal');
    if (levelCompleteModal) {
        const modal = new bootstrap.Modal(levelCompleteModal);
        
        // Next level button
        const nextLevelButton = document.getElementById('nextLevelButton');
        if (nextLevelButton) {
            nextLevelButton.addEventListener('click', () => {
                modal.hide();
                location.reload(); // Refresh to load new level
            });
        }
    }
    
    // Game ending modal (for final level)
    const gameEndingModal = document.getElementById('gameEndingModal');
    if (gameEndingModal) {
        const endingModal = new bootstrap.Modal(gameEndingModal);
        
        // Return to home button
        const returnHomeButton = document.getElementById('returnHomeButton');
        if (returnHomeButton) {
            returnHomeButton.addEventListener('click', () => {
                endingModal.hide();
                window.location.href = '/'; // Go to home page
            });
        }
    }
}

/**
 * Resets the game progress
 */
function resetGame() {
    if (confirm('Are you sure you want to reset your game progress? This will erase all your completed levels and start from level 1.')) {
        fetch('/api/reset', {
            method: 'POST'
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert('Game progress has been reset. The page will now reload.');
                location.reload();
            } else {
                alert('Failed to reset game progress. Please try again.');
            }
        })
        .catch(error => {
            console.error('Error resetting game:', error);
            alert('An error occurred while resetting the game. Please try again.');
        });
    }
}

/**
 * Complete the current level
 * Fetches the level details, calculates time, and shows completion modal
 */
function completeLevel() {
    // Record current time for completion time calculation
    const endTime = new Date().getTime();
    const startTime = window.levelStartTime || endTime; // Fallback to prevent NaN if start time wasn't set
    const completionTimeSeconds = Math.floor((endTime - startTime) / 1000);
    
    // Format completion time
    const minutes = Math.floor(completionTimeSeconds / 60);
    const seconds = completionTimeSeconds % 60;
    const formattedTime = `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
    
    // Update modal with completion time
    document.getElementById('levelCompletionTime').textContent = formattedTime;
    
    // Get the current level ID to mark it as completed
    const levelTitle = document.getElementById('levelTitle');
    const currentLevelId = parseInt(levelTitle.dataset.levelId || document.getElementById('currentLevel').textContent);
    
    // Send completion to server
    fetch('/api/complete_level', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            level_id: currentLevelId,
            completion_time: completionTimeSeconds
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Show level complete modal
            const levelCompleteModal = new bootstrap.Modal(document.getElementById('levelCompleteModal'));
            levelCompleteModal.show();
            
            // If this was the final level, show the game ending modal instead
            if (data.game_completed) {
                const gameEndingModal = new bootstrap.Modal(document.getElementById('gameEndingModal'));
                gameEndingModal.show();
            } else if (data.next_level_data) {
                // Show level complete modal
                const levelCompleteModal = new bootstrap.Modal(document.getElementById('levelCompleteModal'));
                levelCompleteModal.show();
            }
        } else {
            console.error('Failed to complete level');
        }
    })
    .catch(error => {
        console.error('Error completing level:', error);
    });
}
