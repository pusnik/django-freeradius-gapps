import requests

def get_avatar(request, backend, strategy, details, response,
        user=None, *args, **kwargs):
    """
    Get user avatar image and verify if admin. Save data to request session.
    """
    url = None
    if backend.name == 'google-oauth2':
        url = response['image'].get('url')
        ext = url.split('.')[-1]
        domain = response['domain']
        user_id = response['id']
    if url:
        request.session['avatar_url'] = url.split('?')[0]+'?sz=200'
    if response.get('gender'):
        request.session['gender'] = response.get('gender')
    else:
        request.session['gender'] = "male"
    if domain and user_id:
        #check if user is admin   
        response = requests.get(
            ' https://www.googleapis.com/admin/directory/v1/users/{}'.format(user_id),
                params={'access_token': response['access_token']}
        )
        request.session['isAdmin'] = response.json().get('isAdmin')
        request.session['domain'] = domain


