from django.shortcuts import render
from .models import Room, Contribution, Expense
from django.db.models import Sum

def dashboard(request):
    rooms = Room.objects.all()
    contributions = Contribution.objects.all()
    expenses = Expense.objects.all()

    total_contributions = contributions.aggregate(Sum('amount'))['amount__sum'] or 0
    total_expenses = expenses.aggregate(Sum('amount'))['amount__sum'] or 0
    balance = total_contributions - total_expenses

    room_data = []
    for room in rooms:
        total = room.contributions.aggregate(Sum('amount'))['amount__sum'] or 0
        room_data.append({
            'room': room.number,
            'total': total
        })

    context = {
        'room_data': room_data,
        'total_contributions': total_contributions,
        'total_expenses': total_expenses,
        'balance': balance,
    }
    return render(request, 'finance/dashboard.html', context)
