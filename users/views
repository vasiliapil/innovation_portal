from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from .forms import *
from django.views.generic import ListView, DetailView, CreateView
from .models import User, Network_member
from django.http import HttpResponse
from django.template import loader
from django.contrib import messages
from django.contrib.auth import login, authenticate, REDIRECT_FIELD_NAME
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import (
    LogoutView as BaseLogoutView, PasswordChangeView as BasePasswordChangeView,
    PasswordResetDoneView as BasePasswordResetDoneView, PasswordResetConfirmView as BasePasswordResetConfirmView,
)
from django.views.generic.base import TemplateView
from django.shortcuts import get_object_or_404, redirect
from django.utils.crypto import get_random_string
from django.utils.decorators import method_decorator
from django.utils.http import url_has_allowed_host_and_scheme as is_safe_url
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.utils.translation import gettext_lazy as _
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic import View, FormView
from django.conf import settings

from .utils import (send_activation_email, send_reset_password_email, send_forgotten_username_email, send_activation_change_email,
)
from .forms import (
    SignInViaUsernameandPasswordForm, SignInViaEmailForm, SignInViaEmailOrUsernameForm, SignUpForm,
    RestorePasswordForm, RestorePasswordViaEmailOrUsernameForm, RemindUsernameForm,
    ResendActivationCodeForm, ResendActivationCodeViaEmailForm, ChangeEmailForm, ChangeMemberProfileForm
)

from .models import Activation
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic.edit import FormMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)

class Guest(View):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(settings.LOGIN_REDIRECT_URL)

        return super().dispatch(request, *args, **kwargs)


class LogInView(Guest, FormView):
    template_name = 'log_in.html'

    @staticmethod
    def get_form_class(**kwargs):
        

        return SignInViaUsernameandPasswordForm

    @method_decorator(sensitive_post_parameters('password'))
    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        # Sets a test cookie to make sure the user has cookies enabled
        request.session.set_test_cookie()

        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        request = self.request

        if request.session.test_cookie_worked():
            request.session.delete_test_cookie()

        if settings.USE_REMEMBER_ME:
            if not form.cleaned_data['remember_me']:
                request.session.set_expiry(0)

        login(request, form.user_cache)

        redirect_to = request.POST.get(REDIRECT_FIELD_NAME, request.GET.get(REDIRECT_FIELD_NAME))
        url_is_safe = is_safe_url(redirect_to, allowed_hosts=request.get_host(), require_https=request.is_secure())

        if url_is_safe:
            return redirect(redirect_to)
        messages.success(request,'Συνδεθήκατε με επιτυχία!')
        return redirect(settings.LOGIN_REDIRECT_URL)


class SignUpView(Guest, FormView):
    template_name = 'sign_up.html'
    form_class = SignUpForm

    def form_valid(self, form):
        request = self.request
        user = form.save(commit=False)

        

        if settings.ENABLE_USER_ACTIVATION:
            user.is_active = False

        user.save()

        if settings.ENABLE_USER_ACTIVATION:
            code = get_random_string(length=20)

            act = Activation()
            act.code = code
            act.user = user
            act.save()

            send_activation_email(request, user.email, code)

            messages.success(
                request, 'Έχετε πραγματοποιήσει εγγραφή. Για να ενεργοποιήσετε το λογαριασμό σας, ακολουθήστε τις οδηγίες που έχουν σταλεί στο email σας')
        else:
            raw_password = form.cleaned_data['password1']

            user = authenticate(username=user.username, password=raw_password)
            login(request, user)

            messages.success(request, ('Η εγγραφή σας πραγματοποιήθηκε με επιτυχία!'))

        return redirect('home')


class ActivateView(View):
    @staticmethod
    def get(request, code):
        act = get_object_or_404(Activation, code=code)

        user = act.user
        user.is_active = True
        user.save()

        act.delete()

        messages.success(request,'Έχετε ενεργοποιήσει με επιτυχία το λογαριασμό σας!')

        return redirect('log_in')


class ResendActivationCodeView(Guest, FormView):
    template_name = 'resend_activation_code.html'

    @staticmethod
    def get_form_class(**kwargs):
        

        return ResendActivationCodeForm

    def form_valid(self, form):
        user = form.user_cache

        activation = user.activation_set.first()
        activation.delete()

        code = get_random_string(length=20)

        act = Activation()
        act.code = code
        act.user = user
        act.save()

        send_activation_email(self.request, user.email, code)

        messages.success(self.request, _('Ένας νεός κωδικός ενεργοποίησης έχει σταλεί στο email σας.'))

        return redirect('resend_activation_code')


class RestorePasswordView(Guest, FormView):
    template_name = 'restore_password.html'

    @staticmethod
    def get_form_class(**kwargs):
        if settings.RESTORE_PASSWORD_VIA_EMAIL_OR_USERNAME:
            return RestorePasswordViaEmailOrUsernameForm

        return RestorePasswordForm

    def form_valid(self, form):
        user = form.user_cache
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))

        if isinstance(uid, bytes):
            uid = uid.decode()

        send_reset_password_email(self.request, user.email, token, uid)

        return redirect('restore_password_done')



class ChangeEmailView(LoginRequiredMixin, FormView):
    template_name = 'profile/change_email.html'
    form_class = ChangeEmailForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_initial(self):
        initial = super().get_initial()
        initial['email'] = self.request.user.email
        return initial

    def form_valid(self, form):
        user = self.request.user
        email = form.cleaned_data['email']

        if settings.ENABLE_ACTIVATION_AFTER_EMAIL_CHANGE:
            code = get_random_string(20)

            act = Activation()
            act.code = code
            act.user = user
            act.email = email
            act.save()

            send_activation_change_email(self.request, email, code)

            messages.success(self.request, _('Για να ολοκληρώσετε την αλλαγή του email σας, ακολουθήστε τον σύνδεσμο που εστάλη σε αυτό'))
        else:
            user.email = email
            user.save()

            messages.success(self.request, _('Το email σας έχει αλλάξει.'))

        return redirect('change_email')


class ChangeEmailActivateView(View):
    @staticmethod
    def get(request, code):
        act = get_object_or_404(Activation, code=code)

        user = act.user
        user.email = act.email
        user.save()

        act.delete()

        messages.success(request, _('Το email σας άλλαξε με επιτυχία.'))

        return redirect('change_email')


class RemindUsernameView(Guest, FormView):
    template_name = 'remind_username.html'
    form_class = RemindUsernameForm

    def form_valid(self, form):
        user = form.user_cache
        send_forgotten_username_email(user.email, user.username)

        messages.success(self.request, _('Το όνομα χρήστη σας έχει σταλεί στο email σας'))

        return redirect('remind_username')


class ChangePasswordView(BasePasswordChangeView):
    template_name = 'profile/change_password.html'

    def form_valid(self, form):
        user = form.save()

        login(self.request, user)

        messages.success(self.request, _('Ο κωδικός χρήστη σας άλλαξε'))

        return redirect('change_password')


class RestorePasswordConfirmView(BasePasswordResetConfirmView):
    template_name = 'restore_password_confirm.html'

    def form_valid(self, form):
        form.save()

        messages.success(self.request, ('Ο κωδικός χρήστη σας ορίστηκε. Μπορείτε να συνδεθείτε.'))

        return redirect('log_in')


class RestorePasswordDoneView(BasePasswordResetDoneView):
    template_name = 'restore_password_done.html'


class LogOutConfirmView(LoginRequiredMixin, TemplateView):
    template_name = 'log_out_confirm.html'


class LogOutView(LoginRequiredMixin, BaseLogoutView):
    template_name = 'log_out.html'

class UserDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = User
    template_name= 'delete_user.html'
    success_url = 'http://127.0.0.1:8000/'

    def test_func(self):
        user = self.request.user
        return True

class NetWorkRegisterView(CreateView):
    model=Network_member  
    template_name= 'network_register.html'
    fields=("Όνομα", "Επώνυμο", "Φορέας_εργασίας", "Ιδιότητα", "Τηλέφωνο")

    
def network_register(request):
  
  if request.method == 'GET':
    form = MemberRegisterForm()
    return render(request, 'network_register.html', {'form': form})    
   
  if request.method == 'POST':
    form = MemberRegisterForm(request.POST) 
    user=User(request.user.id)
    if form.is_valid():
        
        x = request.POST['Όνομα']
        y = request.POST['Επώνυμο']
        z= request.POST["Φορέας_εργασίας"]
        i= request.POST["Ιδιότητα"]
        t= request.POST["Τηλέφωνο"]
        network_member = Network_member(user= user, Όνομα=x, Επώνυμο=y, Φορέας_εργασίας=z, Ιδιότητα=i, Τηλέφωνο=t)
        network_member.save()
        messages.success(request, 'Εγγραφήκατε στο Δίκτυο Καινοτομίας!')
        return redirect('home')
    else:
        return render(request, 'network_register.html', {'form': form})
    
  
    
def network_members(request):
    
  network_members = Network_member.objects.all().values()
  template = loader.get_template('network_members.html')
  context = {
    'network_members': network_members,
  }
  return HttpResponse(template.render(context, request))

def network_member_details(request, id):
  network_member = Network_member.objects.get(id=id)
  template = loader.get_template('network_member_details.html')
  context = {
    'network_member': network_member
  }
  return HttpResponse(template.render(context, request))       

class ChangeMemberProfileView(LoginRequiredMixin, FormView):
    template_name = 'profile/change_member_profile.html'
    form_class = ChangeMemberProfileForm

    def get_initial(self):
        network_member = Network_member.objects.get(user_id= self.request.user.id)
        initial = super().get_initial()
        initial['Όνομα'] = network_member.Όνομα
        initial['Επώνυμο'] = network_member.Επώνυμο
        initial['Φορέας_εργασίας'] = network_member.Φορέας_εργασίας
        initial['Ιδιότητα'] = network_member.Ιδιότητα
        initial['Τηλέφωνο'] = network_member.Τηλέφωνο
        
        return initial

    def form_valid(self, form):
        network_member = Network_member.objects.get(user_id= self.request.user.id)
        
        network_member.Όνομα = form.cleaned_data['Όνομα']
        network_member.Επώνυμο = form.cleaned_data['Επώνυμο']
        network_member.Φορέας_εργασίας = form.cleaned_data['Φορέας_εργασίας']
        network_member.Ιδιότητα = form.cleaned_data['Ιδιότητα']
        network_member.Τηλέφωνο = form.cleaned_data['Τηλέφωνο']

        network_member.save()

        messages.success(self.request, _('Τα στοιχεία σας ως μέλος του Δικτύου Καινοτομίας επικαιροποιήθηκαν με επιτυχία'))

        return redirect('change_member_profile')     

class DeleteMemberProfileView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Network_member
    template_name= 'delete_network_member.html'
    success_url = 'http://127.0.0.1:8000/network_members/'

    def test_func(self):
        network_member = self.get_object()
        if self.request.user.id == network_member.user_id:
            return True
        return False
