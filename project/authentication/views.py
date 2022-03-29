from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.contrib import messages
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes

from .forms import RegisterForm
from django.contrib.auth import get_user_model
UserModel = get_user_model()


from django.contrib.auth import views as auth_views
from .forms import LoginForm
from django.shortcuts import reverse

from django.contrib.auth import logout
from django.shortcuts import redirect

class LoginView(auth_views.LoginView):
    form_class = LoginForm
    template_name = 'authentication/login.html'

    def get_success_url(self):
        return reverse('home')


def home(request):
    return render(request, 'authentication/home.html')


def signup(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your account.'
            message = render_to_string('authentication/activate_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = form.cleaned_data.get('email')

            email = EmailMessage(
                        mail_subject, message, to=[to_email]
            )
            email.send()
            return render(request, 'authentication/please_activate.html')
        else:
            for msg in form.error_messages:
                messages.error(request, f"{msg}: {form.error_messages[msg]}")
                print(msg)  
    else:
        form = RegisterForm()
    return render(request, 'authentication/register.html', {'form': form})


def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = UserModel._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return render(request, 'authentication/activation_success.html')
    else:
        return HttpResponse('Activation link is invalid!')


def please_activate(request):
    return render(request, 'authentication/please_activate.html')

def activate_success(request):
    return render(request, 'authentication/activation_success.html')


def logoutpage(request):
    logout(request)
    return redirect('home')

from django.contrib.auth.forms import PasswordResetForm
from django.core.mail import send_mail, BadHeaderError
from django.db.models.query_utils import Q

def password_reset_request(request):
    domain = str(get_current_site(request).domain)
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = UserModel.objects.filter(Q(email=data))
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    email_template_name = "authentication/password_reset_email.txt"
                    c = {
                    "email":user.email,
                    'domain': domain,
                    'site_name': 'Website',
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "user": user,
                    'token': default_token_generator.make_token(user),
                    'protocol': 'http',
                    }
                    email = render_to_string(email_template_name, c)
                    try:
                        send_mail(
                        subject,
                        email,
                        'your email',#the email you set in the SMTP config
                        [user.email],
                        fail_silently=False)
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')
                    return redirect ("/password_reset/done/")
    password_reset_form = PasswordResetForm()
    return render(request=request, template_name="authentication/password_reset.html", context={"password_reset_form":password_reset_form})
