# Future Imports
from __future__ import annotations

# Standard Library Imports
import asyncio
import os
import random
import re

# Dependency Imports
from PIL import Image
import discord

# Music Imports
from .playerdata import PlayerData

url_regex = re.compile(
    r"^(?:http|ftp)s?://"  # http:// or https://
    r"(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|"  # domain...
    r"localhost|"  # localhost...
    r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"  # ...or ip
    r"(?::\d+)?"  # optional port
    r"(?:/?|[/?]\S+)$",
    re.IGNORECASE,
)


class GuildManager:
    async def create_guild(self, ctx, owner):
        """
        Create a guild, this is the first step to creating a guild.
        """

        if await PlayerData.check_user(self, ctx, owner) is not True:
            return await ctx.send("You don't have a character!")

        async with self.config.guilds() as guilds:
            if guilds == str(ctx.author.id):
                return await ctx.send("You already own a guild!")

        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        rgb = (r, g, b)

        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        await ctx.send("What do you want to name your guild?")
        try:
            guild_name = await self.bot.wait_for(
                "message", check=check, timeout=30.0
            )
        except asyncio.TimeoutError:
            return await ctx.send(
                "You took too long to respond! Cancelling..."
            )
        if guild_name.content == "None":
            return await ctx.send(
                "Your guild game cant be `None` stupid! Cancelling..."
            )
        if len(guild_name.content) < 3:
            return await ctx.send(
                "Your guild name must be at least 4 characters long!"
            )
        if len(guild_name.content) > 20:
            return await ctx.send(
                "Your guild name must be less than 20 characters long!"
            )
        async with self.config.guilds() as my_guilds:
            for guild in my_guilds:
                if guild["guild_name"] == guild_name.content:
                    return await ctx.send("That guild name is already taken!")

        await ctx.send("What will be your guild motto?")
        try:
            guild_motto = await self.bot.wait_for(
                "message", check=check, timeout=30.0
            )
        except asyncio.TimeoutError:
            return await ctx.send(
                "You took too long to respond! Cancelling..."
            )
        if guild_motto.content == "None":
            await ctx.send(
                "Your guild motto cant be `None` stupid! Cancelling..."
            )
        if len(guild_motto.content) < 3:
            return await ctx.send(
                "Your guild motto must be at least 4 characters long!"
            )
        if len(guild_motto.content) > 50:
            return await ctx.send(
                "Your guild motto must be less than 50 characters long!"
            )

        await ctx.send("What will be your long guild description?")
        try:
            guild_long_desc = await self.bot.wait_for(
                "message", check=check, timeout=30.0
            )
        except asyncio.TimeoutError:
            return await ctx.send(
                "You took too long to respond! Cancelling..."
            )
        if guild_long_desc.content == "None":
            await ctx.send(
                "Your long guild description cant be `None` stupid! Cancelling..."
            )
        if len(guild_long_desc.content) < 3:
            return await ctx.send(
                "Your long guild description must be at least 4 characters long!"
            )
        if len(guild_long_desc.content) > 200:
            return await ctx.send(
                "Your long guild description must be less than 200 characters long!"
            )

        await ctx.send("What will be your short guild description?")
        try:
            guild_short_desc = await self.bot.wait_for(
                "message", check=check, timeout=30.0
            )
        except asyncio.TimeoutError:
            return await ctx.send(
                "You took too long to respond! Cancelling..."
            )
        if guild_short_desc.content == "None":
            await ctx.send(
                "Your short guild description cant be `None` stupid! Cancelling..."
            )
        if len(guild_short_desc.content) < 3:
            return await ctx.send(
                "Your short guild description must be at least 4 characters long!"
            )
        if len(guild_short_desc.content) > 50:
            return await ctx.send(
                "Your short guild description must be less than 50 characters long!"
            )

        await ctx.send("What will be your guild icon?")
        try:
            guild_icon = await self.bot.wait_for(
                "message", check=check, timeout=30.0
            )
        except asyncio.TimeoutError:
            return await ctx.send(
                "You took too long to respond! Cancelling..."
            )
        if guild_icon.content == "None":
            img = Image.new("RGB", (300, 200), rgb)
            # img.close()
            img.save(
                f"/home/ubuntu/mine/rpg/data/{guild_name.content}_icon.png"
            )
            data_guild = self.bot.get_guild(852094131047104593)
            data_channel = data_guild.get_channel(916972251411259402)
            data_msg = await data_channel.send(
                file=discord.File(
                    "/home/ubuntu/mine/rpg/data/{}_icon.png".format(
                        guild_name.content
                    )
                )
            )
            guild_icon_url = data_msg.attachments[0].url
            # await asyncio.sleep(5)
            os.remove(
                "/home/ubuntu/mine/rpg/data/{}_icon.png".format(
                    guild_name.content
                )
            )
        else:
            if re.match(url_regex, guild_icon.content) is not None:
                guild_icon_url = guild_icon.content
            else:
                return await ctx.send(
                    "That is not a valid url! *Cancelling...*"
                )

        await ctx.send("What will be your guild banner?")
        try:
            guild_banner = await self.bot.wait_for(
                "message", check=check, timeout=30.0
            )
        except asyncio.TimeoutError:
            return await ctx.send(
                "You took too long to respond! Cancelling..."
            )
        if guild_banner.content == "None":
            img = Image.new("RGB", (600, 300), rgb)
            img.save(
                f"/home/ubuntu/mine/rpg/data/{guild_name.content}_banner.png"
            )
            data_guild = self.bot.get_guild(852094131047104593)
            data_channel = data_guild.get_channel(916972251411259402)
            data_msg = await data_channel.send(
                file=discord.File(
                    "/home/ubuntu/mine/rpg/data/{}_banner.png".format(
                        guild_name.content
                    )
                )
            )
            guild_banner_url = data_msg.attachments[0].url
            os.remove(
                "/home/ubuntu/mine/rpg/data/{}_banner.png".format(
                    guild_name.content
                )
            )
        else:
            if re.match(url_regex, guild_banner.content) is not None:
                guild_banner_url = guild_banner.content
            else:
                return await ctx.send("That is not a valid url!")

        await ctx.send(
            (
                "I have collected all the data to make a basic guild, more customizations can be made through `[p]guild set <setting>`."
                "\n\nPlease now confirm your guild data:\n"
                "Guid Name: {}\n"
                "Motto: {}\n"
                "Long Description: {}\n"
                "Short Description: {}\n"
                "Icon: {}\n"
                "Banner: {}\n"
                "Tax Rate: {} (This is default and can be customozied through `[p]guild set`"
                "Are you sure you want to create this guild? (y/n)\n\n**NOTE: THIS ACTION IS IRREVERSIBLE**"
            ).format(
                guild_name.content,
                guild_motto.content,
                guild_long_desc.content,
                guild_short_desc.content,
                guild_icon_url,
                guild_banner_url,
                1,
            )
        )
        try:
            guild_confirm = await self.bot.wait_for(
                "message", check=check, timeout=20.0
            )
        except asyncio.TimeoutError:
            return await ctx.send(
                "You took too long to respond! Cancelling..."
            )
        if guild_confirm.content in [
            "y",
            "Y",
            "yes",
            "Yes",
            "YES",
            "True",
            "true",
        ]:
            async with self.config.guilds() as my_guilds:
                my_guilds[str(ctx.author.id)] = {
                    "guild_name": guild_name.content,
                    "guild_owner": ctx.author.id,
                    "guild_members": [ctx.author.id],
                    "guild_motto": guild_motto.content,
                    "guild_long_desc": guild_long_desc.content,
                    "guild_short_desc": guild_short_desc.content,
                    "guild_icon": guild_icon.content,
                    "guild_banner": guild_banner.content,
                    "guild_level": 1,
                    "guild_tax_rate": 1,
                    "guild_funds": 0,
                }
                await self.config.user(ctx.author).guild.set(
                    guild_name.content
                )
            await ctx.send("Guild created!")
        else:
            await ctx.send("Cancelled!")

    async def check_guild_ownership(self, ctx, user):
        user_data = await self.config.user(user).guild()
        if user_data is None:
            return await ctx.send("Your not in a guild!")

        guild_data = await self.config.guilds()
        if guild_data[str(ctx.author.id)]["guild_owner"] == user.id:
            return True
        else:
            return False

    async def delete_guild(self, ctx, user: discord.Member):
        if await PlayerData.check_user(self, ctx, user) is False:
            return await ctx.send(
                "You are not registered, please register with `[p]create`"
            )

        if await GuildManager.check_guild_ownership(self, ctx, user) is False:
            return await ctx.send("You do not own a guild!")

        else:
            guild_data = await self.config.guilds()
            user_guild = self.config.user(user).guild()
            await ctx.send("Are you sure you want to delete your guild? (y/n)")

            def check(m):
                return m.author == ctx.author and m.channel == ctx.channel

            try:
                guild_confirm = await self.bot.wait_for(
                    "message", check=check, timeout=20.0
                )
            except asyncio.TimeoutError:
                return await ctx.send(
                    "You took too long to respond! Cancelling..."
                )
            if guild_confirm.content in [
                "y",
                "Y",
                "yes",
                "Yes",
                "YES",
                "True",
                "true",
            ]:
                async with self.config.guilds() as my_guilds:
                    del my_guilds[str(user.id)]
                # await self.config.user(user).guild.clear()
                await ctx.send("Guild deleted!")
                # del guild_data[str(ctx.author.id)]
                # await ctx.send("Guild deleted!")
                await self.config.user(user).guild.set(None)
            else:
                await ctx.send("Cancelled!")

    async def set_guild_data(
        self, ctx, user: discord.Member, setting: str, value
    ):
        """
        We can set new guild data using this.
        """
        if await GuildManager.check_guild_ownership(self, ctx, user) is False:
            return await ctx.send("You do not own a guild!")

        if setting == "guild_name":
            return await ctx.send(
                "Sorry, but you can't change the guild name."
            )

        if setting == "guild_motto":
            guild_data = await self.config.guilds()
            guild_data[str(user.id)]["guild_motto"] = value
            await ctx.send("Guild motto updated!")

        if setting == "guild_long_desc":
            guild_data = await self.config.guilds()
            guild_data[str(user.id)]["guild_long_desc"] = value
            await ctx.send("Guild long description updated!")

        if setting == "guild_short_desc":
            guild_data = await self.config.guilds()
            guild_data[str(user.id)]["guild_short_desc"] = value
            await ctx.send("Guild short description updated!")

        if setting == "guild_icon":
            guild_data = await self.config.guilds()
            guild_data[str(user.id)]["guild_icon"] = value
            await ctx.send("Guild icon updated!")

        if setting == "guild_banner":
            guild_data = await self.config.guilds()
            guild_data[str(user.id)]["guild_banner"] = value
            await ctx.send("Guild banner updated!")

        if setting == "guild_tax_rate":
            guild_data = await self.config.guilds()
            guild_data[str(user.id)]["guild_tax_rate"] = value
            await ctx.send("Guild tax rate updated!")
