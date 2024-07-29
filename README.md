# Cineplex - Movie Booking Website

Cineplex is a dynamic movie booking website built with Django, offering users a seamless experience to browse, select, and book movie tickets online.

## Features

- **User Authentication**: Secure login and registration system.
- **Movie Listings**: Display of latest and upcoming movies.
- **Movie Details**: Comprehensive information about each movie, including descriptions and trailers.
- **Theater Selection**: Choose from multiple theaters and showtimes.
- **Seat Selection**: Interactive seat selection interface.
- **Booking System**: Secure and user-friendly booking process.
- **Payment Integration**: Stripe integration for smooth payment transactions.
- **Booking History**: Users can view their past bookings.
- **Responsive Design**: Optimized for various devices and screen sizes.

## Technical Highlights

- **Django Framework**: Utilized for robust backend development.
- **External API Integration**: Fetches additional movie data from MovieDatabase API.
- **Caching System**: Implemented to optimize performance and reduce API calls.
- **Database Models**: Comprehensive models for Users, Movies, Theaters, Showtimes, Seats, and Bookings.
- **Stripe API**: Integrated for secure payment processing.
- **JSON Field**: Utilized for flexible storage of theater seating layouts.

## Database Structure

Cineplex employs a comprehensive database structure to support its feature-rich movie booking system. Below is a detailed overview of all models and their relationships:

### Core Models:

1. **User**
   - Extends Django's AbstractUser for authentication and user management.

2. **Movie**
   - Stores movie details: name, image, description, trailer URL, duration.
   - Has a ManyToMany relationship with Genre.

3. **Theater**
   - Represents cinema halls.
   - Includes a JSONField for flexible seating layout storage.
   - Associated with a City through a ForeignKey.

4. **Showtime**
   - Links movies to theaters with specific dates and times.
   - ForeignKey relationships to both Movie and Theater.

5. **Seat**
   - Represents individual seats in a theater.
   - ForeignKey to Theater.

### Supporting Models:

6. **City**
   - Stores city names.
   - Allows for location-based theater queries.

7. **Genre**
   - Represents movie genres.
   - ManyToMany relationship with Movie.

8. **Price**
   - Manages pricing for movie-theater combinations.
   - ForeignKey relationships to both Movie and Theater.

### Booking System Models:

9. **ShowtimeSeat**
   - Tracks the availability of each seat for each showtime.
   - Crucial for preventing double bookings.
   - ForeignKey relationships to both Showtime and Seat.

10. **Booking**
    - Records user bookings.
    - Includes selected seats, total price, and booking status.
    - ForeignKey to User and Showtime.
    - ManyToMany relationship with Seat.
    - Implements atomic transactions for seat reservation.

11. **Payment**
    - Linked one-to-one with Booking for payment details.
    - Stores amount, timestamp, and payment method.

### Additional Feature Model:

12. **Rating**
    - Allows users to rate and review movies.
    - ForeignKey relationships to both User and Movie.

### Key Relationships and Features:

- **City-Theater Relationship**: Enables location-based theater searches.
- **Movie-Genre Relationship**: Facilitates movie categorization and filtering.
- **Theater-Seat Relationship**: Allows for dynamic seat management per theater.
- **Showtime-ShowtimeSeat-Seat Chain**: Enables real-time seat availability tracking for each screening.
- **Booking Process**:
  - Utilizes ShowtimeSeat for availability checks.
  - Implements atomic transactions in the `book_seats` method to prevent overbooking.
  - Calculates total price based on the Price model and selected seats.
- **Payment Integration**: Separate model allows for detailed payment tracking and potential integration with various payment gateways.
- **User Interaction**: The Rating model adds a community aspect, allowing user feedback on movies.

### Real-Time Booking Features:

1. **Concurrent Booking Handling**: The combination of ShowtimeSeat and atomic transactions in Booking ensures accurate handling of simultaneous booking attempts.
2. **Dynamic Pricing**: The Price model allows for flexible pricing strategies based on movies and theaters.
3. **Efficient Querying**: The structure supports quick retrieval of available showtimes, seats, and user-specific information.
4. **Scalability**: The separation of concerns (e.g., separate models for Theater, Showtime, Seat, ShowtimeSeat) allows for easy scaling and maintenance.

This comprehensive database design enables Cineplex to offer a robust, real-time booking system with features like dynamic seat selection, flexible pricing, and user ratings, while maintaining data integrity and system performance.

## Sreen Shots:

### Homepage:

![image](https://github.com/user-attachments/assets/594b1869-154d-400f-999f-fd24d6f4944c)
![image](https://github.com/user-attachments/assets/02dabc02-ba33-459f-b317-57ed8e47a3ce)
![image](https://github.com/user-attachments/assets/f183938a-af77-4eb9-8712-b8ce36f08518)

### Login:

![image](https://github.com/user-attachments/assets/d6152113-39d1-4bc7-95db-9aea56526b48)

### Register:

![image](https://github.com/user-attachments/assets/b8ba25c0-bb4f-4c4c-bf2b-02e6a032943d)

### Description :







