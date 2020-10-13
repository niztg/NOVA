import discord
import aiohttp
import random
import asyncio
import io
import json
from secrets import *
from aiotrivia import TriviaClient, AiotriviaException
from discord.ext import commands


class Fun(commands.Cog):
    """Use NOVA to have a little fun on your server"""

    def __init__(self, client):
        self.client = client
        self.trivia = TriviaClient()

    @commands.Cog.listener()
    async def on_ready(self):
        print('Fun module is ready')

    @commands.command(aliases=['pupper', 'doggo'])
    async def dog(self, ctx):
        # all credit to R.Danny for this command
        """Get a nice dog to brighten your day"""
        async with aiohttp.ClientSession() as cs:
            async with cs.get("https://random.dog/woof") as resp:
                if resp.status != 200:
                    return await ctx.send('<:RedX:707949835960975411> No dog found')

                filename = await resp.text()
                url = f'https://random.dog/{filename}'
                filesize = ctx.guild.filesize_limit if ctx.guild else 8388608
                if filename.endswith(('.mp4', '.webm')):
                    async with ctx.typing():
                        async with cs.get(url) as other:
                            if other.status != 200:
                                return await ctx.send('Could not download dog video :/')

                            if int(other.headers['Content-Length']) >= filesize:
                                return await ctx.send(f'Video was too big to upload... See it here: {url} instead.')

                            fp = io.BytesIO(await other.read())
                            await ctx.send(file=discord.File(fp, filename=filename))
                else:
                    await ctx.send(embed=discord.Embed(color=0x5643fd,
                                                       description=f"<:github:734999696845832252> "
                                                                   f"[Source Code]"
                                                                   f"(https://github.com/Rapptz/RoboDanny/blob/rewrite/"
                                                                   f"cogs/funhouse.py#L44-L66)").set_image(url=url)
                                   .set_footer(text='https://random.dog/woof'))

    @commands.command(aliases=['catto', 'kitty'])
    async def cat(self, ctx):
        """Waste time with some cat images"""
        async with aiohttp.ClientSession() as cs:
            async with cs.get("https://api.thecatapi.com/v1/images/search") as resp:
                if resp.status != 200:
                    return await ctx.send('<:RedX:707949835960975411> No cat found')
                js = await resp.json()
                await ctx.send(embed=discord.Embed(color=0x5643fd,
                                                   description=f"<:github:734999696845832252> "
                                                               f"[Source Code]"
                                                               f"(https://github.com/DevilJamJar"
                                                               f"/DevilBot/blob/master/cogs/fun."
                                                               f"py)").set_image(
                    url=js[0]['url']).set_footer(text='https://api.thecatapi.com/v1/images/search'))

    @commands.group(invoke_without_command=True, aliases=['astronomy'])
    async def apod(self, ctx):
        # APOD command group
        """Astronomy Picture of the Day"""
        p = ctx.prefix
        async with aiohttp.ClientSession() as cs, ctx.typing():
            async with cs.get(f"https://api.nasa.gov/planetary/apod?api_key={nasa_key}") \
                    as resp:
                if resp.status != 200:
                    return await ctx.send('<:RedX:707949835960975411> No image could be found')
                else:
                    js = await resp.json()
                    embed = discord.Embed(color=0x5643fd, title=js['title'],
                                          timestamp=ctx.message.created_at)
                    embed.set_image(url=js['url'])
                    embed.add_field(name='Date', value=js['date'], inline=True)
                    embed.add_field(name='Sub Commands',
                                    value=f"``{p}apod hd``\n``{p}apod description``\n``{p}apod date``",
                                    inline=True)
                    embed.set_footer(text=f"Copyright {js['copyright']}")
                    await ctx.send(embed=embed)

    @apod.command()
    async def date(self, ctx, date):
        """Show the astronomy picture of the day for a given date (YYYY-MM-DD)"""
        link = f"https://api.nasa.gov/planetary/apod?date={date}&api_key={nasa_key}"
        async with aiohttp.ClientSession() as cs, ctx.typing():
            async with cs.get(link) as resp:
                if resp.status != 200:
                    return await ctx.send('<:RedX:707949835960975411> No image could be found')
                else:
                    js = await resp.json()
                    embed = discord.Embed(color=0x5643fd, title=js['title'],
                                          timestamp=ctx.message.created_at)
                    embed.set_image(url=js['url'])
                    embed.add_field(name='Date', value=js['date'], inline=True)
                    embed.add_field(name='HD Version', value=f"<:asset:734531316741046283> [Link]({js['hdurl']})",
                                    inline=True)
                    embed.set_footer(text=f"Copyright {js['copyright']}")
                    await ctx.send(embed=embed)

    @apod.command()
    async def hd(self, ctx):
        """HD version for the astronomy picture of the day"""
        async with aiohttp.ClientSession() as cs, ctx.typing():
            async with cs.get(f"https://api.nasa.gov/planetary/apod?api_key={nasa_key}") \
                    as resp:
                if resp.status != 200:
                    return await ctx.send('<:RedX:707949835960975411> No image could be found')
                else:
                    js = await resp.json()
                    embed = discord.Embed(color=0x5643fd, title=f"{js['title']} (HD)",
                                          timestamp=ctx.message.created_at)
                    embed.set_image(url=js['hdurl'])
                    embed.set_footer(text=f"Copyright {js['copyright']}")
                    await ctx.send(embed=embed)

    @apod.command()
    async def description(self, ctx):
        """Explanation for the astronomy picture of the day"""
        async with aiohttp.ClientSession() as cs, ctx.typing():
            async with cs.get(f"https://api.nasa.gov/planetary/apod?api_key={nasa_key}") \
                    as resp:
                if resp.status != 200:
                    return await ctx.send('<:RedX:707949835960975411> No description could be found')
                else:
                    js = await resp.json()
                    embed = discord.Embed(color=0x5643fd, title=js['title'], description=js['explanation'],
                                          timestamp=ctx.message.created_at)
                    embed.set_footer(text=f"Copyright {js['copyright']}")
                    await ctx.send(embed=embed)

    @commands.command()
    async def inspiro(self, ctx):
        """Look at beautiful auto-generated quotes"""
        url = 'https://inspirobot.me/api?generate=true'
        async with aiohttp.ClientSession() as cs, ctx.typing():
            async with cs.get(url) as r:
                data = await r.text()
        embed = discord.Embed(color=0x5643fd,
                              description="<:github:734999696845832252> [Source Code](https://github.com/DevilJamJar/"
                                          "DevilBot/blob/master/cogs/fun.py)", timestamp=ctx.message.created_at)
        embed.set_image(url=data)
        embed.set_footer(text='Copyright 2020 Deviljamjar')
        await ctx.send(embed=embed)

    @commands.command()
    async def trivia(self, ctx, difficulty: str = None):
        """Test out your knowledge with trivia questions from nizcomix#7532"""
        difficulty = difficulty or random.choice(['easy', 'medium', 'hard'])
        try:
            question = await self.trivia.get_random_question(difficulty)
        except AiotriviaException:
            return await ctx.send(embed=discord.Embed(title='That is not a valid sort.',
                                                      description='Valid sorts are ``easy``, ``medium``, and ``hard``.',
                                                      color=0xFF0000))
        answers = question.responses
        random.shuffle(answers)
        final_answers = '\n'.join([f"{index}. {value}" for index, value in enumerate(answers, 1)])
        message = await ctx.send(embed=discord.Embed(
            title=f"{question.question}", description=f"\n{final_answers}\n\nQuestion about: **{question.category}"
                                                      f"**\nDifficulty: **{difficulty}**",
            color=0x5643fd))
        answer = answers.index(question.answer) + 1
        try:
            while True:
                msg = await self.client.wait_for('message', timeout=15, check=lambda m: m.id != message.id)
                if str(answer) in msg.content:
                    return await ctx.send(embed=discord.Embed(description=f"{answer} was correct ({question.answer})",
                                                              color=0x32CD32, title='Correct!'))
                if str(answer) not in msg.content:
                    return await ctx.send(embed=discord.Embed(description=f"Unfortunately **{msg.content}** was wrong. "
                                                                          f"The "
                                                                          f"correct answer was ``{question.answer}``.",
                                                              title='Incorrect', color=0xFF0000))
        except asyncio.TimeoutError:
            embed = discord.Embed(title='Time expired', color=0xFF0000,
                                  description=f"The correct answer was {question.answer}")
            await ctx.send(embed=embed)

    @commands.command(name='8ball')
    async def _8ball(self, ctx, *, question):
        """Allow the mystical NOVA to answer all of life's important questions"""
        responses = ['It is certain', 'It is decidedly so', 'Without a doubt', 'Yes, definitely', 'You may rely on it',
                     'As I see it, yes', 'Most likely', 'Outlook good', 'Yes', 'Signs point to yes',
                     'Reply hazy, try again', 'Ask again later', 'Better not tell you now', 'Cannot predict now',
                     'Concentrate and ask again', 'Do not count on it', 'My reply is no', 'My sources say no',
                     'The outlook is not so good', 'Very doubtful']
        embed = discord.Embed(title='Magic 8ball says', color=0x5643fd, timestamp=ctx.message.created_at)
        embed.add_field(name='Question:', value=question, inline=False)
        embed.add_field(name='Answer:', value=random.choice(responses), inline=False)
        embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/726475732569555014/747266621512614009/8-Ball-'
                                'Pool-Transparent-PNG.png')
        await ctx.send(embed=embed)

    @commands.command()
    async def motivation(self, ctx):
        """Need motivation? NOVA has you covered."""
        responses = ['https://youtu.be/kGOQfLFzJj8', 'https://youtu.be/kYfM5uKBKKg', 'https://youtu.be/VV_zfO3HmTQ',
                     'https://youtu.be/fLeJJPxua3E', 'https://youtu.be/5aPntFAyRts', 'https://youtu.be/M2NDQOgGycg',
                     'https://youtu.be/FDDLCeVwhx0', 'https://youtu.be/P10hDp6mUG0', 'https://youtu.be/K8S8OvPhMDg',
                     'https://youtu.be/zzfREEPbUsA', 'https://youtu.be/mgmVOuLgFB0', 'https://youtu.be/t8ApMdi24LI',
                     'https://youtu.be/JXQN7W9y_Tw', 'https://youtu.be/fKtmM_45Dno', 'https://youtu.be/k9zTr2MAFRg',
                     'https://youtu.be/bm-cCn0uRXQ', 'https://youtu.be/9bXWNeqKpjk', 'https://youtu.be/ChF3_Zbuems',
                     'https://youtu.be/BmIM8Hx6yh8', 'https://youtu.be/oNYKDM4_ZC4', 'https://youtu.be/vdMOmeljTvA',
                     'https://youtu.be/YPTuw5R7NKk', 'https://youtu.be/jnT29dd7LWM', 'https://youtu.be/7XzxDIJKXlk']
        await ctx.send(random.choice(responses))

    @commands.command()
    async def hex(self, ctx, code):
        """Explore hex colors"""
        color = discord.Colour(int(code, 16))
        async with aiohttp.ClientSession() as cs, ctx.typing():
            async with cs.get(f"https://www.thecolorapi.com/id?hex={code}") \
                    as resp:
                if resp.status != 200:
                    return await ctx.send('<:RedX:707949835960975411> No hex code could be found.')
                else:
                    js = await resp.json()
                    name = js['name']
                    image = js['image']
                    rgb = js['rgb']
                    hsl = js['hsl']
                    hsv = js['hsv']
                    cmyk = js['cmyk']
                    xyz = js['XYZ']
                    embed = discord.Embed(title=f"Showing hex code ``#{code}``", color=color,
                                          timestamp=ctx.message.created_at)
                    embed.add_field(name='Name', value=f"{name['value']}")
                    embed.add_field(name='Exact name?', value=f"``{name['exact_match_name']}``")
                    embed.add_field(name='Closest named hex', value=f"``{name['closest_named_hex']}``")
                    embed.add_field(name='🔗 Image Links',
                                    value=f"<:asset:734531316741046283> [Bare]({image['bare']})\n"
                                          f"<:asset:734531316741046283> [Labeled]({image['named']})", inline=False)
                    embed.add_field(name='Other Codes',
                                    value=f"**rgb**({rgb['r']}, {rgb['g']}, {rgb['b']})\n"
                                          f"**hsl**({hsl['h']}, {hsl['s']}, {hsl['l']})\n"
                                          f"**hsv**({hsv['h']}, {hsv['s']}, {hsv['v']})\n"
                                          f"**cmyk**({cmyk['c']}, {cmyk['m']}, {cmyk['y']}, {cmyk['k']})\n"
                                          f"**XYZ**({xyz['X']}, {xyz['Y']}, {xyz['Z']})", inline=False)
                    await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1, 59, commands.BucketType.member)
    async def poke(self, ctx, member: discord.Member, *, message):
        """This command shows up in the dictionary under the definition of annoying."""
        member = member or ctx.message.author
        await ctx.send(f'<a:a_check:742966013930373151> Message successfully sent to ``{member}``')
        embed = discord.Embed(title=f'Message from {ctx.message.author}:', color=0x5643fd, description=message,
                              timestamp=ctx.message.created_at)
        await member.send(embed=embed)

    @commands.command()
    async def secret(self, ctx):
        """Don't use this command, I'm warning you."""
        thing = await ctx.send('Why did you just use this command?')
        await asyncio.sleep(.5)
        a = await ctx.send("It can't be stopped now.")
        await asyncio.sleep(.5)
        b = await ctx.send("You shouldn't have done this.")
        await asyncio.sleep(.5)
        embed = discord.Embed(color=0x5643fd)
        embed.set_image(url='https://i.imgur.com/RnZJkhU.png')
        message = await ctx.send(embed=embed)
        await asyncio.sleep(1)
        embed1 = discord.Embed(color=0x5643fd)
        embed1.set_image(url='https://i.imgur.com/Z0lf3HK.png')
        await message.edit(embed=embed1)
        await asyncio.sleep(1)
        embed2 = discord.Embed(color=0x5643fd)
        embed2.set_image(url='https://i.imgur.com/X8jlhvf.png')
        await message.edit(embed=embed2)
        await asyncio.sleep(1)
        embed3 = discord.Embed(color=0x5643fd)
        embed3.set_image(url='https://illinoistruckcops.org/wp-content/uploads/bfi_thumb/033-nasy0071d7iqe6nru1klw4h'
                             'qhtzt70v03iypuefoh4.png')
        await message.edit(embed=embed3)
        await asyncio.sleep(3)
        embed4 = discord.Embed(color=0x5643fd)
        embed4.set_image(url='https://media3.giphy.com/media/Ju7l5y9osyymQ/200.gif')
        await message.edit(embed=embed4)
        await asyncio.sleep(5)
        await thing.edit(content='<:shut:696892857998508052>')
        await message.delete()
        await b.delete()
        await a.delete()

    @commands.command()
    async def news(self, ctx, result=0):
        """Show the top headlines in the U.S. for today. Enter a number to show a certain result."""
        url = f'https://newsapi.org/v2/top-headlines?country=us&apiKey={news_key}'
        async with aiohttp.ClientSession() as cs, ctx.typing():
            async with cs.get(url) as resp:
                if resp.status == 500:
                    return await ctx.send("<:redx:732660210132451369> The API's server is currently down. "
                                          "Check back later.")
                if resp.status == 429:
                    return await ctx.send('<:redx:732660210132451369> This command is on a timeout. '
                                          'Check back tomorrow when we have more API requests available.')
                if resp.status == 400:
                    return await ctx.send('<:redx:732660210132451369> Something went wrong with the request. '
                                          'Try again with different paramters.')
                if resp.status == 200:
                    js = await resp.json()
                    a = js['articles'][result]
                    embed = discord.Embed(color=0x5643fd, timestamp=ctx.message.created_at, title=a['title'],
                                          url=a['url'])
                    embed.add_field(name='Content', inline=False, value=a['content'])
                    embed.add_field(name='Total Results', inline=False, value=js['totalResults'])
                    embed.add_field(name='Publish Date', inline=False, value=a['publishedAt'])
                    embed.add_field(name='Source', inline=False, value=a['source']['name'])
                    embed.set_author(name=a['author'])
                    embed.set_thumbnail(url=a['urlToImage'])
                    return await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Fun(client))
