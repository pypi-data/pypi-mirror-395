# Created by Noé Cruz | Zurckz 22 at 22/01/2023
# See https://www.linkedin.com/in/zurckz

from dataclasses import dataclass
from typing import Optional


@dataclass
class Auditable:
    created_at: Optional[str]
    last_modified: Optional[str]

    def audit(self, created_at: str, origin: str):
        if self.created_at is None or self.created_at == "":
            self.created_at = created_at
        if self.last_modified is None or self.last_modified == "":
            self.last_modified = origin
