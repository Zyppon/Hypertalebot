import disnake
from disnake.ext import commands


import sys
intents = disnake.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True


sys.path.insert(0, 'commands')



bot = commands.Bot(command_prefix = '!' , intents=intents , help_command= None)

category_names = ['HyperTale', 'HyperTale enjoy', 'HyperTale never die']
current_index = 0
category_list = []



@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    
    
bot.load_extension("user_commands")
bot.load_extension("moderation")


if __name__ == "__main__":
   bot.run('TOKEN_BOT')
elif __name__ != "__main__":
    print(f"En error has occured.Please Run your project from main file!")