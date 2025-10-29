import razorpay
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Payment


class CreateOrderView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        amount = request.data.get("amount")
        if not amount:
            return Response({"error": "Amount is required"}, status=400)

        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        amount_in_paise = int(float(amount) * 100)

        razorpay_order = client.order.create({
            "amount": amount_in_paise,
            "currency": "INR",
            "payment_capture": 1,
        })

        # Save in DB
        Payment.objects.create(
            user=request.user,
            order_id=razorpay_order["id"],
            amount=amount,
        )

        return Response({
            "order_id": razorpay_order["id"],
            "amount": amount,
            "currency": "INR",
            "key": settings.RAZORPAY_KEY_ID
        })


class VerifyPaymentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        from razorpay.errors import SignatureVerificationError

        data = request.data
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

        try:
            client.utility.verify_payment_signature({
                'razorpay_order_id': data['razorpay_order_id'],
                'razorpay_payment_id': data['razorpay_payment_id'],
                'razorpay_signature': data['razorpay_signature']
            })

            # Update status
            payment = Payment.objects.get(order_id=data['razorpay_order_id'])
            payment.payment_id = data['razorpay_payment_id']
            payment.status = "Success"
            payment.save()

            return Response({"status": "Payment verified successfully"})
        except SignatureVerificationError:
            # mark failed
            payment = Payment.objects.filter(order_id=data.get('razorpay_order_id')).first()
            if payment:
                payment.status = "Failed"
                payment.save()

            return Response({"status": "Payment verification failed"}, status=400)
