const slider = document.querySelector('.slider');
const images = slider.getElementsByTagName('img');
const prevBtn = document.getElementById('prevBtn');
const nextBtn = document.getElementById('nextBtn');
let currentIndex = 0;

function showImage(index) {
  for (let i = 0; i < images.length; i++) {
    images[i].style.display = 'none';
  }
  images[index].style.display = 'block';
}

function nextImage() {
  currentIndex++;
  if (currentIndex >= images.length) {
    currentIndex = 0;
  }
  showImage(currentIndex);
}

function previousImage() {
  currentIndex--;
  if (currentIndex < 0) {
    currentIndex = images.length - 1;
  }
  showImage(currentIndex);
}

// Add event listeners for next and previous buttons
nextBtn.addEventListener('click', nextImage);
prevBtn.addEventListener('click', previousImage);

// Automatically move to the next image every 3 seconds
setInterval(nextImage, 2000);
