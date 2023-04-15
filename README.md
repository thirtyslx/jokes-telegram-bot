# Jokes Telegram Bot

Telegram bot, that can send you random jokes or jokes from specific category.

Includes jokes parser which can be activated manually or from telegram.
Parser collects jokes from [anekdotov.net](https://anekdotov.net) site.

![Explanatory note (RU)](NOTE.md)

## Installation

### Clone repository

```sh
git clone https://gitlab.com/assbreaker/jokes-telegram-bot.git
```

### Create and activate virtual environment

#### Linux or MacOS

```sh
python -m venv venv
source venv/bin/activate
```

#### Windows

```bat
python3 -m venv venv
.\venv\Scripts\activate.bat
```

### Install requirements

```sh
pip install -r requirements.txt
```

## Running

### Collect jokes database

```sh
python3 -m bot.parser
```

### Setup environment variables

#### Required

* TOKEN (you can get it from [@BotFather](https://t.me/BotFather))

#### Optional

* DEBUG (insert any symbols to activate debug mode)
* BLACKLIST (list of unwanted categories while collecting jokes database)

### Start bot

```sh
python3 -m bot
```

## License

This program is licensed under the GPLv3 license, which you can find in the [LICENSE](LICENSE) file.
