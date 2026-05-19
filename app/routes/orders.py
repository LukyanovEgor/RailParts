from flask import Blueprint, request, redirect, make_response
import jwt


orders_bp = Blueprint("orders", __name__)


@orders_bp.route('/orders/redirect/my_orders')
def redirect_to_profile():
    token = request.cookies.get('auth_token')


    try:
        payload = jwt.decode(token, "your-secret-key", algorithms=["HS256"])

        user_id = payload.get("user_id")

        response = make_response(redirect(f"/{user_id}"))

    except Exception as e:

        print(e)
        response = make_response(redirect("/"))



    return response