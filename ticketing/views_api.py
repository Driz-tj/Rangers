from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json


def health_check(request):
    """Health check endpoint for Render"""
    return JsonResponse({
        'status': 'healthy',
        'service': 'Bo Rangers FC Ticketing System'
    })


@csrf_exempt  
def api_status(request):
    """API status endpoint"""
    return JsonResponse({
        'status': 'ok',
        'message': 'API is running'
    })
