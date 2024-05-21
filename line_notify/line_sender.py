import json
import os
from os.path import expanduser
from pathlib import Path
from typing import Optional

import requests


class LineSender:
    def __init__(self, token: Optional[str] = None):
        if token is None:
            token = self._load_token()
        self.header = {"authorization": f"Bearer {token}"}
        self.url = "https://notify-api.line.me/api/notify"

    def _load_token(self) -> str:
        home_dir = Path(expanduser("~"))
        config_dir = home_dir / ".config/line_notify"
        self.config_file = config_dir / ("token.json")
        if self.config_file.exists():
            with open(self.config_file) as f:
                json_dict = json.load(f)
            return json_dict["token"]

        return os.getenv("LINE_TOKEN")

    def send(self, text: str):
        return self._send_text(text)

    def _send_text(self, text: str):
        payload = {"message": text}
        return requests.post(self.url, headers=self.header, params=payload)

    def send_img(self, text: str, image_path: Path):
        if not image_path.exists():
            raise FileNotFoundError(f"image file {str(image_path)} does not exist.")
        return self._send_img(text, image_path)

    def _send_img(self, text: str, image_path):
        payload = {"message": text}
        with open(image_path, "rb") as image_file:
            files = {"imageFile": image_file}
            return requests.post(
                self.url,
                headers=self.header,
                params=payload,
                files=files,
            )
