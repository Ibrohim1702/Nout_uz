from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect

from Tg_Nout_uz.models import Brands
from .forms import BrandsFrom


@staff_member_required(login_url='dashboard_login')
def edit_add(requests, pk=None):
    forms = BrandsFrom()

    if pk:
        brd = Brands.objects.get(pk=pk)
        forms = BrandsFrom(instance=brd)
    else:
        brd = None

    if requests.POST:
        if pk:
            form = BrandsFrom(requests.POST, instance=brd)
        else:
            form = BrandsFrom(requests.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard_brd_list')
        else:
            print(form.errors)

    ctx = {
        "forms": forms
    }
    return render(requests, 'dashboard/brands/from.html', ctx)


@staff_member_required(login_url='dashboard_login')
def ctg_list_detail(requests, pk=None):
    brds = Brands.objects.all()
    html = "list"
    ctx = {
        "brds": brds
    }
    if pk:
        brd = Brands.objects.get(pk=pk)
        ctx['brd'] = brd
        html = "detail"

    return render(requests, f"dashboard/brands/{html}.html", ctx)


@staff_member_required(login_url='dashboard_login')
def del_conf_delete(requests, pk=None, dlt=None):
    if dlt:
        Brands.objects.get(pk=dlt).delete()
        return redirect("dashboard_brd_list")

    brd = Brands.objects.get(pk=pk)
    ctx = {
        "brd": brd
    }
    return render(requests, "dashboard/brands/delete.html", ctx)
