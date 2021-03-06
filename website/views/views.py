from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.template import RequestContext
from website.forms import UserForm, ProductForm, CustomerForm
from website.models import *

def index(request):
    template_name = 'index.html'
    return render(request, template_name, {})


# Create your views here.
def register(request):
    '''Handles the creation of a new user for authentication

    Method arguments:
      request -- The full HTTP request object
    '''

    # A boolean value for telling the template whether the registration was successful.
    # Set to False initially. Code changes value to True when registration succeeds.
    registered = False

    # Create a new user by invoking the `create_user` helper method
    # on Django's built-in User model
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        customer_form = CustomerForm(data=request.POST)

        if user_form.is_valid():
            # Save the user's form data to the database.
            user = user_form.save()
            customer = customer_form.save(commit=False)
            customer.user = user
            customer.save()
            # Now we hash the password with the set_password method.
            # Once hashed, we can update the user object.
            user.set_password(user.password)
            user.save()

            # Update our variable to tell the template registration was successful.
            registered = True

        return login_user(request)

    elif request.method == 'GET':
        user_form = UserForm()
        customer_form = CustomerForm()
        template_name = 'register.html'
        return render(request, template_name, {'user_form': user_form, 'customer_form': customer_form})

# pass profile form through render as well. one visible form, 2 under the hood

def login_user(request):
    '''Handles the creation of a new user for authentication

    Method arguments:
      request -- The full HTTP request object
    '''

    # Obtain the context for the user's request.
    context = RequestContext(request)

    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':

        # Use the built-in authenticate method to verify
        username=request.POST['username']
        password=request.POST['password']
        authenticated_user = authenticate(username=username, password=password)

        # If authentication was successful, log the user in
        if authenticated_user is not None:
            login(request=request, user=authenticated_user)
            return HttpResponseRedirect('/')

        else:
            # Bad login details were provided. So we can't log the user in.
            print("Invalid login details: {}, {}".format(username, password))
            return HttpResponse("Invalid login details supplied.")


    return render(request, 'login.html', {}, context)

# Use the login_required() decorator to ensure only those logged in can access the view.
@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)

    # Take the user back to the homepage. Is there a way to not hard code
    # in the URL in redirects?????
    return HttpResponseRedirect('/')

def list_products(request):
    products = Product.objects.all()
    template_name = 'product/list.html'
    return render(request, template_name, {'products': products})

def detail_product(request, pk):
    product = get_object_or_404(Product, pk=pk)

    template_name = 'product/details.html'
    return render(request, template_name, {'product': product})

def sell_product(request):
    if request.method == 'GET':
        product_form = ProductForm()
        template_name = 'product/create.html'
        return render(request, template_name, {'product_form': product_form})

    elif request.method == 'POST':
        product_form = ProductForm(data=request.POST)
        if product_form.is_valid():
            product = product_form.save(commit=False)
            product.seller = request.user
            product.save()
        template_name = 'product/success.html'
        return render(request, template_name, {'sell': product})

@login_required
def account_view(request):

    return render(request, 'account.html')


def category_product(request):
	categories = Category.objects.all()
	products = Product.objects.all()
	template_name = 'product/category.html'
	return render(request, template_name, {'categories': categories, 'products': products})









