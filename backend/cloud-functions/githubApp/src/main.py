import hashlib
import hmac
import os
import functions_framework
from dotenv import load_dotenv
from .logging.logger import central_logger
from .services.mongodb import mongo_handler

load_dotenv()
WEBHOOK_SECRET = os.environ.get("GITHUB_WEBHOOK_SECRET")
INSTALL_ACTIONS = ["added"]
UNINSTALL_ACTIONS = ["removed"]
CREATE_ACTIONS = ["opened", "reopened", "unlocked"]
REMOVE_ACTIONS = ["closed", "locked"]
UPDATE_ACTIONS = ["labeled", "unlabeled", "edited"]
VALID_ACTIONS = CREATE_ACTIONS + REMOVE_ACTIONS + UPDATE_ACTIONS + UNINSTALL_ACTIONS + INSTALL_ACTIONS

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
        ## Actions related to installion of the bot, only honor repositories_removed and repositories_added 
        if payload.get("action") in INSTALL_ACTIONS or payload.get("action") in UNINSTALL_ACTIONS:
            #TODO: based on repositories_removed and repositories_added update the DB
            pass

        ## Actions related to Issues
        if payload.get("action") in CREATE_ACTIONS:
            # new issue is opened, or old issue is reopened, or unlocked, we need to add this to our DB
            if payload.get("issue") and payload.get("issue").get("state") == "open" or payload.get("issue").get("state") == "reponed":
                mongo_handler.add_issue(payload.get("repository").get("full_name"), payload.get("issue"))
            else:
                central_logger.info("Not an open issue hence not adding it")
        elif payload.get("action") in UPDATE_ACTIONS:
            if payload.get("issue") and payload.get("issue").get("state") == "open" or payload.get("issue").get("state") == "reponed":
                mongo_handler.update_issue(payload.get("repository").get("full_name"), payload.get("issue"))
            else:
                central_logger.info("Not an open issue hence not updating it")
        elif payload.get("action") in REMOVE_ACTIONS:
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
3. We need to know which all repos have us downloaded and used
"""