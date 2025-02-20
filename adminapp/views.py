from django.shortcuts import render,redirect
from .models import CategoryDB,ProductDB
from webpage.models import ContactDB,Newsletter
from django.utils.datastructures import MultiValueDictKeyError
from django.core.files.storage import FileSystemStorage

from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login

def admin_home(request):
    return render(request,"admin_home.html")

def CategoryAdd(request):
    return render(request,"CategoryAdd.html")
def CategoryDisplay(request):
    data = CategoryDB.objects.all()
    return render(request,"CategoryDisplay.html",{'categories':data})
def CategorySave(request):
    if request.method == 'POST':
        na = request.POST.get('name')
        de = request.POST.get('description')
        im = request.FILES['image']
        category = CategoryDB(name=na,description=de,image=im)
        category.save()
        return redirect('CategoryDisplay')
def CategoryDelete(request,cat_id):
    x = CategoryDB.objects.get(id=cat_id)
    x.delete()
    return redirect('CategoryDisplay')
def CategoryEdit(request,cat_id):
    data = CategoryDB.objects.get(id=cat_id)
    return render(request,"CategoryEdit.html",{'data': data})
def CategoryUpdate(request,cat_id):
    if request.method == 'POST':
        na = request.POST.get('name')
        de = request.POST.get('description')
        try:
            im = request.FILES['image']
            fs = FileSystemStorage()
            img_name = "category_images/"+im.name
            file = fs.save(img_name,im)
        except MultiValueDictKeyError:
            file = CategoryDB.objects.get(id=cat_id).image

        CategoryDB.objects.filter(id=cat_id).update(name=na,description=de,image=file)
        return redirect('CategoryDisplay')

def ProductAdd(request):
    category = CategoryDB.objects.all()
    return render(request,"ProductAdd.html",{'category': category})
def ProductDisplay(request):
    data = ProductDB.objects.all()
    return render(request,"ProductDisplay.html",{'products':data})
def ProductSave(request):
    if request.method == 'POST':
        na = request.POST.get('name')
        br = request.POST.get('brand')
        ca = request.POST.get('category')
        de = request.POST.get('description')
        im = request.FILES['image']
        pr = request.POST.get('price')
        product = ProductDB(name=na,brand=br,category=ca,description=de,image=im,price=pr)
        product.save()
        return redirect('ProductDisplay')

def ProductDelete(request,prod_id):
    x = ProductDB.objects.get(id=prod_id)
    x.delete()
    return redirect('ProductDisplay')
def ProductEdit(request,prod_id):
    category = CategoryDB.objects.all()
    data = ProductDB.objects.get(id=prod_id)
    return render(request,"ProductEdit.html",{'data': data, 'category': category})

def ProductUpdate(request,prod_id):
    if request.method == 'POST':
        na = request.POST.get('name')
        br = request.POST.get('brand')
        ca = request.POST.get('category')
        de = request.POST.get('description')
        pr = request.POST.get('price')
        try:
            im = request.FILES['image']
            fs = FileSystemStorage()
            img_name = "product_images/"+im.name
            file = fs.save(img_name,im)
        except MultiValueDictKeyError:
            file = ProductDB.objects.get(id=prod_id).image
        ProductDB.objects.filter(id=prod_id).update(name=na, brand=br, category=ca, description=de, image=file, price=pr)
        return redirect('ProductDisplay')

def admin_login_page(request):
    return render(request,"admin_login_page.html")

def admin_login(request):
    if request.method =="POST":
        un = request.POST.get('username')
        pwd = request.POST.get('password')

        if User.objects.filter(username__contains=un).exists():
            x = authenticate(username=un,password=pwd)
            if x is not None:
                login(request,x)
                request.session['username'] = un
                request.session['password'] = pwd
                return redirect(admin_home)
            else:
                return redirect(admin_login_page)
        else:
            return redirect(admin_login_page)

def admin_logout(request):
    del request.session['username']
    del request.session['password']
    return redirect('admin_login_page')

def ContactDisplay(request):
    contacts = ContactDB.objects.all()
    return render(request, "ContactDisplay.html", {'contacts': contacts})


def ContactDelete(request,contact_id):
    x = ContactDB.objects.get(id=contact_id)
    x.delete()
    return redirect('ContactDisplay')

def NewsletterDisplay(request):
    newsletter = Newsletter.objects.all()
    return render(request, "NewsletterDisplay.html", {'newsletter': newsletter})

def NewsletterDelete(request,news_id):
    x = Newsletter.objects.get(id=news_id)
    x.delete()
    return redirect('NewsletterDisplay')