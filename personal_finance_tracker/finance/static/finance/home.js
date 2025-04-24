// Fancy interactions and animations for Personal Finance Tracker

document.addEventListener('DOMContentLoaded', () => {
  // Smooth scroll for nav links
  document.querySelectorAll('nav ul li a').forEach(link => {
    link.addEventListener('click', (e) => {
      const targetId = link.getAttribute('href');
      if (targetId.startsWith('#')) {
        e.preventDefault();
        document.querySelector(targetId).scrollIntoView({
          behavior: 'smooth'
        });
      }
    });
  });

  // Floating input glow on focus
  const inputs = document.querySelectorAll('input, textarea, select');
  inputs.forEach(input => {
    input.addEventListener('focus', () => {
      input.parentElement.classList.add('focused');
    });
    input.addEventListener('blur', () => {
      input.parentElement.classList.remove('focused');
    });
  });

  // Animate summary boxes on load
  const boxes = document.querySelectorAll('.box');
  boxes.forEach((box, i) => {
    box.style.opacity = 0;
    setTimeout(() => {
      box.style.transition = 'all 0.8s ease';
      box.style.opacity = 1;
      box.style.transform = 'translateY(0)';
    }, 300 * i);
  });

  // Scroll fade-in effect
  const sections = document.querySelectorAll('section');
  const observer = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('show');
      }
    });
  }, { threshold: 0.1 });

  sections.forEach(section => {
    section.classList.add('hidden');
    observer.observe(section);
  });

  // Button click pulse effect
  document.querySelectorAll('button').forEach(button => {
    button.addEventListener('click', function (e) {
      const circle = document.createElement('span');
      circle.classList.add('ripple');
      const rect = button.getBoundingClientRect();
      circle.style.left = `${e.clientX - rect.left}px`;
      circle.style.top = `${e.clientY - rect.top}px`;
      button.appendChild(circle);
      setTimeout(() => circle.remove(), 600);
    });
  });

  // Navbar highlight on scroll
  const navLinks = document.querySelectorAll('nav a');
  const sectionPositions = Array.from(sections).map(section => ({
    id: section.id,
    offset: section.offsetTop
  }));

  window.addEventListener('scroll', () => {
    const scrollY = window.scrollY + 100;
    for (let i = sectionPositions.length - 1; i >= 0; i--) {
      if (scrollY >= sectionPositions[i].offset) {
        navLinks.forEach(link => link.classList.remove('active'));
        const activeLink = document.querySelector(`nav a[href="#${sectionPositions[i].id}"]`);
        if (activeLink) activeLink.classList.add('active');
        break;
      }
    }
  });

  // Glowing border effect on inputs
  inputs.forEach(input => {
    input.addEventListener('focus', () => {
      input.style.boxShadow = '0 0 10px #3fb9ff';
    });
    input.addEventListener('blur', () => {
      input.style.boxShadow = 'none';
    });
  });

  // Card hover lift animation
  document.querySelectorAll('.box').forEach(card => {
    card.addEventListener('mouseenter', () => {
      card.style.transform = 'translateY(-10px) scale(1.03)';
      card.style.boxShadow = '0 15px 25px rgba(0,0,0,0.2)';
    });
    card.addEventListener('mouseleave', () => {
      card.style.transform = 'translateY(0) scale(1)';
      card.style.boxShadow = 'none';
    });
  });

  // Animated gradient background on header
  const header = document.querySelector('header');
  if (header) {
    header.style.background = 'linear-gradient(-45deg, #1e3c72, #2a5298, #1e3c72, #2a5298)';
    header.style.backgroundSize = '400% 400%';
    header.style.animation = 'gradientMove 10s ease infinite';
  }
});
