from gradio_client import Client
import requests

client = Client("dwedew/golu-emo-ai")

def get_ai_response(user_text):
    try:
        result = client.predict(
            user_text,
            api_name="/chat"   # 🔥 FINAL FIX
        )
        return result
    except Exception as e:
        print("AI error:", e)
        return "Sorry, I'm having trouble thinking right now 😢"

import requests
import math

def preprocess_expression(expr):
    try:
        expr = expr.lower().strip()

        # handle sin/cos/tan with degrees → radians
        for func in ["sin", "cos", "tan"]:
            if func in expr:
                parts = expr.split()

                if len(parts) == 2:
                    angle = float(parts[1])
                    rad = angle * math.pi / 180
                    expr = f"{func}({rad})"

        return expr

    except:
        return expr


def solve_newton(operation, expression):
    try:
        expression = preprocess_expression(expression)

        url = f"https://newton.vercel.app/api/v2/{operation}/{expression}"
        response = requests.get(url)
        data = response.json()

        result = data.get("result")

        # 🔥 handle no result
        if not result:
            return None

        # 🔥 FIX: handle infinity properly
        try:
            if abs(float(result)) > 1e10:
                return "undefined"
        except:
            pass

        return result

    except Exception as e:
        print("Newton error:", e)
        return None