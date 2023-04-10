# Jokes Telegram Bot

Telegram bot, that can send you random jokes or jokes from specific category.
Includes jokes parser which can be activated manually or from telegram.
Parser collects jokes from [anekdotov.net](https://anekdotov.net) site.

## Installation

### Clone repository

```shell
git clone https://gitlab.com/assbreaker/jokes-telegram-bot.git
```

### Create and activate virtual environment

#### Linux or MacOS

```shell
python -m venv venv
source venv/bin/activate
```

#### Windows

```shell
python3 -m venv venv
.\venv\Scripts\activate.bat
```

### Install requirements

```shell
pip install -r requirements.txt
```

## Running

### Collect jokes database

```shell
python3 -m bot.parser
```

### Setup environment variables

#### Required

* `TOKEN` (you can get it from [@BotFather]((https://t.me/BotFather)))

#### Optional

* `DEBUG` (insert any symbols to activate debug mode)
* `BLACKLIST` (list of unwanted categories while collecting jokes database)

### Start bot

```shell
python3 -m bot
```

## Licence

This program is licenced under the GPLv3 licence, which you can find in the [LICENCE](LICENCE) file.
