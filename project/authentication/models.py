from django.db import models
from django.contrib.auth.models import AbstractUser



class User(AbstractUser):
    email = models.EmailField(('email address'), unique=True)


from django.db.models.signals import post_save
from django.dispatch import receiver
from allauth.account.models import EmailAddress

@receiver(post_save, sender=User, dispatch_uid="identifying the user")
def account_created(sender, instance, *args, **kwargs):
    if instance.email in str(EmailAddress.objects.all()):
        email = instance.email.split("@")[0]
        username = ''
        for i in email:
            if i.isalnum():
                username+=i
        instance.username = username
        user = User.objects.filter(email = instance.email)
        user.update(username = instance.username)
        print('user created: ', instance.username)
    else:
        print('user not in email addresses')
        

# @receiver(pre_save, sender=User)
# def generate_username(sender, instance, *args, **kwargs):
#     if not User.objects.filter(email=instance.email):
#         print('mails: ', EmailAddress.objects.all())
#         email = instance.email.split("@")[0]
#         username = ''
#         for i in email:
#             if i.isalnum():
#                 username+=i
#         instance.username = username
#     else:
#         print('user exists, redirecting...')
