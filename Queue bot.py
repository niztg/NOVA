import discord
import praw
from discord.ext import commands

client = commands.Bot(command_prefix='.', case_insensitive=True)


@client.event
async def on_ready():
    print('Queue Bot is online')

    @client.command()
    async def ping(ctx):
        embed = discord.Embed(title='Pong!', description=f'{round(client.latency * 1000)}ms', color=0xFF0000)
        await ctx.send(embed=embed)

    @client.command(aliases=['q', 'queue'])
    async def modqueue(ctx):
        try:
            modcomment = []
            modsub = []
            for item in reddit.subreddit('rareinsults').mod.modqueue(only='comments', limit=None):
                modcomment.append(item)
            for item in reddit.subreddit('rareinsults').mod.modqueue(only='submissions', limit=None):
                modsub.append(item)
            count = len(modsub + modcomment)
            post_count = len(modsub)
            comment_count = len(modcomment)
            embed = discord.Embed(title='r/rareinsults Mod Queue', description=f'I found {count} '
                                                                               f'total items in the modqueue.',
                                  color=0xFF0000, timestamp=ctx.message.created_at)
            embed.set_thumbnail(url='https://images-ext-1.discordapp.net/external/UuPKbkZR7LtnB8rwUDRlL1_9OHUDtRq5qTbSP'
                                    'Iwen2U/https/b.thumbs.redditmedia.com/wWCY2qH6nBLeYtLIxWMMSzNKNVAgZq'
                                    'oGnsBQTV4RwWs.png')
            embed.set_footer(text=f'Requested by {ctx.message.author}', icon_url=ctx.message.author.avatar_url)

            embed.add_field(name='Posts', value=post_count, inline=False)
            embed.add_field(name='Comments', value=comment_count, inline=False)

            await ctx.send(embed=embed)
        except Exception as error:
            await ctx.send(error)

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[Reddit]}')


client.run('NzI0ODMzNzI5MjU5NzY1ODQw.XvF_Fg.UQEnN2edhJaaXjzZasDFoPnE2eo')
