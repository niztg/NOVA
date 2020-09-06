import discord
import praw
import random
import datetime
import aiohttp
import asyncio
import humanize
import colorthief
from secrets import *
from discord.ext import commands
from colorthief import ColorThief


class Reddit(commands.Cog):
    """Gather info and posts from many places on reddit"""

    def __init__(self, client, reddit):
        self.client = client
        self.reddit = reddit

    reddit = praw.Reddit(client_id=reddit_client_id,
                         client_secret=reddit_client_secret,
                         username=reddit_username,
                         password=reddit_password,
                         user_agent=reddit_user_agent)

    @commands.Cog.listener()
    async def on_ready(self):
        print('Reddit module is ready')

    @commands.command(aliases=['rs'])
    async def redditstats(self, ctx, user):
        """Gather the reddit stats for a user"""
        thing = discord.Embed(title='Loading...', color=0x5643fd,
                              description='Please stand by this process should be over shortly',
                              timestamp=ctx.message.created_at)
        thing.set_image(url='https://i.pinimg.com/originals/b2/28/13/b228138ca189b63989d295492e8a8b16.gif')
        thing.set_footer(text=f'Requested by {ctx.message.author}', icon_url=ctx.message.author.avatar_url)
        message = await ctx.send(embed=thing)
        redditor = self.reddit.redditor(user)
        ts = int(redditor.created_utc)
        name = redditor.name
        try:
            embed = discord.Embed(color=0x5643fd, timestamp=ctx.message.created_at,
                                  title=f'Reddit Info  -  u/{redditor.name}', url=f'https://reddit.com/user/{name}/')
            embed.set_thumbnail(url=redditor.icon_img)
            embed.set_footer(text=f'Requested by {ctx.message.author}', icon_url=ctx.message.author.avatar_url)

            embed.add_field(name='Total Karma', value=f"{redditor.link_karma + redditor.comment_karma:,}", inline=True)
            embed.add_field(name='Link Karma', value=f"{redditor.link_karma:,}", inline=False)
            embed.add_field(name='Comment Karma', value=f"{redditor.comment_karma:,}", inline=False)
            embed.add_field(name='Account Created', inline=False, value='{}'.format(
                datetime.datetime.fromtimestamp(ts).strftime('%B %d, %Y')))

            await message.edit(embed=embed)
        except Exeption:
            embed = discord.Embed(title='Error', color=0xFF0000, description='That redditor could not be found.')
            embed.set_footer(text=f'Error occurred at {ctx.message.created_at}', icon_url=ctx.message.author.avatar_url)
            await ctx.send(embed=embed)

    @commands.command(aliases=['ms'])
    async def modstats(self, ctx, user):
        """Gather the mod stats for a user"""
        thing = discord.Embed(title='Loading...', color=0x5643fd,
                              description='Please stand by this process should be over shortly',
                              timestamp=ctx.message.created_at)
        thing.set_image(url='https://i.pinimg.com/originals/b2/28/13/b228138ca189b63989d295492e8a8b16.gif')
        thing.set_footer(text=f'Requested by {ctx.message.author}', icon_url=ctx.message.author.avatar_url)
        message = await ctx.send(embed=thing)
        reddits = []
        numbas = []
        modstats = []
        user = self.reddit.redditor(user)
        try:
            async with aiohttp.ClientSession() as cs:
                async with cs.get(f"https://www.reddit.com/user/{user}/moderated_subreddits/.json") as r:
                    res = await r.json()
                subreddits = res['data']
                for subreddit in subreddits:
                    reddits.append(
                        f"[{subreddit['sr_display_name_prefixed']}](https://reddit.com{subreddit['url']}) • "
                        f"<:member:716339965771907099> **{subreddit['subscribers']:,}**")
                    numbas.append(subreddit['subscribers'])
                if len(reddits) > 10:
                    rs = reddits[:10]
                else:
                    rs = reddits

                for index, sr in enumerate(rs, 1):
                    modstats.append(f"{index}. {sr}")

                final_ms = "\n".join(modstats)
                embed = discord.Embed(color=0x5643fd,
                                      timestamp=ctx.message.created_at, title=f'Mod Stats for u/{user}',
                                      url=f'https://reddit.com/user/{user}')
                embed.set_thumbnail(url=user.icon_img)
                embed.set_footer(text=f'Requested by {ctx.message.author}', icon_url=ctx.message.author.avatar_url)
                embed.add_field(name='Sub Count', value=len(subreddits), inline=True)
                embed.add_field(name='Total Subscribers', value=humanize.intcomma(sum(numbas)), inline=True)
                embed.add_field(name="Avg. Subsribers per Sub",
                                value=f"{humanize.intcomma(round(sum(numbas) / len(numbas)))}", inline=True)
                embed.add_field(name='Top Subreddits', value=final_ms, inline=False)
            await message.edit(embed=embed)
        except Exception as error:
            embed = discord.Embed(title=
                                  "Moderator not found, try again with a valid username.", color=0xFF0000,
                                  description=error)
            await ctx.send(embed=embed)

    @commands.command()
    async def meme(self, ctx):
        """Grab a meme from reddit's dankest subreddit"""
        thing = discord.Embed(title='Loading...', color=0x5643fd,
                              description='One dank meme coming right up',
                              timestamp=ctx.message.created_at)
        thing.set_image(url='https://i.pinimg.com/originals/b2/28/13/b228138ca189b63989d295492e8a8b16.gif')
        thing.set_footer(text=f'Requested by {ctx.message.author}', icon_url=ctx.message.author.avatar_url)
        message = await ctx.send(embed=thing)
        posts = []
        for submission in self.reddit.subreddit('dankmemes').top('day', limit=100):
            if not submission.stickied:
                posts.append(submission)
        submission = random.choice(posts)
        embed = discord.Embed(title=submission.title, color=0x5643fd, timestamp=ctx.message.created_at)
        embed.set_author(name=f'u/{submission.author}', icon_url=submission.author.icon_img)
        embed.set_image(url=submission.url)
        embed.set_footer(text='r/dankmemes', icon_url='https://images-ext-1.discordapp.net/external/RBgvzfKtRRBs51Gj'
                                                      'dfLcuQhU6kjF_ycIzTW8LVXvsJg/https/b.thumbs.redditmedia.com/qLE'
                                                      '6RUF_ARSgCZ854L5Hq4iKd1GqzuW2A5k6xf2kEFs.png')

        embed.add_field(name='Score', value=f'<:upvote:718895913342337036> {submission.score}')
        embed.add_field(name='Comments', value=f'💬 {submission.num_comments}')

        await message.edit(embed=embed)

    @commands.command(aliases=['ask'])
    async def askreddit(self, ctx):
        """Get a random askreddit thread with a comment"""
        embedd = discord.Embed(
            colour=0x5643fd, title="Loading...", timestamp=ctx.message.created_at
        )
        embedd.set_footer(text=f'Requested by {ctx.message.author}', icon_url=ctx.message.author.avatar_url)
        embedd.set_image(
            url='https://i.pinimg.com/originals/b2/28/13/b228138ca189b63989d295492e8a8b16.gif')
        message = await ctx.send(embed=embedd)
        try:
            posts = []
            comments = []
            for submission in self.reddit.subreddit("AskReddit").top('day', limit=15):
                posts.append(submission)
            final_post = random.choice(posts)
            if final_post.is_self:
                embed = discord.Embed(title=final_post.title,
                                      description=final_post.selftext + f"\n<:upvote:718895913342337036> "
                                                                        f"**{final_post.score}**     "
                                                                        f"**💬 {final_post.num_comments}**",
                                      colour=0x5643fd, timestamp=ctx.message.created_at)
                embed.set_author(name=final_post.author, icon_url=final_post.author.icon_img)
                for top_level_comment in final_post.comments:
                    comments.append(top_level_comment)
                final_comment = random.choice(comments)
                embed.add_field(
                    name=f"{final_comment.author} | <:upvote:718895913342337036> **{final_comment.score:,}**   **"
                         f"💬 {len(final_comment.replies):,}**",
                    value=final_comment.body)
                embed.set_footer(text=f'Requested by {ctx.message.author}', icon_url=ctx.message.author.avatar_url)
                await message.edit(embed=embed)
        except Exception as error:
            embed = discord.Embed(title='Error Occurred', color=0xFF0000, description=error)
            await ctx.send(embed=embed) if not final_post.over_18 or final_comment.over_18 and ctx.channel.is_nsfw() \
                else await ctx.send(
                f"⚠️:underage: **{ctx.author.mention}**, NSFW channel required!")

    @commands.command()
    async def post(self, ctx, subreddit, sort='hot'):
        """Get a random post from anywhere on reddit"""
        try:
            embedd = discord.Embed(
                colour=0x5643fd, title="Loading...", timestamp=ctx.message.created_at
            )
            embedd.set_footer(text=f'Requested by {ctx.message.author}', icon_url=ctx.message.author.avatar_url)
            embedd.set_image(
                url='https://i.pinimg.com/originals/b2/28/13/b228138ca189b63989d295492e8a8b16.gif')
            message = await ctx.send(embed=embedd)
            reddit = self.reddit.subreddit(subreddit)
            sorts = ['new', 'controversial', 'rising', 'top', 'topever', 'hot', 'controversialever']
            reddits = [reddit.new(limit=50), reddit.controversial(limit=50), reddit.rising(limit=50),
                       reddit.top(limit=150), reddit.top(limit=1), reddit.hot(limit=80), reddit.controversial(limit=1)]
            if sort in sorts:
                posts = [x for x in reddits[sorts.index(sort)] if not x.stickied]
            else:
                return await ctx.send(
                    f"⚠️**{ctx.author.mention}**, that isn't a valid sort! Valid sorts include {', '.join(sorts)}.")
            submission = random.choice(posts)
            if submission.is_self:
                embed = discord.Embed(title=submission.title,
                                      colour=0x5643fd,
                                      description=submission.selftext, timestamp=ctx.message.created_at)
            else:
                embed = discord.Embed(title=submission.title,
                                      colour=0x5643fd,
                                      timestamp=ctx.message.created_at)
                embed.set_image(url=submission.url)

            embed.set_author(name=f"u/{submission.author.name}", icon_url=submission.author.icon_img)
            embed.set_footer(text=f'r/{submission.subreddit}',
                             icon_url=submission.subreddit.icon_img)
            embed.add_field(name='Score', value=f'<:upvote:718895913342337036> {submission.score}')
            embed.add_field(name='Comments', value=f'💬 {submission.num_comments}')
            await message.edit(
                embed=embed) if not submission.over_18 or submission.over_18 and ctx.channel.is_nsfw() \
                else await ctx.send(
                f"⚠️:underage: **{ctx.author.mention}**, NSFW channel required!")
        except Exception as e:
            embed = discord.Embed(title=Error, description=e, color=0xFF0000, timestamp=ctx.message.created_at)
            await ctx.send(embed=embed)

    @commands.command()
    @commands.is_owner()
    async def modq(self, ctx, sub):
        """This isn't for you to use"""
        posts = []
        commentt = []
        embedd = discord.Embed(
            colour=0x5643fd, title="Counting items in the modqueue...", timestamp=ctx.message.created_at)
        embedd.set_footer(text=f'Requested by {ctx.message.author}', icon_url=ctx.message.author.avatar_url)
        embedd.set_image(
            url='https://i.pinimg.com/originals/b2/28/13/b228138ca189b63989d295492e8a8b16.gif')
        message = await ctx.send(embed=embedd)
        for post in self.reddit.subreddit(sub).mod.modqueue(limit=None, only="submissions"):
            posts.append(post)
        for comment in self.reddit.subreddit(sub).mod.modqueue(limit=None, only="comments"):
            commentt.append(comment)
        total_count = len(posts) + len(commentt)
        embed = discord.Embed(title=f'r/{sub} modqueue', color=0x5643fd, timestamp=ctx.message.created_at,
                              description=f'I found ``{total_count}`` total items in the r/{sub} modqueue.')
        embed.add_field(name='Posts', value=len(posts), inline=True)
        embed.add_field(name='Comments', value=len(commentt), inline=True)
        embedd.set_footer(text=f'Requested by {ctx.message.author}', icon_url=ctx.message.author.avatar_url)
        await message.edit(embed=embed)

    @commands.command()
    async def aww(self, ctx):
        """Bleach your eyes with the cute side of reddit"""
        thing = discord.Embed(title='Loading...', color=0x5643fd,
                              description='Grabbing post',
                              timestamp=ctx.message.created_at)
        thing.set_image(url='https://i.pinimg.com/originals/b2/28/13/b228138ca189b63989d295492e8a8b16.gif')
        thing.set_footer(text=f'Requested by {ctx.message.author}', icon_url=ctx.message.author.avatar_url)
        message = await ctx.send(embed=thing)
        posts = []
        for submission in self.reddit.subreddit('eyebleach').hot(limit=100):
            if not submission.stickied:
                posts.append(submission)
        submission = random.choice(posts)
        embed = discord.Embed(title=submission.title, color=0x5643fd, timestamp=ctx.message.created_at)
        embed.set_author(name=f'u/{submission.author}', icon_url=submission.author.icon_img)
        embed.set_image(url=submission.url)

        embed.add_field(name='Score', value=f'<:upvote:718895913342337036> {submission.score}')
        embed.add_field(name='Comments', value=f'💬 {submission.num_comments}')

        await message.edit(embed=embed)


def setup(client):
    client.add_cog(Reddit(client, reddit=praw.Reddit(client_id=reddit_client_id,
                                                     client_secret=reddit_client_secret,
                                                     username=reddit_username,
                                                     password=reddit_password,
                                                     user_agent=reddit_user_agent
                                                     )))
