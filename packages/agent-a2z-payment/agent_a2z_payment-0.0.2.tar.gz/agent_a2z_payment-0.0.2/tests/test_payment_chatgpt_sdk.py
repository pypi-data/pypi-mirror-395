import a2z_payment_agent
from a2z_payment_agent.core import get_payment_sdk


import json
import openai

# 1. Initialize SDK
payment_sdk = get_payment_sdk(env="sandbox")

# 2. Define Tool
tools = [{
    "type": "function",
    "function": {
        "name": "create_payment",
        "description": "Generate a payment checkout card for the user.",
        "parameters": {
            "type": "object",
            "properties": {
                "amount": {"type": "integer", "description": "Amount in"},
                "description": {"type": "string", "description": "Reason for charge"}
            },
            "required": ["amount", "description"]
        }
    }
}]


# 3. Chat Loop
def run_chat(user_input):
    response = openai.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": user_input}],
        tools=tools
    )

    msg = response.choices[0].message

    if msg.tool_calls:
        call = msg.tool_calls[0]
        if call.function.name == "create_payment":
            args = json.loads(call.function.arguments)

            # Create Order
            order = payment_sdk.create_order(args['amount'], description=args['description'])

            # Generate HTML Card
            html_card = payment_sdk.generate_checkout_card(order['id'])

            return {
                "role": "tool",
                "content": "Display this HTML to user: " + html_card
            }

            ##