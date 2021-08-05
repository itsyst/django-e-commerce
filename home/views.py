import decimal
from tags.models import TaggedItem
from django.contrib.contenttypes.models import ContentType
from django.db.models.fields import DecimalField
from django.shortcuts import render
from django.db.models import Value, Q, F, Func, Count, ExpressionWrapper
from django.db.models.functions import Concat, Upper
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.aggregates import Max, Min, Avg, Sum
from store.models import Collection, Customer, Order, OrderItem, Product


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
    # querysets = Order.objects.filter(customer__id=2)[:5]
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

    # selecting fields and related fields to query "__ notation to access the related fields" # return a dictionary
    # queryset = Product.objects.values('id', 'title', 'collection__title')[:5]
    # queryset = Product.objects.values_list('id','title', 'collection__title)[:5] # return a tuple

    # Return a defined fields - a dictionary object - be carefull when using
    # queryset = Product.objects.only('id', 'title')[:5]
    # queryset = Product.objects.defer('description')[:5]

    # Selecting related objects
    # queryset = Product.objects.all() # application is hanging
    # use select_related when the end up of the relationship has one instance like collection
    # queryset = Product.objects.select_related('collection').all()[:5]
    # use prefetch_related when the other end up of the relationship has many objects
    # queryset = Product.objects.prefetch_related('promotions').all()

    # Get the last 5 orders with their customer and items (include product)
    querysets = Order.objects.select_related('customer').prefetch_related(
        'orderitem_set__product').order_by('-placed_at')[:5]

    # Aggregate objects - number of products
    # result = Product.objects.aggregate(
    #    count=Count('id'), min_price=Min('unit_price'))
    # Aggregate objects - number of orders
    # result = Order.objects.aggregate(count = Count('id))
    # Aggregate units of product 1 that has has been sold
    # result = OrderItem.objects.filter(
    #    product__id=1).aggregate(units_sold=Sum('quantity'))
    # Aggregate orders that customer 1 has placed
    # result = Order.objects.filter(customer__id = 1).aggregate( orders_placed = Count('id'))
    # return min, max and avg price of products in collection 3
    result = Product.objects.filter(
        collection__id=3).aggregate(min_price=Min('unit_price'), max_price=Max('unit_price'), avg_price=Avg('unit_price'))

    # Annotating objects - set every field to true
    # results = Customer.objects.annotate(is_new=Value(True))
    # Annotating objects - reference the id field
    # results = Customer.objects.annotate(new_id = F('id') + 1)

    # Calling database functions
    results = Customer.objects.annotate(
        # CONTACT
        full_name=Upper(Func(F('first_name'), Value(' '), F(
            'last_name'), function='CONCAT'))
        # full_name = Concat('first_name', Value(' '), 'last_name')
    )

    # get the number of orders that each customer has placed
    queryset_count = Customer.objects.annotate(orders_count=Count('order'))[:5]

    # Expression wrappers
    # discounted_price = ExpressionWrapper(F('unit_price')*0.8, output_field=DecimalField())
    # queryset = Product.objects.annotate(discounted_price=discounted_price)
    # Customers and their last Id
    # queryset = Customer.objects.annotate(last_order_is = Max('order_id'))
    # Collections and count of their products
    # queryset = Collection.objects.annotate(products_count = Count('product'))
    # Customers with more than 5 orders
    # queryset = Customer.objects.annotate(
    #    orders_count=Count('order')).filter(orders_count__gt=5)
    # Customers and the total amount they have spent
    # queryset = Customer.objects.annotate(total_spent_sum=Sum(
    #    F('order__orderitem__unit_price')*F('order__orderitem__quantity')))
    # Top 5 best selling products and their total sales
    # queryset = Product.objects.annotate(total_sales=Sum(
    #    F('orderitem__unit_price')*F('orderitem__quantity'))).order_by('total_sales')[:5]

    # Quering generic relationships
    # content_type = ContentType.objects.get_for_model(Product)
    # queryset = TaggedItem.objects \
                        #  .select_related('tag') \
                        #  .filter(
                        #        content_type = content_type,
                        #        object_id = 1
                        # )

    return render(request, 'home.html',
                  {
                      'name': 'Khaled',
                      'products': list(queryset),
                      'customers': list(query_set),
                      'orders': list(querysets),
                      'product': product,
                      'result': result,
                      'results': list(results),
                      'counts': list(queryset_count)
                  })
