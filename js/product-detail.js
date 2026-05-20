// Chart Colors
const productColors = {
    positive: '#4ECDC4',
    neutral: '#95A5A6',
    negative: '#E74C3C'
};

// Sentiment Bar Chart
const barCtx = document.getElementById('sentimentBarChart').getContext('2d');
const sentimentBarChart = new Chart(barCtx, {
    type: 'bar',
    data: {
        labels: ['Positive', 'Neutral', 'Negative'],
        datasets: [{
            data: [65, 25, 15],
            backgroundColor: [
                productColors.positive,
                productColors.neutral,
                productColors.negative
            ],
            borderRadius: 8,
            barThickness: 40
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
                    size: 14
                },
                bodyFont: {
                    size: 13
                },
                callbacks: {
                    label: function(context) {
                        return context.label + ': ' + context.parsed.y + '%';
                    }
                }
            }
        },
        scales: {
            y: {
                beginAtZero: true,
                max: 100,
                ticks: {
                    stepSize: 20,
                    callback: function(value) {
                        return value + '%';
                    },
                    font: {
                        size: 11
                    }
                },
                grid: {
                    color: 'rgba(0, 0, 0, 0.05)',
                    drawBorder: false
                }
            },
            x: {
                grid: {
                    display: false,
                    drawBorder: false
                },
                ticks: {
                    font: {
                        size: 12,
                        weight: '500'
                    }
                }
            }
        }
    }
});

// Add hover effect to keyword badges
document.addEventListener('DOMContentLoaded', function() {
    const keywordBadges = document.querySelectorAll('.keyword-badge');
    
    keywordBadges.forEach(badge => {
        badge.addEventListener('click', function() {
            // Could add functionality to filter by keyword
            console.log('Clicked keyword:', this.textContent);
        });
    });

    // Add click effect to product cards
    const productCards = document.querySelectorAll('.product-card');
    
    productCards.forEach(card => {
        card.style.cursor = 'pointer';
        card.addEventListener('click', function() {
            const productName = this.querySelector('.product-card-name').textContent;
            console.log('Clicked product:', productName);
            // Could navigate to product detail or show modal
        });
    });
});

// Optional: Update chart with animation on window resize
window.addEventListener('resize', () => {
    sentimentBarChart.resize();
});

