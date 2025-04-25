from django.shortcuts import render, redirect
from django.http import HttpResponse # new
from django.views import View
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect
from django.urls import reverse
from django import forms
from django.shortcuts import render, redirect
from django.contrib import messages
from .utils import ImageLocalStorage

# Create your views here.
def homePageView(request): # new
    return render(request, 'pages/home.html')# new

class HomePageView(TemplateView):
    template_name = 'pages/home.html'

class AboutPageView(TemplateView):
 template_name = 'pages/about.html'

 def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context.update({
        "title": "About us - Online Store",
        "subtitle": "About us",
        "description": "This is an about page ...",
        "author": "Developed by: Your Name",
    })
    return context

class ContactPageView(TemplateView):
    template_name = 'pages/contact.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "title": "Contact - Online Store",
            "subtitle": "Contact Us",
            "email": "contact@onlinestore.com",
            "address": "123 Fake Street, Springfield",
            "phone": "+1 555-1234",
        })
        return context

class Product:
    products = [
        {"id": "1", "name": "TV", "description": "Best TV", "price": 250},
        {"id": "2", "name": "iPhone", "description": "Best iPhone", "price": 999},
        {"id": "3", "name": "Chromecast", "description": "Best Chromecast", "price": 50},
        {"id": "4", "name": "Glasses", "description": "Best Glasses", "price": 120},
    ]


class ProductIndexView(View):
 template_name = 'products/index.html'

 def get(self, request):
    viewData = {}
    viewData["title"] = "Products - Online Store"
    viewData["subtitle"] = "List of products"
    viewData["products"] = Product.products
    return render(request, self.template_name, viewData)
 
class ProductShowView(View):
    template_name = 'products/show.html'

    def get(self, request, id):
        viewData = {}
        try:
            product = Product.products[int(id)-1]  # Buscar el producto
        except (IndexError, ValueError):  # Si el ID no existe o no es válido
            return HttpResponseRedirect(reverse('home'))  # Redirigir a home

        viewData["title"] = product["name"] + " - Online Store"
        viewData["subtitle"] = product["name"] + " - Product information"
        viewData["product"] = product

        return render(request, self.template_name, viewData)
    
class ProductForm(forms.Form):
    name = forms.CharField(required=True)
    price = forms.FloatField(required=True)

    def clean_price(self):
        price = self.cleaned_data.get("price")
        if price <= 0:
            raise forms.ValidationError("Price must be greater than zero.")
        return price

class ProductCreateView(View):
    template_name = 'products/create.html'  

    def get(self, request):
        form = ProductForm()
        viewData = {}
        viewData["title"] = "Create product"
        viewData["form"] = form
        return render(request, self.template_name, viewData)

    def post(self, request):
        form = ProductForm(request.POST)
        if form.is_valid():
            messages.success(request, "Product created successfully!")  # Mensaje de éxito
            return redirect("product_created")  # Redirigir a la vista de confirmación
        else:
            viewData = {
                "title": "Create product",
                "form": form
            }
            return render(request, self.template_name, viewData)
        
class ProductCreatedView(TemplateView):
    template_name = "products/created.html"

class CartView(View):
    template_name = 'cart/index.html'

    def get(self, request):
        # Productos “simulados” desde una “base de datos”
        products = {
            121: {'name': 'Tv samsung', 'price': '1000'},
            11: {'name': 'Iphone',   'price': '2000'},
        }
        # Productos en carrito guardados en sesión
        cart_data = request.session.get('cart_product_data', {})
        cart_products = {k: v for k, v in products.items() if str(k) in cart_data}

        context = {
            'title': 'Cart - Online Store',
            'subtitle': 'Shopping Cart',
            'products': products,
            'cart_products': cart_products,
        }
        return render(request, self.template_name, context)

    def post(self, request, product_id):
        cart_data = request.session.get('cart_product_data', {})
        cart_data[product_id] = product_id
        request.session['cart_product_data'] = cart_data
        return redirect('cart_index')

class CartRemoveAllView(View):
    def post(self, request):
        if 'cart_product_data' in request.session:
            del request.session['cart_product_data']
        return redirect('cart_index')
    
def ImageViewFactory(image_storage):
    class ImageView(View):
        template_name = 'images/index.html'

        def get(self, request):
            image_url = request.session.get('image_url', '')
            return render(request, self.template_name, {'image_url': image_url})

        def post(self, request):
            image_url = image_storage.store(request)
            request.session['image_url'] = image_url
            return redirect('image_index')
    return ImageView