
from fastapi import Request


# Function to get IP Address from the Request Object from ChatGPT:
async def get_ip_address(request: Request) -> str:
    x_real_ip = request.headers.get("X-Real-IP")
    x_forwarded_for = request.headers.get("X-Forwarded-For")

    if x_real_ip:
        client_ip = x_real_ip
    elif x_forwarded_for:
        # X-Forwarded-For may contain a list of IP addresses, take the first one
        client_ip = x_forwarded_for.split(',')[0]
    else:
        # If neither header is present, try the original method
        client_ip = request.client.host

    return client_ip
