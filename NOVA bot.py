import discord
import os
import json
from secrets import token
from discord.ext import commands, tasks
from itertools import cycle

prefix = ['n.', 'N.']
intents = discord.Intents.default()
intents.members = True
client = commands.Bot(command_prefix=prefix, case_insensitive=True, intents=intents)
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
    if isinstance(error, commands.NSFWChannelRequired):
        embed = discord.Embed(title='Warning!', color=0xFF0000, timestamp=ctx.message.created_at,
                              description=f'{ctx.message.author.mention},  '
                                          f'an NSFW channel is required. Go to horny jail.')
        embed.set_image(url='https://i.kym-cdn.com/entries/icons/facebook/000/033/758/Screen_Shot_2020-04-28_at_12.21'
                            '.48_PM.jpg')
        await ctx.send(embed=embed)
    if isinstance(error, commands.BotMissingPermissions):
        embed = discord.Embed(title='Warning!', color=0xFF0000, timestamp=ctx.message.created_at,
                              description=f'{ctx.message.author.mention},  '
                                          f'NOVA is missing the required permissions to use the command. In order for '
                                          f'NOVA to use this command, ``{error.missing_perms}``'
                                          f'must be enabled in role settings.')
        embed.set_thumbnail(url='https://media.discordapp.net/attachments/726475732569555014/745738546660245664'
                                '/vsPV_ipxVKfJKE3xJGvJZeXwrxKUqqkJGBFdIgwpWWE3X7CIJrZ6kElRSJ4Mdvw5cC7wMPYLTKFNnBBv-'
                                '2K4WP344DoO6Al7RQB4.png')
    if isinstance(error, commands.MissingPermissions):
        await ctx.send(f'⚠ You are not allowed to use this command. You must have ``{error.missing_perms}`` '
                       f'permissions in order to do so.')


for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

client.run(token)