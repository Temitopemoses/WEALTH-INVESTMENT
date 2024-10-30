import requests
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from django.core.mail import send_mail, EmailMessage
from django.conf import settings
from django.utils import timezone
from django.db.models.signals import post_save
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from .models import User


# from decouple import config

@receiver(user_logged_in)
def send_login_notification(sender, request, user, **kwargs):
    subject = "New Login Notification"
    
    # Get the IP address from the request
    ip_address = request.META.get('REMOTE_ADDR')
    
    # Get the user agent from the request
    user_agent = request.META.get('HTTP_USER_AGENT')
    
    # Get location details from the IP address using ipinfo.io
    location_info = get_location_info(ip_address)

    # Format the current time
    current_time = timezone.now().strftime('%Y-%m-%d %H:%M:%S')
    
    company_name = "WealthWise Investments"

    current_year = timezone.now().year

    # # Render the HTML template with context
    # html_content = render_to_string('emails/otp_email.html', {
    #     'user': user.first_name,
    #     'device': user_agent,
    #     'location': location_info,
    #     'ip_address': ip_address,
    #     'current_time': current_time,
    # })

    # text_content = strip_tags(html_content)
    # from_email = settings.DEFAULT_FROM_EMAIL
    # recipient_list = [user.email]

    # Create the email
    # email_message = EmailMultiAlternatives(subject, text_content, from_email, recipient_list)
    # email_message.attach_alternative(html_content, "text/html")

    # Subject
    subject = f"New Login Alert – {company_name}"
    
    # Customize the email content by inserting variables dynamically
    greeting = f"Hi {user.first_name},"
    
    intro = (
        f"We noticed a new login to your account at {company_name}. "
        "Below are the details of the login attempt. If this was you, no further action is needed. "
        "If you did not recognize this activity, please secure your account immediately."
    )
    
    login_details_title = "🔐 Login Details"
    login_details = (
        f"- Device: {user_agent}\n"
        f"- Location: {location_info}\n"
        f"- IP Address: {ip_address}\n"
        f"- Date and Time: {current_time}\n"
    )
    
    action_required_title = "🚨 What Should You Do?"
    action_required_content = (
        "If you did not authorize this login, we recommend that you:\n"
        "- Change your password immediately.\n"
        "- Enable two-factor authentication (if not already enabled).\n"
        "- Contact our support team for further assistance."
    )
    
    support_title = "🤝 Need Help?"
    support_content = (
        f"If you did not attempt to sign in to your account, your password may be compromised. Visit https://wealthwiseinvestments.com/accounts/auth/password-reset-request/ to create a new, strong password for your Apere account.\n\n"
        f"If you'd like to automatically verify devices in the future, consider enabling two-factor authentication on your account. Visit https://docs.wealthwiseinvestments.com/articles/configuring-two-factor-authentication to learn about two-factor authentication."
    )
    
    closing = f"Thank you for staying secure with {company_name}."
    
    sign_off = (
        "Thanks,\n"
        "WealthWise Investments\n"
    )

    # Combine everything into the email body
    message = (
        f"{greeting}\n\n"
        f"{intro}\n\n"
        f"{login_details_title}\n{login_details}\n\n"
        f"{action_required_title}\n{action_required_content}\n\n"
        f"{support_title}\n{support_content}\n\n"
        f"{closing}\n\n"
        f"{sign_off}"
    )
    
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [user.email]

    try:
      # Construct the email message with the subject, body, sender, and recipient
      payload = EmailMessage(subject=subject, body=message, from_email=from_email, to=recipient_list)
      # Send the email, silencing any errors that occur
      payload.send(fail_silently=False)
      return {
          "data": "Email sent successfully"
      }
  
    except Exception as e:
        print(e)
        return {
            "data": f"Email sent failed. {e}"
        }

    
    

def get_location_info(ip_address):
    try:
        print("Got here!")
        response = requests.get(f"https://ipinfo.io/{ip_address}/json")
        # response = requests.get(f"https://api.ipstack.com/{ip_address}?access_key={config('IPSTACK_ACCESS_TOKEN')}/")
        print(f"This is the response body ==> {response}, {response.json()}")
        data = response.json()
        print("Got here!!!!")
        location = data.get("city", "Unknown City") + ", " + data.get("region", "Unknown Region") + ", " + data.get("country", "Unknown Country")
        print("Got here too!")
        return location
    except Exception as e:
        return "Unknown Location"

@receiver(post_save, sender=User)
def send_onboarding_message(sender, instance, created, **kwargs):
    company_name = "Wealth Wise Investments"
    if not instance.is_verified:
       # Email Subject
        subject = f"Welcome to {company_name} – Let’s Get Started!"

        # Customize the email content by inserting variables dynamically
        greeting = f"Hi {instance.first_name},"
        
        intro = (
            f"We’re excited to have you on board at {company_name}! 🎉\n\n"
            f"At {company_name}, we’re committed to providing you with the best experience and tools to help you achieve [specific benefit]. "
            f"Here’s everything you need to get started:\n"
        )
        
        getting_started_title = "🛠️ Getting Started Guide"
        getting_started_content = (
            "Your personalized dashboard is now live! Access it here and start exploring the features that will make your work easier and more efficient.\n"
        )
        
        what_to_expect_title = "🌟 What to Expect Next"
        what_to_expect_content = (
            "- **Step 1:** Complete your profile\n"
            "- **Step 2:** Take a tour of our platform\n"
            "- **Step 3:** Make your first Investment\n"
        )
        
        support_title = "🤝 Need Help?"
        support_content = (
            "If you have any questions, we’re here for you! Our support team is available 24/7 to help you navigate and make the most of our platform.\n\n"
            "- Check out our Help Center\n"
            "- Reach out to us via email or phone"
        )
        
        community_title = "🚀 Join Our Community"
        community_content = (
            "Stay connected and up-to-date with our latest tips, updates, and exclusive offers by following us on social media."
        )
        
        closing = (
            f"Once again, welcome to {company_name}. We’re thrilled to have you as part of our community and can’t wait to see what you’ll achieve!"
        )
        
        sign_off = (
            "Best regards,\n"
            "WealthWise Investments"
        )

        # Combine everything into the email body
        message = (
            f"{greeting}\n\n"
            f"{intro}\n\n"
            f"{getting_started_title}\n{getting_started_content}\n\n"
            f"{what_to_expect_title}\n{what_to_expect_content}\n\n"
            f"{support_title}\n{support_content}\n\n"
            f"{community_title}\n{community_content}\n\n"
            f"{closing}\n\n"
            f"{sign_off}"
        )
        # message = f"Hi {instance.first_name},\n\nWelcome to our platform! We're excited to have you on board."
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [instance.email]
        
        send_mail(subject, message, from_email, recipient_list)
        instance.is_verified = True
        instance.save()