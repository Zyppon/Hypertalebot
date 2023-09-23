import disnake
from disnake.ext import commands


class userCommands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    
    async def rules(self,ctx):
        
        #Rules COmmands
        rules_list = [
           "**1.**Respect and follow [Discord's Terms of Service](https://discord.com/terms) and [Discord Community Guidelines.](https://discord.com/guidelines)**[ Violating them results in permanent ban on our Discord servers! ]**",
           "**2.**Don't offend the players/staff, you will get **permanent MUTE on discord**.",
           "**3.**It is strictly forbidden to use **inappropriate language** towards any player.",
           "**4.**It is forbidden to **insult, swear, threaten another player**.",
           "**5.**It is strictly forbidden to **advertise other servers** (minecraft, sa:mp, discord).",
           "**6.**Advertising to other servers in **Direct Messages is strictly forbidden and is punishable by ban**.",
           "**7.Hacking, exploitation or use of unauthorized clients** by Mojang is strictly prohibited.",
           "**8.Any bugs or problems** should be reported to staff to be fixed.",
           "**9.**HyperTale is a registered trademark, **using HyperTale** to create **another community without permission** is strictly prohibited and **punishable by law**.",
           "**10.**We don't respond if you **bought a rank from an anonymous site**, any payment is only made on **shop.hypertale.org**, **pay close attention to the domain.**",
           "**11.Only this is the official HyperTale server**.",
           "**12.**Promoting **social networks** without permission is punishable by ban.",
           "**13.**HyperTale staff are allowed to sanction you if you make a mistake, if a **staff abuses** please contact a Founder!",
           "**14.**HyperTale is an international community,**racism against gender, skin color, religion and others is not allowed in any way!**",
           "**15.Respect** to be **respected** in return."
        ]
        
        #rules = rules_list.pop()
       # image_path = os.path.join(os.getcwd(), 'assets', 'HypertaleLogo.png')
        embed = disnake.Embed(
            title="**𒆜 Before everything please read the following rules:**",
            description="\n\n".join(rules_list),
            color=disnake.Color.from_rgb(0, 255, 255), 
        )
        
        
        embed.set_author(
            name="HyperTale Rules",
            icon_url=f"https://cdn.discordapp.com/attachments/716434160859873291/1132860845714575420/hypertale___rules.png"
        )
        
        embed.set_footer(
            text="PLAY.HYPERTALE.ORG | 2023 | HYPERTALE.ORG | RULES",
            icon_url="https://cdn.discordapp.com/attachments/716434160859873291/1132860845714575420/hypertale___rules.png"
            #file=disnake.File("/home/zyppon-ng/Documents/HyperTaleBot/assets/HypertaleLogo.png"),
        )
        
        embed.set_thumbnail(file=disnake.File("/home/zyppon-ng/Documents/HyperTaleBot/assets/HypertaleLogo.png"))
        embed.set_image(file=disnake.File("/home/zyppon-ng/Documents/HyperTaleBot/assets/Hypertalebanner.png"))
        
        
        
        #file = disnake.File(image_path, filename='HypertaleLogo.png')
        
       # await ctx.send(file=file , embed=embed)
        await ctx.send(embed=embed)
        
        
  
    #Avatar Profile Command
    @commands.command()
    async def avatar(self, ctx, *,  user : disnake.Member=None):
        user = user or ctx.author
        avatarUrl= user.display_avatar
        embed= disnake.Embed(title=f"{user}'s Profile Photo" , color = disnake.Color.from_rgb(0, 255, 255))
        embed.set_image(url=avatarUrl)
        await ctx.send(embed=embed)
        
    
    
        
def setup(bot):
    bot.add_cog(userCommands(bot))