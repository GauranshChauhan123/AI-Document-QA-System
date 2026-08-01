import requests

from config import BACKEND_URL


def upload_documents(files):
    response = requests.post(
        f"{BACKEND_URL}/upload",
        files=files,
    )
    return response


def ask_question(question):
    response = requests.post(
        f"{BACKEND_URL}/ask",
        json={"question": question},
    )
    return response

def check_backend():

    try:
        response = requests.get(
            f"{BACKEND_URL}/health",
            timeout=2
        )

        return response.status_code == 200

    except Exception:
        return False