from django.shortcuts import render, redirect
from .forms import CreateUserForm, LoginForm, UpdateUserForm

from django.contrib.auth.models import User

from django.contrib.sites.shortcuts import get_current_site   # live olursa gerekli bir kütüphane, localde çalıştığımız için duracak
from .token import user_tokenizer_generate

from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from django.contrib.auth.models import auth
from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.decorators import login_required

from django.contrib import messages

# Create your views here.

def register(request):

    form = CreateUserForm()


    if request.method == 'POST':  # <form method="POST" autocomplete="off"> 
        
        form = CreateUserForm((request.POST))

        if form.is_valid():
            
            user = form.save()  # formu alıp bir objeye dönüştürüyoruz

            user.is_active = False

            user.save()  # database e kaydediyoruz

            # Email verification setup(template)
            current_site = get_current_site(request)

            subject = 'Account verification email'   # email başlığı

            
            message = render_to_string('account/registration/email-verification.html',  {
                #renderlayarak bu templatei bilgileri topluyoruz.
                'user':user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': user_tokenizer_generate.make_token(user),

            })

            user.email_user(subject=subject, message=message)


            return redirect('email-verification-sent')

    context = {'form':form}



    return render(request, 'account/registration/register.html', context=context)



def email_verification(request, uidb64, token):

    # uniqueid
    unique_id = force_str(urlsafe_base64_decode(uidb64))
    user = User.objects.get(pk=unique_id)

    # Success

    if user and user_tokenizer_generate.check_token(user, token):

        user.is_active = True

        user.save()

        return redirect('email-verification-success')
    #Failed
    else:
        return redirect('email-verification-failed')



def email_verification_sent(request):

    return render(request, 'account/registration/email-verification-sent.html')



def email_verification_success(request):

     return render(request, 'account/registration/email-verification-success.html')

def email_verification_failed(request):

    return render(request, 'account/registration/email-verification-failed.html')



def my_login(request):

    form = LoginForm()

    if request.method == 'POST':

        form = LoginForm(request, data=request.POST)  # Tüm veriyi topla

        if form.is_valid():

            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)  # kontrol ediyoruz

            if user is not None: # Eğer kullanıcı varsa

                auth.login(request, user)

                return redirect('dashboard')  # belirtilen yere gönder

    context = {'form': form}

    return render(request, 'account/my-login.html', context)



# Logout

def user_logout(request):

    # auth.logout(request) # Session loginle başlar, bununla kesilir. Tüm sessionlar, cart yüklenen ürünlerin silinmesi yanlış

    # logout değiştirdik böylece cart boşaltılmayacak
    try:
        for key in list(request.session.keys()):

            if key == 'session_key':

                continue
            else:          
                del request.session[key]
    
    except KeyError:

        pass

    messages.success(request, "Logout success")  # base.html de succes kısmına bakarak yazı yazdırıyoruz.

    return redirect('store')  # stor, home page demek




@login_required(login_url='my-login') # login değilsek bu sayfaya ulaşmamız engelleniyor
def dashboard(request):

    return render(request, 'account/dashboard.html')




@login_required(login_url='my-login')
def profile_management(request):


    #updating users username and email
    user_form = UpdateUserForm(instance=request.user)

    if request.method == 'POST':

        user_form = UpdateUserForm(request.POST, instance=request.user)

        if user_form.is_valid():

            user_form.save()

            messages.info(request, "Account updated")

            return redirect('dashboard')


    context = {'user_form':user_form}

    return render(request, 'account/profile-management.html', context=context)



@login_required(login_url='my-login')
def delete_account(request):

    user = User.objects.get(id=request.user.id)

    if request.method == 'POST':
    
        user.delete()

        messages.error(request, "Account deleted")

        return redirect('store')

    return render(request, 'account/delete-account.html')


