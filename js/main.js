// JavaScript code for Multiagro website

document.addEventListener('DOMContentLoaded', function() {
    // Language switching functionality
    const langButtons = document.querySelectorAll('.lang-button');
    langButtons.forEach(button => {
        button.addEventListener('click', function() {
            const lang = this.getAttribute('data-lang');
            switchLanguage(lang);
        });
    });

    // Initialize the carousel
    let currentSlide = 0;
    const slides = document.querySelectorAll('.carousel-slide');
    const totalSlides = slides.length;

    function showSlide(index) {
        slides.forEach((slide, i) => {
            slide.style.display = (i === index) ? 'block' : 'none';
        });
    }

    function nextSlide() {
        currentSlide = (currentSlide + 1) % totalSlides;
        showSlide(currentSlide);
    }

    function prevSlide() {
        currentSlide = (currentSlide - 1 + totalSlides) % totalSlides;
        showSlide(currentSlide);
    }

    document.querySelector('.next').addEventListener('click', nextSlide);
    document.querySelector('.prev').addEventListener('click', prevSlide);

    // Load the initial slide and language
    showSlide(currentSlide);
    switchLanguage('en'); // Default language

    function switchLanguage(lang) {
        fetch(`./lang/${lang}.json`)
            .then(response => response.json())
            .then(translations => {
                document.querySelector('title').innerText = translations.title;
                document.querySelector('.logo').innerText = translations.logo;
                document.querySelector('.cta-btn').innerText = translations.cta;
                // Update other text elements based on translations
            });
    }
});