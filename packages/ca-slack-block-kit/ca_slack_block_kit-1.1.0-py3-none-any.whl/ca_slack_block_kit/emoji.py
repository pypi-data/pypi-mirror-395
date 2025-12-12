from dataclasses import dataclass


@dataclass(frozen=True)
class Emoji:
    """Various emojis for easy use with Slack messages."""

    THUMBS_UP = ":thumbsup:"
    THUMBS_DOWN = ":thumbsdown:"
    PARTY_POPPER = ":tada:"
    WARNING = ":warning:"
    CHECK_MARK = ":white_check_mark:"
    CROSS_MARK = ":x:"
    INFO = ":information_source:"
    ROCKET = ":rocket:"
    EYES = ":eyes:"
    FIRE = ":fire:"
    STAR = ":star:"
    HEART = ":heart:"
    CLAP = ":clap:"
    LIGHT_BULB = ":bulb:"
    HOURGLASS = ":hourglass_flowing_sand:"
    BUG = ":bug:"
    SPARKLES = ":sparkles:"
