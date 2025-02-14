from django.shortcuts import render
from django.http import HttpResponse # new
from django.views import View
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect
from django.urls import reverse
from django import forms
from django.shortcuts import render, redirect
from django.contrib import messages

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