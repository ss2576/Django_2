import datetime
from mainapp.models import Product, ProductCategory
from django.shortcuts import get_object_or_404, render
from basketapp.models import Basket
import random
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings
from django.core.cache import cache
from django.template.loader import render_to_string
from django.views.decorators.cache import cache_page
from django.http import JsonResponse
from django.views.decorators.cache import never_cache



def products_ajax(request, pk=None, page=1):
   title = 'продукты'
   if request.is_ajax():
       links_menu = get_links_menu()

       if pk:
           if pk == '0':
               category = {
                   'pk': 0,
                   'name': 'все'
               }
               products = get_products_orederd_by_price()
           else:
               category = get_category(pk)
               products = get_products_in_category_orederd_by_price(pk)

           block_products = []
           step = 4
           for i in range(0, len(products), step):
               array2 = products[i:i + step]

               if len(array2) == 4:
                   a = array2[0], array2[1], array2[2], array2[3]
                   block_products.append(a)

               elif len(array2) == 3:
                   a = array2[0], array2[1], array2[2]
                   block_products.append(a)

               elif len(array2) == 2:
                   a = array2[0], array2[1]
                   block_products.append(a)
               else:
                   a = array2[0]
                   block_products.append(a)


           paginator = Paginator(block_products, 2)
           try:
               products_paginator = paginator.page(page)
           except PageNotAnInteger:
               products_paginator = paginator.page(1)
           except EmptyPage:
               products_paginator = paginator.page(paginator.num_pages)

           content = {
               'title': title,
               'links_menu': links_menu,
               'category': category,
               'products': products_paginator,
           }

           result = render_to_string('includes/inc_products_list_content.html', context=content, request=request)
           return JsonResponse({'result': result})



def get_links_menu():
   if settings.LOW_CACHE:
       key = 'links_menu'
       links_menu = cache.get(key)
       if links_menu is None:
           links_menu = ProductCategory.objects.filter(is_active=True)
           cache.set(key, links_menu)
       return links_menu
   else:
       return ProductCategory.objects.filter(is_active=True)


def get_category(pk):
   if settings.LOW_CACHE:
       key = f'category_{pk}'
       category = cache.get(key)
       if category is None:
           category = get_object_or_404(ProductCategory, pk=pk)
           cache.set(key, category)
       return category
   else:
       return get_object_or_404(ProductCategory, pk=pk)


def get_products():
   if settings.LOW_CACHE:
       key = 'products'
       products = cache.get(key)
       if products is None:
           products = Product.objects.filter(is_active=True, \
                         category__is_active=True).select_related('category')
           cache.set(key, products)
       return products
   else:
       return Product.objects.filter(is_active=True, \
                         category__is_active=True).select_related('category')


def get_product(pk):
   if settings.LOW_CACHE:
       key = f'product_{pk}'
       product = cache.get(key)
       if product is None:
           product = get_object_or_404(Product, pk=pk)
           cache.set(key, product)
       return product
   else:
       return get_object_or_404(Product, pk=pk)


def get_products_orederd_by_price():
   if settings.LOW_CACHE:
       key = 'products_orederd_by_price'
       products = cache.get(key)
       if products is None:
           products = Product.objects.filter(is_active=True, \
                                  category__is_active=True).order_by('price')
           cache.set(key, products)
       return products
   else:
       return Product.objects.filter(is_active=True,\
                                 category__is_active=True).order_by('price')


def get_products_in_category_orederd_by_price(pk):
   if settings.LOW_CACHE:
       key = f'products_in_category_orederd_by_price_{pk}'
       products = cache.get(key)
       if products is None:
           products = Product.objects.filter(category__pk=pk, is_active=True,\
                              category__is_active=True).order_by('price')
           cache.set(key, products)
       return products
   else:
       return Product.objects.filter(category__pk=pk, is_active=True, \
                              category__is_active=True).order_by('price')




def get_basket(user):
    if user.is_authenticated: 
        return Basket.objects.filter(user=user)
    else:
        return []


def get_hot_product():
   products = get_products()

   return random.sample(list(products), 1)[0]


def get_same_products(hot_product):
    same_products = Product.objects.filter(category=hot_product.category, is_active=True, category__is_active=True).exclude(pk=hot_product.pk)[:3]

    return same_products


def main(request):
    title = 'главная'
    products = get_products()[:4]
    date_begin = datetime.datetime.now()

    content = {
        'title': title,
        'products': products,
        #'basket': get_basket(request.user),
        'date_begin': date_begin,
    }
    return render(request, 'index.html', content)


@never_cache
def products(request, pk=None, page=1):
   title = 'продукты'
   links_menu = get_links_menu()

   if pk:
       if pk == '0':
            category = {
                'pk': 0,
                'name': 'все',
            }
            products = get_products_orederd_by_price()
       else:
            category = get_category(pk)
            products = get_products_in_category_orederd_by_price(pk)

       block_products = []
       step = 4
       for i in range(0, len(products), step):
           array2 = products[i:i + step]

           if len(array2) == 4:
               a = array2[0], array2[1], array2[2], array2[3]
               block_products.append(a)

           elif len(array2) == 3:
               a = array2[0], array2[1], array2[2]
               block_products.append(a)

           elif len(array2) == 2:
               a = array2[0], array2[1]
               block_products.append(a)
           else:
               a = array2[0]
               block_products.append(a)


       paginator = Paginator(block_products, 2)
       try:
           products_paginator = paginator.page(page)
       except PageNotAnInteger:
           products_paginator = paginator.page(1)
       except EmptyPage:
           products_paginator = paginator.page(paginator.num_pages)

       content = {
           'title': title,
           'links_menu': links_menu,
           'category': category,
           'products': products_paginator,
           #'basket': basket,
       }

       return render(request, 'products_list.html', content)

   hot_product = get_hot_product()
   same_products = get_same_products(hot_product)

   content = {
       'title': title,
       'links_menu': links_menu,
       'hot_product': hot_product,
       'same_products': same_products,
       #'basket': basket,
   }

   return render(request, 'products.html', content)


@never_cache
def product(request, pk):
   title = 'продукты'
   links_menu = get_links_menu()
   product = get_product(pk)

   content = {
       'title': title,
       'links_menu': links_menu,
       'product': product,
   }

   return render(request, 'product.html', content)

def contact(request):
   title = 'о нас'

   content = {
       'title': 'контакты',
   }
   return render(request, 'contact.html', content)


def products_all(request):
    links_menu = [
        {'href': 'products_all', 'name': 'все'},
        {'href': 'products_home', 'name': 'дом'},
        {'href': 'products_office', 'name': 'офис'},
        {'href': 'products_modern', 'name': 'модерн'},
        {'href': 'products_classic', 'name': 'классика'},
    ]
    content = {
        'title': 'продукты',
        'links_menu': links_menu
    }
    return render(request, 'products.html', content)


def products_home(request):
    links_menu = [
        {'href': 'products_all', 'name': 'все'},
        {'href': 'products_home', 'name': 'дом'},
        {'href': 'products_office', 'name': 'офис'},
        {'href': 'products_modern', 'name': 'модерн'},
        {'href': 'products_classic', 'name': 'классика'},
    ]
    content = {
        'title': 'продукты',
        'links_menu': links_menu
    }
    return render(request, 'products.html', content)


def products_office(request):
    links_menu = [
        {'href': 'products_all', 'name': 'все'},
        {'href': 'products_home', 'name': 'дом'},
        {'href': 'products_office', 'name': 'офис'},
        {'href': 'products_modern', 'name': 'модерн'},
        {'href': 'products_classic', 'name': 'классика'},
    ]
    content = {
        'title': 'продукты',
        'links_menu': links_menu
    }
    return render(request, 'products.html', content)


def products_modern(request):
    links_menu = [
        {'href': 'products_all', 'name': 'все'},
        {'href': 'products_home', 'name': 'дом'},
        {'href': 'products_office', 'name': 'офис'},
        {'href': 'products_modern', 'name': 'модерн'},
        {'href': 'products_classic', 'name': 'классика'},
    ]
    content = {
        'title': 'продукты',
        'links_menu': links_menu
    }
    return render(request, 'products.html', content)


def products_classic(request):
    links_menu = [
        {'href': 'products_all', 'name': 'все'},
        {'href': 'products_home', 'name': 'дом'},
        {'href': 'products_office', 'name': 'офис'},
        {'href': 'products_modern', 'name': 'модерн'},
        {'href': 'products_classic', 'name': 'классика'},
    ]
    content = {
        'title': 'продукты',
        'links_menu': links_menu
    }
    return render(request, 'products.html', content)
