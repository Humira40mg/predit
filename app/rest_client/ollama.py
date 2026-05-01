from ollama import Client
import json

instance = False

def get_client(url = "http://127.0.0.1:11434", headers = {}):
    global instance
    if instance : return instance

    instance = Client(
        host= url,
        headers=headers
    )
    return instance


def generate(system, prompt, model):
    raw = get_client().generate(system=system, prompt=prompt, model=model, stream=False, format='json')

    try:
        return json.loads(raw["response"]).get("segments")
    except json.JSONDecodeError:
        # Extraire le JSON depuis le texte si le modèle a quand même bavardé
        import re
        match = re.search(r'\{.*\}', raw, re.DOTALL)
        return json.loads(match.group())["segments"]