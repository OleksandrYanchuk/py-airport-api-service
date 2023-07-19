from django.contrib import admin

from flight_service.models import Crew, Flight, Order, Ticket

admin.site.register(Crew)
admin.site.register(Flight)
admin.site.register(Order)
admin.site.register(Ticket)
