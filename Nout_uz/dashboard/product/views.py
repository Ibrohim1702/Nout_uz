from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect
from Tg_Nout_uz.models import Product
from .forms import ProductFrom


@staff_member_required(login_url='dashboard_login')
def edit_add(requests, pk=None):
    forms = ProductFrom()

    if pk:
        product = Product.objects.get(pk=pk)
        forms = ProductFrom(instance=product)
    else:
        product = None

    if requests.POST:
        if pk:
            form = ProductFrom(requests.POST, instance=product)
        else:
            form = ProductFrom(requests.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard_pro_list')
        else:
            print(form.errors)

    ctx = {
        "forms": forms
    }
    return render(requests, 'dashboard/product/from.html', ctx)


@staff_member_required(login_url='dashboard_login')
def ctg_list_detail(requests, pk=None):
    products = Product.objects.all()
    html = "list"
    ctx = {
        "products": products
    }
    if pk:
        product = Product.objects.get(pk=pk)
        ctx['product'] = product
        html = "detail"

    return render(requests, f"dashboard/product/{html}.html", ctx)


@staff_member_required(login_url='dashboard_login')
def del_conf_delete(requests, pk=None, dlt=None):
    if dlt:
        Product.objects.get(pk=dlt).delete()
        return redirect("dashboard_pro_list")

    product = Product.objects.get(pk=pk)
    ctx = {
        "product": product
    }
    return render(requests, "dashboard/product/delete.html", ctx)
