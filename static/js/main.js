// Countdown Timer Logic
const runCountdown = () => {
    // Set Tournament Date to March 31, 2026, 11:00 AM IST
    const countToDate = new Date("March 31, 2026 11:00:00").getTime();
    
    // Check if elements exist
    const daysEl = document.getElementById('days');
    if (!daysEl) return;

    setInterval(() => {
        const currentDate = new Date().getTime();
        const difference = countToDate - currentDate;

        if (difference < 0) {
            daysEl.innerText = "00";
            document.getElementById('hours').innerText = "00";
            document.getElementById('minutes').innerText = "00";
            document.getElementById('seconds').innerText = "00";
            return;
        }

        const days = Math.floor(difference / (1000 * 60 * 60 * 24));
        const hours = Math.floor((difference % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
        const minutes = Math.floor((difference % (1000 * 60 * 60)) / (1000 * 60));
        const seconds = Math.floor((difference % (1000 * 60)) / 1000);

        daysEl.innerText = days < 10 ? '0' + days : days;
        document.getElementById('hours').innerText = hours < 10 ? '0' + hours : hours;
        document.getElementById('minutes').innerText = minutes < 10 ? '0' + minutes : minutes;
        document.getElementById('seconds').innerText = seconds < 10 ? '0' + seconds : seconds;
    }, 1000);
};

// Scroll Reveal Animation
const runReveal = () => {
    const reveals = document.querySelectorAll('.reveal');
    const windowHeight = window.innerHeight;
    const elementVisible = 150;

    reveals.forEach((reveal) => {
        const elementTop = reveal.getBoundingClientRect().top;
        if (elementTop < windowHeight - elementVisible) {
            reveal.classList.add('active');
        }
    });
};

// Simple Particle System Generator
const createParticles = () => {
    const container = document.getElementById('particles-container');
    if (!container) return;
    
    const colors = ['#ff3b3b', '#ff7a18', '#ffffff'];
    const particleCount = 50;
    
    for (let i = 0; i < particleCount; i++) {
        const particle = document.createElement('div');
        particle.style.position = 'absolute';
        
        // Random size between 2px and 6px
        const size = Math.random() * 4 + 2;
        particle.style.width = `${size}px`;
        particle.style.height = `${size}px`;
        particle.style.borderRadius = '50%';
        
        // Random color
        particle.style.backgroundColor = colors[Math.floor(Math.random() * colors.length)];
        
        // Random position
        particle.style.left = `${Math.random() * 100}vw`;
        particle.style.top = `${Math.random() * 100}vh`;
        
        // Random opacity
        particle.style.opacity = Math.random() * 0.4 + 0.1;
        
        // Float animation properties
        const duration = Math.random() * 20 + 15;
        const delay = Math.random() * -20; // negative delay to start mid-animation
        
        particle.style.animation = `floatParticle ${duration}s ease-in-out infinite`;
        particle.style.animationDelay = `${delay}s`;
        
        // Add glow occasionally
        if (Math.random() > 0.7) {
            particle.style.boxShadow = `0 0 ${size * 3}px ${particle.style.backgroundColor}`;
        }
        
        container.appendChild(particle);
    }
    
    // Add particle keyframes to doc only once
    if (!document.getElementById('particle-style')) {
        const style = document.createElement('style');
        style.id = 'particle-style';
        style.innerHTML = `
            @keyframes floatParticle {
                0% { transform: translate(0, 0); }
                33% { transform: translate(${Math.random() * 80 - 40}px, ${Math.random() * -80 - 40}px); }
                66% { transform: translate(${Math.random() * 80 - 40}px, ${Math.random() * -80 - 40}px); }
                100% { transform: translate(0, 0); }
            }
        `;
        document.head.appendChild(style);
    }
};

// Form Validation
const enhanceForms = () => {
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', (e) => {
            const btn = form.querySelector('button[type="submit"]');
            if (btn && form.checkValidity()) {
                const originalText = btn.innerHTML;
                btn.innerHTML = '<i class="fas fa-spinner fa-spin mr-2"></i> Processing...';
                btn.style.opacity = '0.8';
                btn.style.pointerEvents = 'none';
                
                // Form will still submit natively
            }
        });
    });
}

// Wait for DOM
document.addEventListener('DOMContentLoaded', () => {
    runCountdown();
    createParticles();
    enhanceForms();
    
    // Initial check for reveals 
    runReveal();
    // Subsequent checks on scroll
    window.addEventListener('scroll', runReveal);
});
