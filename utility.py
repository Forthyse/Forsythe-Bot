import discord
from discord.ext import commands

class utility(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.guild_only()
    @commands.command(name = "avatar", aliases = ["av", "pic"])
    async def avatar(self, ctx, user: discord.User=None):
        if user is None:
            user = ctx.author
        embed = discord.Embed(color=000000, title=f'{user.name}#{user.discriminator}')
        embed.set_image(url=user.avatar_url)
        await ctx.send(embed=embed)

    @commands.guild_only()
    @commands.command(name="ping")
    @commands.cooldown(2, 3, commands.BucketType.user)
    async def ping(self, ctx):
        pinging = await ctx.send('Pinging...')
        diff = pinging.created_at - ctx.message.created_at
        await pinging.edit(content=f'Pong! Latency: {round(diff.total_seconds()*1000)}ms | Websocket: {round(self.client.latency*1000)}ms')

def setup(client):
    client.add_cog(utility(client))