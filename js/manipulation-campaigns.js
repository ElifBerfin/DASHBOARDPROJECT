// Chart Colors
const campaignColors = {
    fakeDiscount: '#4A90E2',
    limitedStock: '#FF9800',
    botActivity: '#4CAF50',
    fakeCoupon: '#E74C3C'
};

// Manipulation Types Pie Chart
const pieCtx = document.getElementById('manipulationPieChart').getContext('2d');
const manipulationPieChart = new Chart(pieCtx, {
    type: 'pie',
    data: {
        labels: ['Fake Discounts', 'Limited Stock Press', 'Bot Activity', 'Fake Coupons'],
        datasets: [{
            data: [37, 23, 22, 18],
            backgroundColor: [
                campaignColors.fakeDiscount,
                campaignColors.limitedStock,
                campaignColors.botActivity,
                campaignColors.fakeCoupon
            ],
            borderWidth: 3,
            borderColor: '#FFFFFF'
        }]
    },
    options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: {
                display: false
            },
            tooltip: {
                backgroundColor: 'rgba(0, 0, 0, 0.8)',
                padding: 12,
                titleFont: {
                    size: 14,
                    weight: '600'
                },
                bodyFont: {
                    size: 13
                },
                callbacks: {
                    label: function(context) {
                        return context.label + ': ' + context.parsed + '%';
                    }
                }
            }
        }
    }
});

// Add hover effects to table rows
document.addEventListener('DOMContentLoaded', function() {
    const tableRows = document.querySelectorAll('.campaigns-table tbody tr');
    
    tableRows.forEach(row => {
        row.style.cursor = 'pointer';
        
        row.addEventListener('click', function() {
            const campaign = this.querySelector('.campaign-badge').textContent;
            const type = this.querySelector('.type-badge').textContent;
            const confidence = this.querySelector('.confidence-value').textContent;
            
            console.log('Campaign Details:', {
                campaign: campaign,
                type: type,
                confidence: confidence
            });
            
            // Could show a modal or navigate to details page
        });
    });

    // Animate confidence bars on load
    const confidenceFills = document.querySelectorAll('.confidence-fill');
    
    confidenceFills.forEach(fill => {
        const targetWidth = fill.style.width;
        fill.style.width = '0%';
        
        setTimeout(() => {
            fill.style.width = targetWidth;
        }, 100);
    });

    // Add info card click handlers
    const infoCards = document.querySelectorAll('.info-card');
    
    infoCards.forEach(card => {
        card.style.cursor = 'pointer';
        
        card.addEventListener('click', function() {
            const percentage = this.querySelector('h4').textContent;
            const type = this.querySelector('p').textContent;
            
            console.log('Clicked:', type, '-', percentage);
            // Could filter the table by this type
        });
    });
});

// Optional: Update chart with animation on window resize
window.addEventListener('resize', () => {
    manipulationPieChart.resize();
});

// Function to update confidence bars dynamically (example)
function updateConfidenceBars(newData) {
    const confidenceFills = document.querySelectorAll('.confidence-fill');
    
    confidenceFills.forEach((fill, index) => {
        if (newData[index]) {
            fill.style.width = (newData[index] * 100) + '%';
        }
    });
}

// Function to highlight campaigns by type
function filterByType(type) {
    const rows = document.querySelectorAll('.campaigns-table tbody tr');
    
    rows.forEach(row => {
        const typeBadge = row.querySelector('.type-badge');
        const badgeText = typeBadge.textContent.toLowerCase();
        
        if (type === 'all' || badgeText.includes(type.toLowerCase())) {
            row.style.display = '';
            row.style.opacity = '1';
        } else {
            row.style.opacity = '0.3';
        }
    });
}

// Add search functionality (optional)
function searchCampaigns(searchTerm) {
    const rows = document.querySelectorAll('.campaigns-table tbody tr');
    
    rows.forEach(row => {
        const campaign = row.querySelector('.campaign-badge').textContent.toLowerCase();
        
        if (campaign.includes(searchTerm.toLowerCase())) {
            row.style.display = '';
        } else {
            row.style.display = 'none';
        }
    });
}

