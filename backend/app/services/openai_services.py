import openai

async def generate_openai_response(message: str, config: dict) -> str:
    openai.api_key = config['apiKey']
    try:
        response = openai.chat.completions.create(
            model=config['model'],
            messages=[{"role": "user", "content": message}],
            temperature=float(config['temperature'])
        )
        return response.choices[0].message.content
    except Exception as e:
        raise Exception(f"OpenAI API error: {str(e)}")