from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from store.models import Customer, Order, OrderItem, Product


def welcome(request):
    # Customers with .com accounts
    query_set = Customer.objects.filter(email__icontains='.com')
   
    # Collections that don't have a featured product
    # queryset = Product.objects.filter(featured_product__isnull = True)
    # Products with low inventory
    # queryset = Product.objects.filter(inventory__lt = 10)
    # query_set = Product.objects.filter(unit_price__range=(20, 30))
    # query_set = Product.objects.filter(collection__id__range=(1,2,3))
    # queryset = Product.objects.filter(unit_price__gt=20)
    # queryset = Product.objects.filter(last_update__year=2021)
    # queryset = Product.objects.filter(description__isnull = True)
    queryset = Product.objects.filter(title__icontains='Cup')

    # Orders placed by customer with id = 2
    querysets = Order.objects.filter(customer__id=2)
    # Orders items for products in collection 3
    # queryset = OrderItem.objects.filter(product__collection__id=3)

    return render(request,
                  'home.html',
                  {'name': 'Khaled',
                   'products': list(queryset),
                   'customers': list(query_set),
                   'orders': list(querysets)
                   }
                  )
