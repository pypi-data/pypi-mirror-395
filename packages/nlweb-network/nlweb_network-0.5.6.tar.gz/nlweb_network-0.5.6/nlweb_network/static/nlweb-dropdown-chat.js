/**
 * NLWeb Dropdown Chat Component
 * A self-contained search box with dropdown chat functionality
 *
 * Usage:
 * <script type="module">
 *   import { NLWebDropdownChat } from '/static/nlweb-dropdown-chat.js';
 *   const chat = new NLWebDropdownChat({
 *     containerId: 'my-search-container',
 *     site: 'all',
 *     placeholder: 'Ask a question...',
 *     endpoint: 'https://nlw.azurewebsites.net'
 *   });
 * </script>
 */

import { NLWebSSEParser } from './nlweb-sse-parser.js';

export class NLWebDropdownChat {
    constructor(config = {}) {
        this.config = {
            containerId: config.containerId || 'nlweb-search-container',
            site: config.site || 'all',
            placeholder: config.placeholder || 'Ask a question...',
            endpoint: config.endpoint || window.location.origin,
            cssPrefix: config.cssPrefix || 'nlweb-dropdown',
            inputId: config.inputId || 'chat-input',
            ...config
        };

        // Initialize conversation history for v0.54 context
        this.conversationHistory = [];

        this.init();
    }
    
    async init() {
        // Create the HTML structure
        this.createDOM();
        
        // Get references to elements
        this.searchInput = this.container.querySelector(`.${this.config.cssPrefix}-search-input`);
        this.dropdownResults = this.container.querySelector(`.${this.config.cssPrefix}-results`);
        this.messagesContainer = this.container.querySelector(`.${this.config.cssPrefix}-messages-container`);
        this.dropdownConversationsList = this.container.querySelector(`.${this.config.cssPrefix}-conversations-list`);
        this.dropdownConversationsPanel = this.container.querySelector(`.${this.config.cssPrefix}-conversations-panel`);
        this.historyIcon = this.container.querySelector(`.${this.config.cssPrefix}-history-icon`);
        
        // Setup event handlers
        this.setupEventHandlers();
    }
    
    createDOM() {
        // Get container
        this.container = document.getElementById(this.config.containerId);
        if (!this.container) {
            return;
        }

        // Add container class
        this.container.classList.add(`${this.config.cssPrefix}-container`);

        // Create HTML structure
        const htmlStructure = `
            <div class="${this.config.cssPrefix}-search-wrapper">
                <svg class="${this.config.cssPrefix}-history-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <circle cx="12" cy="12" r="10"></circle>
                    <polyline points="12 6 12 12 16 14"></polyline>
                </svg>
                <input type="text" 
                       class="${this.config.cssPrefix}-search-input" 
                       placeholder="${this.config.placeholder}">
            </div>
            
            <div class="${this.config.cssPrefix}-results">
                <div class="${this.config.cssPrefix}-conversations-panel">
                    <div class="${this.config.cssPrefix}-conversations-header">
                        <h3>Past Conversations</h3>
                    </div>
                    <div class="${this.config.cssPrefix}-conversations-list">
                        <!-- Conversations will be loaded here -->
                    </div>
                </div>
                <div class="${this.config.cssPrefix}-messages-container" id="messages-container">
                    <button class="${this.config.cssPrefix}-close" onclick="this.closest('.${this.config.cssPrefix}-results').classList.remove('show')">×</button>
                </div>
                
                <!-- Chat input for follow-up questions -->
                <div class="${this.config.cssPrefix}-chat-input-container" style="display: none;">
                    <div class="${this.config.cssPrefix}-chat-input-wrapper">
                        <div class="${this.config.cssPrefix}-chat-input-box">
                            <textarea 
                                class="${this.config.cssPrefix}-chat-input" 
                                placeholder="Ask a follow-up question..."
                                rows="1"
                            ></textarea>
                            <button class="${this.config.cssPrefix}-send-button">
                                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                    <line x1="22" y1="2" x2="11" y2="13"></line>
                                    <polygon points="22 2 15 22 11 13 2 9 22 2"></polygon>
                                </svg>
                            </button>
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- Hidden elements that the chat interface expects -->
            <div style="display: none;">
                <div id="sidebar"></div>
                <div id="sidebar-toggle"></div>
                <div id="mobile-menu-toggle"></div>
                <div id="new-chat-btn"></div>
                <div id="conversations-list"></div>
                <div class="chat-title"></div>
                <div id="chat-site-info"></div>
                <div id="chat-messages"></div>
                <div id="chat-input"></div>
                <div id="send-button"></div>
            </div>
        `;

        this.container.innerHTML = htmlStructure;
    }
    
    setupEventHandlers() {
        // Search input
        if (this.searchInput) {
            this.searchInput.addEventListener('keypress', (e) => {
                if (e.key === 'Enter') {
                    e.preventDefault();
                    this.handleSearch();
                }
            });
        }

        // History icon
        if (this.historyIcon) {
            this.historyIcon.addEventListener('click', (e) => {
                e.preventDefault();
                e.stopPropagation();
                this.toggleConversationsPanel();
            });
        }
        
        // Chat input and send button
        const chatInput = this.container.querySelector(`.${this.config.cssPrefix}-chat-input`);
        const sendButton = this.container.querySelector(`.${this.config.cssPrefix}-send-button`);

        if (chatInput && sendButton) {
            sendButton.addEventListener('click', () => {
                const message = chatInput.value.trim();
                if (message) {
                    this.sendFollowUpMessage(message);
                    chatInput.value = '';
                    chatInput.style.height = 'auto';
                }
            });

            chatInput.addEventListener('keypress', (e) => {
                if (e.key === 'Enter' && !e.shiftKey) {
                    e.preventDefault();
                    sendButton.click();
                }
            });
            
            // Auto-resize
            chatInput.addEventListener('input', () => {
                chatInput.style.height = 'auto';
                chatInput.style.height = Math.min(chatInput.scrollHeight, 100) + 'px';
            });
        }
        
        // Click outside to close
        document.addEventListener('click', (e) => {
            if (!this.container.contains(e.target)) {
                this.closeDropdown();
            }
        });
        
        // Escape key to close
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape') {
                this.closeDropdown();
            }
        });
    }
    
    async handleSearch() {
        if (!this.searchInput) {
            return;
        }

        const query = this.searchInput.value.trim();
        if (!query) {
            return;
        }

        this.searchInput.value = '';

        // Clear messages if starting a new conversation
        if (this.messagesContainer) {
            this.messagesContainer.innerHTML = '<button class="' + this.config.cssPrefix + '-close" onclick="this.closest(\'.' + this.config.cssPrefix + '-results\').classList.remove(\'show\')">×</button>';
        }

        this.showDropdown();

        // Add user message
        this.addMessage('user', query);

        // Add to conversation history for v0.54 context
        this.conversationHistory.push(query);

        // Show loading indicator
        const loadingMessage = this.addMessage('assistant', '<div class="loading-dots"><div class="loading-dot"></div><div class="loading-dot"></div><div class="loading-dot"></div></div>');

        // Build v0.54 request
        const request = {
            query: {
                text: query,
                ...(this.config.site && { site: this.config.site })
            },
            prefer: {
                streaming: false,
                response_format: 'conv_search'
            },
            meta: {
                api_version: '0.54'
            }
        };

        // Add conversation context if available
        if (this.conversationHistory && this.conversationHistory.length > 0) {
            request.context = {
                '@type': 'ConversationalContext',
                prev: this.conversationHistory.slice(-5) // Last 5 queries
            };
        }

        // Send query to backend (v0.54 format)
        const response = await fetch(`${this.config.endpoint}/ask`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(request)
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        // Remove loading indicator
        if (loadingMessage && loadingMessage.parentNode) {
            loadingMessage.remove();
        }

        // Detect response type and handle accordingly
        const contentType = response.headers.get('content-type') || '';

        // Check if responseType is forced in config
        const responseType = this.config.responseType || 'auto';

        if (responseType === 'json' || (responseType === 'auto' && contentType.includes('application/json'))) {
            // Handle as single JSON response
            await this.handleJSONResponse(response);
        } else if (responseType === 'sse' || (responseType === 'auto' && contentType.includes('text/event-stream'))) {
            // Handle as SSE stream
            await this.handleSSEResponse(response);
        } else {
            // Auto-detect: Try to peek at the response
            // Clone the response so we can read it twice if needed
            const clonedResponse = response.clone();

            try {
                // Try to read as JSON first
                const data = await clonedResponse.json();
                await this.handleJSONResponse(null, data);
            } catch {
                // If JSON parsing fails, assume it's SSE
                await this.handleSSEResponse(response);
            }
        }
    }

    async handleJSONResponse(response, preloadedData = null) {
        // Get the data either from preloaded or from response
        const data = preloadedData || await response.json();

        // Handle v0.54 response types
        if (data._meta && data._meta.response_type) {
            switch (data._meta.response_type) {
                case 'Answer':
                    this.handleAnswerResponse(data);
                    break;
                case 'Elicitation':
                    this.handleElicitationResponse(data);
                    break;
                case 'Promise':
                    this.handlePromiseResponse(data);
                    break;
                case 'Failure':
                    this.handleFailureResponse(data);
                    break;
                default:
                    this.handleLegacyResponse(data);
            }
        } else {
            // Legacy format
            this.handleLegacyResponse(data);
        }

        // Handle conversation ID if present
        if (data._meta && data._meta.session_context && data._meta.session_context.conversation_id) {
            this.currentConversationId = data._meta.session_context.conversation_id;
        }

        // Scroll to show new content
        this.messagesContainer.scrollTop = this.messagesContainer.scrollHeight;

        // Show follow-up input
        this.showFollowUpInput();
    }

    handleAnswerResponse(data) {
        // Create assistant message element
        const messageElement = this.addMessage('assistant', '');
        const contentDiv = messageElement.querySelector('.message-content');
        if (contentDiv) {
            contentDiv.innerHTML = ''; // Clear any placeholder
        }

        // Extract results (handles both conv_search and chatgpt_app formats)
        const results = data.results || data.structuredData || [];

        // Display results
        results.forEach(result => {
            const resourceElement = NLWebSSEParser.createResourceElement(result);
            contentDiv.appendChild(resourceElement);
        });

        // If no results, show message
        if (results.length === 0) {
            contentDiv.innerHTML = '<p>No results found.</p>';
        }
    }

    handleElicitationResponse(data) {
        const messageElement = this.addMessage('assistant', '');
        const contentDiv = messageElement.querySelector('.message-content');
        if (contentDiv) {
            contentDiv.innerHTML = '';
        }

        // Show elicitation text
        const textP = document.createElement('p');
        textP.textContent = data.elicitation.text;
        contentDiv.appendChild(textP);

        // Show questions
        data.elicitation.questions.forEach(q => {
            const questionDiv = document.createElement('div');
            questionDiv.className = 'elicitation-question';

            const questionText = document.createElement('strong');
            questionText.textContent = q.text;
            questionDiv.appendChild(questionText);

            if (q.options) {
                const optionsList = document.createElement('ul');
                q.options.forEach(opt => {
                    const li = document.createElement('li');
                    li.textContent = opt;
                    optionsList.appendChild(li);
                });
                questionDiv.appendChild(optionsList);
            }

            contentDiv.appendChild(questionDiv);
        });
    }

    handlePromiseResponse(data) {
        const messageElement = this.addMessage('assistant', '');
        const contentDiv = messageElement.querySelector('.message-content');
        if (contentDiv) {
            contentDiv.innerHTML = '';
        }

        const estimatedTime = data.promise.estimated_time
            ? ` (estimated ${data.promise.estimated_time}s)`
            : '';
        contentDiv.innerHTML = `<p>Task started${estimatedTime}. Token: <code>${data.promise.token}</code></p>`;
    }

    handleFailureResponse(data) {
        const messageElement = this.addMessage('assistant', '');
        const contentDiv = messageElement.querySelector('.message-content');
        if (contentDiv) {
            contentDiv.innerHTML = '';
        }

        contentDiv.innerHTML = `<p class="error">Error (${data.error.code}): ${data.error.message}</p>`;
    }

    handleLegacyResponse(data) {
        // Parse the message using the SSE parser (for old format)
        const parsed = NLWebSSEParser.parseMessage(data);

        // Create assistant message element
        const messageElement = this.addMessage('assistant', '');
        const contentDiv = messageElement.querySelector('.message-content');
        if (contentDiv) {
            contentDiv.innerHTML = ''; // Clear any placeholder
        }

        // Handle different parsed types
        switch (parsed.type) {
            case 'content':
                // Process all items
                parsed.items.forEach(item => {
                    if (item.type === 'resource') {
                        const resourceElement = NLWebSSEParser.createResourceElement(item.data);
                        contentDiv.appendChild(resourceElement);
                    } else if (item.type === 'text' && this.config.showTextItems !== false) {
                        // Optionally show text items if configured
                        const textElement = document.createElement('p');
                        textElement.textContent = item.text;
                        contentDiv.appendChild(textElement);
                    }
                });
                break;

            case 'text':
                // Legacy text response
                contentDiv.innerHTML = parsed.text;
                break;

            default:
                // Unknown format, show raw data
                contentDiv.textContent = JSON.stringify(data, null, 2);
        }
    }

    async handleSSEResponse(response) {
        const reader = response.body.getReader();
        const decoder = new TextDecoder();
        let buffer = '';
        let currentMessageElement = null;

        while (true) {
            const { value, done } = await reader.read();
            if (done) {
                break;
            }

            const rawChunk = decoder.decode(value, { stream: true });

            buffer += rawChunk;
            const lines = buffer.split('\n');
            buffer = lines.pop();

            for (const line of lines) {
                if (line === '') {
                    continue;
                }

                if (line.startsWith('data: ')) {
                    const dataStr = line.slice(6);
                    const data = JSON.parse(dataStr);
                    const parsed = NLWebSSEParser.parseMessage(data);

                    switch (parsed.type) {
                        case 'metadata':
                            // Skip metadata
                            break;

                        case 'content':
                            // Create message element if needed
                            if (!currentMessageElement) {
                                currentMessageElement = this.addMessage('assistant', '');
                                const contentDiv = currentMessageElement.querySelector('.message-content');
                                if (contentDiv) {
                                    contentDiv.innerHTML = ''; // Clear loading indicator
                                }
                            }

                            const contentDiv = currentMessageElement.querySelector('.message-content') || currentMessageElement;

                            // Process each item - only resources (text items are skipped as duplicates)
                            parsed.items.forEach(item => {
                                if (item.type === 'resource') {
                                    const resourceElement = NLWebSSEParser.createResourceElement(item.data);
                                    contentDiv.appendChild(resourceElement);
                                }
                            });

                            // Scroll to show new content
                            this.messagesContainer.scrollTop = this.messagesContainer.scrollHeight;
                            break;

                        case 'conversation_id':
                            this.currentConversationId = parsed.conversation_id;
                            break;

                        case 'complete':
                            // Stream complete
                            break;

                        case 'text':
                            // Legacy text format
                            if (!currentMessageElement) {
                                currentMessageElement = this.addMessage('assistant', '');
                            }
                            const textDiv = currentMessageElement.querySelector('.message-content') || currentMessageElement;
                            textDiv.innerHTML += parsed.text;
                            break;
                    }
                }
            }
        }

        // Show follow-up input
        this.showFollowUpInput();
    }

    showFollowUpInput() {
        const chatInputContainer = this.container.querySelector(`.${this.config.cssPrefix}-chat-input-container`);
        if (chatInputContainer) {
            chatInputContainer.style.display = 'block';
        }
    }

    async sendFollowUpMessage(message) {
        // Add user message
        this.addMessage('user', message);

        // Add to conversation history for v0.54 context
        this.conversationHistory.push(message);

        // Show loading indicator
        const loadingMessage = this.addMessage('assistant', '<div class="loading-dots"><div class="loading-dot"></div><div class="loading-dot"></div><div class="loading-dot"></div></div>');

        // Build v0.54 request
        const request = {
            query: {
                text: message,
                ...(this.config.site && { site: this.config.site })
            },
            prefer: {
                streaming: false,
                response_format: 'conv_search'
            },
            meta: {
                api_version: '0.54'
            }
        };

        // Add conversation context
        if (this.conversationHistory && this.conversationHistory.length > 0) {
            request.context = {
                '@type': 'ConversationalContext',
                prev: this.conversationHistory.slice(-5) // Last 5 queries
            };
        }

        // Send to backend (v0.54 format)
        try {
            const response = await fetch(`${this.config.endpoint}/ask`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(request)
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            // Remove loading indicator
            if (loadingMessage && loadingMessage.parentNode) {
                loadingMessage.remove();
            }

            // Detect response type and handle accordingly
            const contentType = response.headers.get('content-type') || '';
            const responseType = this.config.responseType || 'auto';

            if (responseType === 'json' || (responseType === 'auto' && contentType.includes('application/json'))) {
                // Handle as single JSON response
                await this.handleJSONResponse(response);
            } else if (responseType === 'sse' || (responseType === 'auto' && contentType.includes('text/event-stream'))) {
                // Handle as SSE stream
                await this.handleSSEResponse(response);
            } else {
                // Auto-detect: Try to peek at the response
                const clonedResponse = response.clone();

                try {
                    // Try to read as JSON first
                    const data = await clonedResponse.json();
                    await this.handleJSONResponse(null, data);
                } catch {
                    // If JSON parsing fails, assume it's SSE
                    await this.handleSSEResponse(response);
                }
            }

        } catch (error) {
            this.addMessage('assistant', 'Sorry, there was an error processing your request.');
        }
    }
    
    addMessage(type, content) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${type}-message`;

        const contentDiv = document.createElement('div');
        contentDiv.className = 'message-content';
        contentDiv.innerHTML = content;

        messageDiv.appendChild(contentDiv);

        // Insert before the close button
        const closeButton = this.messagesContainer.querySelector(`.${this.config.cssPrefix}-close`);
        if (closeButton) {
            this.messagesContainer.insertBefore(messageDiv, closeButton);
        } else {
            this.messagesContainer.appendChild(messageDiv);
        }

        // Scroll to bottom
        this.messagesContainer.scrollTop = this.messagesContainer.scrollHeight;

        return messageDiv;
    }
    
    toggleConversationsPanel() {
        if (!this.dropdownResults.classList.contains('show')) {
            this.showDropdown();
        }
        
        this.dropdownConversationsPanel.classList.toggle('show');
        
        if (this.dropdownConversationsPanel.classList.contains('show')) {
            this.updateConversationsList();
        }
    }
    
    async updateConversationsList() {
        // Load conversations from backend
        try {
            const response = await fetch(`${this.config.endpoint}/conversations`, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                }
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const conversations = await response.json();
            
            if (!conversations || conversations.length === 0) {
                this.dropdownConversationsList.innerHTML = '<div class="nlweb-dropdown-empty-conversations">No conversations yet</div>';
                return;
            }

            this.dropdownConversationsList.innerHTML = '';

            conversations.forEach(conv => {
                const item = document.createElement('div');
                item.className = 'nlweb-dropdown-conversation-item';
                item.dataset.conversationId = conv.id;

                const title = document.createElement('div');
                title.className = 'nlweb-dropdown-conversation-title';
                title.textContent = conv.title || 'Untitled Conversation';

                const deleteBtn = document.createElement('button');
                deleteBtn.className = 'nlweb-dropdown-conversation-delete';
                deleteBtn.innerHTML = '×';
                deleteBtn.onclick = (e) => {
                    e.stopPropagation();
                    this.deleteConversation(conv.id);
                };

                item.appendChild(title);
                item.appendChild(deleteBtn);

                item.onclick = () => this.loadConversation(conv.id);

                this.dropdownConversationsList.appendChild(item);
            });

        } catch (error) {
            this.dropdownConversationsList.innerHTML = '<div class="nlweb-dropdown-empty-conversations">Error loading conversations</div>';
        }
    }
    
    async loadConversation(conversationId) {
        // Load conversation from backend
        try {
            const response = await fetch(`${this.config.endpoint}/conversation/${conversationId}`, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                }
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const conversation = await response.json();
            
            this.currentConversationId = conversationId;

            // Clear messages
            this.messagesContainer.innerHTML = '<button class="' + this.config.cssPrefix + '-close" onclick="this.closest(\'.' + this.config.cssPrefix + '-results\').classList.remove(\'show\')">×</button>';
            
            // Display messages
            if (conversation.messages) {
                conversation.messages.forEach(msg => {
                    this.addMessage(msg.type || msg.message_type, msg.content);
                });
            }
            
            // Show follow-up input
            const chatInputContainer = this.container.querySelector(`.${this.config.cssPrefix}-chat-input-container`);
            if (chatInputContainer) {
                chatInputContainer.style.display = 'block';
            }
            
            // Update active state
            this.dropdownConversationsList.querySelectorAll('.nlweb-dropdown-conversation-item').forEach(item => {
                item.classList.remove('active');
                if (item.dataset.conversationId === conversationId) {
                    item.classList.add('active');
                }
            });

        } catch (error) {
            // Error loading conversation
        }
    }
    
    async deleteConversation(conversationId) {
        try {
            const response = await fetch(`${this.config.endpoint}/conversation/${conversationId}`, {
                method: 'DELETE',
                headers: {
                    'Content-Type': 'application/json',
                }
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            if (this.currentConversationId === conversationId) {
                this.currentConversationId = null;
                this.messagesContainer.innerHTML = '<button class="' + this.config.cssPrefix + '-close" onclick="this.closest(\'.' + this.config.cssPrefix + '-results\').classList.remove(\'show\')">×</button>';
            }

            this.updateConversationsList();

        } catch (error) {
            // Error deleting conversation
        }
    }
    
    showDropdown() {
        this.dropdownResults.classList.add('show');
    }
    
    closeDropdown() {
        this.dropdownResults.classList.remove('show');
        this.dropdownConversationsPanel.classList.remove('show');

        const chatInputContainer = this.container.querySelector(`.${this.config.cssPrefix}-chat-input-container`);
        if (chatInputContainer) {
            chatInputContainer.style.display = 'none';
        }
    }
    
    // Public API methods
    search(query) {
        this.searchInput.value = query;
        this.handleSearch();
    }
    
    setQuery(query) {
        this.searchInput.value = query;
    }
    
    setSite(site) {
        this.config.site = site;
    }
    
    destroy() {
        // Clean up event listeners and DOM
        if (this.container) {
            this.container.innerHTML = '';
        }
    }
}
