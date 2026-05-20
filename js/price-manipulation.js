// Chart Colors
const manipulationColors = {
    warning: '#FF9800',
    inflation: '#FF6B35',
    suspicious: '#D84315',
    fake: '#FF1744',
    inflated: '#FF7043',
    real: '#42A5F5',
    limited: '#FFB74D',
    fakeDiscount: '#FF6B35'
};

// Horizontal Bar Chart - Top Manipulated Products
const barCtx = document.getElementById('barChart').getContext('2d');
const barChart = new Chart(barCtx, {
    type: 'bar',
    data: {
        labels: ['New Balance 530', 'ON Running Cloudin', 'Adidas Run Falcon 2', 'Nike Air Max 270', 'Puma X-Cell Lightspeed'],
        datasets: [
            {
                label: 'Real posts related to manipulated pricing',
                data: [900, 850, 400, 250, 180],
                backgroundColor: manipulationColors.inflation,
                borderRadius: 6,
                barThickness: 25
            },
            {
                label: 'Fake Discount',
                data: [852, 0, 350, 150, 120],
                backgroundColor: manipulationColors.fake,
                borderRadius: 6,
                barThickness: 25
            }
        ]
    },
    options: {
        indexAxis: 'y',
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
                    size: 13
                },
                bodyFont: {
                    size: 12
                },
                callbacks: {
                    label: function(context) {
                        return context.dataset.label + ': ' + context.parsed.x.toLocaleString();
                    }
                }
            }
        },
        scales: {
            x: {
                stacked: true,
                max: 2000,
                ticks: {
                    stepSize: 500,
                    font: {
                        size: 11
                    }
                },
                grid: {
                    color: 'rgba(0, 0, 0, 0.05)'
                }
            },
            y: {
                stacked: true,
                ticks: {
                    font: {
                        size: 11
                    }
                },
                grid: {
                    display: false
                }
            }
        }
    }
});

// Add annotations for specific products
const createProductAnnotations = () => {
    // This would be enhanced with Chart.js annotation plugin
    // For now, we'll use simple labels
};

// Line Chart - Before-After Price Trend
const trendCtx = document.getElementById('trendChart').getContext('2d');
const trendChart = new Chart(trendCtx, {
    type: 'line',
    data: {
        labels: ['Apr 1', 'Apr 11', 'Apr 12', 'Apr 24', 'Apr 24', 'Apr 30'],
        datasets: [
            {
                label: 'Inflated',
                data: [950, 980, 1050, 1150, 1200, 1150],
                borderColor: manipulationColors.inflated,
                backgroundColor: 'rgba(255, 112, 67, 0.1)',
                tension: 0.4,
                borderWidth: 3,
                pointRadius: 5,
                pointHoverRadius: 7,
                pointBackgroundColor: manipulationColors.inflated,
                pointBorderColor: '#FFFFFF',
                pointBorderWidth: 2,
                fill: false,
                borderDash: [5, 5]
            },
            {
                label: 'Real price',
                data: [1000, 1020, 1030, 1050, 1070, 1080],
                borderColor: manipulationColors.real,
                backgroundColor: 'rgba(66, 165, 245, 0.1)',
                tension: 0.4,
                borderWidth: 3,
                pointRadius: 5,
                pointHoverRadius: 7,
                pointBackgroundColor: manipulationColors.real,
                pointBorderColor: '#FFFFFF',
                pointBorderWidth: 2,
                fill: false
            },
            {
                label: 'Limited Stock Pressure',
                data: [850, 880, 920, 950, 980, 1000],
                borderColor: manipulationColors.limited,
                backgroundColor: 'rgba(255, 183, 77, 0.1)',
                tension: 0.4,
                borderWidth: 2,
                pointRadius: 4,
                pointHoverRadius: 6,
                pointBackgroundColor: manipulationColors.limited,
                pointBorderColor: '#FFFFFF',
                pointBorderWidth: 2,
                fill: false,
                borderDash: [2, 2]
            }
        ]
    },
    options: {
        responsive: true,
        maintainAspectRatio: false,
        interaction: {
            mode: 'index',
            intersect: false,
        },
        plugins: {
            legend: {
                position: 'bottom',
                align: 'center',
                labels: {
                    padding: 15,
                    font: {
                        size: 11,
                        family: "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif"
                    },
                    usePointStyle: true,
                    pointStyle: 'circle',
                    boxWidth: 8,
                    boxHeight: 8
                }
            },
            tooltip: {
                backgroundColor: 'rgba(0, 0, 0, 0.8)',
                padding: 12,
                titleFont: {
                    size: 13
                },
                bodyFont: {
                    size: 12
                },
                callbacks: {
                    label: function(context) {
                        return context.dataset.label + ': ' + context.parsed.y.toLocaleString() + ' ₺';
                    }
                }
            }
        },
        scales: {
            y: {
                beginAtZero: false,
                min: 0,
                max: 1600,
                ticks: {
                    stepSize: 200,
                    callback: function(value) {
                        return value.toLocaleString();
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
                        size: 10
                    }
                }
            }
        }
    }
});

// Add annotation for current price
const addPriceAnnotation = () => {
    // Create a text element to show current price
    const priceLabel = document.createElement('div');
    priceLabel.style.cssText = `
        position: absolute;
        right: 50px;
        top: 120px;
        background: white;
        padding: 8px 12px;
        border-radius: 6px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        font-size: 16px;
        font-weight: 600;
        color: ${manipulationColors.real};
    `;
    priceLabel.textContent = '1,190 ₺';
};

// Optional: Update charts with animation on window resize
window.addEventListener('resize', () => {
    barChart.resize();
    trendChart.resize();
});

// Initialize annotations
createProductAnnotations();

