from django.contrib.auth import login, logout
from django.contrib.auth.models import Group
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from fermamarket_02.clients.models import ClientProfile
from fermamarket_02.customusers.forms import RegistrationForm
from fermamarket_02.farmers.models import FarmerProfile
from utils.email_utils import send_registration_email


def register_view(request):
    if request.user.is_authenticated:
        if request.user.has_perm('clients.view_clientprofile'):
            return redirect('client_profile')
        elif request.user.has_perm('farmers.view_farmerprofile'):
            return redirect('farmer_profile')
        else:
            return redirect('home')

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()

            role = form.cleaned_data['role']
            if role == 'farmer':
                group = Group.objects.get(name='Farmers')
                user.groups.add(group)
                FarmerProfile.objects.create(user=user, farm_name='', location='', phone='')
            else:
                group = Group.objects.get(name='Clients')
                user.groups.add(group)
                ClientProfile.objects.create(user=user, full_name='', address='', phone='')

            login(request, user)

            send_registration_email(user)

            return redirect('home')
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})


@csrf_exempt
@require_http_methods(["GET", "POST"])
def custom_logout_view(request):
    logout(request)
    return redirect('home')
