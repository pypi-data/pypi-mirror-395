# Created by Noé Cruz | Zurckz 22 at 04/08/2022
# See https://www.linkedin.com/in/zurckz
from datetime import datetime, UTC


class EventContext:
    aws_request_id: str

    def __init__(self):
        self.aws_request_id = str(datetime.now(UTC))
