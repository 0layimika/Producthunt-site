from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import product
from django.utils import timezone
def home(request):
    products=product.objects
    return render(request, 'products/home.html',{'products':products})

@login_required(login_url="/account/signup")
def create(request):
    if request.method=='POST':
        if request.POST['title'] and request.POST['body'] and request.POST['url'] and request.FILES['icon'] and request.FILES['image']:
            Product = product()
            Product.title = request.POST['title']
            Product.body = request.POST['body']
            if request.POST['url'].startswith('http://') or request.POST['url'].startswith('https://'):
                Product.url = request.POST['url']
            else:
                Product.url = 'http://' + request.POST['url']
            Product.icon = request.FILES['icon']
            Product.image = request.FILES['image']
            Product.pub_date = timezone.datetime.now()
            Product.hunter = request.user
            Product.save()
            return redirect('/product/' + str(Product.id))
        else:
            return render(request, 'products/create.html',{'error':'All fields are required'})
    else:
        return render(request, 'products/create.html')

def detail(request, Product_id):
    Product = get_object_or_404(product, pk=Product_id)
    return render(request, 'products/detail.html',{'product':Product})
@login_required(login_url="/account/signup")
def upvote(request, Product_id):
    if request.method == 'POST':
        Product = get_object_or_404(product, pk=Product_id)
        Product.votes_total += 1
        Product.save()
        return redirect('/product/' + str(Product.id))
