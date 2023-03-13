# Anekdoty Telegram Bot

### Telegram bot, that can send you random jokes or jokes from specific category.

## How to set up

### 1. Install required libraries

``` shell
pip install -r requirements.txt
```

### 2. Collect jokes database (if you dont have one)

You can specify database name and table where jokes will be saved in `config.py`

The command below will scrap and save jokes from `anekdotov.net`

``` shell
python collect_data.py
```

### 3. Configure bot token

You can use env variable `token` or change the way it defines `config.py`

### 4. Run bot

```shell
python bot.py
```