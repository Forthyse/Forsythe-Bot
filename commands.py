import discord
from discord.ext import commands
import json
from datetime import datetime
nopm = "You don't have permission to do that"
  


class Moderation(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.command(
        name="warn",
        aliases=['w']
    )
    @commands.guild_only()
    async def warn(self, ctx: commands.Context, member: discord.Member, *reason: str):
        if ctx.channel.permissions_for(ctx.author).manage_messages:
            try:
                reason = " ".join(reason)
                warn = {
                    "User": f"{member} ({member.id})",
                    "Reason": f"{reason}",
                    "Date": f"{datetime.today().strftime('%m-%d-%Y')}"
                }
                with open('warns.json', 'w') as outfile:
                    json.dump(warn, outfile)
                await ctx.send(f"Warned {member} ({member.id}) for `{reason}`")
            except discord.HTTPException as err:
                await ctx.send(f"Error: {err.text}")
        else:
            await ctx.send(nopm)
    
    @commands.command(name = "ban", aliases = ["smite", "bam"])
    @commands.guild_only()
    async def ban(self, ctx: commands.Context, member: discord.Member, reason=None):
        if ctx.channel.permissions_for(ctx.author).ban_members:
            try:
                await member.ban(reason=reason)
                await ctx.send(f"Successfully banned {member} ({member.id}) for `{reason}`")
            except discord.HTTPException as err:
                await ctx.send(f"Error: {err.text}")
        else:
            await ctx.send(nopm)

    @commands.command(name = "kick", aliases = ["boot", "kapow"])
    @commands.guild_only()
    async def kick(self, ctx: commands.Context, member: discord.Member, reason=None):
        if ctx.channel.permissions_for(ctx.author).kick_members:
            try:
                await member.kick(reason=reason)
                await ctx.send(f"Successfully kicked {member} ({member.id}) for `{reason}`")
            except discord.HTTPException as err:
                await ctx.send(f"Error: {err.text}")
        else:
            await ctx.send(nopm)

    @commands.command(
        name="ping"
    )
    @commands.guild_only()
    @commands.cooldown(2, 3, commands.BucketType.user)
    async def ping(self, ctx: commands.Context):
        await ctx.send(f"Latency: {round(self.client.latency * 1000)}ms")
    
def setup(client: commands.Bot):
    client.add_cog(Moderation(client))



