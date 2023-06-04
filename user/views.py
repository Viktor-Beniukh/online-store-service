from django.contrib.auth.forms import (
    PasswordChangeForm,
    PasswordResetForm,
    SetPasswordForm,
)
from django.contrib.auth.views import (
    PasswordChangeView,
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
)
from django.shortcuts import render
from django.views import generic
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin

from user.forms import UserRegisterForm, EditProfileForm
from user.models import Profile


class UserRegisterView(SuccessMessageMixin, generic.CreateView):
    form_class = UserRegisterForm
    template_name = "user/register.html"
    success_url = reverse_lazy("user:login")
    success_message = (
        "Your account is created successfully, please, "
        "login with your username and password"
    )


class UserEditView(SuccessMessageMixin, generic.UpdateView):
    form_class = EditProfileForm
    template_name = "user/edit_profile.html"
    success_url = reverse_lazy("frontpage")
    success_message = "Your settings has been successfully updated."

    def get_object(self, queryset=None):
        return self.request.user


class EditProfileView(SuccessMessageMixin, generic.UpdateView):
    model = Profile
    template_name = "user/edit_profile_page.html"
    fields = (
        "bio",
        "facebook",
        "twitter",
        "instagram",
        "telegram",
        "youtube",
        "image"
    )
    success_url = reverse_lazy("frontpage")
    success_message = "Your profile has been successfully updated."


class CreateUserProfileView(SuccessMessageMixin, generic.CreateView):
    model = Profile
    template_name = "user/create_user_profile_page.html"
    fields = (
        "bio",
        "facebook",
        "twitter",
        "instagram",
        "telegram",
        "youtube",
        "image",
    )
    success_message = "Your profile has been successfully created."

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class ChangePasswordView(PasswordChangeView):
    form_class = PasswordChangeForm
    template_name = "user/password_change_form.html"
    success_url = reverse_lazy("user:password-success")


def password_success_view(request):
    return render(request, "user/password_change_done.html", {})


class ResetPasswordView(PasswordResetView):
    form_class = PasswordResetForm
    email_template_name = "user/password_reset_email.html"
    template_name = "user/password_reset_form.html"
    success_url = reverse_lazy("user:password_reset_done")


class ResetPasswordDoneView(PasswordResetDoneView):
    template_name = "user/password_reset_done.html"


class ResetPasswordConfirmView(PasswordResetConfirmView):
    form_class = SetPasswordForm
    template_name = "user/password_reset_confirm.html"
    success_url = reverse_lazy("user:password_reset_complete")


class ResetPasswordCompleteView(PasswordResetCompleteView):
    template_name = "user/password_reset_complete.html"
