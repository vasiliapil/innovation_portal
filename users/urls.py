from django.urls import path
from . import views
from .views import *

urlpatterns = [path("log_in/", LogInView.as_view(), name="log_in"),
               path("log_out/confirm/", LogOutConfirmView.as_view(), name='log_out_confirm'),
               path("log_out/", LogOutView.as_view(), name='log_out'),
               path('<int:pk>/delete/', UserDeleteView.as_view(), name='user-delete'),
               path("resend/activation_code/", ResendActivationCodeView.as_view(), name='resend_activation_code'),
               path("sign_up/", SignUpView.as_view(), name='sign_up'),
               path("activate/<code>/", ActivateView.as_view(), name='activate_code'),
               path("restore/password/", RestorePasswordView.as_view(), name='restore_password'),
               path("restore/password/done", RestorePasswordDoneView.as_view(), name='restore_password_done'),
               path('restore/<uidb64>/<token>/', RestorePasswordConfirmView.as_view(), name='restore_password_confirm'),
               path("remind/username/", RemindUsernameView.as_view(), name='remind_username'),
               path("change/password/", ChangePasswordView.as_view(), name='change_password'),
               path("change/email/", ChangeEmailView.as_view(), name='change_email'),
               path("change/email/<code>", ChangeEmailActivateView.as_view(), name='change_email_code'),
               path('network_sign_up/', NetWorkRegisterView.as_view(), name='network_sign_up'),
               path('network_members/', views.network_members, name="network_members"),
               path('network_members/details/<int:id>', views.network_member_details, name='network_member_details'),
               path("network_sign_up/add_member/", views.network_register, name="add_network_member"),
               path("network_members/details/<int:id>/change_profile/", ChangeMemberProfileView.as_view(), name="change_member_profile"),
               path("network_members/details/<int:pk>/delete_profile/", DeleteMemberProfileView.as_view(), name="delete_member_profile"),

    ]