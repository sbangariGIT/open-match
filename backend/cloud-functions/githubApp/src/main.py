import hashlib
import hmac
import os
import functions_framework
from dotenv import load_dotenv
from .logging.logger import central_logger
from .services.mongodb import mongo_handler

load_dotenv()

# Replace with your GitHub webhook secret
WEBHOOK_SECRET = os.environ.get("GITHUB_WEBHOOK_SECRET")
VALID_ACTIONS = ["opened", "reopened", "unlocked", "labeled", "unlabeled", "closed", "locked"]

def verify_github_signature(request):
    """Verify that the request is coming from GitHub by checking the signature."""
    signature_header = request.headers.get('X-Hub-Signature-256')
    if not signature_header:
        central_logger.severe("Missing X-Hub-Signature-256 header")
        return {"error": "Missing X-Hub-Signature-256 header"}, 403

    # Get the raw payload body
    payload_body = request.get_data()

    # Compute the expected signature
    hash_object = hmac.new(WEBHOOK_SECRET.encode('utf-8'), msg=payload_body, digestmod=hashlib.sha256)
    expected_signature = "sha256=" + hash_object.hexdigest()

    # Compare signatures
    if not hmac.compare_digest(expected_signature, signature_header):
        central_logger.severe("Signatures did not match")
        return {"error": "Signatures did not match"}, 403

    return None  # Indicates validation passed

def process_request(payload):
    try:
        if payload.get("action") == VALID_ACTIONS[0] or payload.get("action") == VALID_ACTIONS[1] or payload.get("action") == VALID_ACTIONS[2]:
            # new issue is opened, or old issue is reopened, or unlocked, we need to add this to our DB
            if payload.get("issue") and payload.get("issue").get("state") == "open" or payload.get("issue").get("state") == "reponed":
                mongo_handler.add_issue(payload.get("repository").get("full_name"), payload.get("issue"))
            else:
                central_logger.info("Not an open issue hence not adding it")
        elif payload.get("action") == VALID_ACTIONS[3] or payload.get("action") == VALID_ACTIONS[4]:
            if payload.get("issue") and payload.get("issue").get("state") == "open" or payload.get("issue").get("state") == "reponed":
                mongo_handler.update_issue_label(payload.get("repository").get("full_name"), payload.get("issue"))
            else:
                central_logger.info("Not an open issue hence not updating it")
        elif payload.get("action") == VALID_ACTIONS[5] or payload.get("action") == VALID_ACTIONS[6]:
            # the issue was closed, or locked, we need to remove it from our DB
            mongo_handler.remove_issue(payload.get("repository").get("full_name"), payload.get("issue"))
        return True
    except Exception as e:
        central_logger.severe(f"An Expection occured while processing the following payload ```{payload}```\n Exceptions {str(e)}")
        return False

@functions_framework.http
def github_webhook(request):
    """Handle GitHub webhook payload with signature verification."""
    # Verify the GitHub signature
    verification_error = verify_github_signature(request)
    if verification_error:
        return verification_error

    try:
        # Parse JSON payload
        payload = request.get_json(silent=True)
        if not payload:
            return {"status": "failure", "message": "No payload found"}, 400
        
        if payload.get("action") not in VALID_ACTIONS:
            print("Rejecting payload:", payload)
            {"status": "success", "message": "Payload received, but not useful"}, 200
            central_logger.info("Payload received, but not useful")

        process_request(payload=payload)

        # Return success response
        return {"status": "success", "message": "Payload received"}, 200
    except Exception as e:
        print(f"Error: {e}")
        return {"status": "failure", "message": str(e)}, 500

"""
Notes:
1. Labels can be added to closed issues that we do not care about
2. Currently we only care about issues, so ignore PRs
TODO 3. We need to know which all repos have us downloaded and used
"""