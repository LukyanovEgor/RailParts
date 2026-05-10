from flask import Blueprint, request, redirect, make_response
import jwt, datetime


auth_bp = Blueprint("auth", __name__)


@auth_bp.route('/auth/set-token')
def set_token():
    user_id = request.args.get('user_id')
    email = request.args.get('email')

    payload = {
        "user_id": user_id,
        "email": email,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(days=7)
    }
    token = jwt.encode(payload, "your-secret-key", algorithm="HS256")

    response = make_response(redirect("/"))
    response.set_cookie(
        "auth_token", token,
        max_age=7 * 24 * 60 * 60,
        # max_age=60*5,
        httponly=True,
        secure=False,
        samesite="Lax"
    )
    return response


@auth_bp.route('/auth/logout')
def logout():
    response = make_response(redirect("/"))

    response.delete_cookie("auth_token", path="/")

    return response