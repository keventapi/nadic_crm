from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from ..models import Product
from ..utilits import BuyManagement, ProductDetails

@login_required
def index(response):
    products = ProductDetails.get_products()
    context = {'products': products, 'user': response.user.id}

    return render(response, 'index.html', context)

@login_required
def profile(response, user_id):
    products = ProductDetails.get_product_by_owner(user_id)
    return render(response, 'profile.html', context={'product': products})

@login_required
def view_cart(response):
    cart_item = purchase_handler.get_cart_items(response.user)

    if response.method == "POST":
        action = response.POST.get('action')
        if action == "comprar tudo":
            utilits.handle_sales_from_cart(cart_items)
            cart_items.delete()
            messages.success(response, 'compras realizadas com sucesso')
    return render(response, 'cart.html', {'cart_itens': cart_items})

@login_required
def add_product(request):
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.owner = request.user
            product.save()
            return redirect('seller_dashboard')
    else:
        form = ProductForm()
    return render(request, 'user_product_manager.html', {'form': form})


@login_required
def view_product(response, product_id):
    product = get_object_or_404(Product, id=product_id)
    if response.method == "POST":
        action = response.POST.get('action')
        form = ProductSale(response.POST, product=product)
        
        if action == "comprar":
            if form.is_valid():
                cleaned_quantity = form.fields['quantity'].clean(response.POST.get('quantity'))
                utilits.handle_unique_sells(product, cleaned_quantity)
                messages.success(response, "comprado com sucesso")
            
        elif action == "carrinho":
            cart = Cart.objects.get(cart_owner=response.user)
            if form.is_valid():
                chekcer = CartItems.objects.filter(product=product, cart=cart)
                if len(chekcer) == 0:
                    item = CartItems.objects.create(
                        product=product, 
                        quantity=form.cleaned_data['quantity'], 
                        cart=cart
                    )
                else:
                    item = CartItems.objects.get(product=product)
                    item.save()
                messages.success(response, "produto adicionado ao carrinho com sucesso")

    else:
        form = ProductSale(product=product)
        
    product_context = {'id': product_id, 
                       'name': product.product_name,
                       'image': product.product_image,
                       'price': f'{product.product_price}R$',
                       'stock': product.product_stock,
                       'description': product.product_description,
                       'type': product.product_type}
    product_owner_status =  product.owner == response.user
    return render(response, 'product_view.html', {'product': product_context, 'form': form, 'owner': product_owner_status})

@login_required
def edit_product(response, product_id):
    product_info = get_object_or_404(Product, id=product_id)
    if product_info.owner != response.user:
        return redirect('index')
    if response.method == 'POST':
        action = response.POST.get('action')
        if action == "submit":
            form = EditProductForm(response.POST, response.FILES, instance=product_info)
            if form.is_valid():
                form.save()
                messages.success(response, 'produto editado com sucesso')
                return redirect('seller_dashboard')
        if action == "delete":
            product_info.product_visibility = False
            product_info.save()
            messages.success(response, 'produto deletado com sucesso')
            return redirect('seller_dashboard')
        if action == "cancel":
            return redirect('seller_dashboard')
    else:
        form = EditProductForm(instance=product_info)
    context = {"form": form}
    return render(response, 'product_edit.html', context)

@login_required
def seller_dashboard(response):
    products_list = Product.objects.filter(owner=response.user)
    faturamento = 0
    if len(products_list) > 0:
        for products in products_list:
            sales = Sales.objects.filter(product=products)
            for sale in sales:
                faturamento += sale.owner_net_earning
        
    return render(response, 'seller_dashboard.html', {'products': products_list, 'faturamento': faturamento})

