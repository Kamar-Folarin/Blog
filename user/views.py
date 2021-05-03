from django.shortcuts import render, redirect, reverse
from django.urls import reverse_lazy
from django.views.generic import ListView, FormView, UpdateView
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.core.mail import EmailMessage
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.contrib.auth import login
from django.contrib import messages
from home.models import Post
from .forms import RegisterForm, LoginForm


class LoginFormView(SuccessMessageMixin, LoginView):
    template_name = "user/login.html"
    success_message = "You are Logged in Successfully!"
    redirect_authenticated_user = True
    form_class = LoginForm

    def form_valid(self, form):
        if not(form.cleaned_data['remember_me']):
            self.request.session.set_expiry(0)
        return super().form_valid(form)


class RegisterView(FormView):
    form_class = RegisterForm
    template_name = 'user/register.html'
    success_message = "You are Logged in Successfully!"

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('home')
        return render(request, self.template_name, {'form': self.form_class})

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        current_site = get_current_site(self.request)
        mail_subject = 'Activate your blog account.'
        message = render_to_string('user/account_active_email.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
            'token': account_activation_token.make_token(user),
        })
        to_email = form.cleaned_data.get('email')
        email = EmailMessage(
            mail_subject, message, to=[to_email]
        )
        email.send()
        message = "An Email is sent to " + to_email + ", Please confirm your email address to complete the registration"
        return render(self.request, 'user/email_verification_process.html', {'message': message})


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        messages.success(request, 'Thank you for your email confirmation. You are logged in Successfully')
        return redirect('home')
    else:
        message = 'Activation link is invalid!'
        return render(request, 'user/email_verification_process.html', {'message': message})


class PasswordResetPageView(PasswordResetView):
    template_name = "user/password_reset.html"

    def get_context_data(self, **kwargs):
        context = super(PasswordResetPageView, self).get_context_data(**kwargs)
        context['legend'] = "Reset Password"
        context['button'] = "Reset"
        return context


class PasswordDoneView(PasswordResetDoneView):
    template_name = "user/email_verification_process.html"

    def get_context_data(self, **kwargs):
        context = super(PasswordDoneView, self).get_context_data(**kwargs)
        context['message'] = "An email has been sent to reset your password"
        return context


class PasswordConfirmView(PasswordResetConfirmView):
    template_name = "user/password_reset.html"

    def get_context_data(self, **kwargs):
        context = super(PasswordConfirmView, self).get_context_data(**kwargs)
        context['legend'] = "Email Confirmation"
        context['button'] = "Confirm Email"
        return context


class PasswordCompleteView(PasswordResetCompleteView):
    template_name = 'user/email_verification_process.html'

    def get_context_data(self, **kwargs):
        context = super(PasswordCompleteView, self).get_context_data(**kwargs)
        context['message'] = f"Your password has been set. You can login with new Password <br><a href='{reverse('login')}'>Click here</a> to go to login page"
        return context


class ProfileListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'user/profile.html'
    context_object_name = 'posts'
    paginate_by = 3

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user).order_by('-date_posted')


class ProfileUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = User
    template_name = 'user/profile_update.html'
    fields = ['username', 'email']
    success_url = reverse_lazy('profile')

    def test_func(self):
        user = self.get_object()
        return self.request.user == user

    def form_valid(self, form):
        user = self.request.user
        current_site = get_current_site(self.request)
        mail_subject = 'Change Email Request'
        to_email = form.cleaned_data.get('email')
        message = render_to_string('user/email_change_email.html', {
            'user': user,
            'domain': current_site.domain,
            'email': to_email,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
            'token': account_activation_token.make_token(user),
        })
        email = EmailMessage(
            mail_subject, message, to=[to_email]
        )
        email.send()
        messages.success(self.request, "An Email is sent to " + to_email + ", Please confirm your email address to complete the registration")
        return redirect('profile')


def change_email(request, email, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.email = email
        user.save()
        messages.success(request, 'Thank you for your email confirmation. Your Email is changed Successfully')
        return redirect('profile')
    else:
        messages.success(request, 'Activation link is invalid!')
        return redirect('profile')
