import secrets
import requests
import string

from django.contrib.auth.models import User

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
            usr = User.objects.get(username=gUser.get('primaryEmail'))
            if gUser['suspended']:
                print ("User {} deleted!".format(gUser.get('primaryEmail')))
                usr.delete()
                continue
        except User.DoesNotExist:
            if not gUser['suspended']:
                print(gUser.get('first_name'))
                usr = User.objects.create(
                    email=gUser.get('primaryEmail'),
                    username=gUser.get('primaryEmail'),
                    first_name=gUser.get('name').get('givenName'),
                    last_name=gUser.get('name').get('familyName'))
                pwd = ''.join(secrets.choice(ALPHABET) for i in range(10))
                usr.set_password(pwd)
                usr.save()
                #send email to newely created user with password
                print(u"Created user {} with password: {}".format(gUser.get('primaryEmail'), pwd))
            else:
                continue
           
        except Exception as e:
            print (e)
            continue

        confirmedGappsUsers.append(usr.email)

    #delete users from django that are not gApps users
    User.objects.all().exclude(email__in=confirmedGappsUsers).exclude(is_superuser=True).delete()

    return domain