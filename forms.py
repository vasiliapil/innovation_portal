from datetime import timedelta

from django import forms
from django.forms import ValidationError
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.utils import timezone
from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from .models import Network_member

class UserCacheMixin:
    user_cache = None


class SignIn(UserCacheMixin, forms.Form):
    password = forms.CharField(label=_('Κωδικός χρήστη'), strip=False, widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if settings.USE_REMEMBER_ME:
            self.fields['remember_me'] = forms.BooleanField(label=_('Να με θυμάσαι'), required=False)

    def clean_password(self):
        password = self.cleaned_data['password']

        if not self.user_cache:
            return password

        if not self.user_cache.check_password(password):
            raise ValidationError(_('Μη έγκυρος κωδικός χρήστη'))

        return password


class SignInViaUsernameandPasswordForm(SignIn):
    username = forms.CharField(label=_('Όνομα χρήστη'))

    @property
    def field_order(self):
        if settings.USE_REMEMBER_ME:
            return ['username', 'password', 'remember_me']
        return ['username', 'password']

    def clean_username(self):
        username = self.cleaned_data['username']

        user = User.objects.filter(username=username).first()
        if not user:
            raise ValidationError(_('Μή έγκυρο όνομα χρήστη'))

        if not user.is_active:
            raise ValidationError(_('Ο λογαριασμός δεν είναι ενεργός'))

        self.user_cache = user

        return username


class EmailForm(UserCacheMixin, forms.Form):
    email = forms.EmailField(label=_('Email'))

    def clean_email(self):
        email = self.cleaned_data['email']

        user = User.objects.filter(email__iexact=email).first()
        if not user:
            raise ValidationError(_('Μη έγκυρη διεύθυνση email'))

        if not user.is_active:
            raise ValidationError(_('Ο λογαριασμός δεν είναι ενεργός'))

        self.user_cache = user

        return email


class SignInViaEmailForm(SignIn, EmailForm):
    @property
    def field_order(self):
        if settings.USE_REMEMBER_ME:
            return ['email', 'password', 'remember_me']
        return ['email', 'password']


class EmailOrUsernameForm(UserCacheMixin, forms.Form):
    email_or_username = forms.CharField(label=_('Email ή Όνομα χρήστη'))

    def clean_email_or_username(self):
        email_or_username = self.cleaned_data['email_or_username']

        user = User.objects.filter(Q(username=email_or_username) | Q(email__iexact=email_or_username)).first()
        if not user:
            raise ValidationError(_('Μη έγκυρη διεύθυνση email ή όνομα χρήστη'))

        if not user.is_active:
            raise ValidationError(_('Ο λογαριασμός δεν είναι ενεργός'))

        self.user_cache = user

        return email_or_username


class SignInViaEmailOrUsernameForm(SignIn, EmailOrUsernameForm):
    @property
    def field_order(self):
        if settings.USE_REMEMBER_ME:
            return ['email_or_username', 'password', 'remember_me']
        return ['email_or_username', 'password']


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = settings.SIGN_UP_FIELDS

    email = forms.EmailField(label=_('Email'), help_text=_('Απαιτείται. Εισάγετε μια ενεργή διεύθυνση email'))

    def clean_email(self):
        email = self.cleaned_data['email']

        user = User.objects.filter(email__iexact=email).exists()
        if user:
            raise ValidationError(_('Δεν μπορείτε να χρησιμοποιήσετε αυτή τη διεύθυνση email'))

        return email


class ResendActivationCodeForm(UserCacheMixin, forms.Form):
    email_or_username = forms.CharField(label=_('Email ή Όνομα χρήστη'))

    def clean_email_or_username(self):
        email_or_username = self.cleaned_data['email_or_username']

        user = User.objects.filter(Q(username=email_or_username) | Q(email__iexact=email_or_username)).first()
        if not user:
            raise ValidationError(_('Μη έγκυρη διεύθυνση email ή όνομα χρήστη'))

        if user.is_active:
            raise ValidationError(_('Ο λογαριασμός είναι ήδη ενεργοποιημένος'))

        activation = user.activation_set.first()
        if not activation:
            raise ValidationError(_('Δε βρέθηκε κωδικός ενεργοποίησης'))

        now_with_shift = timezone.now() - timedelta(hours=24)
        if activation.created_at > now_with_shift:
            raise ValidationError(_('Ένας κωδικός ενεργοποίησης έχει ήδη σταλεί. Μπορείτε να ζητήσετε νέο κωδικό σε 24 ώρες'))

        self.user_cache = user

        return email_or_username


class ResendActivationCodeViaEmailForm(UserCacheMixin, forms.Form):
    email = forms.EmailField(label=_('Email'))

    def clean_email(self):
        email = self.cleaned_data['email']

        user = User.objects.filter(email__iexact=email).first()
        if not user:
            raise ValidationError(_('Μη έγκυρη διεύθυνση email'))

        if user.is_active:
            raise ValidationError(_('Ο λογαριασμός έχει ήδη ενεργοποιηθεί'))

        activation = user.activation_set.first()
        if not activation:
            raise ValidationError(_('Δε βρέθηκε κωδικός ενεργοποίησης'))

        now_with_shift = timezone.now() - timedelta(hours=24)
        if activation.created_at > now_with_shift:
            raise ValidationError(_('Ένας κωδικός ενεργοποίησης έχει ήδη σταλεί. Μπορείτε να ζητήσετε νέο κωδικό σε 24 ώρες'))

        self.user_cache = user

        return email


class RestorePasswordForm(EmailForm):
    pass


class RestorePasswordViaEmailOrUsernameForm(EmailOrUsernameForm):
    pass



class ChangeEmailForm(forms.Form):
    email = forms.EmailField(label=_('Email'))

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def clean_email(self):
        email = self.cleaned_data['email']

        if email == self.user.email:
            raise ValidationError(_('Εισάγετε μια άλλη διεύθυνση email'))

        user = User.objects.filter(Q(email__iexact=email) & ~Q(id=self.user.id)).exists()
        if user:
            raise ValidationError(_('Δεν μπορείτε να χρησιμοποιήσετε αυτή τη διεύθυνση email'))

        return email


class RemindUsernameForm(EmailForm):
    pass

    

class MemberRegisterForm(forms.ModelForm):
    
    class Meta:
        model = Network_member

        fields = ['Όνομα', 'Επώνυμο', 'Φορέας_εργασίας', 'Ιδιότητα', 'Τηλέφωνο']
        
class ChangeMemberProfileForm(forms.Form):
    Όνομα = forms.CharField(label=_('Όνομα'), max_length=30, required=False)
    Επώνυμο = forms.CharField(label=_('Επώνυμο'), max_length=150, required=False) 
    Φορέας_εργασίας = forms.CharField(label=_('Φορέας_εργασίας'), max_length=150, required=False)    
    Ιδιότητα = forms.CharField(label=_('Ιδιότητα'), max_length=150, required=False)   
    Τηλέφωνο = forms.CharField(label=_('Τηλέφωνο'), max_length= 20, required=False)    