# Stock Bot
A discord bot to automatically update users when the stock status of a tracked item changes. 
The bot will send a message once the item is in stock.

## Description
Built using the discord.py library. The bot itself is currently responsible for checking whether items have restocked.
Bot connects to a mongoDB to persist state.


### Todo:
- Modify the bot to ping a dedicated backend for stock updates. Move task out of bot
 
### Currently supported commands:
1. !add {url}
Adds the item at the specified url to be tracked by the bot. 

2. !stock
Return and prints a list of all items tracked; their current status; the last date the item was in stock and more details

3. !list
Returns a list of the names of the items currently being tracked by the bot.
