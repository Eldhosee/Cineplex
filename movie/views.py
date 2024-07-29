import datetime
import logging
import json
import random
from django.db import transaction

from django.core.serializers import serialize
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth import login as auth_login, authenticate, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
import stripe
from django.conf import settings 
from django.views.decorators.csrf import csrf_exempt

from movie.api.upcoming import get_movie_by_id, upcoming_movies
from movie.api.anime import Anime_movies, get_anime_by_id
from .models import Movie, Theater, Showtime, Seat, Booking, User, Payment, ShowtimeSeat

stripe.api_key = settings.STRIPE_SECRET_KEY

def homepage(request):
    latest_movies = Movie.objects.filter(latest=True)
    other_movies = Movie.objects.filter(latest=False)
    random_movie = Movie.objects.order_by('?').first()
    all_upcoming = upcoming_movies()
    upcoming = [movie for movie in all_upcoming if movie.get('primaryImage') and movie['primaryImage'].get('url')]
    all_anime = Anime_movies()
    
    return render(request, "movies/homepage.html", {
        "latest_movies": latest_movies,
        "movies": other_movies,
        "random": random_movie,
        "upcoming": upcoming,
        "all_anime": all_anime
    })

def login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            auth_login(request, user)
            request.session['user_id'] = user.id
            request.session['email'] = user.email

            # Redirect to payment if redirected from booking
            next_url = request.GET.get('next')
            if next_url:
                return HttpResponseRedirect(next_url)
            
            return HttpResponseRedirect(reverse("homepage"))
        else:
            return render(request, "movies/login_2.html", {
                "message": "Invalid username and/or password."
            })
    return render(request, "movies/login_2.html")

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        
        if not all([username, email, password, confirmation]):
            return render(request, "movies/register.html", {"message": "Enter all details."})
        
        if password != confirmation:
            return render(request, "movies/register.html", {"message": "Passwords must match."})
        
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "movies/register.html", {"message": "Username already taken."})
        
        return HttpResponseRedirect(reverse("login"))
    return render(request, "movies/register.html")

def movie_detail(movie_id):
    movie = get_movie_by_id(movie_id)
    if movie:
        return {'movie': movie}
    else:
        return {}
    
def anime_detail(anime_id):
    anime = get_anime_by_id(anime_id)
    if anime:
        return {'anime': anime}
    else:
        return {}
    
def description(request, id):
    try:
        details = get_object_or_404(Movie, pk=id)
        return render(request, "movies/description.html", {"movie_details": details, "live": True})
    except:
        detail = movie_detail(id)
        if detail:
            return render(request, "movies/description.html", {"movie_details": detail, "live": False})
        else:
            detail = anime_detail(id)
            return render(request, "movies/description.html", {"movie_details": detail, "live": False})

logger = logging.getLogger(__name__)

def theater(request, id):
    movie = get_object_or_404(Movie, pk=id)
    showtimes = Showtime.objects.filter(movie=movie).order_by('date', 'time')

    # Correctly format JSON
    showtimes_data = json.loads(serialize('json', showtimes))
    showtimes_json = json.dumps([{
        'id': item['pk'],
        'date': item['fields']['date'],
        'time': item['fields']['time'],
        'theater_name': Theater.objects.get(pk=item['fields']['theater']).name,
        'available_seats': item['fields']['total_seats']
    } for item in showtimes_data])

    # Extract available dates
    available_dates = list(set(item['fields']['date'] for item in showtimes_data))
    available_dates_json = json.dumps(available_dates)

    # Print or log the JSON strings
    print("Showtimes JSON:")
    print(showtimes_json)
    print("\nAvailable Dates JSON:")
    print(available_dates_json)

    # Or use Django's logging system
    logger.debug("Showtimes JSON: %s", showtimes_json)
    logger.debug("Available Dates JSON: %s", available_dates_json)

    return render(request, "movies/theater.html", {
        "showtimes": showtimes_json,
        "available_dates": available_dates_json,
        "id": id,
        "movie": movie
    })

def seatselect(request, id):
    showtime = get_object_or_404(Showtime, pk=id)
    theater = showtime.theater

    # Get the layout from the theater
    seats_layout = theater.layout.get('rows', [])

    # Get booked seats for this showtime
    booked_seats = ShowtimeSeat.objects.filter(showtime=showtime, is_available=False).values_list('seat__seat_number', flat=True)

    # Mark booked and available seats in the layout
    processed_layout = []
    for row in seats_layout:
        processed_row = []
        for seat in row:
            if seat:
                seat_status = 'booked' if seat in booked_seats else 'available'
                processed_row.append({
                    'seat_number': seat,
                    'status': seat_status
                })
            else:
                processed_row.append(None)  # Represents a space
        processed_layout.append(processed_row)

    context = {
        'seats_layout': processed_layout,
        'showtime': showtime
    }

    return render(request, "movies/seatselect.html", context)

@login_required(login_url='login')
def seatselected(request):
    if request.method == 'POST':
        showtime_id = request.POST.get('showtime_id')
        seat_numbers = request.POST.get('selected_seats').split(',')
        
        seats = Seat.objects.filter(seat_number__in=seat_numbers)
        
        price = len(seats) * 100  # Assuming a fixed price per seat

        # Store details in session
        request.session['showtime_id'] = showtime_id
        request.session['seat_numbers'] = seat_numbers
        request.session['price'] = price

        return redirect('payment')  # Redirect to payment page
    return redirect('homepage')

@login_required(login_url='login')
def payment(request):
    # Retrieve data from session
    showtime_id = request.session.get('showtime_id')
    seat_numbers = request.session.get('seat_numbers')
    price = request.session.get('price')

    showtime = get_object_or_404(Showtime, pk=showtime_id)

    return render(request, "movies/payment.html", {
        "showtime": showtime,
        "seatselected": ','.join(seat_numbers),
        "price": price,
        "message": "Please pay to confirm your booking",
        "stripe_public_key": settings.STRIPE_PUBLISHABLE_KEY,
    })

@login_required(login_url='login')
def history(request):
    bookings = Booking.objects.filter(user=request.user).order_by('-id')
   
    return render(request, "movies/history.html", {"history": bookings})

def logout_view(request):
    logout(request)
    return redirect('login')

@csrf_exempt
def stripe_config(request):
    if request.method == 'GET':
        stripe_config = {'publicKey': settings.STRIPE_PUBLISHABLE_KEY}
        return JsonResponse(stripe_config, safe=False)

@csrf_exempt
def create_checkout_session(request):
    if request.method == 'GET':
        domain_url = 'http://127.0.0.1:8000/'
        showtime_id = request.session.get('showtime_id')
        price = request.session.get('price')
        
        showtime = get_object_or_404(Showtime, pk=showtime_id)
        
        try:
            checkout_session = stripe.checkout.Session.create(
                line_items=[{
                    'price_data': {
                        'currency': 'inr',
                        'product_data': {
                            'name': f"{showtime.movie.movie_name} - {showtime.theater.name}",
                        },
                        'unit_amount': price * 100,
                    },
                    'quantity': 1,
                }],
                mode='payment',
                success_url=domain_url + 'success',
                cancel_url=domain_url + 'cancel',
            )
            return JsonResponse({'sessionId': checkout_session['id']})
        except Exception as e:
            return JsonResponse({'error': str(e)})

def success(request):
    
        showtime_id = request.session.get('showtime_id')
        seat_numbers = request.session.get('seat_numbers')
        price = request.session.get('price')
        print(dict(request.session))

        # Get the showtime object or 404 if not found
        showtime = get_object_or_404(Showtime, pk=showtime_id)
        
        # Retrieve the seats based on seat numbers
        seats = Seat.objects.filter(seat_number__in=seat_numbers)
        
        # Start an atomic transaction for safe booking and seat updating
        with transaction.atomic():
            # Create a new booking entry
            booking = Booking.objects.create(
                user=request.user,
                showtime=showtime,
                total_price=price
            )
            
            # Associate the seats with the booking
            booking.seats.set(seats)
            
            # Update or create ShowtimeSeat records
            for seat in seats:
                showtime_seat, created = ShowtimeSeat.objects.get_or_create(
                    showtime=showtime,
                    seat=seat,
                    defaults={'is_available': False}
                )
                # If not created, mark the seat as unavailable
                if not created:
                    showtime_seat.is_available = False
                    showtime_seat.save()

            # Record the payment transaction
            Payment.objects.create(
                booking=booking, 
                amount=price, 
                payment_method='Stripe'
            )
        
            
        
        
        return render(request, "movies/success.html")


def cancel(request):
        return render(request, "movies/cancel.html")

