from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import authenticate,login,logout,get_user_model
from django.urls import reverse
from django.utils import timezone

from cafemanagement.settings import TABLE_BASE_PRICE
from .models import BookTable, CustomUser,Product
from django.conf import settings
from django.http import HttpResponseRedirect, JsonResponse
import paypalrestsdk
from django.core.mail import send_mail

from django.http import JsonResponse
from django.template.loader import render_to_string

PAYPAL_API_BASE = "https://api.sandbox.paypal.com"

# def index(request):
#     return render(request,'index.html')
from django.shortcuts import render
from .models import Product

def index(request):
    products = Product.objects.all()  # Fetch all products from the database
    return render(request, 'index.html', {'products': products})


def about(request):
    return render(request,'about.html')

CustomUser = get_user_model()
def uregistration(request):
    if request.method == "POST":
        uname = request.POST['email']
        upass = request.POST['password']
        ucpass = request.POST['cpassword']
        fullname = request.POST['fullname']
        address = request.POST['address']
        city = request.POST['city']
        mobileno = request.POST['mobileno']
        gender = request.POST['gender']

        print(request.POST)

        context={}
        if not uname or not upass or not ucpass or not fullname or not address or not city or not mobileno or not gender:
            context['errmsg']="Fields cannot be empty"
            return render(request,'registration.html',context)
        elif upass!=ucpass:
            context['errmsg']="Password and Confirm Password are different"
            return render(request,'registration.html',context)
        else:
            try:
                u=CustomUser.objects.create_user(username=uname,
                email=uname,
                password=upass,
                fullname=fullname,
                address=address,
                city=city,
                mobileno=mobileno,
                gender=gender)
                u.set_password(upass)
                # u.save()
                context['sucmsg']="Registration Successful."
                return render(request,'registration.html',context)
            except Exception:
                context['errmsg']="User already exists"
                return render(request,'registration.html',context)
    else:
        return render(request,'registration.html')
    
def ulogin(request):
    if request.method=="POST":
        luname=request.POST['luname']
        lupass=request.POST['lupass']
        print(luname)
        print(lupass)
        context={}
        if luname=="" or lupass =="":
            context['errmsg']="Fields cannot be empty"
            return render(request,'login.html',context)
        else:
            u=authenticate(username=luname,password=lupass)
            # print(u)
            # print(u.username)
            # print(u.password)

            if u is not None:
                login(request,u)
                return redirect('index')
            else:
                context['errmsg']="User doesnot exists!"
                return render(request,'login.html',context)
    else:
        return render(request,'login.html')

def ulogout(request):
    logout(request)
    return redirect('index')


def bookTable(request):
    context = {}
    if request.method == "POST":
        
        fullname = request.POST.get('fullname')
        bookemail = request.POST.get('bookemail')
        connum = request.POST.get('connum')
        people = request.POST.get('people')
        bookdate = request.POST.get('bookdate')
        booktime = request.POST.get('booktime')
        booknote = request.POST.get('booknote', '')
        if request.user.is_authenticated:
            cutomerId = request.user.id
        else:
            context['errmsg']= "You must be logged in to book a table."
            return render(request, 'index.html', context)
        
        
        createdate =  timezone.now()
        isCancelled = False  
        price_per_person = TABLE_BASE_PRICE/2
        try:
            people = int(people)
        except ValueError:
            context['errmsg'] = "Invalid number of people."
            return render(request, 'index.html', context)
        if people%2 != 0:
            temp_people=people+1
        else:
            temp_people=people

        print(people)
        finalPrice = (temp_people * price_per_person)
        print("final price:= ",finalPrice)       
       
        try:
            customer = get_object_or_404(CustomUser, id=cutomerId)
            
            print("Customer: ", customer)
            booking = BookTable.objects.create(
                fullname=fullname,
                bookemail=bookemail,
                connum=connum,
                people=people,
                bookdate=bookdate,
                booktime=booktime,
                createdate=createdate,
                booknote=booknote,
                cutomerId = customer,
                isCancelled=isCancelled,
                finalPrice=finalPrice
            )
            # print(booking)

            context['sucmsg'] = "Table booking successful."
            context['booking'] = booking 
            
            return render(request, 'book.html', context)  
        except Exception as e:
            print(e)
            context['errmsg'] = "Something went wrong. Please try again."
            return render(request, 'index.html', context)

    else:
        return render(request, 'index.html', context)


# def paypal_order_create(request):
#     if request.method == 'POST':
#         try:
#             # Create a PayPal order
#             order = paypalrestsdk.Order({
#                 "intent": "authorize",
#                 "payer": {
#                     "payment_method": "paypal"
#                 },
#                 "redirect_urls": {
#                     "return_url": "http://localhost:8000/payment/success",  # Change to your success URL
#                     "cancel_url": "http://localhost:8000/payment/cancel"  # Change to your cancel URL
#                 },
#                 "transactions": [{
#                     "item_list": {
#                         "items": [{
#                             "name": "Order Payment",
#                             "sku": "item_sku",
#                             "price": "10.00",  # Replace with actual price
#                             "currency": "USD",
#                             "quantity": 1
#                         }]
#                     },
#                     "amount": {
#                         "total": "10.00",  # Replace with actual total amount
#                         "currency": "USD"
#                     },
#                     "description": "This is the payment description."
#                 }]
#             })

#             if order.create():
#                 approval_url = next(link['href'] for link in order.links if link['rel'] == 'approval_url')
#                 return JsonResponse({'id': order.id, 'approval_url': approval_url, 'status': 'CREATED'}, status=201)
#             else:
#                 return JsonResponse({'error': order.error}, status=400)

#         except Exception as e:
#             return JsonResponse({'error': str(e)}, status=400)

#     return JsonResponse({'error': 'Invalid request method'}, status=405)
paypalrestsdk.configure({
    "mode": settings.PAYPAL_MODE,  # sandbox or live
    "client_id": settings.PAYPAL_CLIENT_ID,
    "client_secret": settings.PAYPAL_CLIENT_SECRET,
})

def make_payment(request):
    context = {}
    if request.user.is_authenticated:
        customerId = request.user.id  
    else:
        context['errmsg'] = "You must be logged in to book a table."
        return render(request, 'index.html', context)
    bookings = BookTable.objects.filter(cutomerId=customerId, isCancelled=False).order_by('-createdate').first()
    if bookings is None:
        context['errmsg'] = "No bookings found."
        return render(request, 'index.html', context)

    total_amount = bookings.finalPrice
    payment = paypalrestsdk.Payment({
        "intent": "sale",
        "payer": {
            "payment_method": "paypal"
        },
        "transactions": [{
            "amount": {
                "total": "{:.2f}".format(total_amount),
                "currency": "USD"
            },
            "description": "Order payment for booking ID: {}".format(bookings.id)
        }],
        "redirect_urls": {
            "return_url": "http://localhost:8000/paypal/execute/",
            "cancel_url": "http://localhost:8000/paypal/cancel/"
        }
    })

    if payment.create():
        print("Payment created successfully")

        subject = settings.SUBJECT
        recipient_list = [bookings.bookemail] 
        from_email = settings.EMAIL_HOST_USER

        try:
            context = {
            'customer_name': bookings.fullname,
            'booking_id': bookings.id,
            'booking_date': bookings.bookdate,
            'booking_time': bookings.booktime,
            'number_of_guests': bookings.people,
            'total_amount': total_amount,
            }

            message = render_to_string('booking_confirmation_email.html', context)
            print(message)
            email = send_mail(subject, message.format(context), from_email, recipient_list, fail_silently=False)
            print("Email sent successfully")
        except Exception as e:
            print(f"Error sending email: {e}")
        for link in payment.links:
            if link.rel == "approval_url":
                return redirect(link.href)
    else:
        print(payment.error)
        return JsonResponse({'error': payment.error}, status=500)
    
def payment_success(request):
    return render(request, 'payment_success.html')

def payment_failed(request):
    return render(request, 'payment_failed.html')

def execute_payment(request):
    print(request.GET)

    payment_id = request.GET.get('paymentId')
    payer_id = request.GET.get('PayerID')

    if payment_id and payer_id:
        payment = paypalrestsdk.Payment.find(payment_id)

        if payment:
            
            if payment.state == 'approved':
                return HttpResponseRedirect(reverse('payment_success')) 

            
            if payment.execute({"payer_id": payer_id}):
                return HttpResponseRedirect(reverse('payment_success')) 
            else:
                # Handle specific errors
                error_response = payment.error
                if error_response and error_response.get('name') == 'PAYMENT_ALREADY_DONE':
                    return HttpResponseRedirect(reverse('payment_success')) 

                
                print(payment.error)
                return HttpResponseRedirect(reverse('payment_failed'))
        else:
            return HttpResponseRedirect(reverse('payment_failed'))
    else:
        return HttpResponseRedirect(reverse('payment_failed')) 
    
def products(request):
    products = Product.objects.all()
    context={}
    context['products']=products
    return render(request, 'products.html', context)

def product_details(request, id):
    context={}
    product = get_object_or_404(Product, id=id)
    context['product']=product
    return render(request, 'product_details.html', context)