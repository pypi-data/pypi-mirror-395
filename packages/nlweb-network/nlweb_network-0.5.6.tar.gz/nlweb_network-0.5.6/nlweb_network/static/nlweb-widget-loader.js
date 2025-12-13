/**
 * NLWeb Widget Loader - Simple script to load the dropdown widget
 *
 * Usage:
 * <script src="https://nlw.azurewebsites.net/static/nlweb-widget-loader.js"></script>
 * <script>
 *   NLWebWidget.init({
 *     containerId: 'search-container',
 *     site: 'imdb.com'
 *   });
 * </script>
 */

(function(window) {
    'use strict';

    // Configuration defaults
    const DEFAULT_CONFIG = {
        baseUrl: 'https://nlw.azurewebsites.net',
        containerId: 'nlweb-search-container',
        site: 'all',
        placeholder: 'Ask a question...',
        responseType: 'auto' // 'auto' | 'sse' | 'json' - auto-detect by default
    };

    // Main widget object
    window.NLWebWidget = {
        // Initialize the widget
        init: async function(userConfig = {}) {
            const config = { ...DEFAULT_CONFIG, ...userConfig };

            try {
                // Load CSS if not already loaded
                if (!document.querySelector('link[href*="nlweb-dropdown-chat.css"]')) {
                    const css = document.createElement('link');
                    css.rel = 'stylesheet';
                    css.href = `${config.baseUrl}/static/nlweb-dropdown-chat.css`;
                    document.head.appendChild(css);
                }

                // Ensure container exists
                const container = document.getElementById(config.containerId);
                if (!container) {
                    console.error(`NLWebWidget: Container with id "${config.containerId}" not found`);
                    return null;
                }

                // Dynamically import the module
                const module = await import(`${config.baseUrl}/static/nlweb-dropdown-chat.js`);

                // Create widget instance
                const widget = new module.NLWebDropdownChat({
                    containerId: config.containerId,
                    site: config.site,
                    placeholder: config.placeholder,
                    endpoint: config.baseUrl,
                    responseType: config.responseType
                });

                console.log('NLWebWidget: Initialized successfully');
                return widget;

            } catch (error) {
                console.error('NLWebWidget: Failed to initialize', error);

                // Show user-friendly error in container
                const container = document.getElementById(config.containerId);
                if (container) {
                    container.innerHTML = `
                        <div style="padding: 20px; background: #f8f9fa; border: 1px solid #dee2e6; border-radius: 8px; color: #dc3545;">
                            <strong>Failed to load search widget</strong><br>
                            <small>${error.message || 'Please check your internet connection and try again.'}</small>
                        </div>
                    `;
                }

                return null;
            }
        },

        // Convenience method to create and initialize in one step
        create: function(config = {}) {
            // Wait for DOM to be ready
            if (document.readyState === 'loading') {
                document.addEventListener('DOMContentLoaded', () => {
                    this.init(config);
                });
            } else {
                this.init(config);
            }
        }
    };

    // Auto-initialize if data attributes are present
    document.addEventListener('DOMContentLoaded', function() {
        const autoContainers = document.querySelectorAll('[data-nlweb-widget]');

        autoContainers.forEach(container => {
            const config = {
                containerId: container.id || 'nlweb-search-container',
                site: container.dataset.nlwebSite || 'all',
                placeholder: container.dataset.nlwebPlaceholder || 'Ask a question...',
                baseUrl: container.dataset.nlwebEndpoint || 'https://nlw.azurewebsites.net',
                responseType: container.dataset.nlwebResponseType || 'auto'
            };

            // Ensure container has an ID
            if (!container.id) {
                container.id = 'nlweb-widget-' + Math.random().toString(36).substr(2, 9);
                config.containerId = container.id;
            }

            window.NLWebWidget.init(config);
        });
    });

})(window);