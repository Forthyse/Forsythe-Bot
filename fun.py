import discord, random
from discord.ext import commands

class fun(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name = 'hug')
    async def _hug(self, ctx, member: discord.Member):
        await ctx.send(f"{ctx.message.author.mention} gave {member.mention} a big hug! ^.^")

    @commands.command(name = 'slap')
    async def _slap(self, ctx, member: discord.Member):
        await ctx.send(f"{ctx.message.author.mention} gave {member.mention} **A HUGE SLAP** (. ﾟーﾟ)!")

    @commands.command(name = 'throw')
    async def _throw(self, ctx, member: discord.Member):
        await ctx.send(f"{ctx.message.author.mention} **THREW** {member.mention} **ALL THE WAY TO CHINA**! ＼(●~▽~●)")

    @commands.command(name = 'cupcake')
    async def _cupcake(self, ctx, member: discord.Member):
        await ctx.send(f"{ctx.message.author.mention} gave {member.mention} a sweet cupcake! ＼(^-^)／ ")

    @commands.command(name= 'nuke')
    async def _nuke(self, ctx, member: discord.Member):
        await ctx.send(f"{ctx.message.author.mention} **NUKED** {member.mention} **{random.randint(0, 1000)}** **TIMES!**. （ ´∀｀）☆")

def setup(client):
    client.add_cog(fun(client))
