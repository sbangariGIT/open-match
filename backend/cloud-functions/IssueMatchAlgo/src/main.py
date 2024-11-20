import time
import functions_framework
from .models.userprofile import UserProfile
from .services.db import DB
from .logging.logger import central_logger


def process_request(data):
    try:
        userProfile = UserProfile(**data)
        central_logger.info(f"YAY!!! {userProfile.firstName}, {userProfile.email} has requested to use our service")
        embedding = userProfile.get_query_embedding()
        result = {"result": embedding}
        result = DB.get_k_nearest_issues(embedding, k=4)
        central_logger.info(f"UFF!!! Done proccessing request for {userProfile.firstName}, {userProfile.email}")
        return result, 200
    except ValueError as e:
        central_logger.severe(f"OHHH NOOO!!! An Error Occured {str(e)}")
        return {"error": str(e)}, 200
    except Exception as e:
        central_logger.severe(f"OHHH NOOO!!! An Error Occured {str(e)}")
        return {"error": str(e)}, 200

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
            start_time = time.time()
            result, status_code = process_request(data=payload)
            end_time = time.time()
            result.update({'request_process_time': end_time - start_time})
            central_logger.info(f"request process time took {end_time - start_time}")
            return result, status_code, headers
        except Exception as e:
            central_logger.severe(f"OHHH NOOO!!! An Error Occured {str(e)}")
            return 'Not a valid JSON', 400, headers