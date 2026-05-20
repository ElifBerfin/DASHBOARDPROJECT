// Chart Colors
const chartColors = {
    positive: '#4ECDC4',
    neutral: '#95A5A6',
    negative: '#E74C3C',
};

// Pie Chart - Sentiment Distribution
const pieCtx = document.getElementById('pieChart').getContext('2d');
const pieChart = new Chart(pieCtx, {
    type: 'pie',
    data: {
        labels: ['Positive', 'Negative', 'Neutral'],
        datasets: [{
            data: [64, 15, 21],
            backgroundColor: [
                chartColors.positive,
                chartColors.negative,
                chartColors.neutral
            ],
            borderWidth: 2,
            borderColor: '#FFFFFF'
        }]
    },
    options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: {
                position: 'right',
                labels: {
                    padding: 20,
                    font: {
                        size: 13,
                        family: "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif"
                    },
                    usePointStyle: true,
                    pointStyle: 'circle'
                }
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
                        return context.label + ': ' + context.parsed + '%';
                    }
                }
            }
        }
    }
});

// Line Chart - Sentiment Trend
const lineCtx = document.getElementById('lineChart').getContext('2d');
const lineChart = new Chart(lineCtx, {
    type: 'line',
    data: {
        labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
        datasets: [
            {
                label: 'Positive',
                data: [55, 48, 52, 45, 50, 52],
                borderColor: chartColors.positive,
                backgroundColor: 'rgba(78, 205, 196, 0.1)',
                tension: 0.4,
                borderWidth: 2,
                pointRadius: 4,
                pointHoverRadius: 6,
                pointBackgroundColor: chartColors.positive,
                pointBorderColor: '#FFFFFF',
                pointBorderWidth: 2,
                fill: false
            },
            {
                label: 'Negative',
                data: [35, 40, 38, 42, 38, 35],
                borderColor: chartColors.negative,
                backgroundColor: 'rgba(231, 76, 60, 0.1)',
                tension: 0.4,
                borderWidth: 2,
                pointRadius: 4,
                pointHoverRadius: 6,
                pointBackgroundColor: chartColors.negative,
                pointBorderColor: '#FFFFFF',
                pointBorderWidth: 2,
                fill: false
            },
            {
                label: 'Neutral',
                data: [30, 28, 25, 28, 30, 32],
                borderColor: chartColors.neutral,
                backgroundColor: 'rgba(149, 165, 166, 0.1)',
                tension: 0.4,
                borderWidth: 2,
                pointRadius: 4,
                pointHoverRadius: 6,
                pointBackgroundColor: chartColors.neutral,
                pointBorderColor: '#FFFFFF',
                pointBorderWidth: 2,
                fill: false
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
                position: 'top',
                align: 'end',
                labels: {
                    padding: 15,
                    font: {
                        size: 12,
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
                    size: 14
                },
                bodyFont: {
                    size: 13
                },
                callbacks: {
                    label: function(context) {
                        return context.dataset.label + ': ' + context.parsed.y + '%';
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
                        size: 11
                    }
                }
            }
        }
    }
});

// Optional: Update charts with animation on window resize
window.addEventListener('resize', () => {
    pieChart.resize();
    lineChart.resize();
});

