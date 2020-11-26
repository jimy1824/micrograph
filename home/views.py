from django.contrib.auth.decorators import login_required
from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from custom_auth.helper.graph_helper import get_calendar_events
from custom_auth.helper.auth_helper import get_token
import dateutil.parser


def home(request):
    context = initialize_context(request)

    return render(request, 'home.html', context)


def initialize_context(request):
    context = {}

    # Check for any errors in the session
    error = request.session.pop('flash_error', None)

    if error != None:
        context['errors'] = []
        context['errors'].append(error)

    # Check for user in the session
    context['user'] = request.session.get('user', {'is_authenticated': False})
    return context


def calendar(request):
    context = initialize_context(request)

    token = get_token(request)

    events = get_calendar_events(token)

    if events:
        # Convert the ISO 8601 date times to a datetime object
        # This allows the Django template to format the value nicely
        for event in events['value']:
            event['start']['dateTime'] = dateutil.parser.parse(event['start']['dateTime'])
            event['end']['dateTime'] = dateutil.parser.parse(event['end']['dateTime'])

        context['events'] = events['value']

    return render(request, 'calendar.html', context)


@login_required
def about(request):
    return render(request, 'about.html', )
