import decimal
from django.contrib.contenttypes.models import ContentType
from django.db.models.fields import DateTimeCheckMixin, DateTimeField, DecimalField
from django.shortcuts import render
from django.db.models import Value, Q, F, Func, Count, ExpressionWrapper
from django.db.models.functions import Concat, Upper
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.aggregates import Max, Min, Avg, Sum
from store.models import Cart, CartItem, Collection, Customer, Order, OrderItem, Product, InitializationStatus  
from tags.models import TaggedItem, TaggedItemManager
from django.db import connection, transaction

# @transaction.atomic() #decorator to this view function- wrap all code inside the transaction


def welcome(request):
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
    # queryset = Product.objects.filter(inventory=F('collection_id')).order_by('unit_price', '-title')[:5]

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
    products = Product.objects.select_related('collection').all()[:5]
    # use prefetch_related when the other end up of the relationship has many objects
    # queryset = Product.objects.prefetch_related('promotions').all()[:5]

    # Customers with .com accounts
    customers = Customer.objects.filter(email__icontains='.com')[:5]

    # Get the last 5 orders with their customer and items (include product)
    orders = Order.objects.select_related('customer').prefetch_related('orderitem_set').prefetch_related('orderitem_set__product').order_by('-placed_at')[:5]
    for order in orders:
        for item in order.orderitem_set.all():
            item.total_price = item.unit_price * item.quantity
    # Aggregate objects - number of products
    # result = Product.objects.aggregate(count=Count('id'), min_price=Min('unit_price'))
    # Aggregate objects - number of orders
    # result = Order.objects.aggregate(count = Count('id))
    # Aggregate units of product 1 that has has been sold
    # result = OrderItem.objects.filter(
    #    product__id=1).aggregate(units_sold=Sum('quantity'))
    # Aggregate orders that customer 14 has placed and count only failed payments
    result = Order.objects.filter(customer__id = 14).aggregate( orders_placed = Count('payment_status', filter=Q(payment_status='F')))
    # return min, max and avg price of products in collection 3
    #result = Product.objects.filter(collection__id=3).aggregate(min_price=Min('unit_price'), max_price=Max('unit_price'), avg_price=Avg('unit_price'))

    # Annotating objects - set every field to true
    # results = Customer.objects.annotate(is_new=Value(True))[:5]
    # Annotating objects - reference the id field
    # results = Customer.objects.annotate(new_id = F('id') + 1)[:5]

    # Calling database functions
    results = Customer.objects.annotate(
        # CONTACT
        # full_name=Upper(Func(F('first_name'), Value(' '), F(
        #     'last_name'), function='CONCAT'))
        full_name = Upper(Concat('first_name', Value(' '), 'last_name')),
        is_new=Value(True)
    )[:5]

    # get the number of orders that each customer has placed
    orders_count = Customer.objects.annotate(orders_count=Count('order'))[:5]

    # Expression wrappers
    # discounted_price = ExpressionWrapper(F('unit_price')*0.8, output_field=DecimalField())
    # queryset = Product.objects.annotate(discounted_price=discounted_price)[:5]
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
    # tags_set = TaggedItem.objects \
    #                      .select_related('tag') \
    #                      .filter(
    #                            content_type = content_type,
    #                            object_id = 12
    #                     )
    # Using custom manager - class model -> models.py
    tags_set = TaggedItem.objects.get_tags_for(Product, 12)
    
    # QuerySet Cache : structure the code for better cache 

   
    ## Create a new collection object
    # Check if the initialization has already run
    init_status, created = InitializationStatus.objects.get_or_create(id=1)
    if not init_status.has_run:
      collection = Collection()
      ## collection = Collection(title = 'Video Games') other way to initialise this collection  but better with . dot operator
      collection.title = 'Videos Games'
      collection.featured_product = Product(pk=13)
      ## collection.featured_product_id = 1 or use the pk of the product_id field
      ### Other short way to create this collection.
      ### Collection.objects.create(
      ###    title="Videos",
      ###    featured_product=Product(pk=2)
      ###)

      collection.save()
      # Update the initialization status
      init_status.has_run = True
      init_status.save()

    if created:
        print("The InitializationStatus object was created.")
    else:
        print("The InitializationStatus object already existed.")

    ###  Update collection
    if not init_status.update_applied:
      # collection = Collection.objects.get(pk=11)
      # collection.featured_product = None
      ##Alternatively using update method
      Collection.objects.filter(pk=2).update(
          featured_product=None
      )

      # Mark the update as applied
      init_status.update_applied = True
      init_status.save()
      collection.save()

    ##  Delete single collection
    if not init_status.delete_applied:
      collection = Collection(pk=11)
      collection.delete()

      # Mark the delete operation as applied
      init_status.delete_applied = True
      init_status.save()

      # ## Delete multiple collections with id greater than 5
      # Collection.objects.filter(id__gt=12).delete()
      # ## Mark the delete operation as applied
      # init_status.delete_applied = True
      # init_status.save()

      ## Transactions: multiple changes in database
      # This part has to be inside a transaction function
      # with transaction.atomic():
      #     order = Order()
      #     order.customer = Customer(pk=1)
      #     order.save()

      #     item = OrderItem()
      #     item.order = order
      #     item.product = Product(pk=1)
      #     item.quantity = 2
      #     item.unit_price = 16
      #     item.save()

      ## Execute Raw sql queries for complex queries only
      ## queryset_raw = Product.objects.raw('SELECT id, title FROM store_product')
      # # access the database directly
      # with connection.cursor() as cursor:
      #     sql = 'SELECT title FROM store_collection'
      #     cursor.execute(sql)
          ##call a procedure / return all customers
          ##cursor.callproc('get_customers')
          ##call a procedure / return specific customer
          ##cursor.callproc('get_customer', [1])


    ####
    ###  Create a shopping cart with an item
    # cart = Cart()
    # cart.save()
    # item = CartItem()
    # item.cart = cart
    # item.product_id =2
    # item.quantity = 2
    # item.save()
    # item = CartItem.objects.create(
    #     cart=Cart(pk=1),
    #     product=Product(pk=1),
    #     quantity=1
    # )

    ####
    ###  Update the quantity of an item in a shopping cart
    # item = CartItem.objects.get(pk=2)
    # item.quantity = 3
    # item.save()
    # CartItem.objects.filter(pk=2).update(
    #     quantity=3
    # )


    ###
    ##  Remove a shopping cart with its items (Cascade no need to delete each item individually)
    # item = CartItem(pk=2)
    # item.delete()
    # CartItem.objects.filter(pk=2).delete()



    return render(request, 'home.html',
                  {
                      'name': 'Khaled',
                      'product': product,
                      'products': list(products),
                      'customers': list(customers),
                      'orders': list(orders),
                      'result': result,
                      'results': list(results),
                      'counts': list(orders_count),
                      'tags': list(tags_set),
                      # 'rows': list(queryset_raw),
                  })


# python manage.py createsuperuser    
# username: admin
# password: password     
# forget password run this command:
# python manage.py changepassword admin