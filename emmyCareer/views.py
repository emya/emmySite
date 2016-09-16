from django.shortcuts import render, render_to_response, get_object_or_404

from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, login, authenticate

from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader, RequestContext
from django.core.urlresolvers import reverse

from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_protect

from django.conf import settings
import stripe
from django.utils import timezone

from .models import Purchase
from .forms import InquiryForm, RegistrationForm, TempUserForm 


# Create your views here.

def index(request):
    template = loader.get_template('emmyCareer/index.html') 
    return HttpResponse(template.render())

def sample(request):
    template = loader.get_template('emmyCareer/sample.html') 
    return HttpResponse(template.render())

def about(request):
    #template = loader.get_template('emmyCareer/about.html') 
    #return HttpResponse(template.render())
    return render_to_response("emmyCareer/about.html", RequestContext(request))

def resumeHelper(request):
    return render_to_response("emmyCareer/resumeHelper.html", RequestContext(request))

def onlineCounselling(request):
    print request.user
    print request.user.is_authenticated()
    return render_to_response("emmyCareer/counselling.html", RequestContext(request))
    #template = loader.get_template('emmyCareer/counselling.html') 
    #return HttpResponse(template.render())

def precounsellingPayform(request):
    stripe.api_key = settings.STRIPE_API_KEY
    price = 1000
    menu = 0101

    if request.method == "POST":
        token = request.POST['stripeToken']
        try:
           charge = stripe.Charge.create(
           amount=price, # amount in cents, again
           currency="usd",
           source=token,
           description="Example charge"
           )

           if request.user.is_authenticated():
               p = Purchase.objects.create(user=request.user, price=price, date=timezone.now(), menu=menu)
               p.save()

        except stripe.error.CardError, e:
           #The card has been declined
           print "except"
    return render_to_response("emmyCareer/counsellingPrepurchase.html", RequestContext(request))

@login_required
def resumeReviewPayform(request):
    stripe.api_key = settings.STRIPE_API_KEY
    price = 4000
    menu = 0201

    if request.method == "POST":
        token = request.POST['stripeToken']
        try:
           charge = stripe.Charge.create(
           amount=price, # amount in cents, again
           currency="usd",
           source=token,
           description="Example charge"
           )

           if request.user.is_authenticated():
               p = Purchase.objects.create(user=request.user, price=price, date=timezone.now(), menu=menu)
               p.save()

           send_mail('Dear '+request.user.username, "Thank you for purchasing!", 'emi.usuyama@gmail.com', [request.user.email], fail_silently=False)

           return render_to_response("emmyCareer/resumePurchaseSuccess.html", RequestContext(request))

        except stripe.error.CardError, e:
           #The card has been declined
           print "except"
    else:
        return render_to_response("emmyCareer/resumeReviewPurchase.html", RequestContext(request))

def validateEmail(email):
    from django.core.validators import validate_email
    from django.core.exceptions import ValidationError
    try:
        validate_email(email)
        return True
    except ValidationError:
        return False

def resumeReviewPayformWithoutSign(request):

    if request.method == "POST":
        print "POST"
        form = TempUserForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            request.session['data'] = data

            print "data", data
            return HttpResponseRedirect(reverse('emmyCareer:resumeReviewPaymentWithoutSign2'))
            #return render(request, 'emmyCareer/resumeReviewPurchaseWithoutSign2.html', {'data': data, 'form': form})
        else:
            print "else"

    print "Not POST"
    form = TempUserForm()
    return render(request, 'emmyCareer/resumeReviewPurchaseWithoutSign.html', {'form': form})

def resumeReviewPayformWithoutSign2(request):
    stripe.api_key = settings.STRIPE_API_KEY
    price = 4000
    menu = 0201

    print "sign2"
    print request.session.get('data', [])
    data = request.session.get('data', [])

    if request.method == "POST":
        token = request.POST['stripeToken']
        try:
           charge = stripe.Charge.create(
           amount=price, # amount in cents, again
           currency="usd",
           source=token,
           description="Example charge"
           )

           send_mail('Dear '+data['username'], "Thank you for purchasing!", 'emi.usuyama@gmail.com', [data['email']], fail_silently=False)
           return render_to_response("emmyCareer/resumePurchaseSuccess.html", RequestContext(request))

        except stripe.error.CardError, e:
           #The card has been declined
           print "except"
    else:
        return render_to_response("emmyCareer/resumeReviewPurchaseWithoutSign2.html", RequestContext(request))

def inquiry(request):
    messages = []

    if request.method == 'POST':
        form = InquiryForm(request.POST)
        if form.is_valid():
            name = request.POST.get('name')
            email = request.POST.get('email')
            inquiry = request.POST.get('inquiry')
            send_mail('Dear '+name, inquiry, 'from@example.com', [email], fail_silently=False)
            print "name", name
            messages.append("Your inquiry was successfully sent!")
        else:
            print "error", form.errors
            messages.append(form.errors)

    return render(request, 'emmyCareer/inquiry.html', {'messages':messages})

@csrf_protect
def signup(request):
    if request.method == 'POST':
        print "POST"
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
            username = form.cleaned_data['username'],
            password = form.cleaned_data['password1'],
            email = form.cleaned_data['email'],
            )

            name = request.POST.get('username')
            email = request.POST.get('email')

            send_mail('Dear '+name, "Thank you for registering!", 'emi.usuyama@gmail.com', [email], fail_silently=False)

            return HttpResponseRedirect('success/')
    else:
        print "not POST"
        form = RegistrationForm()

    variables = RequestContext(request, {'form':form})
    return render_to_response('emmyCareer/signup.html', variables, )

def signup_success(request):
    return render_to_response('emmyCareer/success.html')

def signout(request):
    logout(request)
    template = loader.get_template('emmyCareer/index.html') 
    return HttpResponse(template.render())
    #return HttpResponseRedirect('/')

def signin(request):
    logout(request)
    username = password = ""
    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                print "path: ", request.path
                return HttpResponseRedirect('/emmyCareer/userhome/')
    return render_to_response('emmyCareer/signin.html', context_instance=RequestContext(request))

@login_required
def userhome(request):
    print "request.user.id", request.user.id
    #purchase = get_object_or_404(Purchase, user=request.user)
    purchase = Purchase.objects.filter(user=request.user)
    print "purchase", purchase.count()
    return render_to_response('emmyCareer/userhome.html', {'user':request.user, 'purchase':purchase})

