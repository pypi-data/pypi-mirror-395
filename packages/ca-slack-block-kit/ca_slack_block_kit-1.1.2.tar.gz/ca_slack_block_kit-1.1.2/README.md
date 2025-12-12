# CA Slack Block Kit

A collection of simple, pre-configured Slack block kit components to use to construct Slack notification messages.

## Installation

This package is available for installation via PyPi:

### UV Project

`uv add ca-slack-block-kit`

### Poetry Project

`poetry add ca-slack-block-kit`

### Pip

`pip install ca-slack-block-kit`

## Usage

To form a Slack message, import the required components from the package and use them to build your message payload as a list of Block instances.

```python
from ca_slack_block_kit import Block, Divider, Header, MarkdownSection, render_blocks

message: list[Block] = []

message.append(Header("This is a header"))
message.append(Divider())
message.append(MarkdownSection("**This is a markdown section**"))

# The message can then be sent using the Slack SDK
client = slack_sdk.WebClient(token=slack_bot_token)
client.chat_postMessage(
    channel=<slack_channel_id>,
    text=<title_text>,
    blocks=render_blocks(message),
)
```

## Available Blocks

See the [full documentation](docs.md) for a list of available blocks and their usage.
