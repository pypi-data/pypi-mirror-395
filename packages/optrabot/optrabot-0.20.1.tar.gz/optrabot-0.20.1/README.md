# OptraBot
OptraBot is a Options Trading Bot which can be used to run fully automated options trading strategies using your Interactive Brokers or Tastytrade trading account.

## System requirements
Microsoft Windows, MacOS or Linux operating system

Python 3.13

For Interactive Brokers: Trader Workstation or IB Gateway

## Installation

OptraBot uses the Python Package Manager UV from Astral (https://docs.astral.sh/uv/).

Use the following command for automatic installation procedure depending on your Operating System.

Windows: `powershell -ExecutionPolicy ByPass -c "irm https://app.optrabot.io/static/assets/scripts/install-optrabot.ps1 | iex"`

Windows Server: `powershell -ExecutionPolicy ByPass -c "irm [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12;  https://app.optrabot.io/static/assets/scripts/install-optrabot.ps1 | iex"`

MacOS/Linux: `curl -LsSf https://app.optrabot.io/static/assets/scripts/install-optrabot.sh | bash`

This will download and automatically install UV if necessary, the correct Python version and the OptraBot itself.

## Updating

The OptraBot got a auto-update functionality integrated. There is no need to update it manually.

The UV Package Manager can be updated with the command `uv self update`

## Run OptraBot

OptraBot can be started with the following command: `optrabot`

## Disclaimer
Be aware that you're using this software at your own risk. The author is not liable for any losses occuring with using this software.
