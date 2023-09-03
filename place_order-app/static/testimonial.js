function displayTestimonials() {
  const testimonials = document.querySelectorAll('.testimonial');

  let currentIndex = 0;

  function showTestimonial() {
    const currentTestimonial = testimonials[currentIndex];

    testimonials.forEach((testimonial) => {
      testimonial.style.opacity = '0';
      testimonial.style.transform = 'translateY(20px)';
    });

    setTimeout(() => {
      currentTestimonial.style.opacity = '1';
      currentTestimonial.style.transform = 'translateY(0)';
    }, 0);

    setTimeout(() => {
      currentTestimonial.style.opacity = '0';
      currentTestimonial.style.transform = 'translateY(20px)';
      currentIndex = (currentIndex + 1) % testimonials.length;
      setTimeout(showTestimonial, 500); // Wait for fade out transition before displaying next testimonial
    }, 5000); // 5 seconds for testimonial display
  }

  showTestimonial();
}

displayTestimonials();
