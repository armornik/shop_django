from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from django.template.loader import render_to_string
from django.http import JsonResponse
from django.db.models import F, Q

from basketapp.models import Basket
from mainapp.models import Product


@login_required
def basket(request):
    title = 'корзина'
    basket_items = Basket.objects.filter(user=request.user).order_by('product__category')
    context = {
        'title': title,
        'basket_items': basket_items,
    }
    return render(request, 'basketapp/basket.html', context)


@login_required
def basket_add(request, pk):
    if 'login' in request.META.get('HTTP_REFERER'):
        return HttpResponseRedirect(reverse('products:product', args=[pk]))

    product = get_object_or_404(Product, pk=pk)

    # Фильтрация по обоим
    basket = Basket.objects.filter(user=request.user, product=product).first()
    # # Фильтрация или
    # basket = Basket.objects.filter(Q(user=request.user) | Q(product=product)).first()

    if not basket:
        basket = Basket(user=request.user, product=product)

    basket.quantity += 1
    basket.save()

    # # Пример использования F-объекта
    # old_basket_item = Basket.get_product(user=request.user, product=product)
    # if old_basket_item:
    #     old_basket_item[0].quantity = F('quantity') + 1
    #     old_basket_item[0].save()
    # else:
    #     pass

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def basket_remove(request, pk):
    basket_record = get_object_or_404(Basket, pk=pk)
    basket_record.delete()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def basket_edit(request, pk, quantity):
    if request.is_ajax():
        quantity = int(quantity)
        new_basket_item = Basket.objects.get(pk=int(pk))

        if quantity > 0:
            new_basket_item.quantity = quantity
            new_basket_item.save()
        else:
            new_basket_item.delete()

        basket_items = Basket.objects.filter(user=request.user).order_by('product__category')

        context = {
            'basket_items': basket_items,
        }

        result = render_to_string('basketapp/includes/inc_basket_list.html', context)

        return JsonResponse({'result': result})
