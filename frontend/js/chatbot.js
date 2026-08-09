// chatbot.js

document.addEventListener('DOMContentLoaded', () => {
  // Inject HTML for chatbot
  const chatbotHTML = `
    <div class="chatbot-widget" id="chatbotWidget">
      <button class="chatbot-btn" id="chatbotBtn" aria-label="Open Chat">
        <i data-lucide="message-square"></i>
      </button>
      <div class="chat-window">
        <div class="chat-header">
          <h3><i data-lucide="bot"></i> Civic AI Assistant</h3>
          <button class="close-chat" id="closeChatBtn"><i data-lucide="x"></i></button>
        </div>
        <div class="chat-messages" id="chatMessages">
          <div class="chat-msg bot">Hello! I'm the AI Smart Civic Assistant. I can help you report issues, track complaints, or understand how the platform works. How can I help you today?</div>
        </div>
        <div class="chat-input-area">
          <input type="text" class="chat-input" id="chatInput" placeholder="Ask a question..." autocomplete="off">
          <button class="chat-send" id="chatSendBtn"><i data-lucide="send" style="width:18px;height:18px;"></i></button>
        </div>
      </div>
    </div>
  `;

  document.body.insertAdjacentHTML('beforeend', chatbotHTML);
  if (typeof lucide !== 'undefined') {
    lucide.createIcons();
  }

  const widget = document.getElementById('chatbotWidget');
  const btn = document.getElementById('chatbotBtn');
  const closeBtn = document.getElementById('closeChatBtn');
  const messagesContainer = document.getElementById('chatMessages');
  const input = document.getElementById('chatInput');
  const sendBtn = document.getElementById('chatSendBtn');

  // Chat History for API
  let chatHistory = [];

  // Toggle Window
  btn.addEventListener('click', () => {
    widget.classList.toggle('open');
    if (widget.classList.contains('open')) {
      input.focus();
    }
  });

  closeBtn.addEventListener('click', () => {
    widget.classList.remove('open');
  });

  // Send Message
  const sendMessage = async () => {
    const text = input.value.trim();
    if (!text) return;

    // Add user message to UI
    addMessage(text, 'user');
    input.value = '';
    sendBtn.disabled = true;

    // Add to history
    chatHistory.push({ role: 'user', content: text });

    // Show typing indicator
    const typingId = showTypingIndicator();

    try {
      const response = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: text, history: chatHistory.slice(0, -1) }) // Send history excluding current message
      });

      removeTypingIndicator(typingId);

      if (!response.ok) {
        addMessage('Sorry, I encountered an error. Please try again later.', 'bot');
      } else {
        const data = await response.json();
        addMessage(data.reply, 'bot');
        chatHistory.push({ role: 'model', content: data.reply });
      }
    } catch (error) {
      removeTypingIndicator(typingId);
      addMessage('Network error. Cannot reach the server.', 'bot');
    } finally {
      sendBtn.disabled = false;
      input.focus();
    }
  };

  sendBtn.addEventListener('click', sendMessage);
  input.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') sendMessage();
  });

  // UI Helpers
  function addMessage(text, sender) {
    const msgDiv = document.createElement('div');
    msgDiv.className = `chat-msg ${sender}`;
    // Simple bold markdown parser for nicer bot responses
    const formattedText = text.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>').replace(/\n/g, '<br>');
    msgDiv.innerHTML = formattedText;
    messagesContainer.appendChild(msgDiv);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
  }

  function showTypingIndicator() {
    const id = 'typing-' + Date.now();
    const typingDiv = document.createElement('div');
    typingDiv.className = 'typing-indicator';
    typingDiv.id = id;
    typingDiv.innerHTML = '<div class="typing-dot"></div><div class="typing-dot"></div><div class="typing-dot"></div>';
    messagesContainer.appendChild(typingDiv);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
    return id;
  }

  function removeTypingIndicator(id) {
    const el = document.getElementById(id);
    if (el) el.remove();
  }
});
