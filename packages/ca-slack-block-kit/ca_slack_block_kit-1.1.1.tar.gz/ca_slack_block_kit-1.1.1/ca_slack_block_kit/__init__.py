"""Slack message blocks for notifications and alerts.

This module defines various Slack message block types used to construct messages
sent to Slack channels using the Blocks format. Each block type is represented
by a class that implements the Block interface.

By constructing a list of these blocks, we can then render them into the format
required by the Slack API.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass

from .emoji import Emoji  # type: ignore[import]

__all__ = ["Emoji"]


def render_blocks(blocks: list["Block"]) -> list[dict]:
    """Render a list of Block objects into a list of dictionaries compatible with the Slack SDK client chat_postMessage function.

    Args:
        blocks (list[Block]): List of Block objects to render.

    Returns:
        list[dict]: List of dictionaries representing the Slack message blocks.
    """
    return [block.render() for block in blocks]


class Block(ABC):
    """Base class for Slack message blocks.

    All block types should inherit from this class and implement the render method.
    """

    @abstractmethod
    def render(self) -> dict:
        pass


class Divider(Block):
    """Divider block."""

    def render(self) -> dict:
        return {"type": "divider"}


@dataclass
class Header(Block):
    """Header block. Plain text with emoji support enabled.

    Args:
        text: The header text.
    """

    text: str

    def render(self) -> dict:
        return {
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": self.text,
                "emoji": True,
            },
        }


@dataclass
class MarkdownSection(Block):
    """Markdown section block with a single piece of text.

    Args:
        text: The markdown formatted text for the section.
    """

    text: str

    def render(self) -> dict:
        return {
            "type": "section",
            "text": {"type": "mrkdwn", "text": self.text},
        }


@dataclass
class MarkdownSectionFields(Block):
    """Markdown section block with multiple fields.

    Args:
        fields: A list of markdown formatted text strings for the fields.
    """

    fields: list[str]

    def render(self) -> dict:
        return {
            "type": "section",
            "fields": [{"type": "mrkdwn", "text": field} for field in self.fields],
        }


@dataclass
class CodeBlock(Block):
    """Code block section.

    Args:
        code: The code string to display in the block.
    """

    code: str

    def render(self) -> dict:
        return {
            "type": "section",
            "text": {"type": "mrkdwn", "text": f"```{self.code}```"},
        }
