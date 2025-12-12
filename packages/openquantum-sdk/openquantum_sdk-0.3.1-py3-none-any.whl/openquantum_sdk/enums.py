from enum import Enum
from typing import Literal


class ExecutionPlanType(Enum):
    PUBLIC = "072f7eb6-574b-4bae-aafa-d3399c4abe7a"
    PRIVATE = "f83fd52f-c691-470f-9521-26b81c4e53bd"


class QueuePriorityType(Enum):
    STANDARD = "0f7b91a3-d1bf-46fb-af9c-55b77fa72bed"
    PRIORITY = "4ea2b9de-2d20-46d4-b1b5-0b71537a584f"
    INSTANT = "74cebc3d-14d8-455d-900e-daedc1566384"


AutoChoice = Literal["auto"]
