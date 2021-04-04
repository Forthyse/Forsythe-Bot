import discord, json
from discord.ext import commands
from datetime import datetime
from pymongo import MongoClient, ReturnDocument

nopm = "You don't have permission to do that"
mcli = MongoClient("MONGODBGOHERE")
db = mcli.Scythe

class moderation(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.guild_only()
    @commands.command(name="warn", aliases=['w'])
    async def warn(self, ctx, member: discord.Member, *reason: str):
        if ctx.channel.permissions_for(ctx.author).manage_messages:
            try:
                reas = " ".join(reason)
                user = self.client.get_user(member.id)
                warn = {
                    "mid": db.ScytheStorage.count() + 1,
                    "user": member.display_name,
                    "uid": member.id,
                    "reason": reas,
                    "moderator": ctx.message.author.display_name
                }

                db.ScytheStorage.insert_one(warn)
                await ctx.send(f"Warned {member} ({member.id}) for `{reas}`")
                await user.send(f"You were warned for {reas}")
            except discord.HTTPException as err:
                await ctx.send(f"Error: {err.text}")
        else:
            await ctx.send(nopm)

    @commands.guild_only()
    @commands.command(name="mute", aliases=['m'])
    async def mute(self, ctx: commands.Context, member: discord.Member, *reason: str):
        if ctx.channel.permissions_for(ctx.author).manage_messages:
            try:
                reas = " ".join(reason)
                role = discord.utils.get(ctx.guild.roles, name="Muted")
                user = self.client.get_user(member.id)
                mute = {
                    "User": f"{member} ({member.id})",
                    "Reason": f"{reas}",
                    "Date": f"{datetime.today().strftime('%m-%d-%Y')}"
                }
                with open('mute.json', 'a+') as outfile:
                    json.dump(mute, outfile)
                    outfile.write("\n")
                await member.add_roles(role)
                await ctx.send(f"Muted {member} ({member.id}) for `{reas}`")
                await user.send(f"You were muted for {reas}")
            except discord.HTTPException as err:
                await ctx.send(f"Error: {err.text}")

        else:
            await ctx.send(nopm)            

    @commands.guild_only()
    @commands.command(name="unmute", aliases=['um'])
    async def unmute(self, ctx, member: discord.Member, *reason: str):
        if ctx.channel.permissions_for(ctx.author).manage_messages:
            try:
                reas = " ".join(reason)
                role = discord.utils.get(ctx.guild.roles, name="Muted")
                user = self.client.get_user(member.id)
                mute = {
                    "User": f"{member} ({member.id})",
                    "Reason": f"{reas}",
                    "Date": f"{datetime.today().strftime('%m-%d-%Y')}"
                }
                with open('mute.json', 'a+') as outfile:
                    json.dump(mute, outfile)
                    outfile.write("\n")
                await member.remove_roles(role)
                await ctx.send(f"Unmuted {member} ({member.id}) for `{reas}`")
                await user.send(f"You were unmuted for {reas}")
            except discord.HTTPException as err:
                await ctx.send(f"Error: {err.text}")

        else:
            await ctx.send(nopm)

    @commands.guild_only()
    @commands.command(name = "kick", aliases = ["boot", "kapow"])
    async def kick(self, ctx, member: discord.Member, reason=None):
        if ctx.channel.permissions_for(ctx.author).kick_members:
            try:
                await member.kick(reason=reason)
                await ctx.send(f"Successfully kicked {member} ({member.id}) for `{reason}`")
            except discord.HTTPException as err:
                await ctx.send(f"Error: {err.text}")
        else:
            await ctx.send(nopm)
        
    @commands.guild_only()
    @commands.command(name = "ban", aliases = ["smite", "bam"])
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        if ctx.channel.permissions_for(ctx.author).ban_members:
            try:
                await member.ban(reason=reason)
                await ctx.send(f"Successfully banned {member} ({member.id}) for `{reason}`")
            except discord.HTTPException as err:
                await ctx.send(f"Error: {err.text}")
        else:
            await ctx.send(nopm)

    @commands.guild_only()
    @commands.command(name="unban", aliases = ["heal", "YAY"])
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, member:discord.User, *, reason=None):
        await ctx.guild.unban(member, reason=reason)
        await ctx.send(f"Successfully unbanned {member} ({member.id}) for `{reason}`")

    @commands.guild_only()
    @commands.command(name="purge", aliases=['clean', 'prune'])
    @commands.has_guild_permissions(manage_messages=True)
    async def purge(self, ctx, amt: int):
        await ctx.channel.purge(limit=amt)
        msg = await ctx.send("Successfully cleared the chat!")
        await msg.delete(delay=5)



def setup(client):
    client.add_cog(moderation(client))


