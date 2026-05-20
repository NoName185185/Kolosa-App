from urllib import request

from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages


from shop.forms import AdForm, RegisterForm, LoginForm,ProfileForm,ChangePasswordForm
from shop.models import Ad

# Create your views here.
def cars_view(request):
    ads = Ad.objects.filter(status='active')
    sort = request.GET.get('sort', '-id')
    brand = request.GET.get('brand')
    year_from = request.GET.get('year_from')
    year_to = request.GET.get('year_to')
    
    if sort == 'price_asc':
        ads = ads.order_by('price')
    elif sort == 'price_desc':
        ads = ads.order_by('-price')
    elif sort == 'year_asc':
        ads = ads.order_by('year')
    elif sort == 'year_desc':
        ads = ads.order_by('-year')
    
    if brand:
        ads = ads.filter(brand__icontains=brand)
    if year_from:
        ads = ads.filter(year__gte=year_from)
    if year_to:
        ads = ads.filter(year__lte=year_to)

    brands = Ad.objects.values_list('brand', flat=True).distinct().order_by('brand')
    years = Ad.objects.values_list('year', flat=True).distinct().order_by('-year')

    return render(request, 'cars.html', {
        'ads': ads,
        'brands': brands,
        'years': years,
        'current_sort': sort,
        'current_brand': brand,
        'current_year_from': year_from,
        'current_year_to': year_to
        })

def ad_detail(request, id):
    ad =  Ad.objects.get(id=id)
    return render(request,'ad_detail.html', {'ad': ad})
def register_view(request):
    if  request.method=='POST':
        form=RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            user=authenticate(username=form.cleaned_data['username'],password = form.cleaned_data['password'] )
            login(request, user)
            return redirect('cars')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})
def login_view(request):
    if request.method == 'POST':
        form= LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'],password = form.cleaned_data['password'] )
            if user is not None:
                login(request, user)
                return redirect('cars')
            else:
                messages.error(request, 'Invalid username or password')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})
def logout_view(request):
    logout(request)
    return redirect('cars')

@login_required
def profile_view(request):
    user_ads = request.user.ads.all()
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileForm(instance=request.user)
    ad_form = AdForm()
    return render(request, 'profile.html', {'form': form, 'user_ads': user_ads, 'ad_form': ad_form})

@login_required
def change_password_view(request):
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            if request.user.check_password(form.cleaned_data['old_password']):
                request.user.set_password(form.cleaned_data['new_password'])
                request.user.save()
                login(request, request.user)
                return redirect('cars')
            else:
                messages.error(request,'Invalid old password')
    else:
        form = ChangePasswordForm()
    return render(request, 'change_password.html', {'form': form})

@login_required
def create_ad_view(request):
    if request.method == 'POST':
        form = AdForm(request.POST, request.FILES)
        if form.is_valid():
            ad = form.save(commit=False)
            ad.user = request.user
            ad.save()
            return redirect('profile')
    else:
        form = AdForm()
    return redirect('profile')

@login_required
def delete_ad_view(request, id):
    if request.method == 'POST':
        ad = Ad.objects.get(id=id)
        if ad.user == request.user:
            ad.delete()
    return redirect('profile')

@login_required
def change_status_view(request):
    if request.method == 'POST':
        import json
        data = json.loads(request.body)
        ad_id = data.get('ad_id')
        new_status = data.get('status')
        try:
            ad = Ad.objects.get(id=ad_id, user=request.user)
            if new_status in ['active', 'sold']:
                ad.status = new_status
                ad.save()
                return JsonResponse({'success': True})
        except Ad.DoesNotExist:
            pass
        return JsonResponse({'success': False, 'error': 'Недостаточно прав'})
    return JsonResponse({'error': 'Метод не поддерживается'}, status=405)