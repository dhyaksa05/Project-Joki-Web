// Mobile menu toggle
const mobileMenuBtn = document.getElementById('mobileMenuBtn');
const mobileMenu = document.getElementById('mobileMenu');

mobileMenuBtn.addEventListener('click', () => {
    mobileMenu.classList.toggle('hidden');
});

// Mobile category toggle
const mobileCategoryBtn = document.getElementById('mobileCategoryBtn');
const mobileCategoryMenu = document.getElementById('mobileCategoryMenu');
const mobileCategoryIcon = document.getElementById('mobileCategoryIcon');

mobileCategoryBtn.addEventListener('click', () => {
    mobileCategoryMenu.classList.toggle('hidden');
    mobileCategoryIcon.classList.toggle('rotate-180');
});

// Scroll to search function
function scrollToSearch() {
    document.getElementById('searchSection').scrollIntoView({
        behavior: 'smooth'
    });
}

// Budget form handling
const budgetForm = document.getElementById('budgetForm');
const budgetInput = document.getElementById('budgetInput');
const errorMessage = document.getElementById('errorMessage');
const recommendationsSection = document.getElementById('recommendationsSection');
const budgetDisplay = document.getElementById('budgetDisplay');
const recommendationCards = document.getElementById('recommendationCards');
const usageSelect = document.getElementById('usageSelect'); // Added usage select element

budgetForm.addEventListener('submit', (e) => {
    e.preventDefault();
    
    const budget = parseInt(budgetInput.value);
    
    // Validate budget input
    if (!budget || budget < 1000000) {
        errorMessage.classList.remove('hidden');
        return;
    }
    
    errorMessage.classList.add('hidden');

    // Format budget display
    const formattedBudget = new Intl.NumberFormat('id-ID', {
        style: 'currency',
        currency: 'IDR',
        minimumFractionDigits: 0
    }).format(budget);
    
    budgetDisplay.textContent = `Budget: ${formattedBudget}`;
    
    recommendationsSection.classList.remove('hidden');
    
    // Generate recommendations based on budget and usage
    generateRecommendations(budget);
    
    // Scroll to recommendations
    recommendationsSection.scrollIntoView({
        behavior: 'smooth'
    });
});

// Generate recommendations based on budget and selected usage
function generateRecommendations(budget) {
    const selectedUsage = usageSelect.value; // Get the selected usage
    let filteredRecommendations = [];

    // Sample data with usage types
    const sampleRecommendations = [
        {
            category: 'Processor',
            name: 'AMD Ryzen 5 5600X',
            price: 'Rp 2.500.000',
            image: '🖥️',
            usage: ['Gaming', 'Design/Video Editing']
        },
        {
            category: 'RAM',
            name: 'Corsair Vengeance 16GB',
            price: 'Rp 1.200.000',
            image: '💾',
            usage: ['Gaming', 'Office/Kerja']
        },
        {
            category: 'VGA',
            name: 'RTX 3060 Ti',
            price: 'Rp 6.000.000',
            image: '🎮',
            usage: ['Gaming']
        },
        {
            category: 'PSU',
            name: 'Seasonic 650W Gold',
            price: 'Rp 1.500.000',
            image: '⚡',
            usage: ['Office/Kerja', 'Design/Video Editing']
        },
        {
            category: 'Storage',
            name: 'Samsung 970 EVO 1TB',
            price: 'Rp 1.800.000',
            image: '💿',
            usage: ['Office/Kerja', 'Programming']
        }
    ];

    // Filter recommendations based on the selected usage
    filteredRecommendations = sampleRecommendations.filter(item => item.usage.includes(selectedUsage));
    
    recommendationCards.innerHTML = filteredRecommendations.map(item => `
        <div class="bg-white rounded-lg shadow-lg p-6 transition-transform duration-300 hover:scale-105">
            <div class="text-4xl mb-4 text-center">${item.image}</div>
            <h3 class="font-semibold text-gray-900 mb-2">${item.category}</h3>
            <p class="text-sm text-gray-600 mb-2">${item.name}</p>
            <p class="font-bold text-blue-600">${item.price}</p>
        </div>
    `).join('');
}
