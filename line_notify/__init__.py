from .line_sender import LineSender


def main(text: str) -> int:
    ls = LineSender()
    response = ls.send(text)
    if response.status_code == 200:
        return 0
    return response.status_code
