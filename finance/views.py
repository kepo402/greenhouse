from django.shortcuts import render
from .models import Room, Contribution, Expense, Announcement
from django.db.models import Sum
from datetime import datetime

def dashboard(request):
    # 🧹 Clean up old announcements
    Announcement.delete_old_non_important()
    announcements = Announcement.objects.order_by('-is_important', '-date_posted')

    selected_month = request.GET.get('month')
    month_name = None

    if selected_month:
        year = int(selected_month[:4])
        month = int(selected_month[5:7])
        month_name = datetime.strptime(selected_month, "%Y-%m").strftime("%B %Y")

        # 🟩 Filter for selected month
        contributions_month = Contribution.objects.filter(
            date_added__year=year,
            date_added__month=month
        )
        expenses_month = Expense.objects.filter(
            date_added__year=year,
            date_added__month=month
        )
    else:
        contributions_month = Contribution.objects.none()
        expenses_month = Expense.objects.none()

    # 🟩 All-time data
    contributions_all = Contribution.objects.all()
    expenses_all = Expense.objects.all().order_by('-date_added')
    rooms = Room.objects.all()

    # 🟩 Totals
    total_contributions_month = contributions_month.aggregate(Sum('amount'))['amount__sum'] or 0
    total_expenses_month = expenses_month.aggregate(Sum('amount'))['amount__sum'] or 0
    balance_month = total_contributions_month - total_expenses_month

    total_contributions_all = contributions_all.aggregate(Sum('amount'))['amount__sum'] or 0
    total_expenses_all = expenses_all.aggregate(Sum('amount'))['amount__sum'] or 0
    balance_all = total_contributions_all - total_expenses_all

    # 🟩 Room contributions (monthly + overall)
    room_data = []
    for room in rooms:
        month_total = contributions_month.filter(room=room).aggregate(Sum('amount'))['amount__sum'] or 0
        overall_total = contributions_all.filter(room=room).aggregate(Sum('amount'))['amount__sum'] or 0
        room_data.append({
            'room': room.number,
            'month_total': month_total,
            'overall_total': overall_total,
        })

    context = {
        'selected_month': selected_month,
        'month_name': month_name,
        'room_data': room_data,

        # 🟩 Send both monthly and all-time expenses
        'expenses_month': expenses_month,
        'expenses_all': expenses_all,

        'total_contributions_month': total_contributions_month,
        'total_expenses_month': total_expenses_month,
        'balance_month': balance_month,

        'total_contributions_all': total_contributions_all,
        'total_expenses_all': total_expenses_all,
        'balance_all': balance_all,

        'announcements': announcements,
    }

    return render(request, 'finance/dashboard.html', context)
