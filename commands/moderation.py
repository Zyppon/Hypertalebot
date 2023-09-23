import disnake
from disnake.ext import commands
import asyncio
import aiohttp

class ModerationCommands(commands.Cog):
    def __init__(self , bot):
        self.bot = bot
        
    category_name = ['hypertale']

    @commands.command()
    async def createlive(self, ctx, category_name):
        if not ctx.author.guild_permissions.manage_channels:
            await ctx.send("Nu aveți permisiunea de a crea categorii.")
            return

        guild = ctx.guild

        # Verificăm dacă categoria există deja în guild
        existing_category = disnake.utils.get(guild.categories, name=category_name)
        if not existing_category:
            # Dacă categoria nu există, o creăm
            category = await guild.create_category_channel(category_name)
            await ctx.send(f"Category '{category.name}' created successfully.")
        else:
            category = existing_category

        # Crearea primului canal vocal în categoria nou creată și setarea ca privat pentru membrii
        voice_channel_name = "Members Online:"
        overwrites = {
            guild.default_role: disnake.PermissionOverwrite(view_channel=False),  # Dezactivează accesul pentru rolul implicit
            ctx.author: disnake.PermissionOverwrite(view_channel=True)  # Activează accesul pentru autorul comenzii
        }
        voice_channel = await guild.create_voice_channel(voice_channel_name, category=category, overwrites=overwrites)

        # Redenumirea primului canal vocal cu membri online din serverul Discord
        online_members_discord = sum(member.status == disnake.Status.online and not member.bot for member in guild.members)
        new_name_discord = f"{voice_channel.name} - {online_members_discord}"
        await voice_channel.edit(name=new_name_discord)

        # Crearea celui de-al doilea canal vocal în categoria nou creată și setarea ca privat pentru membrii
        voice_channel_name = "Players Online:"
        voice_channel_2_overwrites = {
            guild.default_role: disnake.PermissionOverwrite(view_channel=False),  # Dezactivează accesul pentru rolul implicit
            ctx.author: disnake.PermissionOverwrite(view_channel=True)  # Activează accesul pentru autorul comenzii
        }
        await guild.create_voice_channel(voice_channel_name, category=category, overwrites=voice_channel_2_overwrites)

        # Așteptați un pic pentru a permite serverului să creeze al doilea canal vocal
        await asyncio.sleep(2)

        # Redenumirea celui de-al doilea canal vocal cu jucători online de pe serverul Minecraft
        voice_channel_2 = disnake.utils.get(category.voice_channels, name=voice_channel_name)
        if voice_channel_2:
            server_address ="play.hypertale.org"  # Schimbați cu adresa serverului Minecraft dorită
            online_players_minecraft = await self.get_online_players(server_address)
            new_name_minecraft = f"{voice_channel_2.name} - {online_players_minecraft}"
            await voice_channel_2.edit(name=new_name_minecraft)

        await ctx.send("Two voice channels created successfully in the category.")

    async def get_online_players(self, server_address):
        url = f"https://api.minetools.eu/ping/{server_address}"
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    data = await response.json()
                    if "error" not in data:
                        online_players = data["players"]["online"]
                        return online_players
                    else:
                        return 0
        except Exception as e:
            print(f"Error retrieving Minecraft server status: {e}")
            return 0
       
       
       #Kick and unKick 
    @commands.command()
    async def kick(self, ctx, member: disnake.Member, *, reason=None):
        if not ctx.author.guild_permissions.kick_members:
            await ctx.send("You don't have permissions to kick members.")
            return

        if ctx.author.top_role <= member.top_role:
            await ctx.send("You can't kick this member because because he has a bigger role than you or equal to you.")
            return

        await member.kick(reason=reason)
        await ctx.send(f"{member.mention} has been kicked from this server. \n Reason: {reason or 'No Reason.'}")

    @commands.command()
    async def unckick(self, ctx, member_id: int):
        if not ctx.author.guild_permissions.kick_members:
            await ctx.send("You don't have permissions to unkick users.")
            return

        try:
            user = await self.bot.fetch_user(member_id)
            await ctx.guild.unban(user)
            await ctx.send(f"{user.mention} has been readmited.")
        except disnake.NotFound:
            await ctx.send("Can't find a user with this id.")
            
        #Mute and Unmute Commands    
    @commands.command()
    async def mute(self, ctx, member: disnake.Member, *, reason=None):
        if not ctx.author.guild_permissions.manage_roles:
            await ctx.send("You don't have permissions to mute members.")
            return

        if ctx.author.top_role <= member.top_role:
            await ctx.send("You can't mute this member because because he has a bigger role than you or equal to you.")
            return

        muted_role = disnake.utils.get(ctx.guild.roles, name="Muted")
        if not muted_role:
            try:
                muted_role = await ctx.guild.create_role(name="Muted", reason="Creating Muted role for mute command", permissions=disnake.Permissions(send_messages=False))
                for channel in ctx.guild.channels:
                    await channel.set_permissions(muted_role, send_messages=False, speak=False)
            except disnake.Forbidden:
                await ctx.send("I don't have permissions to mnage roles or channels.")
                return

        if muted_role in member.roles:
            await ctx.send(f"{member.mention} already muted.")
            return

        await member.add_roles(muted_role, reason=reason)
        await ctx.send(f"{member.mention} has been muted. \n Reason: {reason or 'No reason.'}")

    @commands.command()
    async def unmute(self, ctx, member: disnake.Member):
        if not ctx.author.guild_permissions.manage_roles:
            await ctx.send("You don't have permissions to unmute members.")
            return

        if ctx.author.top_role <= member.top_role:
            await ctx.send("You can't unmute this member because because he has a bigger role than you or equal to you.")
            return

        muted_role = disnake.utils.get(ctx.guild.roles, name="Muted")
        if not muted_role:
            await ctx.send("No Muted role on this server.")
            return

        if muted_role not in member.roles:
            await ctx.send(f"{member.mention} is not muted.")
            return

        await member.remove_roles(muted_role)
        await ctx.send(f"{member.mention} has been unmuted.")
        
    #Ban and Unban commands
    
    @commands.command()
    async def ban(self, ctx, member: disnake.Member, *, reason=None):
        if not ctx.author.guild_permissions.ban_members:
            await ctx.send("Nu aveți permisiunea de a da ban membrilor.")
            return

        if ctx.author.top_role <= member.top_role:
            await ctx.send("Nu puteți da ban unui membru cu rolul egal sau mai mare decât al dvs.")
            return

        try:
            await member.ban(reason=reason)
            await ctx.send(f"{member.mention} a fost dat ban. Motiv: {reason or 'Niciun motiv specificat.'}")
        except disnake.Forbidden:
            await ctx.send("Bot-ul nu are permisiunea de a da ban membrilor.")
        except disnake.HTTPException:
            await ctx.send("A apărut o eroare la executarea comenzii.")


    @commands.command()
    async def unban(self, ctx, *, member):
        if not ctx.author.guild_permissions.ban_members:
            await ctx.send("Nu aveți permisiunea de a da unban membrilor.")
            return

        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split("#")

        for ban_entry in banned_users:
            user = ban_entry.user
            if (user.name, user.discriminator) == (member_name, member_discriminator):
                try:
                    await ctx.guild.unban(user)
                    await ctx.send(f"{user.mention} a fost dat unban.")
                    return
                except disnake.Forbidden:
                    await ctx.send("Bot-ul nu are permisiunea de a da unban membrilor.")
                    return
                except disnake.NotFound:
                    await ctx.send("Nu am putut găsi utilizatorul respectiv în lista de membri banate.")
                    return
                except disnake.HTTPException:
                    await ctx.send("A apărut o eroare la executarea comenzii.")
                    return

        await ctx.send("Nu s-a găsit niciun membru banat cu acele date.")
        
def setup(bot):
   # category_names = ['HyperTale', 'HyperTale enjoy', 'HyperTale never die']
    bot.add_cog(ModerationCommands(bot))
    
