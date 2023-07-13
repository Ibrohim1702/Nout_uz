from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect

from Tg_Nout_uz.models import Category
from .forms import CategoryFrom


@staff_member_required(login_url='dashboard_login')
def edit_add(requests, pk=None):
    forms = CategoryFrom()

    if pk:
        ctg = Category.objects.get(pk=pk)
        forms = CategoryFrom(instance=ctg)
    else:
        ctg = None

    if requests.POST:
        if pk:
            form = CategoryFrom(requests.POST, instance=ctg)
        else:
            form = CategoryFrom(requests.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard_ctg_list')
        else:
            print(form.errors)

    ctx = {
        "forms": forms
    }
    return render(requests, 'dashboard/category/from.html', ctx)


@staff_member_required(login_url='dashboard_login')
def ctg_list_detail(requests, pk=None):
    ctgs = Category.objects.all()
    html = "list"
    ctx = {
        "ctgs": ctgs
    }
    if pk:
        ctg = Category.objects.get(pk=pk)
        ctx['ctg'] = ctg
        html = "detail"

    return render(requests, f"dashboard/category/{html}.html", ctx)


@staff_member_required(login_url='dashboard_login')
def del_conf_delete(requests, pk=None, dlt=None):
    if dlt:
        Category.objects.get(pk=dlt).delete()
        return redirect("dashboard_ctg_list")

    ctg = Category.objects.get(pk=pk)
    ctx = {
        "ctg": ctg
    }
    return render(requests, "dashboard/category/delete.html", ctx)
