from django.shortcuts import render, redirect
from django.views import View
from customer.models import OrderModel
from django.utils.timezone import datetime
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

# Create your views here.
class Dashboard(LoginRequiredMixin, UserPassesTestMixin, View):
    def get(self, request, *args, **kwargs):
        today = datetime.today()
        orders = OrderModel.objects.filter(
            created_on__year=today.year,
            created_on__month=today.month,
            created_on__day=today.day)
        total_revenue = 0

        unshipped_orders = []

        for order in orders:
            total_revenue += order.price

            if not order.is_shipped:
                unshipped_orders.append(order)

        context = {
            'orders': unshipped_orders,
            "total_revenue": total_revenue,
            'total_orders': len(orders)
        }

        return render(request, 'restaurant/dashboard.html', context)

    def test_func(self):

        return self.request.user.groups.filter(name='Staff').exists()

class OrderDetails(LoginRequiredMixin, UserPassesTestMixin, View):
    def get(self, request, pk, *args, **kwargs):
        order = OrderModel.objects.get(pk=pk)

        context = {'order': order}

        return render(request, 'restaurant/order-details.html', context)

    def test_func(self):

        return self.request.user.groups.filter(name='Staff').exists()

    def post(self, request, pk, *args, **kwargs):
        order = OrderModel.objects.get(pk=pk)
        order.is_shipped = True
        order.save()

        context = {'order': order}

        return render(request, 'restaurant/order-details.html', context)

    def test_func(self):

        return self.request.user.groups.filter(name='Staff').exists()