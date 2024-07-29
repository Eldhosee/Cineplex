document.addEventListener('DOMContentLoaded', function() {
    const dateContainer = document.getElementById('dateContainer');
    const prevButton = document.getElementById('prevDate');
    const nextButton = document.getElementById('nextDate');
    const showtimesContainer = document.getElementById('showtimesContainer');
    const noDatesContainer = document.getElementById('noDatesContainer'); // Container for SVG

    let showtimes = [];
    let availableDates = [];

// Parse the showtimes data passed from Django
try {
    const showtimesRaw = document.getElementById('showtimes-data').textContent;
    console.log('Raw showtimes data:', showtimesRaw);
    showtimes = JSON.parse(showtimesRaw);
    console.log('Parsed showtimes:', showtimes);
} catch (e) {
    console.error('Error parsing showtimes data:', e);
}

// Parse available dates data passed from Django
try {
    const availableDatesRaw = document.getElementById('available-dates-data').textContent;
    console.log('Raw available dates data:', availableDatesRaw);
    availableDates = JSON.parse(availableDatesRaw);
    availableDates = availableDates.map(dateStr => new Date(dateStr));
    console.log('Parsed available dates:', availableDates);
} catch (e) {
    console.error('Error parsing available dates data:', e);
}
    let currentPage = 0;
    const datesPerPage = 7; // Show a week of dates per page

    function createDateElement(date) {
        const dateItem = document.createElement('div');
        dateItem.className = 'date-item';

        const dayName = date.toLocaleDateString('en-US', { weekday: 'short' }).toUpperCase();
        const dayNumber = date.getDate();
        const monthName = date.toLocaleDateString('en-US', { month: 'short' }).toUpperCase();

        dateItem.innerHTML = `
            <div class="day">${dayName}</div>
            <div class="date">${dayNumber}</div>
            <div class="month">${monthName}</div>
        `;

        dateItem.addEventListener('click', function() {
            document.querySelectorAll('.date-item').forEach(item => item.classList.remove('selected'));
            this.classList.add('selected');
            updateShowtimes(date);
        });

        return dateItem;
    }

    function updateDates() {
        if (!dateContainer || !noDatesContainer) {
            console.error('Required container elements not found.');
            return;
        }

        dateContainer.innerHTML = '';
        noDatesContainer.innerHTML = '';  // Clear any existing content

        if (availableDates.length === 0) {
            // Show SVG if no dates are available
              noDatesContainer.innerHTML = `
                <object
                    data="${notFoundSVGPath}"
                    type="image/svg+xml"
                    class="no-dates-svg"
                    alt="No available dates"
                    style="width: 400px; height: 400px; "

                >
                    <!-- Fallback content if SVG is not supported -->
                    <img src="${notFoundSVGPath}" alt="No available dates" class="no-dates-svg-fallback">
                    
                </object>
                <h3 style="color:#FFFF;font-size:1.2em">Sorry ..No show available ...</h3>
            `;
            return;
        }

        const startIndex = currentPage * datesPerPage;
        const endIndex = startIndex + datesPerPage;
        const currentDates = availableDates.slice(startIndex, endIndex);

        currentDates.forEach((date, index) => {
            const dateElement = createDateElement(date);
            if (index === 0) dateElement.classList.add('selected');
            dateContainer.appendChild(dateElement);
        });

        updateShowtimes(currentDates[0]);
    }

    function updateShowtimes(selectedDate) {
        showtimesContainer.innerHTML = '';
        const filteredShowtimes = showtimes.filter(showtime => {
            const showtimeDate = new Date(showtime.date);
            return showtimeDate.toDateString() === selectedDate.toDateString();
        });

        if (filteredShowtimes.length === 0) {
            showtimesContainer.innerHTML = '<p>No showtimes available for this date.</p>';
            return;
        }

        filteredShowtimes.forEach(showtime => {
            const showtimeElement = document.createElement('div');
            showtimeElement.className = 'showtime-item';
            showtimeElement.innerHTML = `
            <div class="flex items-center mt-3 gap-4 bg-[#202931] rounded-xl px-4 min-h-[72px]  py-2 justify-between">
              <div class="flex flex-col justify-center">
                <p class="text-white lg:text-[25px] text-base font-medium leading-normal line-clamp-1">${showtime.theater_name}</p>
                <p class=" lg:text-[15px] text-[#e0e0e0] text-base font-medium leading-normal line-clamp-1">Available Seats: ${showtime.available_seats}</p>
                <p class="text-[#93adc8] text-sm font-normal leading-normal line-clamp-2"> ${showtime.time}</p>
              </div>

              <div class=" mr-8">
                <div class="text-white flex size-10 items-center justify-center" data-icon="CaretRight" data-size="24px" data-weight="regular">
                  
                <button class="book" onclick="bookShowtime(${showtime.id})">Book Now</button>
            
                </div>
              </div>
            </div>
            </div>
                
            `;
            
            showtimesContainer.appendChild(showtimeElement);
            const bookButton = showtimeElement.querySelector('.book');

      // Add event listeners for click and hover
      bookButton.addEventListener('click', function() {
        this.style.color = '#ff4081'; 
      });

      bookButton.addEventListener('mouseover', function() {
        this.style.color = '#ff4081'; 
      });

      bookButton.addEventListener('mouseout', function() {
        this.style.color = '#ffff'; 
      });
        });
    }

    prevButton.addEventListener('click', function() {
        if (currentPage > 0) {
            currentPage--;
            updateDates();
        }
    });

    nextButton.addEventListener('click', function() {
        if ((currentPage + 1) * datesPerPage < availableDates.length) {
            currentPage++;
            updateDates();
        }
    });

    updateDates();
});

function bookShowtime(showtimeId) {
    // Implement booking logic here
    console.log('Booking showtime:', showtimeId);
    // You might want to redirect to a booking page or open a modal
    window.location.href = `/seatselect/${showtimeId}`;
}
