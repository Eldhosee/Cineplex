from datetime import date
from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import Movie, Rating,Theater, Price,Showtime,Payment,City, Seat, Booking, User, Payment, ShowtimeSeat,Genre

class SeatResource(resources.ModelResource):
   class Meta:
      model = Seat
class SeatAdmin(ImportExportModelAdmin):
   resource_class = SeatResource

class TheaterResource(resources.ModelResource):
   class Meta:
      model = Theater
class TheaterAdmin(ImportExportModelAdmin):
   resource_class = TheaterResource

# Register your models here.
admin.site.register(User)
admin.site.register(Theater,TheaterAdmin)
admin.site.register(Showtime)
admin.site.register(Movie)
admin.site.register(Seat,SeatAdmin)
admin.site.register(Booking)
admin.site.register(ShowtimeSeat)
admin.site.register(Payment)
admin.site.register(Genre)
admin.site.register(Rating)
admin.site.register(Price)
admin.site.register(City)


