# Third-party
from openai import AsyncOpenAI
import requests

# Project
import config as cf

client = AsyncOpenAI(base_url=cf.gpt.get('base_url'))


async def send_gpt_request(prompt: str, image_url: str = "") -> str:
    response = await client.chat.completions.create(
        model="gpt-3.5-turbo-0125",
        messages=[{"role": "user", "content": prompt}] #+ '\n Check the code for operability. Answer simply: does it work or not. If not, then explain why. If code is working fine, then write unit or mock tests for it and send the code (code only)!'}],
    )
    if image_url:
        response = await client.chat.completions.create(
            model="gpt-3.5-turbo-0125",
            messages=[
                {
                "role": "user",
                "content": [
                    {"type": "text", "text": f"{prompt}"},
                    {
                    "type": "image_url",
                    "image_url": {
                        "url": f"{image_url}",
                    },
                    },
                ],
                }
            ],
        )
    else:
        response = await client.chat.completions.create(
            model="gpt-4o-2024-05-13",
            messages=[{"role": "user", "content": prompt}],
        )

    return response.choices[0].message.content


def get_balance():
    url = "https://api.proxyapi.ru/proxyapi/balance"
    headers = {
        "Authorization": f"Bearer {cf.gpt.get('key')}"
    }
    response = requests.get(url, headers=headers)
    return response.json()
