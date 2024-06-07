from dataclasses import dataclass


@dataclass
class SunoNewsModel:
    title: str = None
    link: str = None
    date: str = None
    author: str = None
    content: str = None
    analysis: str = None
