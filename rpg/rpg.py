# Future Imports
from __future__ import annotations

# Standard Library Imports
import datetime
import random

# Dependency Imports
from discord.ext import tasks
from redbot.core import commands, Config
from redbot.core.i18n import cog_i18n, Translator
import discord

# Music Imports
from .checks import is_bot_dev
from .utils.functions import DropdownView
from .utils.guildmanager import GuildManager as gm
from .utils.playerdata import PlayerData as pd
from .utils.rpgutils import RPGUtils

_ = Translator("RPG", __file__)


@cog_i18n(_)
class RPG(commands.Cog):
    """Explore dungeons, join clans, make friends and have lots of fun!"""

    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=815153881217892372)
        default_global = {
            "guilds": {},
            "shop": {"items": {}},
            "adventures": {"ongoing": {}, "completed": {}},
        }
        default_user = {
            "registered": False,
            "username": None,
            "next_adventure": 0,
            "current_adventure": {
                "level": None,
                "finish": 0,
                "status": "idle",
                "ended": {},
            },
            "guild": None,
            # "health": 100,
            # "mana": 50,
            "_class": None,
            "rebirths": None,
            "level": {
                "current": 0,
                "xp": 0,
            },
            "equipment": {"equipped": {}, "backpack": {}},
            "stats": {
                "strength": 1,
                "dexterity": 1,
                "magic": 1,
                "intelligence": 1,
                "wisdom": 1,
                "charisma": 1,
            },
        }
        self.config.register_global(**default_global)
        self.config.register_user(**default_user)

    @tasks.loop(seconds=300)
    async def adventure_ender(self):
        """
        End adventure if its their time.
        """
        async with self.config.adventures.ongoing() as ongoing:
            for adv in ongoing:
                if int(adv["finish"]) <= datetime.now():
                    await RPGUtils.end_adventure(adv)

    @commands.command(name="stats")
    @commands.guild_only()
    async def _stats(self, ctx, *, user: discord.Member = None):
        """View your or another member's stats."""
        if user is None:
            user = ctx.author
        if user.bot:
            return await ctx.send(_("Bots don't have stats."))
        await pd.get_profile(self, ctx, user)

    @commands.group(name="charactermanage", aliases=["cmanage", "charmanage"])
    @commands.guild_only()
    async def _charactermanage(self, ctx):
        """Manage your character."""
        pass

    @_charactermanage.command(name="create")
    @commands.cooldown(1, 86400, commands.BucketType.user)
    @commands.guild_only()
    async def _charactermanage_create(self, ctx, name: str = None):
        """Create a character."""
        if name is None:
            name = ctx.author.name
        user = ctx.author
        await pd.create_character(self, ctx, name, user)

    @_charactermanage.command(name="delete")
    @commands.guild_only()
    @commands.cooldown(1, 172800, commands.BucketType.user)
    async def _charactermanage_delete(self, ctx):
        """
        Delete your character.

        **NOTE: THIS ACTION IS IRREVERSIBLE**
        """
        user = ctx.author

        await pd.delete_character(self, ctx, user)

    @commands.group(name="rpgdev", aliases=["adev"])
    @commands.check(is_bot_dev)
    async def _rpgdev(self, ctx):
        """
        Manage the rpg cog.

        This command is only available to bot developers.
        """
        pass

    @_rpgdev.group(name="charactermanage", aliases=["cmanage"])
    async def _rpgdev_cmanage(self, ctx):
        """
        Manage a user's characters.

        This command is only available to bot developers.
        """
        pass

    @_rpgdev_cmanage.command(name="updatestats")
    async def _rpgdev_cmanage_updatestats(self, ctx, user: discord.Member):
        """
        Update a user's stats.

        This command is only available to bot developers.
        """
        view = DropdownView()
        await ctx.send(
            _(
                "What would you like to edit in {}'s stats?"
                ).format(
                    user.mention
                ),
                view=view,
        )

    @commands.group(name="guild")
    @commands.guild_only()
    async def _guild(self, ctx):
        """
        Guild management commands.
        """
        pass

    @_guild.group(name="set")
    @commands.guild_only()
    async def _guild_set(self, ctx):
        pass

    @_guild_set.command(name="create")
    @commands.guild_only()
    async def _guild_create(self, ctx):
        """
        Create a guild.
        """
        author = ctx.author
        await gm.create_guild(self, ctx, author)

    @_guild_set.command(name="delete")
    @commands.guild_only()
    async def _guild_delete(self, ctx):
        """
        Delete your guild.
        """
        author = ctx.author
        await gm.delete_guild(self, ctx, author)

    @_guild_set.command(name="name")
    @commands.guild_only()
    @commands.cooldown(1, 1800, commands.BucketType.user)
    async def _guild_set_name(self, ctx, *, new_name: str):
        """
        Set the guild's name.
        """
        author = ctx.author
        await gm.set_guild_data(self, ctx, author, "guild_name", new_name)

    @_guild_set.command(name="motto")
    @commands.guild_only()
    @commands.cooldown(1, 1800, commands.BucketType.user)
    async def _guild_set_motto(self, ctx, *, new_motto: str):
        """
        Set the guild's motto.
        """
        author = ctx.author
        await gm.set_guild_data(self, ctx, author, "guild_motto", new_motto)

    @_guild_set.command(name="description")
    @commands.guild_only()
    @commands.cooldown(1, 1800, commands.BucketType.user)
    async def _guild_set_description(self, ctx, *, new_description: str):
        """
        Set the guild's description.
        """
        author = ctx.author
        await gm.set_guild_data(
            self, ctx, author, "guild_description", new_description
        )

    @_guild_set.command(name="icon")
    @commands.guild_only()
    @commands.cooldown(1, 1800, commands.BucketType.user)
    async def _guild_set_icon(self, ctx, *, new_icon: str):
        """
        Set the guild's icon.
        """
        author = ctx.author
        await gm.set_guild_data(self, ctx, author, "guild_icon", new_icon)

    @_guild_set.command(name="banner")
    @commands.guild_only()
    @commands.cooldown(1, 1800, commands.BucketType.user)
    async def _guild_set_banner(self, ctx, *, new_banner: str):
        """
        Set the guild's banner.
        """
        author = ctx.author
        await gm.set_guild_data(self, ctx, author, "guild_banner", new_banner)

    @_guild_set.command(name="taxrate", aliases=["tax"])
    @commands.guild_only()
    @commands.cooldown(1, 1800, commands.BucketType.user)
    async def _guild_set_taxrate(self, ctx, *, new_taxrate: int):
        """
        Set the guild's tax rate.
        """
        author = ctx.author
        await gm.set_guild_data(
            self, ctx, author, "guild_taxrate", new_taxrate
        )

    #### ACTUAL ADVENTURE SHIT ####

    @commands.group(name="adventure", aliases=["explore", "dungeon"])
    @commands.guild_only()
    async def _adventure(self, ctx, difficulty: int):
        """
        `<difficulty>` - a whole number from 1 to 30
        Send your character on an adventure with the difficulty `<difficulty>`.
        The adventure will take `<difficulty>` hours if no time booster is used, and half as long if a time booster is used.
        Booster' time will be reduced by 5%
        Be sure to check `{prefix}status` to check how much time is left, or to check if you survived or died.
        """
        author = ctx.author
        await RPGUtils.rpg_start(self, ctx, author, difficulty)


async def setup(bot):
    bot.add_cog(RPG(bot))
