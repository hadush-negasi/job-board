import sys
from django.http import JsonResponse, HttpResponseServerError
from django.shortcuts import render
from django.db import OperationalError, DatabaseError
import psycopg2
from django.core.exceptions import PermissionDenied

class GlobalErrorMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            response = self.get_response(request)
            return response
        except (OperationalError, DatabaseError, psycopg2.OperationalError) as e:
            # Log the database error for debugging
            print(f"Database error: {e}", file=sys.stderr)
            
            # Return user-friendly error page
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'error': 'Database connection issue. Please try again later.'
                }, status=503)
            
            return render(request, 'errors/503.html', status=503)
        
        except PermissionDenied:
            return render(request, 'errors/403.html', status=403)
        
        except Exception as e:
            # Log other unexpected errors
            print(f"Unexpected error: {e}", file=sys.stderr)
            
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'error': 'Something went wrong. Please try again.'
                }, status=500)
            
            return render(request, 'errors/500.html', status=500)