from ollama import Client

instance = False

def get_client(url = "http://127.0.0.1:11434", headers = {}):
    global instance
    if instance : return instance

    instance = Client(
        host= url,
        headers=headers
    )
    return instance

