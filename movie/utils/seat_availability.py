from movie.models import ShowtimeSeat


def get_seat_availability(theater, showtime):
    layout = theater.layout['rows']
    booked_seats = ShowtimeSeat.objects.filter(
        showtime=showtime, is_available=False
    ).values_list('seat__seat_number', flat=True)

    processed_layout = []
    for row in layout:
        processed_row = []
        for seat in row:
            if seat and seat in booked_seats:
                processed_row.append({'seat_number': seat, 'status': 'booked'})
            elif seat:
                processed_row.append({'seat_number': seat, 'status': 'available'})
            else:
                processed_row.append(None)  # Represents a space
        processed_layout.append(processed_row)

    return processed_layout
