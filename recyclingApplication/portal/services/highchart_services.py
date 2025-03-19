from portal.models import *
from homepage.models import *
from django.db.models import Count


def createVolunteerRankingChart():

    requests = Request.objects.filter(status='completed').values('claimed_by').annotate(claimed_count=Count('claimed_by')).order_by('-claimed_count')[:10]
    raw_data = {
        'categories': [],
        'completed': [],  
    }
    for entry in requests:
        user = AuthUser.objects.get(id=entry['claimed_by'])
        raw_data['categories'].append(user.first_name + ' ' + user.last_name)
        raw_data['completed'].append(entry['claimed_count'])

    data = {
        'chart': {
            'type': 'column'
        },
        'title': {
            'text': 'Volunteer Rankings'
        },
        'xAxis': {
            'categories': raw_data['categories']
        },
        'yAxis': {
            'title': {
                'text': 'Count'
            }
        },
        'series': [{
            'name': 'Count',
            'data': raw_data['completed']
        }]
    }
    return data

# Method to get the volunteer status for charting. 
def createActiveUserChart():
    # Query the database onlu reutrn volunteer information
    user_status_counts = AuthUser.objects.all().filter(
        is_staff=False).values('is_active').annotate(count=Count('id'))
    
    # Construct the data
    data = {
        'chart': {
            'type': 'column'
        },
        'title': {
            'text': 'Volunteer Status'
        },
        'xAxis': {
            'categories': ['Active' if entry['is_active'] == True else 'Inactive' for entry in user_status_counts]
        },
        'yAxis': {
            'title': {
                'text': 'Count'
            }
        },
        'series': [{
            'name': 'Count',
            'data': [entry['count'] for entry in user_status_counts]
        }]
    }

    return data


def createCityCountChart():
    city_counts = Request.objects.values('city').annotate(
        total=Count('id')).order_by('-total')
    formatted_data = [{'name': entry['city'], 'y': entry['total']}
                      for entry in city_counts]
    data = {
        'chart': {
            'type': 'pie'
        },
        'title': {
            'text': 'City Request Count'
        },
        'series': [{
            'name': 'Count',
            'data': formatted_data
        }]
    }

    return data


def createCityCountBreakdownChart():
    status_count_by_city = Request.objects.values('city', 'status') \
        .annotate(count=Count('id')) \
        .order_by('city', 'status')
    chart_data = {}

    for entry in status_count_by_city:
        city = entry['city']
        status = entry['status']
        count = entry['count']

        if city not in chart_data:
            chart_data[city] = {}

        chart_data[city][status] = count

    cities = list(chart_data.keys())
    completed_counts = [data.get('completed', 0) for data in chart_data.values()]
    in_progress_counts = [data.get('in_progress',0) for data in chart_data.values()]
    pending_counts = [data.get('pending',0) for data in chart_data.values()]

    data = {
        'chart': {
            'type': 'bar'
        },
        'title': {
            'text': 'Request Breakdown by City'
        },
        'xAxis': {
            'categories': cities,
            'title': {
                'text': 'City'
            },
            'gridLineWidth': 1,
            'lineWidth': 0
        },
        'yAxis': {
            'min': 0,
            'title': {
                'text': 'Count',
                'align': 'high'
            },
            'labels': {
                'overflow': 'justify'
            },
            'gridLineWidth': 0
        },
        'tooltip': {
            'valueSuffix': ' millions'
        },
        'plotOptions': {
            'bar': {
                'borderRadius': '50%',
                'dataLabels': {
                    'enabled': 'true'
                },
                'groupPadding': 0.1
            }
        },
        'legend': {
            'layout': 'vertical',
            'align': 'right',
            'verticalAlign': 'top',
            'x': 0,
            'y': 0,
            'floating': 'true',
            'borderWidth': 1,
            'backgroundColor': '#FFFFFF',
            'shadow': 'true'
        },
        'credits': {
            'enabled': 'false'
        },
        'series': [{
            'name': 'Completed',
            'data': completed_counts
        }, {
            'name': 'In Progress',
            'data': in_progress_counts
        }, {
            'name': 'Pending',
            'data': pending_counts
        }]
    }

    return data