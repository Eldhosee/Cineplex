from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import transaction

class User(AbstractUser):
    pass

class City(models.Model):
    name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name

class Theater(models.Model):
    name = models.CharField(max_length=50)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    layout = models.JSONField(default=dict)  # Store seating layout as JSON

    def __str__(self):
        return f"{self.name},{self.id}"

class Genre(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Movie(models.Model):
    movie_name = models.CharField(max_length=40)
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    description = models.TextField(null=True, default='')
    latest = models.BooleanField(default=False)
    trailer = models.URLField(null=True, blank=True)
    genres = models.ManyToManyField(Genre)
    duration = models.IntegerField(help_text="Duration in minutes")
    
    def __str__(self):
        return self.movie_name

class Price(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    theater = models.ForeignKey(Theater, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    
    def __str__(self):
        return f"{self.movie.movie_name} - {self.theater.name}: ₹{self.price}"

class Seat(models.Model):
    theater = models.ForeignKey(Theater, on_delete=models.CASCADE,default=None)
    seat_number = models.CharField(max_length=10)
    

    def __str__(self):
        return f"{self.theater.name} - {self.seat_number}"

    class Meta:
        unique_together = ['theater', 'seat_number']

class Showtime(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    theater = models.ForeignKey(Theater, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    total_seats = models.IntegerField()
    
    def __str__(self):
        return f"{self.movie.movie_name} - {self.theater.name} - {self.date} {self.time}"

class ShowtimeSeat(models.Model):
    showtime = models.ForeignKey(Showtime, on_delete=models.CASCADE)
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE)
    is_available = models.BooleanField(default=True)

    class Meta:
        unique_together = ['showtime', 'seat']
    def get_seat_availability(theater, showtime):
        layout = theater.layout['rows']
        booked_seats = ShowtimeSeat.objects.filter(showtime=showtime, is_available=False).values_list('seat__seat_number', flat=True)

        # Mark seats as booked or available
        processed_layout = []
        for row in layout:
            processed_row = []
            for seat in row:
                if seat and seat in booked_seats:
                    processed_row.append({
                        'seat_number': seat,
                        'status': 'booked'
                    })
                elif seat:
                    processed_row.append({
                        'seat_number': seat,
                        'status': 'available'
                    })
                else:
                    processed_row.append(None)  # Represents a space
            processed_layout.append(processed_row)

        return processed_layout


class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    showtime = models.ForeignKey(Showtime, on_delete=models.CASCADE)
    seats = models.ManyToManyField(Seat)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=[
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    ], default='confirmed')
    
    def book_seats(self, selected_seat_ids):
        with transaction.atomic():
            available_seats = ShowtimeSeat.objects.select_for_update().filter(
                showtime=self.showtime,
                seat_id__in=selected_seat_ids,
                is_available=True
            )

            if available_seats.count() != len(selected_seat_ids):
                raise Exception("One or more seats are already booked.")

            available_seats.update(is_available=False)
            self.seats.add(*available_seats.values_list('seat', flat=True))
            self.total_price = self.calculate_total_price()
            self.save()

    def calculate_total_price(self):
        price_per_seat = Price.objects.get(
            movie=self.showtime.movie,
            theater=self.showtime.theater
        ).price
        return price_per_seat * self.seats.count()
    
    def __str__(self):
        return f"{self.user.username} - {self.showtime}"

class Payment(models.Model):
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=50)

    def __str__(self):
        return f"Payment for {self.booking}"

class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    review = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'movie']

    def __str__(self):
        return f"{self.user.username}'s rating for {self.movie.movie_name}"