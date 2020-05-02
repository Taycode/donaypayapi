from django.conf import settings


def get_flutterwave_sdk():
    return Flutterwave(
        public_key=settings.FLUTTERWAVE_PUBLIC_KEY,
        secret_key=settings.FLUTTERWAVE_SECRET_KEY
    )
