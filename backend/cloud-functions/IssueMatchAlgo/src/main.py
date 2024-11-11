import time
import functions_framework


@functions_framework.http
def get_issue_match(request):
    # Set CORS headers
    headers = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "POST, OPTIONS",
        "Access-Control-Allow-Headers": "Content-Type",
    }

    # Handle preflight OPTIONS request
    if request.method == "OPTIONS":
        return "", 204, headers
    
    payload = {}
    if request.data:
        try:
            payload = request.get_json()
            print(payload)
            start_time = time.time()
            result, status_code = {}, 200
            end_time = time.time()
            result.update({'request_process_time': end_time - start_time})
            return result, status_code, headers
        except Exception as e:
            return 'Invalid Request:', 400, headers