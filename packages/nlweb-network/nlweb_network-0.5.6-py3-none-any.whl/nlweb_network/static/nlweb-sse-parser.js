/**
 * NLWeb SSE Parser - Shared utility for parsing Server-Sent Event messages
 * Used by both nlweb-chat.js and nlweb-dropdown-chat.js
 */

export class NLWebSSEParser {
    /**
     * Parse an SSE message and return structured data
     * @param {Object} data - The parsed JSON data from SSE
     * @returns {Object} Parsed message with type and content
     */
    static parseMessage(data) {
        // Handle _meta message
        if (data._meta) {
            return {
                type: 'metadata',
                metadata: data._meta
            };
        }

        // Handle v0.54 results array (Answer response)
        if (data.results && Array.isArray(data.results)) {
            const items = data.results.map(result => ({
                type: 'resource',
                data: result
            }));

            return {
                type: 'content',
                items: items
            };
        }

        // Handle v0.54 elicitation response
        if (data.elicitation) {
            return {
                type: 'elicitation',
                text: data.elicitation.text,
                questions: data.elicitation.questions || []
            };
        }

        // Handle v0.54 promise response
        if (data.promise) {
            return {
                type: 'promise',
                promise_token: data.promise.promise_token,
                estimated_time: data.promise.estimated_time
            };
        }

        // Handle v0.54 failure response
        if (data.error) {
            return {
                type: 'error',
                code: data.error.code,
                message: data.error.message
            };
        }

        // Handle legacy content array (NLWeb format)
        if (data.content && Array.isArray(data.content)) {
            const items = [];

            data.content.forEach(item => {
                // Skip text items - they're duplicates of the resource descriptions
                // Only handle resource items
                if (item.type === 'resource' && item.resource && item.resource.data) {
                    items.push({
                        type: 'resource',
                        data: item.resource.data
                    });
                }
            });

            return {
                type: 'content',
                items: items
            };
        }

        // Handle v0.54 structuredData (chatgpt_app format)
        if (data.structuredData && Array.isArray(data.structuredData)) {
            const items = data.structuredData.map(result => ({
                type: 'resource',
                data: result
            }));

            return {
                type: 'content',
                items: items
            };
        }

        // Handle conversation_id
        if (data.type === 'conversation_id' && data.conversation_id) {
            return {
                type: 'conversation_id',
                conversation_id: data.conversation_id
            };
        }

        // Handle stream complete
        if (data.type === 'done' || data.type === 'complete') {
            return {
                type: 'complete'
            };
        }

        // Handle legacy text format
        if (data.type === 'text' || data.text) {
            return {
                type: 'text',
                text: data.content || data.text
            };
        }

        // Handle legacy item/result format
        if (data.type === 'item' || data.type === 'result' || data.title) {
            return {
                type: 'item',
                title: data.title,
                snippet: data.snippet || data.description,
                link: data.link || data.url
            };
        }

        // Unknown format
        return {
            type: 'unknown',
            data: data
        };
    }

    /**
     * Create HTML element for a resource item
     * @param {Object} resourceData - The resource data
     * @returns {HTMLElement} The created DOM element
     */
    static createResourceElement(resourceData) {
        const container = document.createElement('div');
        container.className = 'item-container';

        const content = document.createElement('div');
        content.className = 'item-content';

        // Title row with link
        const titleRow = document.createElement('div');
        titleRow.className = 'item-title-row';
        const titleLink = document.createElement('a');
        titleLink.href = resourceData.url || resourceData.grounding || '#';
        titleLink.className = 'item-title-link';
        titleLink.textContent = resourceData.name || resourceData.title || resourceData.description?.substring(0, 50) + '...' || 'Result';
        titleLink.target = '_blank';
        titleRow.appendChild(titleLink);
        content.appendChild(titleRow);

        // Site link
        if (resourceData.site) {
            const siteLink = document.createElement('a');
            siteLink.href = `/ask?site=${resourceData.site}`;
            siteLink.className = 'item-site-link';
            siteLink.textContent = resourceData.site;
            content.appendChild(siteLink);
        }

        // Description
        if (resourceData.description) {
            const description = document.createElement('div');
            description.className = 'item-description';
            description.textContent = resourceData.description;
            content.appendChild(description);
        }

        container.appendChild(content);

        // Image - handle different formats (string, array, or object)
        if (resourceData.image) {
            let imageUrl = null;

            // Handle different image data formats
            if (typeof resourceData.image === 'string') {
                // Simple string URL
                imageUrl = resourceData.image;
            } else if (Array.isArray(resourceData.image) && resourceData.image.length > 0) {
                // Array of image objects - look for a valid image URL
                for (const img of resourceData.image) {
                    if (typeof img === 'string') {
                        imageUrl = img;
                        break;
                    } else if (img && typeof img === 'object') {
                        // Try to find actual image URL, not just an anchor reference
                        const potentialUrl = img.url || img.contentUrl || img.src;
                        if (potentialUrl && !potentialUrl.startsWith('#')) {
                            imageUrl = potentialUrl;
                            break;
                        }
                        // Only use @id if it's not just an anchor
                        if (img['@id'] && !img['@id'].startsWith('#') && img['@id'].includes('#')) {
                            // This might be a URL with an anchor, but not useful as an image src
                            continue;
                        }
                    }
                }
            } else if (typeof resourceData.image === 'object') {
                // Single ImageObject
                // Try actual image properties first
                imageUrl = resourceData.image.url || resourceData.image.contentUrl || resourceData.image.src;

                // Only use @id if other properties don't exist and it's not just an anchor
                if (!imageUrl && resourceData.image['@id']) {
                    const id = resourceData.image['@id'];
                    // Skip if it's a page anchor reference (contains #primaryimage or similar)
                    if (!id.includes('#primaryimage') && !id.startsWith('#')) {
                        imageUrl = id;
                    }
                }
            }

            // Only create img element if we have a valid image URL
            // Must start with http(s) and not be an anchor reference
            if (imageUrl && typeof imageUrl === 'string' &&
                (imageUrl.startsWith('http://') || imageUrl.startsWith('https://')) &&
                !imageUrl.endsWith('#primaryimage')) {
                const imgWrapper = document.createElement('div');
                const img = document.createElement('img');
                img.src = imageUrl;
                img.alt = 'Item image';
                img.className = 'item-image';
                img.onerror = function() {
                    // Hide broken images
                    this.style.display = 'none';
                };
                imgWrapper.appendChild(img);
                container.appendChild(imgWrapper);
            }
        }

        return container;
    }
}