document.addEventListener('DOMContentLoaded', () => {
  const selectedSeats = new Set();
  const selectedSeatsInput = document.getElementById('selected-seats');

  // Ensure seats are selected correctly
  const availableSeats = document.querySelectorAll('.seat.available');
  console.log('Available seats:', availableSeats);

  // Loop through each available seat
  availableSeats.forEach(seat => {
    seat.addEventListener('click', () => {
      console.log('Seat clicked:', seat);  // Log seat click
      const seatNumber = seat.dataset.seatNumber;
      
      // Toggle selected class and manage the set
      seat.classList.toggle('selected');
      console.log('Seat classList:', seat.classList);

      if (seat.classList.contains('selected')) {
        selectedSeats.add(seatNumber);
      } else {
        selectedSeats.delete(seatNumber);
      }

      // Log current selected seats
      console.log('Selected seats:', Array.from(selectedSeats));

      // Update hidden input value
      selectedSeatsInput.value = Array.from(selectedSeats).join(',');
    });
  });
});
