import hashlib
import hmac
import os
import functions_framework
from dotenv import load_dotenv
from .logging.logger import central_logger

load_dotenv()

# Replace with your GitHub webhook secret
WEBHOOK_SECRET = os.environ.get("GITHUB_WEBHOOK_SECRET")


def verify_github_signature(request):
    """Verify that the request is coming from GitHub by checking the signature."""
    signature_header = request.headers.get('X-Hub-Signature-256')
    if not signature_header:
        return {"error": "Missing X-Hub-Signature-256 header"}, 403

    # Get the raw payload body
    payload_body = request.get_data()

    # Compute the expected signature
    hash_object = hmac.new(WEBHOOK_SECRET.encode('utf-8'), msg=payload_body, digestmod=hashlib.sha256)
    expected_signature = "sha256=" + hash_object.hexdigest()

    # Compare signatures
    if not hmac.compare_digest(expected_signature, signature_header):
        return {"error": "Signatures did not match"}, 403

    return None  # Indicates validation passed


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

        print("Received payload:", payload)
        central_logger.info(f"Received payload: ```{payload}```")

        # Return success response
        return {"status": "success", "message": "Payload received"}, 200
    except Exception as e:
        print(f"Error: {e}")
        return {"status": "failure", "message": str(e)}, 500

"""
Notes:
1. Labels can be added to closed issues that we do not care about
2. Currently we only care about issues, so ignore PRs creations
3. We need to know which all repos have us downloaded and used
"""