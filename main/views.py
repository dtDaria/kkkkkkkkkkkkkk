from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import CreateView
from django.urls import reverse_lazy
from .forms import RegisterUserForm, OrderCreate
from django.contrib.auth.decorators import login_required
from .models import Order


class RegisterView(CreateView):
    template_name = 'registration/register.html'
    form_class = RegisterUserForm
    success_url = reverse_lazy('login')


def catalog(request):
    orders = Order.objects.filter(status="canceled")
    order_by = request.GET.get('order_by')
    counter = Order.objects.filter(status='confirmed').count()

    if order_by:
        orders = orders.order_by(order_by)
    else:
        orders = orders.order_by('-date')[:4]

    return render(request, 'catalog/catalog.html',
                  context={
                      'orders': orders,
                      'counter': counter,
                  })


# для автор.пользователей
@login_required
def order_list(request):
    STATUS_CHOICES = [
        ('new', 'Новая'),
        ('confirmed', 'Принято в работу'),
        ('canceled', 'Выполнено')
    ]
    status = request.GET.get('status')
    if status:
        orderlist = Order.objects.filter(author=request.user, status=status)
    else:
        orderlist = Order.objects.filter(author=request.user)

    return render(request, 'catalog/orders.html', context={
        'status': STATUS_CHOICES,
        'order_list': orderlist,
    })


@login_required
def order_view(request):
    if request.method == 'POST':
        form = OrderCreate(request.POST, request.FILES)
        if form.is_valid():
            form.instance.author_id = request.user.pk
            order = form.save()
            messages.add_message(request, messages.SUCCESS,
                                 'Заявка создана')
            return redirect('/orders')
    else:
        form = OrderCreate(initial={'author': request.user.pk})
    context = {'form': form}
    return render(request, 'catalog/order_create.html', context)


@login_required
def delete_order(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if order.status != 'new':
        messages.add_message(request, messages.ERROR, 'статус изменен нельзя удалить')
        return redirect('orders')
    if request.method == 'POST':
        order.delete()
        messages.add_message(request, messages.SUCCESS, 'удалено')
        return redirect('orders')
    else:
        context = {'order': order}
        return render(request, 'catalog/order_delete.html', context)
