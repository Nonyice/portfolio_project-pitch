document.addEventListener('DOMContentLoaded', function() {
    fetch('/get_reviews')
        .then(response => response.json())
        .then(data => {
            const testimonialsSection = document.querySelector('.testimonials');

            data.reviews.forEach(review => {
                const testimonialDiv = document.createElement('div');
                testimonialDiv.className = 'testimonial';
                testimonialDiv.innerHTML = `
                    <img src="${review.image}" alt="${review.name}">
                    <h5>${review.name}</h5>
                    <p>${review.message}</p>
                `;
                testimonialsSection.appendChild(testimonialDiv);
            });
        });
});
