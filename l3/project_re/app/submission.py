import datetime
import numpy as np
from dataclasses import dataclass

@dataclass
class Submission:
    url: str = ''
    author: str = ''
    subreddit: str = ''
    text: str = ''
    text_embedding: list = None
    upvote_ratio: float = -1.0
    score: int = 0
    over_18: bool = None
    comments_num: int = -1
    title: str = ''
    created: datetime.datetime = None