from django.shortcuts import render
from django.db.models import Q, F
from django.core.exceptions import ObjectDoesNotExist
from store.models import Customer, Order, OrderItem, Product


def welcome(request):
    # Customers with .com accounts
    query_set = Customer.objects.filter(email__icontains='.com')[:5]

    # Collections that don't have a featured product
    # queryset = Product.objects.filter(featured_product__isnull = True)
    # Products with low inventory
    # queryset = Product.objects.filter(inventory__lt = 10)
    # query_set = Product.objects.filter(unit_price__range=(20, 30))
    # query_set = Product.objects.filter(collection__id__range=(1,2,3))
    # queryset = Product.objects.filter(unit_price__gt=20)
    # queryset = Product.objects.filter(last_update__year=2021)
    # queryset = Product.objects.filter(description__isnull = True)
    # queryset = Product.objects.filter(title__icontains='Cup')

    # Orders placed by customer with id = 2
    querysets = Order.objects.filter(customer__id=2)[:5]
    # Orders items for products in collection 3
    # queryset = OrderItem.objects.filter(product__collection__id=3)

    # Products: inventory < 10 AND price < 20 => Complex lookup
    # queryset = Product.objects.filter(inventory__lt=10, unit_price__lt=20)
    # Same result
    # queryset = Product.objects.filter(inventory__lt=10).filter(unit_price__lt=20)

    # Products: inventory < 10 OR price < 20 => not less than 20 negation ~Q(unit_price__lt=20)
    # queryset = Product.objects.filter(
    #    Q(inventory__lt=10) | Q(unit_price__lt=20))

    # Products: inventory = price: Using the F object comparing
    # queryset = Product.objects.filter(inventory=F('unit_price'))
    # queryset = Product.objects.filter(inventory=F('collection_id')).order_by('title')
    # queryset sort by multiple fields and in order desc
    queryset = Product.objects.filter(inventory=F(
        'collection_id')).order_by('unit_price', '-title')[:5]

    # return the first 5 objects 0,1,2,3,4
    # queryset = Product.objects.all()[:5]

    # return 5 objects 5,6,7,8,9
    # queryset = Product.objects.all()[5:10]

    # get a unique object
    # product = Product.objects.order_by('unit_price')[0]

    # get the first object
    # product = Product.objects.earliest('unit_price')

    # get the last object
    product = Product.objects.latest('unit_price')

    # selecting fields and related fields to query "__ notation to access the related fields"
    # return a dictionary
    # queryset = Product.objects.values('id', 'title', 'collection__title')[:5]
    # queryset = Product.objects.values_list('id','title', 'collection__title)[:5] # return a tuple

    # Return products that have been ordred and sort them by title
    queryset = Product.objects.filter(id__in=OrderItem.objects.values(
        'product_id').distinct()).order_by('title')[:5]

    return render(request, 'home.html',
                  {
                      'name': 'Khaled',
                      'products': list(queryset),
                      'customers': list(query_set),
                      'orders': list(querysets),
                      'product': product
                  })
