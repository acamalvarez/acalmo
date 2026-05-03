document.addEventListener('DOMContentLoaded', () => {
    const toggleBtn = document.getElementById('chatbot-toggle');
    const expandBtn = document.getElementById('chatbot-expand');
    const closeBtn = document.getElementById('chatbot-close');
    const windowEl = document.getElementById('chatbot-window');
    const form = document.getElementById('chatbot-form');
    const input = document.getElementById('chatbot-input');
    const messagesBox = document.getElementById('chatbot-messages');

    const EXTERNAL_API_URL = window.CHATBOT_API_URL;

    // Helper to format newlines
    const formatText = (text) => {
        return text.replace(/\n/g, '<br>');
    };

    const createMessageBubble = (sender) => {
        const msgDiv = document.createElement('div');
        msgDiv.classList.add('chatbot-msg');
        msgDiv.classList.add(sender === 'user' ? 'user-message' : 'bot-message');
        messagesBox.appendChild(msgDiv);
        return msgDiv;
    };

    const renderStaticMessage = (text, sender) => {
        const msgDiv = createMessageBubble(sender);
        msgDiv.innerHTML = formatText(text);
        scrollToBottom();
    };

    const showTypingIndicator = () => {
        const div = document.createElement('div');
        div.className = 'chatbot-msg bot-message typing';
        div.id = 'chatbot-typing';
        div.innerHTML = '<div class="dot"></div><div class="dot"></div><div class="dot"></div>';
        messagesBox.appendChild(div);
        scrollToBottom();
    };

    const removeTypingIndicator = () => {
        const el = document.getElementById('chatbot-typing');
        if (el) el.remove();
    };

    const scrollToBottom = () => {
        messagesBox.scrollTop = messagesBox.scrollHeight;
    };

    // Toggle open/close
    toggleBtn.addEventListener('click', () => {
        windowEl.classList.remove('hidden');
        toggleBtn.style.transform = 'scale(0)';
        input.focus();
    });

    closeBtn.addEventListener('click', () => {
        windowEl.classList.add('hidden');
        windowEl.classList.remove('expanded');
        toggleBtn.style.transform = 'scale(1)';
    });

    // Expand mode
    expandBtn.addEventListener('click', () => {
        windowEl.classList.toggle('expanded');
        const icon = expandBtn.querySelector('i');
        if (windowEl.classList.contains('expanded')) {
            icon.classList.remove('uil-expand-arrows');
            icon.classList.add('uil-compress-arrows');
        } else {
            icon.classList.add('uil-expand-arrows');
            icon.classList.remove('uil-compress-arrows');
        }
        scrollToBottom();
    });

    // Handle form submission and streaming response
    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        const text = input.value.trim();
        if (!text) return;

        renderStaticMessage(text, 'user');
        input.value = '';

        showTypingIndicator();

        try {
            const response = await fetch(EXTERNAL_API_URL, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message: text })
            });

            if (!response.ok) {
                removeTypingIndicator();
                renderStaticMessage(`Error: ${response.statusText}`, 'bot');
                return;
            }

            // Stream reader
            const reader = response.body.getReader();
            const decoder = new TextDecoder('utf-8');
            let done = false;
            let fullText = '';
            let charIndex = 0;
            let msgDiv = null;

            const processQueue = () => {
                if (charIndex < fullText.length) {
                    if (!msgDiv) {
                        removeTypingIndicator();
                        msgDiv = createMessageBubble('bot');
                    }
                    const remaining = fullText.length - charIndex;
                    let charsToType = 1;
                    if (remaining > 150) charsToType = 4;
                    else if (remaining > 50) charsToType = 2;

                    charIndex += charsToType;
                    if (charIndex > fullText.length) charIndex = fullText.length;

                    msgDiv.innerHTML = formatText(fullText.substring(0, charIndex));
                    scrollToBottom();

                    setTimeout(processQueue, 20);
                } else if (!done) {
                    setTimeout(processQueue, 50);
                } else if (done && !msgDiv) {
                    removeTypingIndicator();
                }
            };

            // Start the typewriter loop
            processQueue();

            while (!done) {
                const { value, done: readerDone } = await reader.read();
                done = readerDone;
                if (value) {
                    const chunk = decoder.decode(value, { stream: true });
                    fullText += chunk;
                }
            }
        } catch (error) {
            removeTypingIndicator();
            renderStaticMessage('Network error. Is the FastAPI backend running?', 'bot');
            console.error('Chat error:', error);
        }
    });
});
