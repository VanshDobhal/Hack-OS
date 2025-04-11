/**
 * Initializes the terminal and its event listeners
 */
function initializeTerminal() {
    const terminalInput = document.getElementById('terminalInput');
    const terminalForm = document.getElementById('terminalForm');
    
    // Set up form submit handler
    terminalForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const command = terminalInput.value.trim();
        if (command) {
            // Process the command
            processCommand(command);
            
            // Clear the input
            terminalInput.value = '';
            
            // Add to history
            commandHistory.push(command);
            historyIndex = commandHistory.length;
        }
    });
    
    // Set up keyboard event for terminal input (for history navigation)
    terminalInput.addEventListener('keydown', function(e) {
        if (e.key === 'ArrowUp') {
            // Navigate up in history
            navigateHistory(1);
            e.preventDefault();
        } else if (e.key === 'ArrowDown') {
            // Navigate down in history
            navigateHistory(-1);
            e.preventDefault();
        }
    });
    
    // Focus the terminal input when the terminal is clicked
    document.querySelector('.terminal').addEventListener('click', function() {
        terminalInput.focus();
    });
    
    // Update the terminal prompt with the user's alias
    updateTerminalPrompt(getCurrentDirectory());
}

// Command history array and index for navigation
const commandHistory = [];
let historyIndex = 0;

/**
 * Navigate through command history
 * @param {number} direction - Direction to navigate (1 for up, -1 for down)
 */
function navigateHistory(direction) {
    const terminalInput = document.getElementById('terminalInput');
    
    if (direction === 1) {
        // Up arrow - go back in history
        if (historyIndex > 0) {
            historyIndex--;
            terminalInput.value = commandHistory[historyIndex];
        }
    } else {
        // Down arrow - go forward in history
        if (historyIndex < commandHistory.length - 1) {
            historyIndex++;
            terminalInput.value = commandHistory[historyIndex];
        } else if (historyIndex === commandHistory.length - 1) {
            // At the end of history, clear the input
            historyIndex = commandHistory.length;
            terminalInput.value = '';
        }
    }
    
    // Put cursor at the end of the input
    setTimeout(() => {
        terminalInput.selectionStart = terminalInput.selectionEnd = terminalInput.value.length;
    }, 0);
}

/**
 * Process a command entered in the terminal
 * @param {string} command - The command to process
 */
function processCommand(command) {
    // Get user alias safely
    let userAlias = "user";
    try {
        const aliasElement = document.querySelector('.mission-info div:nth-child(2) span');
        if (aliasElement && aliasElement.textContent) {
            userAlias = aliasElement.textContent.trim();
        }
    } catch (error) {
        console.error("Could not find user alias:", error);
    }
    
    // Add the command to the terminal output
    addToTerminal(`<span class="terminal-prompt">${userAlias}@hackos:${getCurrentDirectory()}$ </span>${command}`);
    
    // If command is clear, just clear the terminal
    if (command.toLowerCase() === 'clear') {
        clearTerminal();
        return;
    }
    
    // Send the command to the server for processing
    fetch('/api/command', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            command: command,
            level: parseInt(document.getElementById('currentLevel').textContent),
            directory: getCurrentDirectory() // Get the current directory
        })
    })
    .then(response => response.json())
    .then(data => {
        // Handle special response for clear command
        if (data.output === "CLEAR_TERMINAL") {
            clearTerminal();
            return;
        }
        
        // Add response to terminal
        addToTerminal(data.output);
        
        // Update directory if needed
        if (data.update_directory) {
            updateTerminalPrompt(data.update_directory);
            
            // Update directory on the server
            fetch("/api/update_directory", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    directory: data.update_directory
                })
            }).catch(error => console.error("Error updating directory:", error));
        }
        
        // Check if command was successful for completing level
        if (data.success && data.level_complete) {
            addToTerminal("\nLevel objective achieved!");
            
            // Complete level
            completeLevel();
        }
    })
    .catch(error => {
        console.error('Error executing command:', error);
        addToTerminal("ERROR: Command execution failed. Please try again.");
        updateTerminalPrompt(getCurrentDirectory()); // Ensure prompt stays consistent
    });
}

/**
 * Add text to the terminal output
 * @param {string} text - Text to add to the terminal
 */
function addToTerminal(text) {
    const terminalOutput = document.getElementById('terminalOutput');
    const newLine = document.createElement('div');
    newLine.className = 'terminal-line';
    newLine.innerHTML = text;
    terminalOutput.appendChild(newLine);
    
    // Scroll to bottom
    terminalOutput.scrollTop = terminalOutput.scrollHeight;
}

/**
 * Clear the terminal output
 */
function clearTerminal() {
    const terminalOutput = document.getElementById('terminalOutput');
    terminalOutput.innerHTML = '';
}

/**
 * Get the current directory from the terminal prompt
 */
function getCurrentDirectory() {
    const prompt = document.querySelector('.terminal-input-line .terminal-prompt');
    if (prompt) {
        const promptText = prompt.textContent;
        // Format is "username@hackos:directory$ "
        const parts = promptText.split(':');
        if (parts.length > 1) {
            // Extract directory excluding the trailing $ and space
            return parts[1].replace('$', '').trim();
        }
    }
    return '/';
}

/**
 * Update the terminal prompt with a new directory
 * @param {string} newDirectory - The new directory to display in the prompt
 */
function updateTerminalPrompt(newDirectory) {
    const currentPrompt = document.querySelector('.terminal-input-line .terminal-prompt');
    // Get the user alias from the session
    let userAlias = document.querySelector('.mission-info div span').textContent.trim() || 'user';
    if (!userAlias) {
        userAlias = "user"; // Fallback if alias not found
    }
    
    if (currentPrompt) {
        currentPrompt.textContent = `${userAlias}@hackos:${newDirectory}$ `;
    }
}
