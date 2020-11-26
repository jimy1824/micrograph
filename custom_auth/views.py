from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from custom_auth.helper.auth_helper import get_sign_in_url, get_token_from_code, store_token, store_user, \
    remove_user_and_token, get_token
from custom_auth.helper.graph_helper import get_user


# Create your views here.
def home(request):
    return render(request, 'home.html')


def sign_in(request):
    # Get the sign-in URL
    sign_in_url, state = get_sign_in_url()
    # Save the expected state so we can validate in the callback
    request.session['auth_state'] = state
    # Redirect to the Azure sign-in page
    return HttpResponseRedirect(sign_in_url)


def sign_out(request):
    # Clear out the user and token
    remove_user_and_token(request)
    logout(request)

    return HttpResponseRedirect(reverse('home'))


def callback(request):
    # Get the state saved in session
    expected_state = request.session.pop('auth_state', '')
    # Make the token request
    token = get_token_from_code(request.get_full_path(), expected_state)

    # Get the user's profile
    user = get_user(token)

    # Save token and user
    store_token(request, token)
    store_user(request, user)

    return HttpResponseRedirect(reverse('home'))
