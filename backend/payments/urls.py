from django.urls import path
from .views import CreateOrderView, VerifyPaymentView

app_name = "payments"

urlpatterns = [
    path("create-order/", CreateOrderView.as_view(), name="create-order"),
    path("verify-payment/", VerifyPaymentView.as_view(), name="verify-payment"),
]
