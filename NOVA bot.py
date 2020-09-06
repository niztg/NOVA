import discord
import os
import json
from secrets import token
from discord.ext import commands, tasks
from itertools import cycle

prefix = ['n.', 'N.']
client = commands.Bot(command_prefix=prefix, case_insensitive=True)
client.remove_command('help')


@client.event
async def on_ready():
    print('NOVA is online')
    await client.change_presence(activity=discord.Game('n.help'))


@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        embed = discord.Embed(title='Warning!',
                              description='This command is on a cooldown.\n '
                                          'Please try again in ``{:.2f}`` seconds'.format(error.retry_after),
                              color=0xFF0000, timestamp=ctx.message.created_at)
        embed.set_thumbnail(url='https://media.discordapp.net/attachments/726475732569555014/745738546660245664'
                                '/vsPV_ipxVKfJKE3xJGvJZeXwrxKUqqkJGBFdIgwpWWE3X7CIJrZ6kElRSJ4Mdvw5cC7wMPYLTKFNnBBv-'
                                '2K4WP344DoO6Al7RQB4.png')
        await ctx.send(embed=embed)
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(title='Warning!', color=0xFF0000, timestamp=ctx.message.created_at,
                              description=f'{ctx.message.author.mention},  '
                                          f'``{error.param}`` is a required argument that is missing.')
        embed.set_thumbnail(url='https://media.discordapp.net/attachments/726475732569555014/745738546660245664'
                                '/vsPV_ipxVKfJKE3xJGvJZeXwrxKUqqkJGBFdIgwpWWE3X7CIJrZ6kElRSJ4Mdvw5cC7wMPYLTKFNnBBv-'
                                '2K4WP344DoO6Al7RQB4.png')
        await ctx.send(embed=embed)

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

client.run(token)
