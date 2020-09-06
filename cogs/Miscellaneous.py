import discord
import random
import humanize
import asyncio
import datetime
from discord.ext import commands


class Miscellaneous(commands.Cog):
    """Helpful commands that don't quite fit in a certain category"""

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Miscellaneous module is ready')

    @commands.command()
    async def invite(self, ctx):
        """Invite NOVA to your own server"""
        embed = discord.Embed(title='Invite links for NOVA',
                              description='[<:news:730866149109137520> Required Permissions](https://discord.com/oauth2'
                                          '/'
                                          'authorize?client'
                                          '_id=709922850953494598&permissions=470150214&scope=bot)\n'
                                          '[<:news:730866149109137520> No Permissions]'
                                          '(https://discord.com/api/oauth2/authorize?client_id=709922850953494598&permi'
                                          'ssions=0&scope=bot)\n[<:news:730866149109137520> All Permissions (admin)]'
                                          '(https://discord.com/api/oauth2/authorize?client_id=709922850953494598&perm'
                                          'issions=8&scope=bot)', color=0x5643fd)
        embed.set_footer(text='Developed by YeetVegetabales', icon_url='https://cdn.discordapp.com/avatars'
                                                                       '/569374429218603019'
                                                                       '/a_6dac6946906e498650f6c2466aa82200.gif?size'
                                                                       '=256&f=.gif')
        embed.set_thumbnail(url='https://images-ext-2.discordapp.net/external/54Mim4lahztGCP4hgmpy4lOdEUc4'
                                '-dOeNA_x6hVHMlc/%3Fsize%3D4096/https/cdn.discordapp.com/avatars/709922850953494598'
                                '/f78ed19924e8c95abc30f406d47670d7.png')
        await ctx.send(embed=embed)

    @commands.command()
    async def discord(self, ctx):
        """Generate a link to join NOVA's discord server!"""
        embed = discord.Embed(title='Join the discord today!', color=0x5643fd, description="This server is where "
                                                                                           "all of "
                                                                                           "NOVA's updates and "
                                                                                           "important "
                                                                                           "announcements will pass "
                                                                                           "through. The creator of "
                                                                                           "this "
                                                                                           "bot, YeetVegetabales#5313, "
                                                                                           "will also be there testing "
                                                                                           "and letting the communtiy "
                                                                                           "in "
                                                                                           "on things first hand!")
        embed.set_thumbnail(url='https://images-ext-2.discordapp.net/external/AQCEqCF4Yl_PWAfuA-GReZoDify6'
                                '--y4hXOJVkqaDHo/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/709922850953494598'
                                '/f78ed19924e8c95abc30f406d47670d7.png')
        embed.add_field(name='Server Invite', value='<:news:730866149109137520> '
                                                    '[Join here](https://discord.gg/Uqh9NXY)')
        await ctx.send(embed=embed)

    @commands.command()
    @commands.is_owner()
    async def load(self, ctx, extension):
        """Loads a cog (owner only)"""
        client.load_extension(f'cogs.{extension}')
        embed = discord.Embed(title='Cog successfully loaded', color=0x5643fd)
        await ctx.send(embed=embed)

    @commands.command()
    @commands.is_owner()
    async def unload(self, ctx, extension):
        """Unloads a cog (owner only)"""
        client.unload_extension(f'cogs.{extension}')
        embed = discord.Embed(title='Cog successfully unloaded', color=0x5643fd)
        await ctx.send(embed=embed)

    @commands.command()
    @commands.is_owner()
    async def reload(self, ctx, extension):
        """Reloads a cog (owner only)"""
        client.unload_extension(f'cogs.{extension}')
        client.load_extension(f'cogs.{extension}')
        embed = discord.Embed(title='Cog successfully reloaded', color=0x5643fd)
        await ctx.send(embed=embed)

    @commands.command(aliases=['calc', 'math'])
    async def calculate(self, ctx, operation):
        """Calculate an expression using a fancy discord calculator"""
        expression = operation
        words = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
                 'u', 'v', 'w', 'x', 'y', 'z', '\\', '{', '}', '"', '&', '^', '$', '#', '@', '[', ']', '|', '?', '**']
        if any(words in operation for words in words):
            embed = discord.Embed(title='Warning', description='You are not allowed to do that.', color=0xFF0000)
            embed.set_thumbnail(url='https://i.imgur.com/uafPEpb.png')
            await ctx.send(embed=embed)
            return
        meme = ['9+10']
        if any(words in operation for words in meme):
            embed = discord.Embed(title='Discord Calculator', color=0x5643fd, timestamp=ctx.message.created_at)
            embed.set_footer(text=f'Requested by {ctx.message.author}', icon_url=ctx.message.author.avatar_url)
            embed.set_thumbnail(url='https://pngimg.com/uploads/calculator/calculator_PNG7939.png')

            embed.add_field(name='Input Expression', value=f"```py\n{expression}```", inline=False)

            embed.add_field(name='Output Solution', value="```py\n21```", inline=False)

            return await ctx.send(embed=embed)
        if len(str(operation)) < 21:
            try:
                solution = eval(operation)
                embed = discord.Embed(title='Discord Calculator', color=0x5643fd, timestamp=ctx.message.created_at)
                embed.set_footer(text=f'Requested by {ctx.message.author}', icon_url=ctx.message.author.avatar_url)
                embed.set_thumbnail(url='https://pngimg.com/uploads/calculator/calculator_PNG7939.png')

                embed.add_field(name='Input Expression', value=f"```py\n{expression}```", inline=False)

                embed.add_field(name='Output Solution', value=f"```py\n{solution}```", inline=False)

                await ctx.send(embed=embed)
            except ZeroDivisionError:
                embed = discord.Embed(title='Error...', color=0xFF0000, description="You cannot divide by zero.")
                embed.set_footer(text=f'Error occurred at {ctx.message.created_at}',
                                 icon_url=ctx.message.author.avatar_url)
                embed.set_thumbnail(url='https://imgur.com/uafPEpb')
                await ctx.send(embed=embed)
            except ValueError:
                embed = discord.Embed(title='Error...', color=0xFF0000, description="That expression is invalid.")
                embed.set_footer(text=f'Error occurred at {ctx.message.created_at}',
                                 icon_url=ctx.message.author.avatar_url)
                embed.set_thumbnail(url='https://imgur.com/uafPEpb')
                await ctx.send(embed=embed)
            return
        else:
            embed = discord.Embed(title='Warning!', color=0xFF0000,
                                  description='Your operation must be under 21 characters long.',
                                  timestamp=ctx.message.created_at)
            embed.set_thumbnail(url='https://imgur.com/uafPEpb')
            await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1, 30, commands.BucketType.channel)
    async def timer(self, ctx, seconds: int = 60):
        """Set a timer using NOVA"""
        try:
            if seconds < 301:
                le_seconds = list(range(seconds))
                embed = discord.Embed(color=0x5643fd, title="Discord Stopwatch", description=f'```py\n{seconds}```',
                                      timestamp=ctx.message.created_at)
                msg = await ctx.send(embed=embed)
                for num in le_seconds[::-1]:
                    embed.description = f'```py\n{num}```'
                    await msg.edit(embed=embed)
                    if num != 0:
                        await asyncio.sleep(1)
                    continue
                embed.description = f"Timer Complete\nSuccessfully counted down from **{seconds}**"
                await msg.edit(embed=embed)
                return
            else:
                embed = discord.Embed(title='Warning! That number is too large.', color=0xFF0000,
                                      description='The maximum amount of seconds if 300.',
                                      timestamp=ctx.message.created_at)
                embed.set_thumbnail(url='https://imgur.com/uafPEpb')
                await ctx.send(embed=embed)
        except commands.CommandOnCooldown:
            embed = discord.Embed(title='This command is on cooldown!', color=0xFF0000,
                                  description='You must wait 30 seconds before using this command again.')
            await ctx.send(embed=embed)

    @commands.Cog.listener(name='on_message')
    async def maymayhelper_mention(self, message):
        if "<@&710880987168505898>" in message.content:
            for i in ["<:upvote:700689655607197746>", "<:downvote:700689654906880063>", "<:yes:719841750788866060>",
                      "<:pepesquint:700692817789321269>"]:
                await message.add_reaction(i)

    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f"``{self.client.latency * 1000}``ms")


def setup(client):
    client.add_cog(Miscellaneous(client))
