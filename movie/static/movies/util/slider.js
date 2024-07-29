
 function displayUpcomingMovies() {
    

   

    // Initialize Swiper
    new Swiper('.swiper-container', {
        slidesPerView: 'auto',
        spaceBetween: 20,
        pagination: {
            el: '.swiper-pagination',
            clickable: true,
        },
        
        breakpoints: {
            400: {
                slidesPerView: 2,
            },
            768: {
                slidesPerView: 4,
            },
            1024: {
                slidesPerView: 6,
            },
        }
    });
}

// Call this function when the page loads
document.addEventListener('DOMContentLoaded', displayUpcomingMovies);