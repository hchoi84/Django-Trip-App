from django.shortcuts import render, redirect, HttpResponse
from .models import Trip
from apps.user.models import User
from django.contrib import messages
from django.contrib.messages import get_messages
from datetime import datetime

def edit(request, trip_id):
    if not 'uid' in request.session:
        messages.error(request, "Please log in", extra_tags="log_in")
        return redirect("/")
    trip = Trip.objects.get(id=trip_id)
    start_date = datetime.strftime(trip.start_date, '%Y-%m-%d')
    context={
        "destination": trip.destination,
        "start_date": datetime.strftime(trip.start_date, '%Y-%m-%d'),
        "end_date": datetime.strftime(trip.end_date, '%Y-%m-%d'),
        "plan": trip.plan,
        "trip_id": trip.id,
        "user": User.objects.get(id=request.session['uid'])
    }
    return render(request, "trips/edit.html", context)

def new(request):
    if not 'uid' in request.session:
        messages.error(request, "Please log in", extra_tags="log_in")
        return redirect("/")
    user = User.objects.get(id=request.session['uid'])
    context={
        "user": user.first_name,
    }
    return render(request, "trips/new.html", context)

def trip_info(request, trip_id):
    if not 'uid' in request.session:
        messages.error(request, "Please log in", extra_tags="log_in")
        return redirect("/")
    trip = Trip.objects.get(id=trip_id)
    user = User.objects.get(id=request.session['uid'])
    context={
        "trip": trip,
        "user": User.objects.get(id=request.session['uid']),
        "joining": trip.users.all().exclude(id=user.id)
    }
    return render(request, "trips/trip_info.html", context)

def create_trip(request):
    if not 'uid' in request.session:
        messages.error(request, "Please log in", extra_tags="log_in")
        return redirect("/")
    # validate form
    errors = Trip.objects.validate_trip_creation(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value, extra_tags=key)
        return redirect("/trips/new")

    # process trip creation here
    userid = request.session['uid']
    trip_id = Trip.objects.process_trip_creation(request.POST, userid)
    print(trip_id)
    this_trip = Trip.objects.get(id=trip_id)
    this_trip.users.add(User.objects.get(id=userid))
    return redirect('/dashboard')

def remove(request, trip_id):
    if not 'uid' in request.session:
        messages.error(request, "Please log in", extra_tags="log_in")
        return redirect("/")
    Trip.objects.get(id=trip_id).delete()
    return redirect("/dashboard")

def update_trip(request, trip_id):
    if not 'uid' in request.session:
        messages.error(request, "Please log in", extra_tags="log_in")
        return redirect("/")
    errors = Trip.objects.validate_trip_creation(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value, extra_tags=key)
        return redirect(f"/trips/edit/{trip_id}")
    Trip.objects.update_trip(request.POST, trip_id)
    return redirect("/dashboard")

def cancel_joined(request, joined_id):
    if not 'uid' in request.session:
        messages.error(request, "Please log in", extra_tags="log_in")
        return redirect("/")
    user = User.objects.get(id=request.session['uid'])
    Trip.objects.get(id=joined_id).users.remove(user)
    return redirect("/dashboard")

def join_trip(request, join_id):
    if not 'uid' in request.session:
        messages.error(request, "Please log in", extra_tags="log_in")
        return redirect("/")
    user = User.objects.get(id=request.session['uid'])
    Trip.objects.get(id=join_id).users.add(user)
    return redirect("/dashboard")