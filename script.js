// PC Builder JavaScript - Enhanced Version with Dark Mode & Performance Optimizations

// =====================================
// GLOBAL VARIABLES & DOM ELEMENTS
// =====================================

const elements = {
    // Mobile menu elements
    mobileMenuBtn: document.getElementById('mobileMenuBtn'),
    mobileMenu: document.getElementById('mobileMenu'),
    mobileCategoryBtn: document.getElementById('mobileCategoryBtn'),
    mobileCategoryMenu: document.getElementById('mobileCategoryMenu'),
    mobileCategoryIcon: document.getElementById('mobileCategoryIcon'),
    
    // Dark mode elements
    darkModeToggle: document.getElementById('darkModeToggle'),
    mobileDarkModeToggle: document.getElementById('mobileDarkModeToggle'),
    sunIcon: document.getElementById('sunIcon'),
    moonIcon: document.getElementById('moonIcon'),
    mobileSunIcon: document.getElementById('mobileSunIcon'),
    mobileMoonIcon: document.getElementById('mobileMoonIcon'),
    html: document.documentElement,
    
    // Budget form elements
    budgetForm: document.getElementById('budgetForm'),
    budgetInput: document.getElementById('budgetInput'),
    errorMessage: document.getElementById('errorMessage'),
    usageSelect: document.getElementById('usageSelect'),
    
    // Results elements
    recommendationsSection: document.getElementById('recommendationsSection'),
    budgetDisplay: document.getElementById('budgetDisplay'),
    recommendationCards: document.getElementById('recommendationCards'),
    searchSection: document.getElementById('search-section'),
    
    // Animation elements
    fadeElements: document.querySelectorAll('.fade-in-on-scroll')
};

// Enhanced sample recommendations data with more details
const SAMPLE_RECOMMENDATIONS = [
    {
        category: 'Processor',
        name: 'AMD Ryzen 5 5600X',
        price: 2500000,
        image: '🖥️',
        usage: ['Gaming', 'Design/Video Editing'],
        specs: '6 Cores, 12 Threads, 3.7-4.6GHz',
        performance: 95
    },
    {
        category: 'Processor',
        name: 'Intel Core i5-12400F',
        price: 2300000,
        image: '🖥️',
        usage: ['Gaming', 'Office/Kerja'],
        specs: '6 Cores, 12 Threads, 2.5-4.4GHz',
        performance: 90
    },
    {
        category: 'Processor',
        name: 'AMD Ryzen 3 3300X',
        price: 1800000,
        image: '🖥️',
        usage: ['Office/Kerja', 'Programming'],
        specs: '4 Cores, 8 Threads, 3.8-4.3GHz',
        performance: 75
    },
    {
        category: 'RAM',
        name: 'Corsair Vengeance LPX 16GB DDR4-3200',
        price: 1200000,
        image: '💾',
        usage: ['Gaming', 'Office/Kerja', 'Programming'],
        specs: '16GB (2x8GB) DDR4-3200 CL16',
        performance: 85
    },
    {
        category: 'RAM',
        name: 'G.Skill Ripjaws V 32GB DDR4-3600',
        price: 2200000,
        image: '💾',
        usage: ['Design/Video Editing', 'Programming'],
        specs: '32GB (2x16GB) DDR4-3600 CL18',
        performance: 95
    },
    {
        category: 'RAM',
        name: 'Crucial Ballistix 8GB DDR4-2666',
        price: 600000,
        image: '💾',
        usage: ['Office/Kerja'],
        specs: '8GB (1x8GB) DDR4-2666 CL16',
        performance: 60
    },
    {
        category: 'VGA',
        name: 'NVIDIA RTX 3060 Ti',
        price: 6000000,
        image: '🎮',
        usage: ['Gaming'],
        specs: '8GB GDDR6, 1410-1665MHz',
        performance: 90
    },
    {
        category: 'VGA',
        name: 'NVIDIA RTX 4060',
        price: 5500000,
        image: '🎮',
        usage: ['Gaming', 'Design/Video Editing'],
        specs: '8GB GDDR6, 1830-2460MHz',
        performance: 85
    },
    {
        category: 'VGA',
        name: 'NVIDIA GTX 1650',
        price: 2500000,
        image: '🎮',
        usage: ['Office/Kerja', 'Programming'],
        specs: '4GB GDDR5, 1485-1665MHz',
        performance: 65
    },
    {
        category: 'VGA',
        name: 'AMD RX 6600',
        price: 4200000,
        image: '🎮',
        usage: ['Gaming'],
        specs: '8GB GDDR6, 1968-2491MHz',
        performance: 80
    },
    {
        category: 'PSU',
        name: 'Seasonic Focus GX-650 80+ Gold',
        price: 1500000,
        image: '⚡',
        usage: ['Gaming', 'Office/Kerja', 'Design/Video Editing', 'Programming'],
        specs: '650W, 80+ Gold, Modular',
        performance: 95
    },
    {
        category: 'PSU',
        name: 'Corsair CV450 80+ Bronze',
        price: 800000,
        image: '⚡',
        usage: ['Office/Kerja', 'Programming'],
        specs: '450W, 80+ Bronze, Non-Modular',
        performance: 70
    },
    {
        category: 'Storage',
        name: 'Samsung 970 EVO Plus 1TB NVMe',
        price: 1800000,
        image: '💿',
        usage: ['Gaming', 'Design/Video Editing', 'Programming'],
        specs: '1TB NVMe PCIe 3.0, 3500MB/s Read',
        performance: 95
    },
    {
        category: 'Storage',
        name: 'Kingston NV2 500GB NVMe',
        price: 700000,
        image: '💿',
        usage: ['Office/Kerja', 'Programming'],
        specs: '500GB NVMe PCIe 4.0, 3500MB/s Read',
        performance: 80
    },
    {
        category: 'Storage',
        name: 'WD Blue 1TB HDD',
        price: 600000,
        image: '💿',
        usage: ['Office/Kerja'],
        specs: '1TB 7200RPM SATA III',
        performance: 50
    },
    {
        category: 'Motherboard',
        name: 'MSI B450M PRO-VDH MAX',
        price: 1200000,
        image: '🔧',
        usage: ['Gaming', 'Office/Kerja', 'Programming'],
        specs: 'AMD B450, AM4, mATX, DDR4',
        performance: 75
    },
    {
        category: 'Motherboard',
        name: 'ASUS ROG STRIX B550-F GAMING',
        price: 2500000,
        image: '🔧',
        usage: ['Gaming', 'Design/Video Editing'],
        specs: 'AMD B550, AM4, ATX, DDR4, WiFi',
        performance: 90
    }
];

// Constants
const MIN_BUDGET = 1000000;
const MAX_BUDGET = 100000000;
const CURRENCY_OPTIONS = {
    style: 'currency',
    currency: 'IDR',
    minimumFractionDigits: 0
};

// Performance optimization - debounce function
const debounce = (func, wait) => {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
};

// =====================================
// UTILITY FUNCTIONS
// =====================================

/**
 * Format currency to Indonesian Rupiah
 * @param {number} amount - Amount to format
 * @returns {string} Formatted currency string
 */
function formatCurrency(amount) {
    return new Intl.NumberFormat('id-ID', CURRENCY_OPTIONS).format(amount);
}

/**
 * Smooth scroll to element with offset
 * @param {HTMLElement} element - Element to scroll to
 * @param {number} offset - Offset from top (default: -80 for navbar)
 */
function smoothScrollTo(element, offset = -80) {
    if (element) {
        const elementPosition = element.getBoundingClientRect().top;
        const offsetPosition = elementPosition + window.pageYOffset + offset;

        window.scrollTo({
            top: offsetPosition,
            behavior: 'smooth'
        });
    }
}

/**
 * Toggle element visibility with animation
 * @param {HTMLElement} element - Element to toggle
 * @param {string} className - Class name to toggle (default: 'hidden')
 */
function toggleVisibility(element, className = 'hidden') {
    if (element) {
        element.classList.toggle(className);
    }
}

/**
 * Show/hide error message with animation
 * @param {boolean} show - Whether to show the error
 * @param {string} message - Error message to display
 */
function toggleErrorMessage(show, message = '') {
    if (elements.errorMessage) {
        if (show) {
            elements.errorMessage.textContent = message;
            elements.errorMessage.classList.remove('hidden');
            elements.errorMessage.classList.add('animate-slide-up');
        } else {
            elements.errorMessage.classList.add('hidden');
            elements.errorMessage.classList.remove('animate-slide-up');
        }
    }
}

/**
 * Show loading state
 * @param {HTMLElement} element - Element to show loading in
 */
function showLoading(element) {
    if (element) {
        element.innerHTML = `
            <div class="col-span-full flex justify-center items-center py-12">
                <div class="loading-spinner"></div>
                <span class="ml-3 text-gray-600 dark:text-gray-300">Memuat rekomendasi...</span>
            </div>
        `;
    }
}

// =====================================
// ENHANCED DARK MODE FUNCTIONALITY
// =====================================

/**
 * Initialize dark mode functionality with system preference detection
 */
function initializeDarkMode() {
    // Check for saved theme preference or system preference
    const savedTheme = localStorage.getItem('theme');
    const systemTheme = window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
    
    const theme = savedTheme || systemTheme;
    
    if (theme === 'dark') {
        elements.html.classList.add('dark');
    } else {
        elements.html.classList.remove('dark');
    }
    
    updateDarkModeIcons();
    
    // Desktop dark mode toggle
    if (elements.darkModeToggle) {
        elements.darkModeToggle.addEventListener('click', toggleDarkMode);
    }
    
    // Mobile dark mode toggle
    if (elements.mobileDarkModeToggle) {
        elements.mobileDarkModeToggle.addEventListener('click', toggleDarkMode);
    }
    
    // Listen for system theme changes
    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', (e) => {
        if (!localStorage.getItem('theme')) {
            if (e.matches) {
                elements.html.classList.add('dark');
            } else {
                elements.html.classList.remove('dark');
            }
            updateDarkModeIcons();
        }
    });
}

/**
 * Toggle dark mode with smooth transition
 */
function toggleDarkMode() {
    elements.html.classList.toggle('dark');
    
    // Save preference to localStorage
    const theme = elements.html.classList.contains('dark') ? 'dark' : 'light';
    localStorage.setItem('theme', theme);
    
    updateDarkModeIcons();
    
    // Add a smooth transition effect
    document.body.style.transition = 'background-color 0.3s ease, color 0.3s ease';
    setTimeout(() => {
        document.body.style.transition = '';
    }, 300);
}

/**
 * Update dark mode icons visibility
 */
function updateDarkModeIcons() {
    const isDark = elements.html.classList.contains('dark');
    
    // Update desktop icons
    if (elements.sunIcon && elements.moonIcon) {
        elements.sunIcon.classList.toggle('hidden', isDark);
        elements.sunIcon.classList.toggle('dark:hidden', !isDark);
        elements.moonIcon.classList.toggle('hidden', !isDark);
        elements.moonIcon.classList.toggle('dark:block', isDark);
    }
    
    // Update mobile icons
    if (elements.mobileSunIcon && elements.mobileMoonIcon) {
        elements.mobileSunIcon.classList.toggle('hidden', isDark);
        elements.mobileSunIcon.classList.toggle('dark:hidden', !isDark);
        elements.mobileMoonIcon.classList.toggle('hidden', !isDark);
        elements.mobileMoonIcon.classList.toggle('dark:block', isDark);
    }
}

// =====================================
// MOBILE MENU FUNCTIONALITY
// =====================================

/**
 * Initialize mobile menu functionality with enhanced animations
 */
function initializeMobileMenu() {
    // Mobile menu toggle
    if (elements.mobileMenuBtn && elements.mobileMenu) {
        elements.mobileMenuBtn.addEventListener('click', () => {
            toggleVisibility(elements.mobileMenu);
            
            // Animate hamburger icon
            const icon = elements.mobileMenuBtn.querySelector('svg');
            if (icon) {
                icon.classList.toggle('rotate-90');
            }
        });
    }

    // Mobile category menu toggle
    if (elements.mobileCategoryBtn && elements.mobileCategoryMenu && elements.mobileCategoryIcon) {
        elements.mobileCategoryBtn.addEventListener('click', () => {
            toggleVisibility(elements.mobileCategoryMenu);
            elements.mobileCategoryIcon.classList.toggle('rotate-180');
        });
    }
    
    // Close mobile menu when clicking outside
    document.addEventListener('click', (e) => {
        if (elements.mobileMenu && !elements.mobileMenu.contains(e.target) && 
            !elements.mobileMenuBtn.contains(e.target)) {
            elements.mobileMenu.classList.add('hidden');
        }
    });
}

// =====================================
// SEARCH FUNCTIONALITY
// =====================================

/**
 * Scroll to search section
 */
function scrollToSearch() {
    smoothScrollTo(elements.searchSection);
}

// =====================================
// ENHANCED RECOMMENDATION SYSTEM
// =====================================

/**
 * Filter recommendations based on budget, usage, and performance
 * @param {number} budget - User's budget
 * @param {string} usage - Selected usage type
 * @param {Array} selectedComponents - Selected components
 * @returns {Array} Filtered and sorted recommendations
 */
function filterRecommendations(budget, usage, selectedComponents = []) {
    let filtered = SAMPLE_RECOMMENDATIONS.filter(item => {
        // Filter by usage type
        const matchesUsage = item.usage.includes(usage);
        
        // Filter by selected components
        const matchesComponent = selectedComponents.length === 0 || 
                                selectedComponents.includes(item.category);
        
        // Filter by budget (dynamic budget allocation based on component type)
        let budgetMultiplier = 0.8; // default 80% of budget for individual components
        
        // Adjust budget multiplier based on component importance for usage
        if (usage === 'Gaming' && item.category === 'VGA') {
            budgetMultiplier = 0.6; // Allow higher budget for gaming VGA
        } else if (usage === 'Design/Video Editing' && (item.category === 'RAM' || item.category === 'Processor')) {
            budgetMultiplier = 0.5;
        }
        
        const withinBudget = item.price <= (budget * budgetMultiplier);
        
        return matchesUsage && matchesComponent && withinBudget;
    });
    
    // Sort by performance score (higher is better)
    return filtered.sort((a, b) => b.performance - a.performance);
}

/**
 * Generate enhanced recommendation cards HTML with performance indicators
 * @param {Array} recommendations - Array of recommendation objects
 * @returns {string} HTML string for recommendation cards
 */
function generateRecommendationHTML(recommendations) {
    if (recommendations.length === 0) {
        return `
            <div class="col-span-full text-center py-12">
                <div class="text-6xl mb-4">🔍</div>
                <p class="text-gray-500 dark:text-gray-400 text-lg mb-2">Tidak ada rekomendasi yang sesuai</p>
                <p class="text-gray-400 dark:text-gray-500 text-sm">Coba tingkatkan budget atau ubah kategori penggunaan</p>
            </div>
        `;
    }

    return recommendations.map(item => {
        const performanceColor = item.performance >= 90 ? 'green' : 
                               item.performance >= 75 ? 'yellow' : 'red';
        
        return `
            <div class="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-6 transition-all duration-300 hover:scale-105 hover:shadow-xl dark:hover:shadow-2xl border border-gray-100 dark:border-gray-700 group">
                <div class="text-4xl mb-4 text-center group-hover:animate-bounce-subtle">${item.image}</div>
                
                <!-- Performance Indicator -->
                <div class="flex items-center justify-between mb-3">
                    <span class="text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wide">${item.category}</span>
                    <div class="flex items-center">
                        <div class="w-2 h-2 rounded-full bg-${performanceColor}-400 mr-1"></div>
                        <span class="text-xs text-gray-500 dark:text-gray-400">${item.performance}%</span>
                    </div>
                </div>
                
                <h3 class="font-semibold text-gray-900 dark:text-white mb-2 text-lg leading-tight">${item.name}</h3>
                <p class="text-sm text-gray-600 dark:text-gray-300 mb-3 line-clamp-2">${item.specs}</p>
                
                <div class="flex items-center justify-between mb-4">
                    <p class="font-bold text-blue-600 dark:text-blue-400 text-lg">${formatCurrency(item.price)}</p>
                </div>
                
                <div class="flex flex-wrap gap-1">
                    ${item.usage.map(use => `
                        <span class="inline-block bg-blue-100 dark:bg-blue-900 text-blue-800 dark:text-blue-200 text-xs px-2 py-1 rounded-full">
                            ${use}
                        </span>
                    `).join('')}
                </div>
            </div>
        `;
    }).join('');
}

/**
 * Generate recommendations with loading animation
 * @param {number} budget - User's budget
 */
function generateRecommendations(budget) {
    const selectedUsage = elements.usageSelect?.value || 'Office/Kerja';
    
    // Get selected components
    const checkboxes = elements.budgetForm?.querySelectorAll('input[type="checkbox"]:checked') || [];
    const selectedComponents = Array.from(checkboxes).map(cb => 
        cb.parentElement.textContent.trim()
    );
    
    // Show loading state
    if (elements.recommendationCards) {
        showLoading(elements.recommendationCards);
    }
    
    // Simulate API call delay for better UX
    setTimeout(() => {
        const filteredRecommendations = filterRecommendations(budget, selectedUsage, selectedComponents);
        
        if (elements.recommendationCards) {
            elements.recommendationCards.innerHTML = generateRecommendationHTML(filteredRecommendations);
        }
    }, 800);
}

// =====================================
// ENHANCED BUDGET FORM HANDLING
// =====================================

/**
 * Enhanced budget validation with detailed feedback
 * @param {string} budgetValue - Budget input value
 * @returns {Object} Validation result
 */
function validateBudget(budgetValue) {
    const budget = parseInt(budgetValue.replace(/\D/g, ''));
    
    if (!budgetValue || isNaN(budget)) {
        return { valid: false, error: 'Mohon masukkan budget yang valid (hanya angka)' };
    }
    
    if (budget < MIN_BUDGET) {
        return { 
            valid: false, 
            error: `Budget minimum adalah ${formatCurrency(MIN_BUDGET)}` 
        };
    }
    
    if (budget > MAX_BUDGET) {
        return { 
            valid: false, 
            error: `Budget maksimum adalah ${formatCurrency(MAX_BUDGET)}` 
        };
    }
    
    return { valid: true, budget };
}

/**
 * Handle budget form submission with enhanced validation
 * @param {Event} event - Form submit event
 */
function handleBudgetSubmit(event) {
    event.preventDefault();
    
    const budgetValue = elements.budgetInput?.value;
    const usageValue = elements.usageSelect?.value;
    
    // Validate budget
    const validation = validateBudget(budgetValue);
    
    if (!validation.valid) {
        toggleErrorMessage(true, validation.error);
        elements.budgetInput?.focus();
        return;
    }
    
    // Validate usage selection
    if (!usageValue) {
        toggleErrorMessage(true, 'Mohon pilih kegunaan komputer Anda');
        elements.usageSelect?.focus();
        return;
    }
    
    // Hide error message
    toggleErrorMessage(false);
    
    // Update budget display with usage info
    if (elements.budgetDisplay) {
        elements.budgetDisplay.innerHTML = `
            <span class="font-semibold">Budget:</span> ${formatCurrency(validation.budget)} • 
            <span class="font-semibold">Kegunaan:</span> ${usageValue}
        `;
    }
    
    // Show recommendations section with animation
    if (elements.recommendationsSection) {
        elements.recommendationsSection.classList.remove('hidden');
        elements.recommendationsSection.classList.add('animate-fade-in');
    }
    
    // Generate recommendations
    generateRecommendations(validation.budget);
    
    // Scroll to recommendations after a short delay
    setTimeout(() => {
        smoothScrollTo(elements.recommendationsSection);
    }, 300);
}

/**
 * Format budget input in real-time
 */
const formatBudgetInput = debounce((event) => {
    const input = event.target;
    const value = input.value.replace(/\D/g, '');
    const formatted = value.replace(/\B(?=(\d{3})+(?!\d))/g, '.');
    input.value = formatted;
}, 300);

/**
 * Initialize enhanced budget form functionality
 */
function initializeBudgetForm() {
    if (elements.budgetForm) {
        elements.budgetForm.addEventListener('submit', handleBudgetSubmit);
    }
    
    // Add real-time validation and formatting
    if (elements.budgetInput) {
        elements.budgetInput.addEventListener('input', (event) => {
            toggleErrorMessage(false);
            formatBudgetInput(event);
        });
        
        // Add placeholder animation
        elements.budgetInput.addEventListener('focus', () => {
            elements.budgetInput.classList.add('ring-2', 'ring-blue-500');
        });
        
        elements.budgetInput.addEventListener('blur', () => {
            elements.budgetInput.classList.remove('ring-2', 'ring-blue-500');
        });
    }
}

// =====================================
// ENHANCED SCROLL ANIMATIONS
// =====================================

/**
 * Initialize enhanced scroll animations with stagger effect
 */
function initializeScrollAnimations() {
    if (elements.fadeElements.length === 0) return;
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach((entry, index) => {
            if (entry.isIntersecting) {
                // Add stagger delay for multiple elements
                setTimeout(() => {
                    entry.target.classList.add('visible');
                }, index * 100);
                
                observer.unobserve(entry.target);
            }
        });
    }, {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    });
    
    elements.fadeElements.forEach(element => {
        observer.observe(element);
    });
}

// =====================================
// PERFORMANCE MONITORING
// =====================================

/**
 * Log performance metrics
 */
function logPerformance() {
    if (window.performance && window.performance.timing) {
        const timing = window.performance.timing;
        const loadTime = timing.loadEventEnd - timing.navigationStart;
        console.log(`✅ ByteBudget loaded in ${loadTime}ms`);
    }
}

// =====================================
// INITIALIZATION
// =====================================

/**
 * Initialize all functionality when DOM is loaded
 */
function initializeApp() {
    try {
        console.log('🚀 Initializing ByteBudget...');
        
        initializeDarkMode();
        initializeMobileMenu();
        initializeBudgetForm();
        initializeScrollAnimations();
        
        // Log performance after everything is loaded
        setTimeout(logPerformance, 100);
        
        console.log('✅ ByteBudget initialized successfully with enhanced features');
    } catch (error) {
        console.error('❌ Error initializing ByteBudget:', error);
    }
}

// =====================================
// EVENT LISTENERS & INITIALIZATION
// =====================================

// Initialize when DOM is fully loaded
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initializeApp);
} else {
    initializeApp();
}

// Make functions globally available
window.scrollToSearch = scrollToSearch;
window.toggleDarkMode = toggleDarkMode;

// Add keyboard shortcuts
document.addEventListener('keydown', (e) => {
    // Ctrl/Cmd + D to toggle dark mode
    if ((e.ctrlKey || e.metaKey) && e.key === 'd') {
        e.preventDefault();
        toggleDarkMode();
    }
    
    // Escape to close mobile menu
    if (e.key === 'Escape' && elements.mobileMenu && !elements.mobileMenu.classList.contains('hidden')) {
        toggleVisibility(elements.mobileMenu);
    }
});