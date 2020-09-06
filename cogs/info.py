import discord

from discord.ext import commands


class Info(commands.Cog):
    """Gain some info on users or servers"""

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Info module is ready')

    @commands.command(aliases=["av"])
    async def avatar(self, ctx, *, member: discord.Member = None):
        """See the profile picture for a user"""
        member = member or ctx.message.author
        embed = discord.Embed(
            color=0x5643fd, title=f"Here is {member}'s avatar")
        url = str(member.avatar_url).replace(".webp", ".png")
        embed.set_image(url=url)
        await ctx.send(embed=embed)

    @commands.command(aliases=['ui'])
    async def userinfo(self, ctx, member: discord.Member = None):
        """See info on a member in the server"""
        status_list = {
            "online": "<:online:726127263401246832> -  Online",
            "offline": "<:offline:726127263203983440> -  Offline",
            "idle": "<:idle:726127192165187594> -  Idle",
            "dnd": "<:dnd:726127192001478746> -  Do not disturb"}
        member = member or ctx.message.author
        roles = [role for role in member.roles]
        embed = discord.Embed(color=0x5643fd, timestamp=ctx.message.created_at)
        embed.set_author(name=f'User Info  -  {member}')
        embed.set_thumbnail(url=member.avatar_url)
        embed.set_footer(text=f'Requested by {ctx.message.author}', icon_url=ctx.message.author.avatar_url)

        embed.add_field(name='ID', value=member.id, inline=False)

        embed.add_field(name='Account Created', value=member.created_at.strftime('%a, %B %d %Y, %I:%M %p UTC'),
                        inline=False)

        embed.add_field(name='Joined Server', value=member.joined_at.strftime('%a, %B %d %Y, %I:%M %p UTC'),
                        inline=False)

        embed.add_field(name='Status', value=status_list[str(member.status)], inline=False)

        embed.add_field(name=f"Top Roles ({len(roles)} total)",
                        value=" ".join([role.mention for role in roles[::-1][:5]]), inline=False)

        await ctx.send(embed=embed)

    @commands.command(aliases=['si'], usage='')
    @commands.guild_only()
    async def serverinfo(self, ctx, *, guild_id: int = None):
        """Get info on a server"""

        if guild_id is not None and await self.client.is_owner(ctx.author):
            guild = self.client.get_guild(guild_id)
            if guild is None:
                return await ctx.send(f'Invalid Guild ID given.')
        else:
            guild = ctx.guild

        roles = [role for role in guild.roles]

        class Secret:
            pass

        secret_member = Secret()
        secret_member.id = 0
        secret_member.roles = [guild.default_role]

        e = discord.Embed(title=f'Server Info  -  {guild.name}', color=0x5643fd, timestamp=ctx.message.created_at)
        e.add_field(name='ID', value=guild.id, inline=False)
        e.add_field(name='Owner', value=guild.owner.mention, inline=False)
        if guild.icon:
            e.set_thumbnail(url=guild.icon_url)
        e.add_field(name='Roles', value=
        ', '.join([role.mention for role in roles[::-1][:10]]) if len(roles) < 10 else len(roles))
        e.add_field(name='Members', value=guild.member_count,
                    inline=False)
        e.add_field(name='Server Created', inline=False, value=guild.created_at.strftime('%a, %B %d %Y, %I:%M %p UTC'))
        e.set_footer(text=f'Requested by {ctx.message.author}', icon_url=ctx.message.author.avatar_url)
        await ctx.send(embed=e)

    @commands.command(aliases=['ab'])
    async def about(self, ctx):
        """Get basic information about NOVA"""
        pre = ctx.prefix
        guild = ctx.guild
        embed = discord.Embed(title='About NOVA', color=0x5643fd, timestamp=ctx.message.created_at,
                              description=f'My prefix for {guild.name} is ``{pre}``\nDo ``'
                                          f'{pre}help`` for a list of commands')
        embed.set_footer(text=f'Requested by {ctx.message.author}', icon_url=ctx.message.author.avatar_url)
        embed.set_thumbnail(url='https://cdn.discordapp.com/avatars/709922850953494598/f78ed19924e8c95abc30f406d47670d7'
                                '.png?size=1024')
        embed.set_author(name='Developed by YeetVegetabales#5313',
                         icon_url='https://cdn.discordapp.com/avatars/5693744'
                                  '29218603019/a_b6d992c79036b86d1ac49f27093b'
                                  'c813.gif?size=1024')
        embed.add_field(inline=False, name='Info',
                        value='NOVA is a general purpose discord bot that has tools to help you better moderate your '
                              'server as well as have a little fun')
        embed.add_field(name='Stats',
                        value=f'**•** ``{len(self.client.guilds)}`` servers with ``{len(self.client.users)}``'
                              f' total users',
                        inline=False)
        embed.add_field(name='Commands', value=f'**•** ``{len(self.client.commands)}`` commands with '
                                               f'``{len(self.client.cogs)}`` cogs', inline=False)
        embed.add_field(name='Other', value='<:news:730866149109137520> [Discord Server](https://discord.gg/Uqh9NXY)\n'
                                            '<:news:730866149109137520> [Invite Link](https://discor'
                                            'd.com/api/oauth2/authorize?client_id=709922850953494598&permissions=470150'
                                            '214&scope=bot)', inline=True)
        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Info(client))
