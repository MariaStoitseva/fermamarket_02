# fermamarket_02/utils/email_utils.py

from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings


def send_registration_email(user):
    subject = 'Добре дошли във FermaMarket!'
    context = {'username': user.username}

    plain_message = render_to_string('emails/registration_welcome.txt', context)
    html_message = render_to_string('emails/registration_welcome.html', context)

    send_mail(
        subject,
        plain_message,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        fail_silently=False,
        html_message=html_message,
    )


def send_order_emails(order, cart_items, client_profile):
    # Email до клиента
    subject_client = f'Вашата поръчка #{order.id} е получена'
    context_client = {
        'order': order,
        'cart_items': cart_items,
        'total_price': order.total_price,
        'client': client_profile,
    }
    plain_message_client = render_to_string('emails/order_confirmation_client.txt', context_client)
    html_message_client = render_to_string('emails/order_confirmation_client.html', context_client)

    send_mail(
        subject_client,
        plain_message_client,
        settings.DEFAULT_FROM_EMAIL,
        [client_profile.user.email],
        fail_silently=False,
        html_message=html_message_client,
    )

    # Email до фермерите (уникални)
    notified_emails = set()
    for item in cart_items:
        farmer = item['product'].farmer
        if farmer.user.email not in notified_emails:
            notified_emails.add(farmer.user.email)
            context_farmer = {'farmer': farmer, 'order': order}
            plain_message_farmer = render_to_string('emails/order_notification_farmer.txt', context_farmer)
            html_message_farmer = render_to_string('emails/order_notification_farmer.html', context_farmer)

            send_mail(
                'Нова поръчка във вашия фермерски магазин',
                plain_message_farmer,
                settings.DEFAULT_FROM_EMAIL,
                [farmer.user.email],
                fail_silently=True,
                html_message=html_message_farmer,
            )
