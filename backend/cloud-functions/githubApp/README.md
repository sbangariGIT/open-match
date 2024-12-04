# GitHub Webhook

This is a webhook designed to be triggered by our Github App. It logs the payload sent by the app for further processing or debugging.

## How It Works

1. The GitHub App sends event payloads (e.g., push events, issue creation) to this webhook's endpoint.
2. The webhook will handle the payload appropriately.

## Deployment

This webhook is implemented as a Google Cloud Function, making it serverless, scalable, and easy to deploy. Later if we think the load is high we can change it to a service.
