# Future Imports
from __future__ import annotations

# Dependency Imports
from redbot.core.utils.predicates import MessagePredicate
import discord

# from ..rpg import _


class PlayerData:
    async def check_user(self, ctx, user: discord.Member):
        """
        Check if a user is registered in our rpg database. We use the member object and not an

        Arguments:
            user: {discord.Member} -- The user to check. This arguement is optional and will default to the author of the command if a user is not specified

        Example:
            await check_user(self, ctx)

        The user arguement is optional and it will default to the author is it is not provided.

        If you wish to check the regisstration of a specific user, you can use the user arguement.

        Example:
            await check_user(self, ctx, {user_object})
        """
        # if user is None:
        #     user = ctx.author
        if await self.config.user(user).registered():
            return True
        else:
            return False

    # async def get_stat(self, ctx, stat: str):
    #     """
    #     Get a stat's data.

    #     Example:
    #         await get_stat(self, ctx, stat="strength") or await get_stat(self, ctx, "strength")

    #     """
    #     if await check_user(self, ctx) is not True:
    #         return await ctx.send(
    #             "You need to be registered to use this command.\n\nRegister with `{}cmanage create`".format(
    #                 ctx.prefix
    #             )
    #         )

    #     if stat.lower() == "strength":
    #         await self.config.user(ctx.author).stats.strength()
    #     elif stat.lower() == "dexterity":
    #         await self.config.user(ctx.author).stats.dexterity()
    #     elif stat.lower() == "magic":
    #         await self.config.user(ctx.author).stats.magic()
    #     elif stat.lower() == "intelligence":
    #         await self.config.user(ctx.author).stats.intelligence()
    #     elif stat.lower() == "wisdom":
    #         await self.config.user(ctx.author).stats.wisdom()
    #     elif stat.lower() == "charisma":
    #         await self.config.user(ctx.author).stats.charisma()
    #     elif stat.lower() == "health":
    #         await self.config.user(ctx.author).health()
    #     elif stat.lower() == "mana":
    #         await self.config.user(ctx.author).mana()
    #     elif stat.lower() == "level":
    #         await self.config.user(ctx.author).level()
    #     else:
    #         return await ctx.send("Invalid stat.")

    async def get_profile(self, ctx, user: discord.Member):
        """Get a user's profile."""
        # if user is None:
        #     user = ctx.author
        if await PlayerData.check_user(self, ctx, user) is not True:
            if user.id == ctx.author.id:
                return await ctx.send(
                    "You are not registered. Please register an account with `{}cmanage create`.".format(
                        ctx.prefix
                    )
                )
            else:
                return await ctx.send(
                    "{} is not registered. Please ask them to register an account with `{}cmanage create` and then try again.".format(
                        user.name, ctx.prefix
                    )
                )
        level = await self.config.user(user).level.current()
        guild = await self.config.user(user).guild()
        # health = await self.config.user(user).health()
        # mana = await self.config.user(user).mana()
        _class = await self.config.user(user)._class()
        sstrength = await self.config.user(user).stats.strength()
        sdexterity = await self.config.user(user).stats.dexterity()
        smagic = await self.config.user(user).stats.magic()
        sintelligence = await self.config.user(user).stats.intelligence()
        swisdom = await self.config.user(user).stats.wisdom()
        scharisma = await self.config.user(user).stats.charisma()
        username = await self.config.user(user).username()
        exp = await self.config.user(user).level.exp()
        embed = discord.Embed(
            title="{} ({})'s Profile".format(username, user.name),
            color=await ctx.embed_color(),
        )
        embed.add_field(name="Guild", value=guild)
        embed.add_field(
            name="Level Info", value="Level: {} | XP: {}".format(level, exp)
        )
        # embed.add_field(name="Health", value=health)
        # embed.add_field(name="Mana", value=mana)
        embed.add_field(name="Class", value=_class)
        embed.add_field(name="Strength", value=sstrength)
        embed.add_field(name="Dexterity", value=sdexterity)
        embed.add_field(name="Magic", value=smagic)
        embed.add_field(name="Intelligence", value=sintelligence)
        embed.add_field(name="Wisdom", value=swisdom)
        embed.add_field(name="Charisma", value=scharisma)
        await ctx.send(embed=embed)

    async def create_character(self, ctx, name: str, user: discord.Member):
        """Create a character."""
        if await PlayerData.check_user(self, ctx, user) is True:
            return await ctx.send(_("You already have a character!"))
        await self.config.user(ctx.author).username.set(name)
        await self.config.user(ctx.author).registered.set(True)
        # await self.config.user(ctx.author).level.set(0)
        # await self.config.user(ctx.author).guild.set(None)
        # await self.config.user(ctx.author).health.set(random.randint(50, 200))
        # await self.config.user(ctx.author).mana.set(random.randint(0, 100))
        # await self.config.user(ctx.author)._class.set(None)
        # await self.config.user(ctx.author).stats.strength.set(random.randint(1, 10))
        # await self.config.user(ctx.author).stats.dexterity.set(random.randint(1, 10))
        # await self.config.user(ctx.author).stats.magic.set(random.randint(1, 10))
        # await self.config.user(ctx.author).stats.intelligence.set(random.randint(1, 10))
        # await self.config.user(ctx.author).stats.wisdom.set(random.randint(1, 10))
        # await self.config.user(ctx.author).stats.charisma.set(random.randint(1, 10))
        await ctx.send("Character created!")

    async def delete_character(self, ctx, user: discord.Member):
        """Delete a character."""
        if await PlayerData.check_user(self, ctx, user) is not True:
            return await ctx.send("You don't have a character!")
        await ctx.send(
            "Are you sure you want to delete your character? (y/n)\n\n**NOTE: THIS ACTION IS IRREVERSIBLE**"
        )
        pred = MessagePredicate.yes_or_no(ctx)
        await self.bot.wait_for("message", check=pred)
        if pred.result is True:
            await self.config.user(ctx.author).clear()
            await ctx.send("Character deleted!")
        else:
            await ctx.send("Ok, cancelling...")
