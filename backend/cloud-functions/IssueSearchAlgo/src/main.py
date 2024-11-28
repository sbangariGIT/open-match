import time
import functions_framework
from .services.db import DB


def process_request():
    try:
        result = DB.get_issues()
        return result, 200
    except ValueError as e:
        return {"error": str(e)}, 200
    except Exception as e:
        return {"error": str(e)}, 200

@functions_framework.http
def get_issue_search(request):
    # Set CORS headers
    headers = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "GET, OPTIONS",
        "Access-Control-Allow-Headers": "Content-Type",
    }

    # Handle preflight OPTIONS request
    if request.method == "OPTIONS":
        return "", 204, headers
    
    try:
        start_time = time.time()
        result, status_code = process_request()
        end_time = time.time()
        result.update({'request_process_time': end_time - start_time})
        return result, status_code, headers
    except Exception as e:
        print(e)
        return 'Something Wrong Happened', 400, headers