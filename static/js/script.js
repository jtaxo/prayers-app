document.addEventListener('DOMContentLoaded', () => {
    
    // 1. Mouse Follow Radial Glow
    const glow = document.getElementById('ambient-glow');
    if (glow) {
        window.addEventListener('mousemove', (e) => {
            requestAnimationFrame(() => {
                glow.style.transform = `translate(${e.clientX}px, ${e.clientY}px) translate(-50%, -50%)`;
            });
        });
    }

    // 2. Floating Particles Generation
    const container = document.getElementById('particles-container');
    if (container) {
        const isMobile = window.innerWidth <= 900;
        const particleCount = isMobile ? 8 : 30;
        for (let i = 0; i < particleCount; i++) {
            const particle = document.createElement('div');
            particle.classList.add('particle');
            
            // Random size between 1 and 4px
            const size = Math.random() * 3 + 1;
            particle.style.width = `${size}px`;
            particle.style.height = `${size}px`;
            
            // Random start position
            particle.style.left = `${Math.random() * 100}vw`;
            particle.style.top = `${Math.random() * 100}vh`;
            
            // Random animation duration and delay
            particle.style.animationDuration = `${Math.random() * 15 + 15}s`;
            particle.style.animationDelay = `${Math.random() * 10}s`;
            
            container.appendChild(particle);
        }
    }

    // 3. Magnetic Button Hover & Ripple Click
    const btn = document.querySelector('.magnetic-btn');
    if (btn) {
        // Magnetic effect
        btn.addEventListener('mousemove', (e) => {
            const rect = btn.getBoundingClientRect();
            const x = e.clientX - rect.left - rect.width / 2;
            const y = e.clientY - rect.top - rect.height / 2;
            
            // Pull factor (0.1 means 10% of cursor distance)
            btn.style.transform = `translate(${x * 0.15}px, ${y * 0.15}px)`;
        });

        btn.addEventListener('mouseleave', () => {
            // Spring back
            btn.style.transform = `translate(0px, 0px)`;
        });

        // Ripple click effect
        btn.addEventListener('click', function(e) {
            const rect = btn.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;

            const ripple = document.createElement('span');
            ripple.classList.add('ripple');
            ripple.style.left = `${x}px`;
            ripple.style.top = `${y}px`;

            this.appendChild(ripple);

            setTimeout(() => {
                ripple.remove();
            }, 600);
        });
    }

    // 4. Parallax effect on the Glass Card
    const card = document.querySelector('.glass-card');
    if (card && window.innerWidth > 900) {
        window.addEventListener('mousemove', (e) => {
            const x = (window.innerWidth / 2 - e.pageX) / 40;
            const y = (window.innerHeight / 2 - e.pageY) / 40;
            // Apply slight 3D rotation based on mouse position
            card.style.transform = `rotateY(${x}deg) rotateX(${y}deg)`;
        });
        
        // Reset rotation on mouse leave
        window.addEventListener('mouseout', () => {
            card.style.transform = `rotateY(0deg) rotateX(0deg)`;
        });
    }
});
