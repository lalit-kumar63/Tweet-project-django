from django.shortcuts import render, redirect, HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from tweet.models import Tweet
from django.http import HttpResponseNotAllowed
from django.contrib.auth import logout

# Login for custom admin
def admin_login(request):
    try:
        if request.user.is_authenticated:
            return redirect('customadmin:dashboard')
        
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            
            # Check if username exists
            user_obj = User.objects.filter(username=username)
            if not user_obj.exists():
                messages.info(request, 'Account not found')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            
            # Authenticate user
            user_obj = authenticate(username=username, password=password)
            if user_obj and user_obj.is_superuser:
                login(request, user_obj)
                return redirect('customadmin:dashboard')
            
            messages.info(request, 'Invalid password')
            return redirect('/')
        
        return render(request, 'customadmin/login.html')
    
    except Exception as e:
        print(e)
        return HttpResponse("Internal server error")

# Dashboard view
@login_required
def dashboard(request):
    if not request.user.is_superuser:
        return HttpResponse("Unauthorized", status=403)
    
    tweets = Tweet.objects.select_related('user').order_by('-created_at')
    context = {
        'tweets': tweets
    }
    return render(request, 'customadmin/dashboard.html', context)


from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt

@login_required
def tweet_detail(request, tweet_id):
    if not request.user.is_superuser:
        return HttpResponse("Unauthorized", status=403)

    tweet = get_object_or_404(Tweet, id=tweet_id)
    return render(request, 'customadmin/tweet_detail.html', {'tweet': tweet})


@login_required
def tweet_create_now(request):
    if not request.user.is_superuser:
        return HttpResponse("Unauthorized", status=403)

    if request.method == 'POST':
        text = request.POST.get('text')
        photo = request.FILES.get('photo')
        user = request.user  # or choose another user

        Tweet.objects.create(
            user=user,
            text=text,
            photo=photo
        )
        messages.success(request, "Tweet created successfully!")
        return redirect('customadmin:dashboard')

    return render(request, 'customadmin/tweet_form.html', {'action': 'Create'})


@login_required
def tweet_update(request, tweet_id):
    if not request.user.is_superuser:
        return HttpResponse("Unauthorized", status=403)

    tweet = get_object_or_404(Tweet, id=tweet_id)

    if request.method == 'POST':
        tweet.text = request.POST.get('text')
        if 'photo' in request.FILES:
            tweet.photo = request.FILES['photo']
        tweet.save()
        messages.success(request, "Tweet updated successfully!")
        return redirect('customadmin:dashboard')

    return render(request, 'customadmin/tweet_form.html', {'tweet': tweet, 'action': 'Update'})

@login_required
def tweet_delete(request, tweet_id):
    if request.method == 'POST':
        tweet = get_object_or_404(Tweet, id=tweet_id)
        tweet.delete()
        return redirect('customadmin:dashboard')  # Redirect back to admin dashboard
    return HttpResponseNotAllowed(['POST'])

#logout
def admin_logout(request):
    logout(request)
    return redirect('customadmin:admin_login')   # Replace with your login URL name
