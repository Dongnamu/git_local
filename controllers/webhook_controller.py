from flask import Blueprint, request, abort, current_app
import hmac
import hashlib
import json
from services.webhook_service import handle_github_event

webhook_blueprint = Blueprint('webhook', __name__)

@webhook_blueprint.route("/webhook", methods=["POST"])
def github_webhook():
    # GitHub 웹훅 서명 헤더
    signature = request.headers.get("X-Hub-Signature-256")
    if not signature:
        abort(400, "Signature missing")
    # 요청 본문 검증
    payload = request.data
    secret = current_app.config['GITHUB_SECRET'].encode()
    calculated_signature = "sha256=" + hmac.new(secret, payload, hashlib.sha256).hexdigest()
    
    if not hmac.compare_digest(calculated_signature, signature):
        abort(400, "Invalid signature")
    
    # 이벤트 타입 확인
    event = request.headers.get("X-GitHub-Event", "ping")

    if event == "ping":
        return {"msg": "pong"}
    elif event in ["push", "pull_request"]:
        data = request.get_json()
        # 서비스 레벨 로직 처리
        response_msg = handle_github_event(data, event, current_app.config)
        return {"msg": response_msg}
    else:
        print(f"Unhandled event: {event}")
        return {"msg": f"Unhandled event: {event}"}
        
    



