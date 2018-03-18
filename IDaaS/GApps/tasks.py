import secrets
import requests
import string

from django.contrib.auth.models import User
from django_freeradius.base.models import _encode_secret
from django_freeradius.models import RadiusCheck

from django.conf import settings

ALPHABET = string.ascii_letters + string.digits

#here we should only create task to cleanup users that are suspended

def copyToDjango(user_email):
    """
    Task to copy GApps to django user list
    """
    user = User.objects.get(email=user_email)
    social = user.social_auth.get(provider='google-oauth2')
    domain = user_email.split('@')[1]
    response = requests.get(
            'https://www.googleapis.com/admin/directory/v1/users?domain={}'.format(domain),
                params={'access_token': social.extra_data['access_token']}
        )
    gappsUsers = response.json().get('users')
    # update records
    confirmedGappsUsers = []
    for gUser in gappsUsers:
        try:
            usr = RadiusCheck.objects.get(username=gUser.get('primaryEmail'))
            if gUser['suspended']:
                print ("User {} deleted!".format(gUser.get('primaryEmail')))
                usr.delete()
                continue
        except RadiusCheck.DoesNotExist:
            if not gUser['suspended']:
                pwd = "".join(secrets.choice(ALPHABET) for i in range(10))
                usr = RadiusCheck.objects.create(
                    username=gUser.get('primaryEmail'),
                    attribute=settings.DEFAULT_RADIUS_PWD_TYPE,
                    op=":=",
                    value=_encode_secret(settings.DEFAULT_RADIUS_PWD_TYPE, pwd))
    
                #send email to newely created user with password
                #print(u"Created user {} with password: {}".format(gUser.get('primaryEmail'),pwd))
            else:
                continue
           
        except Exception as e:
            print (e)
            continue

        confirmedGappsUsers.append(usr.username)

    #delete users from django that are not gApps users
    RadiusCheck.objects.all().exclude(username__in=confirmedGappsUsers).delete()

    return domain