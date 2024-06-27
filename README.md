# Discord Moderation Bot

This is a moderation bot for Discord written in Python using the `discord.py` library. The bot provides moderation functionalities such as kick, ban, warnings (warn), and auto chat moderation.

## Features

- **Kick**: Kick a user from the server.
- **Ban**: Ban a user from the server.
- **Unban**: Unban a previously banned user.
- **Warn**: Add a warning to a user. After 3 warnings, the user is automatically kicked.
- **Warnlist**: View the list of warnings for a user.
- **Report**: Report a user for inappropriate behavior.
- **Chat-Moderation**: automatic chat moderation.

## Requirements

- Python 3.8+
- `discord.py`, `commands`, `Asyncio`, `OS`, `DateTime` library

## Usage

1. **Run the bot:**

    ```sh
    python bot.py
    ```

2. **Bot Commands:**

    - `!kick @user [reason]`: Kick a user from the server.
    - `!ban @user [reason]`: Ban a user from the server.
    - `!unban user_id [reason]`: Unban a user using their ID.
    - `!warn @user [reason]`: Add a warning to a user.
    - `!warnlist @user`: View the list of warnings for a user.
    - `!report @user [reason]`: Report a user.
    - `!suggest [suggestion]` : To suggest.
    - `!info` : Server info.
    - `!userinfo @user`: User info.
    - `!botinfo`: Bot info.
    - `!aiuto`: Help for commands.
    - `!addrole @user [role]`: Give a role from a user.
    - `!removerole @user [role]`: Remove a role from a user.
    - `!pex @user`: Pex a user.
    - `!depex @user`: Depex a user.
    - `!createrole [role name] [permissions]`: Create a custom role.
