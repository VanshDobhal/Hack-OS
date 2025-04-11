/**
 * Typing effect functionality
 * Provides functions for creating typing animations
 */

// Default typing speed (lower number = faster typing)
window.typingSpeed = 30;

/**
 * Animates typing text into an element
 * @param {Element|string} element - The element or selector to type text into
 * @param {string} [textToType] - Optional text to type (if not provided, uses data-text attribute)
 * @param {number} [speed] - Typing speed in milliseconds (optional)
 * @returns {Promise} - Resolves when typing is complete
 */
function typeText(element, textToType, speed) {
    // Handle selector string
    if (typeof element === 'string') {
        element = document.querySelector(element);
    }
    
    if (!element) {
        console.error('Element not found for typing effect');
        return Promise.reject(new Error('Element not found'));
    }
    
    // Use provided speed or global default
    const typingSpeed = speed || window.typingSpeed;
    
    // Get text to type from parameter or data attribute
    const text = textToType || element.getAttribute('data-text') || '';
    
    // Clear the element
    element.textContent = '';
    
    return new Promise(resolve => {
        let charIndex = 0;
        
        // Skip typing if text is empty
        if (!text) {
            resolve();
            return;
        }
        
        const interval = setInterval(() => {
            if (charIndex < text.length) {
                // Add next character
                element.textContent += text.charAt(charIndex);
                charIndex++;
            } else {
                // Typing complete
                clearInterval(interval);
                resolve();
            }
        }, typingSpeed);
    });
}

/**
 * Adds blinking cursor to element
 * @param {Element} element - Element to add cursor to
 */
function addBlinkingCursor(element) {
    // Remove existing cursor if any
    element.classList.remove('cursor-blink');
    
    // Add cursor class
    element.classList.add('cursor-blink');
}

/**
 * Removes blinking cursor from element
 * @param {Element} element - Element to remove cursor from
 */
function removeBlinkingCursor(element) {
    element.classList.remove('cursor-blink');
}

/**
 * Simple delay function
 * @param {number} ms - Milliseconds to delay
 * @returns {Promise} - Resolves after delay
 */
function delay(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

/**
 * Types a sequence of text into multiple elements in order
 * @param {Array} sequence - Array of {element, text, speed} objects
 * @param {number} [delayBetween=500] - Delay between elements in ms
 * @returns {Promise} - Resolves when sequence is complete
 */
async function typeSequence(sequence, delayBetween = 500) {
    for (let i = 0; i < sequence.length; i++) {
        const item = sequence[i];
        const el = typeof item.element === 'string' ? 
            document.querySelector(item.element) : item.element;
        
        if (el) {
            await typeText(el, item.text, item.speed);
            await delay(delayBetween);
        }
    }
    
    return Promise.resolve();
}
