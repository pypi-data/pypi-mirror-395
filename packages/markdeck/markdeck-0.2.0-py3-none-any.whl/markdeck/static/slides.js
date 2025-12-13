// MarkDeck presentation viewer
class SlideShow {
    constructor() {
        this.slides = [];
        this.currentSlideIndex = 0;
        this.totalSlides = 0;
        this.title = '';
        this.isFullscreen = false;

        this.elements = {
            loading: document.getElementById('loading'),
            presentation: document.getElementById('presentation'),
            slideContainer: document.getElementById('slide-container'),
            slideContent: document.getElementById('slide-content'),
            currentSlide: document.getElementById('current-slide'),
            totalSlidesEl: document.getElementById('total-slides'),
            progressFill: document.getElementById('progress-fill'),
            helpOverlay: document.getElementById('help-overlay'),
            closeHelp: document.getElementById('close-help'),
            error: document.getElementById('error'),
            errorMessage: document.getElementById('error-message'),
        };

        this.init();
    }

    async init() {
        try {
            // Configure marked.js with custom renderer for mermaid diagrams
            const renderer = new marked.Renderer();
            const originalCode = renderer.code.bind(renderer);

            renderer.code = function(code, language) {
                if (language === 'mermaid') {
                    // Create a unique ID for this diagram
                    const id = 'mermaid-' + Math.random().toString(36).substr(2, 9);
                    return `<div class="mermaid" id="${id}">${code}</div>`;
                }
                return originalCode(code, language);
            };

            marked.setOptions({
                breaks: true,
                gfm: true,
                renderer: renderer,
                highlight: function(code, lang) {
                    if (lang === 'mermaid') {
                        return code; // Don't highlight mermaid code
                    }
                    if (lang && hljs.getLanguage(lang)) {
                        try {
                            return hljs.highlight(code, { language: lang }).value;
                        } catch (err) {
                            console.error('Highlighting error:', err);
                        }
                    }
                    return hljs.highlightAuto(code).value;
                }
            });

            // Load slides from API
            await this.loadSlides();

            // Set up event listeners
            this.setupEventListeners();

            // Set up WebSocket for hot reloading
            await this.setupHotReload();

            // Show first slide
            this.showSlide(0);

            // Hide loading, show presentation
            this.elements.loading.classList.add('hidden');
            this.elements.presentation.classList.remove('hidden');
        } catch (error) {
            this.showError(error.message);
        }
    }

    async loadSlides() {
        const response = await fetch('/api/slides');
        if (!response.ok) {
            throw new Error(`Failed to load slides: ${response.statusText}`);
        }

        const data = await response.json();
        this.slides = data.slides;
        this.totalSlides = data.total;
        this.title = data.title;

        if (this.totalSlides === 0) {
            throw new Error('No slides found in presentation');
        }

        document.title = `${this.title} - MarkDeck`;
        this.elements.totalSlidesEl.textContent = this.totalSlides;
    }

    setupEventListeners() {
        // Keyboard navigation
        document.addEventListener('keydown', (e) => this.handleKeyPress(e));

        // Help overlay close button
        this.elements.closeHelp.addEventListener('click', () => this.toggleHelp());

        // Prevent default behavior for navigation keys
        document.addEventListener('keydown', (e) => {
            if (['Space', 'ArrowLeft', 'ArrowRight', 'PageUp', 'PageDown'].includes(e.code)) {
                e.preventDefault();
            }
        });
    }

    async setupHotReload() {
        // Check if watch mode is enabled
        try {
            const response = await fetch('/api/watch-enabled');
            const data = await response.json();

            if (!data.watch_enabled) {
                return;
            }

            // Connect to WebSocket for hot reload
            const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
            const wsUrl = `${protocol}//${window.location.host}/ws`;

            const connectWebSocket = () => {
                const ws = new WebSocket(wsUrl);

                ws.onopen = () => {
                    console.log('Hot reload connected');
                };

                ws.onmessage = async (event) => {
                    const message = JSON.parse(event.data);
                    if (message.type === 'reload') {
                        console.log('File changed, reloading slides...');
                        await this.reloadPresentation();
                    }
                };

                ws.onerror = (error) => {
                    console.error('WebSocket error:', error);
                };

                ws.onclose = () => {
                    console.log('WebSocket closed, reconnecting in 2s...');
                    setTimeout(connectWebSocket, 2000);
                };
            };

            connectWebSocket();
        } catch (error) {
            console.error('Failed to set up hot reload:', error);
        }
    }

    async reloadPresentation() {
        const currentSlide = this.currentSlideIndex;

        try {
            await this.loadSlides();
            // Try to stay on the same slide, or go to last slide if current doesn't exist
            const targetSlide = Math.min(currentSlide, this.totalSlides - 1);
            this.showSlide(targetSlide);

            // Show a brief notification
            this.showReloadNotification();
        } catch (error) {
            console.error('Failed to reload presentation:', error);
        }
    }

    showReloadNotification() {
        // Create a temporary notification
        const notification = document.createElement('div');
        notification.textContent = 'Presentation reloaded';
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            left: 50%;
            transform: translateX(-50%);
            background: rgba(74, 158, 255, 0.9);
            color: white;
            padding: 10px 20px;
            border-radius: 6px;
            z-index: 10000;
            font-size: 1rem;
            animation: fadeInOut 2s ease-in-out;
        `;

        // Add animation style if not exists
        if (!document.getElementById('reload-animation')) {
            const style = document.createElement('style');
            style.id = 'reload-animation';
            style.textContent = `
                @keyframes fadeInOut {
                    0% { opacity: 0; transform: translateX(-50%) translateY(-10px); }
                    20% { opacity: 1; transform: translateX(-50%) translateY(0); }
                    80% { opacity: 1; transform: translateX(-50%) translateY(0); }
                    100% { opacity: 0; transform: translateX(-50%) translateY(-10px); }
                }
            `;
            document.head.appendChild(style);
        }

        document.body.appendChild(notification);
        setTimeout(() => notification.remove(), 2000);
    }

    handleKeyPress(e) {
        switch (e.key) {
            case 'ArrowRight':
            case ' ':
            case 'PageDown':
                this.nextSlide();
                break;
            case 'ArrowLeft':
            case 'PageUp':
                this.previousSlide();
                break;
            case 'Home':
                this.goToSlide(0);
                break;
            case 'End':
                this.goToSlide(this.totalSlides - 1);
                break;
            case 'f':
            case 'F':
                this.toggleFullscreen();
                break;
            case '?':
                this.toggleHelp();
                break;
            case 'Escape':
                if (this.isFullscreen) {
                    this.exitFullscreen();
                } else if (!this.elements.helpOverlay.classList.contains('hidden')) {
                    this.toggleHelp();
                }
                break;
        }
    }

    showSlide(index) {
        if (index < 0 || index >= this.totalSlides) {
            return;
        }

        this.currentSlideIndex = index;
        const slide = this.slides[index];

        // Render markdown
        this.elements.slideContent.innerHTML = marked.parse(slide.content);

        // Rewrite relative image paths to use /assets/ endpoint
        this.elements.slideContent.querySelectorAll('img').forEach((img) => {
            const src = img.getAttribute('src');
            if (src && !src.startsWith('http://') && !src.startsWith('https://') && !src.startsWith('//') && !src.startsWith('/')) {
                // Remove leading ./ if present
                const cleanPath = src.startsWith('./') ? src.slice(2) : src;
                img.setAttribute('src', '/assets/' + cleanPath);
            }
        });

        // Apply syntax highlighting to code blocks
        this.elements.slideContent.querySelectorAll('pre code').forEach((block) => {
            hljs.highlightElement(block);
        });

        // Render math equations with KaTeX
        if (window.renderMathInElement) {
            renderMathInElement(this.elements.slideContent, {
                delimiters: [
                    { left: '$$', right: '$$', display: true },
                    { left: '$', right: '$', display: false },
                    { left: '\\[', right: '\\]', display: true },
                    { left: '\\(', right: '\\)', display: false }
                ],
                throwOnError: false
            });
        }

        // Render mermaid diagrams if present
        const mermaidElements = this.elements.slideContent.querySelectorAll('.mermaid');
        if (mermaidElements.length > 0 && window.mermaid) {
            // Run mermaid on all diagrams in the current slide
            mermaidElements.forEach((element) => {
                element.removeAttribute('data-processed');
            });
            window.mermaid.run({
                nodes: mermaidElements
            });
        }

        // Notify server to log speaker notes to terminal
        this.notifySlideChange(index);

        // Update progress indicator
        this.elements.currentSlide.textContent = index + 1;
        const progressPercent = ((index + 1) / this.totalSlides) * 100;
        this.elements.progressFill.style.width = `${progressPercent}%`;

        // Scroll to top of slide
        this.elements.slideContainer.scrollTop = 0;
    }

    async notifySlideChange(index) {
        try {
            await fetch('/api/log-notes', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ slide_index: index }),
            });
        } catch (error) {
            // Silently fail - don't interrupt presentation
            console.error('Failed to notify server of slide change:', error);
        }
    }

    nextSlide() {
        if (this.currentSlideIndex < this.totalSlides - 1) {
            this.showSlide(this.currentSlideIndex + 1);
        }
    }

    previousSlide() {
        if (this.currentSlideIndex > 0) {
            this.showSlide(this.currentSlideIndex - 1);
        }
    }

    goToSlide(index) {
        this.showSlide(index);
    }

    toggleFullscreen() {
        if (!document.fullscreenElement) {
            document.documentElement.requestFullscreen();
            this.isFullscreen = true;
            document.body.classList.add('fullscreen');
        } else {
            this.exitFullscreen();
        }
    }

    exitFullscreen() {
        if (document.fullscreenElement) {
            document.exitFullscreen();
        }
        this.isFullscreen = false;
        document.body.classList.remove('fullscreen');
    }

    toggleHelp() {
        this.elements.helpOverlay.classList.toggle('hidden');
    }

    showError(message) {
        this.elements.loading.classList.add('hidden');
        this.elements.error.classList.remove('hidden');
        this.elements.errorMessage.textContent = message;
    }
}

// Initialize the slideshow when the DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    new SlideShow();
});
