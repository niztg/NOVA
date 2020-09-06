import discord
import asyncio
import random
from discord.ext import commands


class Moderation(commands.Cog):
    """Commands to help you better manage your server"""

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Moderation module is ready')

    @commands.command()
    @commands.has_permissions(kick_members=True)
    @commands.bot_has_guild_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        """Kick a member from the server"""
        await member.kick(reason=reason)
        await ctx.send(f"<:GreenTick:707950252434653184> Successfully kicked {member}")
        await member.send(f"You have been kicked from **{ctx.guild.name}** for the following reason:"
                          f"\n```py\n{reason}```")

    @commands.command()
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_guild_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        """Ban a member from the server"""
        await member.ban(reason=reason)
        await ctx.send(f"<:GreenTick:707950252434653184> Successfully banned {member}")
        await member.send(f"You have been banned from **{ctx.guild.name}** for the following reason:"
                          f"\n```py\n{reason}```")

    @commands.command()
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_guild_permissions(ban_members=True)
    async def unban(self, ctx, *, member):
        """Unban a member"""
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split('#')

        for ban_entry in banned_users:
            user = ban_entry.user

            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                await ctx.send(f"<:GreenTick:707950252434653184> Successfully unbanned {user}")
                await user.send(f'<:tickgreen:732660186560462958> You have been unbanned from **{ctx.guild.name}**')
                return

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    @commands.bot_has_guild_permissions(manage_messages=True)
    async def clear(self, ctx, amount: int = 5):
        """Purge any amount of messages with a default of 5"""
        await ctx.channel.purge(limit=amount + 1)
        await ctx.send(f'<:GreenTick:707950252434653184>  ``{amount}`` messages have been cleared',
                       delete_after=3.0)

    @commands.command()
    @commands.has_permissions(manage_channels=True)
    @commands.bot_has_guild_permissions(manage_channels=True)
    async def slowmode(self, ctx, seconds: int = 10):
        """Set the slowmode for a channel"""
        await ctx.channel.edit(slowmode_delay=seconds)
        if seconds == 0:
            await ctx.send(f"<:GreenTick:707950252434653184> "
                           f"Slowmode for <#{ctx.channel.id}> has been removed.")
            return
        else:
            await ctx.send(f"<:GreenTick:707950252434653184> "
                           f"Slowmode for <#{ctx.channel.id}> has been set to ``{seconds}`` seconds."
                           f"\nDo ``n.slowmode 0`` to remove slowmode!")

    @commands.command(aliases=['suggest', 'vote'])
    async def poll(self, ctx, *, msg):
        """Use NOVA to hold an organized vote"""
        embed = discord.Embed(title=f'New Poll', color=0x5643fd, description=msg, timestamp=ctx.message.created_at)
        embed.set_footer(icon_url=ctx.message.author.avatar_url, text=ctx.message.author)
        poll = await ctx.send(embed=embed)
        for e in ['⬆️', '⬇️']:
            await poll.add_reaction(e)


def setup(client):
    client.add_cog(Moderation(client, ))
