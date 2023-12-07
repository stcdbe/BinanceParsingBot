from typing import Annotated

from pydantic import StringConstraints
from beanie import Document, Indexed


class Task(Document):
    user_id: Annotated[int, Indexed()]
    tickers_pair: Annotated[str, StringConstraints(max_length=10)]
    percentage: float
    interval_minutes: int
    price: float
