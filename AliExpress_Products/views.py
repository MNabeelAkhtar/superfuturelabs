import re
from django.shortcuts import render, redirect
from AliExpress_Products.models import ProductsDetails
from bot import scrape_aliex_data

def products(request):
    if request.method == "GET":
        display_products = ProductsDetails.objects.all()
        if request.GET.get("title"):
            display_products = display_products.filter(product_name__icontains=request.GET["title"])
        if request.GET.get("shipping_method"):
            display_products = display_products.filter(shipping_method=request.GET["shipping_method"])
            print(request.GET["shipping_method"])
        if request.GET.get("min_price") and request.GET.get("max_price"):
            display_products = display_products.filter(
                total_price__gte=request.GET["min_price"],
                total_price__lte=request.GET["max_price"]
            )
        elif request.GET.get("min_price"):
            display_products = display_products.filter(total_price__gte=request.GET["min_price"])
        elif request.GET.get("max_price"):
            display_products = display_products.filter(total_price__lte=request.GET["max_price"])
        if request.GET.get("price_range") == "low_high":
            display_products = display_products.order_by('total_price')
        elif request.GET.get("price_range") == "high_low":
            display_products = display_products.order_by('-total_price')
        return render(request,'Index.html',{"ProductDetails":display_products})
    else:
        scrape_aliex_data(request.POST["search"])
        return redirect("/")