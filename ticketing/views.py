from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.forms import UserCreationForm
from django.core.paginator import Paginator
from .models import Match, Ticket, TicketCategory, News, UserProfile
from .forms import TicketBookingForm, UserRegistrationForm
import json


def home(request):
    """Home page view"""
    recent_matches = Match.objects.filter(status='completed').order_by('-date_time')[:3]
    upcoming_matches = Match.objects.filter(status='upcoming').order_by('date_time')[:3]
    latest_news = News.objects.all()[:4]
    
    context = {
        'recent_matches': recent_matches,
        'upcoming_matches': upcoming_matches,
        'latest_news': latest_news,
    }
    return render(request, 'ticketing/home.html', context)


def fixtures(request):
    """Fixtures page showing all matches"""
    match_list = Match.objects.all().order_by('date_time')
    paginator = Paginator(match_list, 10)
    page_number = request.GET.get('page')
    matches = paginator.get_page(page_number)
    
    return render(request, 'ticketing/fixtures.html', {'matches': matches})


@login_required
def book_ticket(request, match_id):
    """Book ticket for a specific match"""
    match = get_object_or_404(Match, id=match_id, status='upcoming')
    categories = TicketCategory.objects.all()
    
    if request.method == 'POST':
        form = TicketBookingForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.match = match
            ticket.total_amount = ticket.category.price * ticket.quantity
            ticket.save()
            messages.success(request, 'Ticket booked successfully!')
            return redirect('ticket_detail', ticket_id=ticket.id)
    else:
        form = TicketBookingForm()
    
    context = {
        'match': match,
        'categories': categories,
        'form': form,
    }
    return render(request, 'ticketing/book_ticket.html', context)


@login_required
def ticket_detail(request, ticket_id):
    """View ticket details"""
    ticket = get_object_or_404(Ticket, id=ticket_id, user=request.user)
    return render(request, 'ticketing/ticket_detail.html', {'ticket': ticket})


@login_required
def my_tickets(request):
    """View user's tickets"""
    tickets = Ticket.objects.filter(user=request.user).order_by('-booking_date')
    return render(request, 'ticketing/my_tickets.html', {'tickets': tickets})


def news_list(request):
    """News listing page"""
    news_list = News.objects.all()
    paginator = Paginator(news_list, 10)
    page_number = request.GET.get('page')
    news = paginator.get_page(page_number)
    
    return render(request, 'ticketing/news_list.html', {'news': news})


def news_detail(request, news_id):
    """News detail page"""
    news_item = get_object_or_404(News, id=news_id)
    return render(request, 'ticketing/news_detail.html', {'news_item': news_item})


def register(request):
    """User registration"""
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.create(
                user=user,
                phone=form.cleaned_data.get('phone', ''),
            )
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('home')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'registration/register.html', {'form': form})


@csrf_exempt
def process_payment(request):
    """Mock payment processing"""
    if request.method == 'POST':
        data = json.loads(request.body)
        ticket_id = data.get('ticket_id')
        payment_method = data.get('payment_method')
        
        try:
            ticket = Ticket.objects.get(id=ticket_id, user=request.user)
            ticket.payment_method = payment_method
            ticket.is_paid = True
            ticket.save()
            
            return JsonResponse({'success': True, 'message': 'Payment successful'})
        except Ticket.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Ticket not found'})
    
    return JsonResponse({'success': False, 'message': 'Invalid request'})
