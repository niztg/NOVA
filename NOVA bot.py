import discord
import os
from secrets import token
from discord.ext import commands
from aiohttp import ClientSession

intents = discord.Intents.default()
intents.members = True

client = commands.Bot(
    prefix=['n.', 'N.'],
    intents=intents,
    case_insensitive=True
)

client.remove_command('help')
client.session = ClientSession()
client.cogs = [f"cogs.{f[:-3]}" for f in os.listdir('./cogs') if f.endswith('.py')]
client.loop.create_task(start())

async def start():
    print(f'{client.user.name} is online')
    for cog in client.cogs:
        try:
            client.load_extension(cog)
        except Exception as error:
            print(error)
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
    if isinstance(error, commands.UserNotFound):
        embed = discord.Embed(title='Warning!', color=0xFF0000, timestamp=ctx.message.created_at,
                              description=f'{ctx.message.author.mention},  '
                                          f'that user could not be found.')
        embed.set_thumbnail(url='https://media.discordapp.net/attachments/726475732569555014/745738546660245664'
                                '/vsPV_ipxVKfJKE3xJGvJZeXwrxKUqqkJGBFdIgwpWWE3X7CIJrZ6kElRSJ4Mdvw5cC7wMPYLTKFNnBBv-'
                                '2K4WP344DoO6Al7RQB4.png')
        await ctx.send(embed=embed)
    if isinstance(error, commands.CommandInvokeError):
        embed = discord.Embed(title='Warning!', color=0xFF0000, timestamp=ctx.message.created_at,
                              description=f'{ctx.message.author.mention},  '
                                          f'there was an error with this command. If you would like to report this '
                                          f'issue to the creator of this bot, join the support server.\n'
                                          f'🔗  [Link](https://discord.gg/Uqh9NXY)')
        embed.add_field(name='Error:', value=f'```py\n{error}```')
        embed.set_thumbnail(url='https://media.discordapp.net/attachments/726475732569555014/745738546660245664'
                                '/vsPV_ipxVKfJKE3xJGvJZeXwrxKUqqkJGBFdIgwpWWE3X7CIJrZ6kElRSJ4Mdvw5cC7wMPYLTKFNnBBv-'
                                '2K4WP344DoO6Al7RQB4.png')
        await ctx.send(embed=embed)

client.run(token)
