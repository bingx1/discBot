# Stock Bot
A discord bot to automatically update users when the stock status of a tracked item changes. 
The bot will send a message once the item is in stock.

## Description
Built using the discord.py library. The bot itself is currently responsible for checking whether items have restocked.
Bot connects to a mongoDB to persist state.

![alt_text](https://user-images.githubusercontent.com/50439413/113514258-ee50fd80-95b0-11eb-87db-ddad1a1f1e1e.png)

### Quickstart
1. Clone this repository
2. Install docker
3. Create a new virtual environment and install the packages in requirements.txt
4. Build the image from the dockerfile
5. Run inside container

### Todo:
- Modify the bot to ping a dedicated backend for stock updates. Move task out of bot
- Support more manufacturers - this is also accomplished by 
 
### Currently supported commands:
1. !add {url}
Adds the item at the specified url to be tracked by the bot. 

2. !stock
Return and prints a list of all items tracked; their current status; the last date the item was in stock and more details

3. !list
Returns a list of the names of the items currently being tracked by the bot.
