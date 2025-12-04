/**
 * Veterinary Clinic Chat Widget
 * AI-powered assistant for answering questions about the clinic and pet health
 */

class VetChatWidget {
    constructor() {
        this.isOpen = false;
        this.isLoading = false;
        this.messages = [];
        this.apiUrl = '/api/chatbot/chat/';
        
        this.init();
    }
    
    init() {
        this.createWidget();
        this.attachEventListeners();
        this.loadFromSession();
    }
    
    createWidget() {
        // Create toggle button
        const toggleBtn = document.createElement('button');
        toggleBtn.className = 'chat-toggle-btn';
        toggleBtn.innerHTML = `
            <i class="bi bi-chat-heart-fill"></i>
            <span class="chat-badge" style="display: none;">1</span>
        `;
        toggleBtn.setAttribute('aria-label', 'Открыть чат с ассистентом');
        this.toggleBtn = toggleBtn;
        
        // Create chat window
        const chatWindow = document.createElement('div');
        chatWindow.className = 'chat-window';
        chatWindow.innerHTML = `
            <div class="chat-header">
                <div class="chat-header-avatar">
                    <i class="bi bi-heart-pulse"></i>
                </div>
                <div class="chat-header-info">
                    <h4 class="chat-header-title">ВетАссистент</h4>
                    <span class="chat-header-status">Онлайн</span>
                </div>
                <button class="chat-header-close" aria-label="Закрыть чат">
                    <i class="bi bi-x-lg"></i>
                </button>
            </div>
            <div class="chat-messages" id="chatMessages">
                <div class="chat-welcome">
                    <div class="chat-welcome-icon">
                        <i class="bi bi-heart-pulse"></i>
                    </div>
                    <h3>Привет! 👋</h3>
                    <p>Я виртуальный ассистент ВетКлиники. Могу ответить на вопросы о наших услугах, ценах, а также помочь с информацией о здоровье питомцев.</p>
                    <div class="chat-quick-actions">
                        <button class="chat-quick-btn" data-message="Где находится клиника?">📍 Адрес</button>
                        <button class="chat-quick-btn" data-message="Какие услуги вы предоставляете?">💉 Услуги</button>
                        <button class="chat-quick-btn" data-message="Расскажите о ваших врачах">👨‍⚕️ Врачи</button>
                        <button class="chat-quick-btn" data-message="Как записаться на приём?">📅 Запись</button>
                    </div>
                </div>
            </div>
            <div class="chat-input-container">
                <div class="chat-input-wrapper">
                    <textarea 
                        class="chat-input" 
                        id="chatInput" 
                        placeholder="Напишите ваш вопрос..."
                        rows="1"
                    ></textarea>
                    <button class="chat-send-btn" id="chatSendBtn" aria-label="Отправить">
                        <i class="bi bi-send-fill"></i>
                    </button>
                </div>
            </div>
        `;
        this.chatWindow = chatWindow;
        
        // Append to body
        document.body.appendChild(toggleBtn);
        document.body.appendChild(chatWindow);
        
        // Cache elements
        this.messagesContainer = chatWindow.querySelector('#chatMessages');
        this.inputField = chatWindow.querySelector('#chatInput');
        this.sendBtn = chatWindow.querySelector('#chatSendBtn');
        this.closeBtn = chatWindow.querySelector('.chat-header-close');
    }
    
    attachEventListeners() {
        // Toggle button
        this.toggleBtn.addEventListener('click', () => this.toggle());
        
        // Close button
        this.closeBtn.addEventListener('click', () => this.close());
        
        // Send button
        this.sendBtn.addEventListener('click', () => this.sendMessage());
        
        // Input field
        this.inputField.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.sendMessage();
            }
        });
        
        // Auto-resize textarea
        this.inputField.addEventListener('input', () => {
            this.inputField.style.height = 'auto';
            this.inputField.style.height = Math.min(this.inputField.scrollHeight, 120) + 'px';
        });
        
        // Quick action buttons
        this.chatWindow.addEventListener('click', (e) => {
            if (e.target.classList.contains('chat-quick-btn')) {
                const message = e.target.dataset.message;
                if (message) {
                    this.inputField.value = message;
                    this.sendMessage();
                }
            }
        });
        
        // Close on escape
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && this.isOpen) {
                this.close();
            }
        });
    }
    
    toggle() {
        if (this.isOpen) {
            this.close();
        } else {
            this.open();
        }
    }
    
    open() {
        this.isOpen = true;
        this.chatWindow.classList.add('open');
        this.toggleBtn.classList.add('active');
        this.toggleBtn.querySelector('i').className = 'bi bi-x-lg';
        this.inputField.focus();
        
        // Hide badge
        this.toggleBtn.querySelector('.chat-badge').style.display = 'none';
    }
    
    close() {
        this.isOpen = false;
        this.chatWindow.classList.remove('open');
        this.toggleBtn.classList.remove('active');
        this.toggleBtn.querySelector('i').className = 'bi bi-chat-heart-fill';
    }
    
    async sendMessage() {
        const text = this.inputField.value.trim();
        if (!text || this.isLoading) return;
        
        // Clear input
        this.inputField.value = '';
        this.inputField.style.height = 'auto';
        
        // Remove welcome message if exists
        const welcome = this.messagesContainer.querySelector('.chat-welcome');
        if (welcome) {
            welcome.remove();
        }
        
        // Add user message
        this.addMessage(text, 'user');
        
        // Show typing indicator
        this.showTyping();
        
        // Prepare history for API
        const history = this.messages.slice(0, -1).map(msg => ({
            role: msg.type === 'user' ? 'user' : 'assistant',
            content: msg.text
        }));
        
        try {
            this.isLoading = true;
            this.sendBtn.disabled = true;
            
            const response = await fetch(this.apiUrl, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    message: text,
                    history: history
                })
            });
            
            const data = await response.json();
            
            this.hideTyping();
            
            if (data.success) {
                this.addMessage(data.response, 'assistant');
            } else {
                this.addMessage(data.error || 'Произошла ошибка. Попробуйте позже.', 'error');
            }
            
        } catch (error) {
            console.error('Chat error:', error);
            this.hideTyping();
            this.addMessage('Не удалось отправить сообщение. Проверьте подключение к интернету.', 'error');
        } finally {
            this.isLoading = false;
            this.sendBtn.disabled = false;
            this.inputField.focus();
        }
        
        // Save to session
        this.saveToSession();
    }
    
    addMessage(text, type) {
        const time = new Date().toLocaleTimeString('ru-RU', { 
            hour: '2-digit', 
            minute: '2-digit' 
        });
        
        this.messages.push({ text, type, time });
        
        if (type === 'error') {
            const errorEl = document.createElement('div');
            errorEl.className = 'chat-error';
            errorEl.textContent = text;
            this.messagesContainer.appendChild(errorEl);
        } else {
            const messageEl = document.createElement('div');
            messageEl.className = `chat-message ${type}`;
            
            const avatarIcon = type === 'user' ? 'bi-person-fill' : 'bi-heart-pulse';
            
            messageEl.innerHTML = `
                <div class="chat-message-avatar">
                    <i class="bi ${avatarIcon}"></i>
                </div>
                <div class="chat-message-content">
                    <p class="chat-message-text">${this.formatMessage(text)}</p>
                    <span class="chat-message-time">${time}</span>
                </div>
            `;
            
            this.messagesContainer.appendChild(messageEl);
        }
        
        // Scroll to bottom
        this.scrollToBottom();
    }
    
    formatMessage(text) {
        // Escape HTML
        text = text.replace(/&/g, '&amp;')
                   .replace(/</g, '&lt;')
                   .replace(/>/g, '&gt;');
        
        // Convert URLs to clickable links
        const urlRegex = /(https?:\/\/[^\s<]+)/g;
        text = text.replace(urlRegex, '<a href="$1" target="_blank" rel="noopener noreferrer">$1</a>');
        
        // Convert markdown-like formatting
        // Bold: **text** or __text__
        text = text.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
        text = text.replace(/__(.*?)__/g, '<strong>$1</strong>');
        
        // Line breaks
        text = text.replace(/\n/g, '<br>');
        
        return text;
    }
    
    showTyping() {
        const typingEl = document.createElement('div');
        typingEl.className = 'chat-typing';
        typingEl.id = 'chatTyping';
        typingEl.innerHTML = `
            <div class="chat-message-avatar">
                <i class="bi bi-heart-pulse"></i>
            </div>
            <div class="chat-typing-dots">
                <span></span>
                <span></span>
                <span></span>
            </div>
        `;
        this.messagesContainer.appendChild(typingEl);
        this.scrollToBottom();
    }
    
    hideTyping() {
        const typingEl = document.getElementById('chatTyping');
        if (typingEl) {
            typingEl.remove();
        }
    }
    
    scrollToBottom() {
        this.messagesContainer.scrollTop = this.messagesContainer.scrollHeight;
    }
    
    saveToSession() {
        try {
            // Keep only last 20 messages
            const toSave = this.messages.slice(-20);
            sessionStorage.setItem('vetchat_messages', JSON.stringify(toSave));
        } catch (e) {
            console.warn('Could not save chat to session:', e);
        }
    }
    
    loadFromSession() {
        try {
            const saved = sessionStorage.getItem('vetchat_messages');
            if (saved) {
                const messages = JSON.parse(saved);
                if (messages && messages.length > 0) {
                    // Remove welcome message
                    const welcome = this.messagesContainer.querySelector('.chat-welcome');
                    if (welcome) {
                        welcome.remove();
                    }
                    
                    // Restore messages
                    messages.forEach(msg => {
                        this.messages.push(msg);
                        this.renderStoredMessage(msg);
                    });
                }
            }
        } catch (e) {
            console.warn('Could not load chat from session:', e);
        }
    }
    
    renderStoredMessage(msg) {
        if (msg.type === 'error') {
            const errorEl = document.createElement('div');
            errorEl.className = 'chat-error';
            errorEl.textContent = msg.text;
            this.messagesContainer.appendChild(errorEl);
        } else {
            const messageEl = document.createElement('div');
            messageEl.className = `chat-message ${msg.type}`;
            
            const avatarIcon = msg.type === 'user' ? 'bi-person-fill' : 'bi-heart-pulse';
            
            messageEl.innerHTML = `
                <div class="chat-message-avatar">
                    <i class="bi ${avatarIcon}"></i>
                </div>
                <div class="chat-message-content">
                    <p class="chat-message-text">${this.formatMessage(msg.text)}</p>
                    <span class="chat-message-time">${msg.time}</span>
                </div>
            `;
            
            this.messagesContainer.appendChild(messageEl);
        }
    }
}

// Initialize chat widget when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    window.vetChatWidget = new VetChatWidget();
});
