import re
import time
from django.shortcuts import render, redirect
from futurelabs.models import ProductsDetails
from django.contrib import messages
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
        return render(request,'index.html',{"products":display_products})
    else:
        res = scrape_aliex_data(request.POST["search"])
        if res:
            messages.success(request, 'Scrapped Data Stored Successfully')
        else:
            messages.success(request, 'Internal Error! Please Refresh and try Again')
        time.sleep(3)
        return redirect("/")

def delete_products(request):
    ProductsDetails.objects.all().delete()
    messages.success(request, 'Products Data Cleared Successfully')
    return redirect("/")
