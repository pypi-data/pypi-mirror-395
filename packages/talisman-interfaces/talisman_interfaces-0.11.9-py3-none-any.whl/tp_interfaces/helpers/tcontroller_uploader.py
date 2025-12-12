import logging
import os
from multiprocessing.pool import ThreadPool
from typing import Iterable

import requests

from talisman_tools.helper.serializers import MessageModel
from tp_interfaces.abstract import Message

logger = logging.getLogger(__name__)


class TControllerUploader:

    def __init__(self) -> None:
        self.tcontroller_url = os.environ.get("TCONTROLLER_URL")
        self.num_processes = int(os.getenv("NUM_PROCESSES_UPLOAD", 8))

        logger.warning(f"Use TControllerUploader (url: {self.tcontroller_url})")

    def upload(self, messages: Iterable[Message], topic: str) -> None:
        worker = lambda message: self.upload_message(message, topic)
        with ThreadPool(processes=self.num_processes) as pool:
            pool.map(worker, messages)

    def upload_message(self, message: Message, topic: str) -> None:
        message = MessageModel.serialize(message)
        data = {
            "id": message.id,
            "topic": topic,
            "message": message.model_dump(by_alias=True, exclude_none=True)
        }

        status_code = 500
        while status_code != 200:
            r = requests.post(f"{self.tcontroller_url}/messages/add", json=data)
            status_code = r.status_code
            logger.warning(f"upload message to tcontroller with uuid {data['id']}, code: {status_code}, content: {r.content.decode()}")
