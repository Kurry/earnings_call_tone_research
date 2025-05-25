// Interactive JavaScript for earnings call research site

// Performance metrics animation
document.addEventListener('DOMContentLoaded', function() {
    // Animate performance metrics on scroll
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.animation = 'fadeInUp 0.6s ease-out';
                entry.target.style.opacity = '1';
            }
        });
    }, observerOptions);

    // Observe all performance metric boxes
    document.querySelectorAll('.performance-metric').forEach(metric => {
        metric.style.opacity = '0';
        observer.observe(metric);
    });

    // Interactive quintile visualization
    createQuintileVisualization();
    
    // Table sorting functionality
    addTableSorting();
});

// Create interactive quintile performance chart
function createQuintileVisualization() {
    const quintileData = [
        { quintile: 'Q1', return: 1.683, description: 'Highest Dispersion' },
        { quintile: 'Q2', return: 2.5, description: 'High Dispersion' },
        { quintile: 'Q3', return: 3.0, description: 'Medium Dispersion' },
        { quintile: 'Q4', return: 3.8, description: 'Low Dispersion' },
        { quintile: 'Q5', return: 4.748, description: 'Lowest Dispersion' }
    ];

    const container = document.getElementById('quintile-chart');
    if (!container) return;

    const maxReturn = Math.max(...quintileData.map(d => d.return));
    
    quintileData.forEach((data, index) => {
        const bar = document.createElement('div');
        bar.className = `quintile-bar q${index + 1}`;
        bar.style.height = `${(data.return / maxReturn) * 150}px`;
        bar.innerHTML = `
            <div>${data.quintile}</div>
            <div style="font-size: 0.7rem; margin-top: 0.5rem;">${data.return.toFixed(1)} bps</div>
        `;
        
        // Add hover tooltip
        bar.title = `${data.description}: ${data.return.toFixed(3)} bps return`;
        
        // Add click interaction
        bar.addEventListener('click', function() {
            showQuintileDetails(data);
        });
        
        container.appendChild(bar);
    });
}

// Show detailed quintile information
function showQuintileDetails(data) {
    const modal = document.createElement('div');
    modal.className = 'quintile-modal';
    modal.innerHTML = `
        <div class="modal-content">
            <span class="close">&times;</span>
            <h3>Quintile ${data.quintile} Details</h3>
            <p><strong>Description:</strong> ${data.description}</p>
            <p><strong>5-Day Return:</strong> ${data.return.toFixed(3)} bps</p>
            <p><strong>Interpretation:</strong> ${getQuintileInterpretation(data.quintile)}</p>
        </div>
    `;
    
    document.body.appendChild(modal);
    modal.style.display = 'block';
    
    // Close modal functionality
    modal.querySelector('.close').onclick = function() {
        document.body.removeChild(modal);
    };
    
    modal.onclick = function(event) {
        if (event.target === modal) {
            document.body.removeChild(modal);
        }
    };
}

function getQuintileInterpretation(quintile) {
    const interpretations = {
        'Q1': 'Stocks with highest tone dispersion (uncertainty) show the lowest returns.',
        'Q2': 'High dispersion stocks with moderate underperformance.',
        'Q3': 'Medium dispersion stocks with average market performance.',
        'Q4': 'Low dispersion stocks beginning to show outperformance.',
        'Q5': 'Stocks with lowest tone dispersion (certainty) show the highest returns.'
    };
    return interpretations[quintile] || 'Performance analysis for this quintile.';
}

// Add table sorting functionality
function addTableSorting() {
    document.querySelectorAll('.table-performance th').forEach(header => {
        header.style.cursor = 'pointer';
        header.addEventListener('click', function() {
            sortTable(this);
        });
    });
}

function sortTable(header) {
    const table = header.closest('table');
    const columnIndex = Array.from(header.parentNode.children).indexOf(header);
    const rows = Array.from(table.querySelectorAll('tbody tr'));
    
    const isNumeric = rows.every(row => {
        const cell = row.children[columnIndex];
        return cell && !isNaN(parseFloat(cell.textContent.replace(/[^\d.-]/g, '')));
    });
    
    const direction = header.classList.contains('sort-asc') ? 'desc' : 'asc';
    
    // Remove sort classes from all headers
    table.querySelectorAll('th').forEach(th => {
        th.classList.remove('sort-asc', 'sort-desc');
    });
    
    // Add sort class to current header
    header.classList.add(`sort-${direction}`);
    
    rows.sort((a, b) => {
        const aVal = a.children[columnIndex].textContent.trim();
        const bVal = b.children[columnIndex].textContent.trim();
        
        if (isNumeric) {
            const aNum = parseFloat(aVal.replace(/[^\d.-]/g, ''));
            const bNum = parseFloat(bVal.replace(/[^\d.-]/g, ''));
            return direction === 'asc' ? aNum - bNum : bNum - aNum;
        } else {
            return direction === 'asc' ? aVal.localeCompare(bVal) : bVal.localeCompare(aVal);
        }
    });
    
    // Reinsert sorted rows
    const tbody = table.querySelector('tbody');
    rows.forEach(row => tbody.appendChild(row));
}

// Performance metrics counter animation
function animateCounter(element, target, duration = 2000) {
    const start = 0;
    const increment = target / (duration / 16);
    let current = start;
    
    const timer = setInterval(() => {
        current += increment;
        if (current >= target) {
            current = target;
            clearInterval(timer);
        }
        element.textContent = current.toFixed(3);
    }, 16);
}

// Smooth scrolling for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// Add CSS for modal and animations
const style = document.createElement('style');
style.textContent = `
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .quintile-modal {
        display: none;
        position: fixed;
        z-index: 1000;
        left: 0;
        top: 0;
        width: 100%;
        height: 100%;
        background-color: rgba(0,0,0,0.5);
    }
    
    .modal-content {
        background-color: #fefefe;
        margin: 15% auto;
        padding: 20px;
        border-radius: 8px;
        width: 80%;
        max-width: 500px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.3);
    }
    
    .close {
        color: #aaa;
        float: right;
        font-size: 28px;
        font-weight: bold;
        cursor: pointer;
    }
    
    .close:hover {
        color: #000;
    }
    
    .sort-asc::after {
        content: ' ↑';
    }
    
    .sort-desc::after {
        content: ' ↓';
    }
    
    .quintile-bar {
        transition: all 0.3s ease;
        cursor: pointer;
    }
    
    .quintile-bar:hover {
        transform: scale(1.05);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
`;
document.head.appendChild(style);