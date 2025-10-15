from django.shortcuts import render
from .models import Room, Contribution, Expense, Announcement
from django.db.models import Sum
from datetime import datetime

def dashboard(request):


    Announcement.delete_old_non_important()

    announcements = Announcement.objects.order_by('-is_important', '-date_posted')

    # Get selected month (e.g., '2025-10')
    selected_month = request.GET.get('month')
    month_name = None

    if selected_month:
        # Convert month like '2025-10' to readable name
        month_name = datetime.strptime(selected_month, "%Y-%m").strftime("%B %Y")
        contributions = Contribution.objects.filter(date_added__year=selected_month[:4],
                                                    date_added__month=selected_month[5:7])
        expenses = Expense.objects.filter(date_added__year=selected_month[:4],
                                          date_added__month=selected_month[5:7])
    else:
        contributions = Contribution.objects.all()
        expenses = Expense.objects.all()

    rooms = Room.objects.all()

    # Monthly totals
    total_contributions_month = contributions.aggregate(Sum('amount'))['amount__sum'] or 0
    total_expenses_month = expenses.aggregate(Sum('amount'))['amount__sum'] or 0
    balance_month = total_contributions_month - total_expenses_month

    # Overall totals
    total_contributions_all = Contribution.objects.aggregate(Sum('amount'))['amount__sum'] or 0
    total_expenses_all = Expense.objects.aggregate(Sum('amount'))['amount__sum'] or 0
    balance_all = total_contributions_all - total_expenses_all

    # Room contributions for the selected month
    room_data = []
    for room in rooms:
        room_total = contributions.filter(room=room).aggregate(Sum('amount'))['amount__sum'] or 0
        room_data.append({
            'room': room.number,
            'total': room_total
        })

    context = {
        'selected_month': selected_month,
        'month_name': month_name,
        'room_data': room_data,
        'expenses': expenses,
        'total_contributions_month': total_contributions_month,
        'total_expenses_month': total_expenses_month,
        'balance_month': balance_month,
        'total_contributions_all': total_contributions_all,
        'total_expenses_all': total_expenses_all,
        'balance_all': balance_all,
        'announcements': announcements,
    }

    return render(request, 'finance/dashboard.html', context)

