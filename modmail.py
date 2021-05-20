from discord.ext import commands
from discord import utils
import discord
import asyncio

class modmail(commands.Cog):
	def __init__(self, bot):
		self.client = bot

	@commands.Cog.listener()
	async def on_message(self, message):
		if message.author.bot:
			return

		if isinstance(message.channel, discord.DMChannel):
			guild = self.client.get_guild(797993478134956032)
			category = utils.get(guild.categories, name = "Modmail tickets")
			if not category:
				overwrites = {
					guild.default_role : discord.PermissionOverwrite(read_messages = False),
					guild.me : discord.PermissionOverwrite(read_messages = True)
				}
				categ = await guild.create_category(name = "Modmail tickets", overwrites = overwrites)

			channel = utils.get(categ.channels, topic = str(message.author.id))
			if not channel:
				channel = await categ.create_text_channel(name = f"{message.author.name}#{message.author.discriminator}", topic = str(message.author.id))
				await channel.send(f"New modmail created by {message.author.mention}")

			embed = discord.Embed(description = message.content, colour = 0x696969)
			embed.set_author(name = message.author, icon_url = message.author.avatar_url)
			await channel.send(embed = embed)

		elif isinstance(message.channel, discord.TextChannel):
			if message.content.startswith(self.client.command_prefi):
				pass
			else:
				topic = message.channel.topic
				if topic:
					member = message.guild.get_member(int(topic))
					if member:
						embed = discord.Embed(description = message.content, colour = 0x696969)
						embed.set_author(name = message.author, icon_url = message.author.avatar_url)
						await member.send(embed = embed)

@commands.command()
async def close(self, ctx, reason=None):
	if ctx.channel.category.name == "Modmail tickets":
		await ctx.channel.delete()
		await ctx.send(f"`{reason}`")


def setup(bot):
	bot.add_cog(modmail(bot))     

# note this is a work in progess
