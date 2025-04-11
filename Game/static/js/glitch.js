// Glitch AI Chat Functionality

/**
 * Initializes Glitch chat functionality
 */
function initializeGlitch() {
    const chatInput = document.getElementById('chatInput');
    const sendButton = document.getElementById('sendButton');
    const openChatButton = document.getElementById('openChatButton');
    const chatMessagesContainer = document.getElementById('chatMessages');
    const glitchMessagesPreview = document.getElementById('glitchMessages');
    
    // Create a chat messages container if it doesn't exist
    if (!chatMessagesContainer) {
        const chatMessages = document.createElement('div');
        chatMessages.id = 'chatMessages';
        chatMessages.className = 'chat-messages';
        document.querySelector('.chat-container').appendChild(chatMessages);
    }
    
    // Initialize Glitch Chat Modal
    const glitchChatModal = new bootstrap.Modal(document.getElementById('glitchChatModal'));
    
    // Open chat button
    openChatButton.addEventListener('click', function() {
        glitchChatModal.show();
    });
    
    // Handle chat input
    chatInput.addEventListener('keydown', function(e) {
        if (e.key === 'Enter') {
            e.preventDefault();
            sendMessage();
        }
    });
    
    // Send button click
    sendButton.addEventListener('click', function() {
        sendMessage();
    });
    
    // Show initial greeting in both places
    setTimeout(() => {
        const initialMessage = "Hey there! I'm Glitch. I'll help you take down Nexus. Ask me anything!";
        addGlitchMessage(initialMessage);
        addGlitchPreviewMessage(initialMessage);
    }, 1000);
}

/**
 * Sends a user message to Glitch and gets a response
 */
function sendMessage() {
    const chatInput = document.getElementById('chatInput');
    const message = chatInput.value.trim();
    
    if (!message) return;
    
    // Add user message to chat
    addUserMessage(message);
    
    // Clear input field
    chatInput.value = '';
    
    // Show typing indicator
    showTypingIndicator();
    
    // Get current level
    const currentLevel = parseInt(document.getElementById('currentLevel').textContent);
    
    // Send message to server
    fetch('/api/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            message: message,
            level_id: currentLevel
        })
    })
    .then(response => response.json())
    .then(data => {
        // Remove typing indicator
        removeTypingIndicator();
        
        // Add Glitch's response after a short delay
        setTimeout(() => {
            const response = data.response;
            addGlitchMessage(response);
            addGlitchPreviewMessage(response);
        }, 300);
    })
    .catch(error => {
        console.error('Error sending message:', error);
        removeTypingIndicator();
        
        // Add error message
        const errorMessage = "Sorry, I'm having trouble connecting. The signal is weak. Try again?";
        setTimeout(() => {
            addGlitchMessage(errorMessage);
            addGlitchPreviewMessage(errorMessage);
        }, 300);
    });
}

/**
 * Adds a user message to the chat
 * @param {string} message - The message to add
 */
function addUserMessage(message) {
    const chatMessages = document.getElementById('chatMessages');
    
    // Create message element
    const messageElement = document.createElement('div');
    messageElement.className = 'chat-message user-message';
    
    // Add message content
    const messageContent = document.createElement('div');
    messageContent.className = 'message-content';
    messageContent.textContent = message;
    
    messageElement.appendChild(messageContent);
    chatMessages.appendChild(messageElement);
    
    // Auto-scroll to bottom
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

/**
 * Adds a message from Glitch to the chat
 * @param {string} message - The message to add
 */
function addGlitchMessage(message) {
    const chatMessages = document.getElementById('chatMessages');
    
    // Create message element
    const messageElement = document.createElement('div');
    messageElement.className = 'chat-message glitch-message';
    
    // Add avatar
    const avatar = document.createElement('div');
    avatar.className = 'avatar';
    const img = document.createElement('img');
    img.src = '/static/images/glitch-avatar.png';
    img.alt = 'Glitch Avatar';
    avatar.appendChild(img);
    
    // Add message content
    const messageContent = document.createElement('div');
    messageContent.className = 'message-content';
    messageContent.textContent = message;
    
    messageElement.appendChild(avatar);
    messageElement.appendChild(messageContent);
    chatMessages.appendChild(messageElement);
    
    // Auto-scroll to bottom
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

/**
 * Adds a message from Glitch to the preview panel
 * @param {string} message - The message to add
 */
function addGlitchPreviewMessage(message) {
    const glitchMessagesPreview = document.getElementById('glitchMessages');
    
    // Create message element
    const messageElement = document.createElement('div');
    messageElement.className = 'glitch-preview-message';
    messageElement.textContent = message;
    
    // Add with fade-in effect
    messageElement.style.opacity = '0';
    glitchMessagesPreview.appendChild(messageElement);
    
    // Apply fade-in
    setTimeout(() => {
        messageElement.style.opacity = '1';
    }, 50);
    
    // Limit to last 3 messages in preview pane
    const messages = glitchMessagesPreview.querySelectorAll('.glitch-preview-message');
    if (messages.length > 3) {
        glitchMessagesPreview.removeChild(messages[0]);
    }
}

/**
 * Shows a typing indicator in the chat
 */
function showTypingIndicator() {
    const chatMessages = document.getElementById('chatMessages');
    
    // Check if typing indicator already exists
    if (document.getElementById('typingIndicator')) return;
    
    // Create typing indicator element
    const indicatorElement = document.createElement('div');
    indicatorElement.id = 'typingIndicator';
    indicatorElement.className = 'chat-message glitch-message typing-indicator';
    
    // Add avatar
    const avatar = document.createElement('div');
    avatar.className = 'avatar';
    const img = document.createElement('img');
    img.src = '/static/images/glitch-avatar.png';
    img.alt = 'Glitch Avatar';
    avatar.appendChild(img);
    
    // Add typing animation
    const messageContent = document.createElement('div');
    messageContent.className = 'message-content';
    messageContent.innerHTML = 'Glitch is typing<span class="dot">.</span><span class="dot">.</span><span class="dot">.</span>';
    
    indicatorElement.appendChild(avatar);
    indicatorElement.appendChild(messageContent);
    chatMessages.appendChild(indicatorElement);
    
    // Auto-scroll to bottom
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

/**
 * Removes the typing indicator from the chat
 */
function removeTypingIndicator() {
    const typingIndicator = document.getElementById('typingIndicator');
    if (typingIndicator) {
        typingIndicator.remove();
    }
}
