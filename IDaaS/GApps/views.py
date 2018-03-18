from django.http import HttpResponse
from django.contrib.auth.forms import AdminPasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.views.generic import TemplateView
from django.shortcuts import redirect, render

from django_freeradius.models import RadiusCheck
from django_freeradius.base.models import _encode_secret
from GApps.models import ScheduledSyncs
from GApps.tasks import copyToDjango

class LoginView(TemplateView):
    template_name = "login.html"

    def dispatch(self, request, *args, **kwargs):
        print(request.user.is_authenticated)
        if request.user.is_authenticated == True:
            return redirect('profile')

        return super(LoginView, self).dispatch(request, *args, **kwargs)


class ProfileView(TemplateView):
    template_name = "profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)        
        context['user'] = self.request.user
        context['form'] = AdminPasswordChangeForm(self.request.user)
        return context

    def post(self, request, *args, **kwargs):
        form = AdminPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            pwd = form.cleaned_data['password1']
            try:
                credentials = RadiusCheck.objects.get(username=request.user.email)
                credentials.value = _encode_secret(credentials.attribute, pwd)
                credentials.save()
            except RadiusCheck.DoesNotExist:
                messages.error(request, "User doesn't exist!")
                context = self.get_context_data()
                context['form'] = form
                return render(request, self.template_name, context)

            messages.success(request, 'Your password was successfully updated!')
            return render(request, self.template_name, self.get_context_data())
        else:
            context = self.get_context_data()
            context['form'] = form
            return render(request, self.template_name, context)

def triggerSync(request):
    print("Start google sync!")
    domain = copyToDjango(request.user.email)
    obj, created = ScheduledSyncs.objects.get_or_create(user=request.user, domain=domain)
    return HttpResponse("Done")
