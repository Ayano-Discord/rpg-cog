# Future Imports
from __future__ import annotations

# Standard Library Imports
from datetime import datetime, timedelta
from decimal import Decimal
import random

# Dependency Imports
import discord

# Music Imports
from ..checks import is_premium
from .playerdata import PlayerData

ADVENTURE_NAMES = {
    1: "Spider Cave",
    2: "Troll Bridge",
    3: "A Night Alone Outside",
    4: "Ogre Raid",
    5: "Proof Of Confidence",
    6: "Dragon Canyon",
    7: "Orc Tower",
    8: "Seamonster's Temple",
    9: "Dark Wizard's Castle",
    10: "Slay The Famous Dragon Arzagor",
    11: "Search For Excalibur",
    12: "Find Atlantis",
    13: "Tame A Phoenix",
    14: "Slay The Death Reaper",
    15: "Meet Adrian In Real Life",
    16: "The League Of Vecca",
    17: "The Gem Expedition",
    18: "Gambling Problems?",
    19: "The Necromancer Of Kord",
    20: "Last One Standing",
    21: "Gambling Problems? Again?",
    22: "Insomnia",
    23: "Illuminated",
    24: "Betrayal",
    25: "IdleRPG",
    26: "Learn Programming",
    27: "Scylla's Temple",
    28: "Trial Of Osiris",
    29: "Meet The War God In Hell",
    30: "Divine Intervention",
}


levels = {
    1: 0,
    2: 1500,
    3: 9000,
    4: 22500,
    5: 42000,
    6: 67500,
    7: 99000,
    8: 136500,
    9: 180000,
    10: 229500,
    11: 285000,
    12: 346500,
    13: 414000,
    14: 487500,
    15: 567000,
    16: 697410,
    17: 857814,
    18: 1055112,
    19: 1297787,
    20: 1596278,
    21: 1931497,
    22: 2298481,
    23: 2689223,
    24: 3092606,
    25: 3494645,
    26: 3879056,
    27: 4228171,
    28: 4608707,
    29: 5023490,
    30: 5475604,
}


def xptolevel(xp):
    for level, point in levels.items():
        if xp == point:
            return level
        elif xp < point:
            return level - 1
    return 30


def xptonextlevel(xp):
    level = xptolevel(xp)
    if level == 30:
        return "Infinity"
    else:
        nextxp = levels[level + 1]
        return f"{nextxp - xp}"


def calcchance(
    sword,
    shield,
    dungeon,
    level,
    luck,
    returnsuccess=False,
    booster=False,
    bonus=0,
):
    if returnsuccess is False:
        val1 = sword + shield + 75 - dungeon * 7 + bonus - level / Decimal("2")
        val2 = sword + shield + 75 - dungeon + bonus + level
        val1 = round(val1 * luck) if val1 >= 0 else round(val1 / luck)
        val2 = round(val2 * luck) if val2 >= 0 else round(val2 / luck)
        if booster:
            val1 += 25
            val2 += 25
        return (val1, val2)
    else:
        randomn = random.randint(0, 100)
        if booster:
            randomn -= 25
        success = (
            sword
            + shield
            + 75
            - (dungeon * (random.randint(1, 7)))
            + random.choice([level, -level / Decimal("2")])
            + bonus
        )
        if success >= 0:
            success = round(success * luck)
        else:
            success = round(success / luck)
        return randomn <= success


class RPGUtils:
    async def rpg_start(self, ctx, user: discord.Member, difficulty: int):
        """Start the rpg."""
        if await PlayerData.check_user(self, ctx, user) is not True:
            try:
                return await ctx.author.send(
                    "You don't have a character, get started with {}cmanage create".format(
                        ctx.prefix
                    )
                )
            except discord.Forbidden:
                return await ctx.send(
                    "You don't have a character, get started with {}cmanage create".format(
                        ctx.prefix
                    )
                )
        if self.config.user(user).current_adventure.status == "active":
            return await ctx.send(
                "You are already on an adventure. Use `{}status` to see how long it lasts.".format(
                    ctx.prefix
                )
            )
        if difficulty > xptolevel(self.config.user(user).level.exp()):
            return await ctx.send(
                "You must be on level **{level}** to do this adventure."
            ).format(level=difficulty)
        time = timedelta(hours=difficulty)
        if is_premium():
            time = time * 0.95

        await ctx.send(
            "Successfully sent your character out on an adventure. Use"
            " `{prefix}status` to see the current status of the mission.".format(
                prefix=ctx.prefix
            )
        )
        await self.config.user(user).current_adventure.level.set(difficulty)
        finish_time = datetime.now() + time
        await self.config.user(user).current_adventure.time.set(
            datetime.timestamp(finish_time)
        )
        await self.config.user(user).current_adventure.status.set("active")
        async with self.config.adventure.ongoing() as ongoing:
            ongoing[str(user.id)] = {
                "user": user,
                "difficulty": difficulty,
                "finish_time": finish_time,
            }

    async def rpg_status(self, ctx, user: discord.Member):
        """Check the status of the rpg."""
        if await PlayerData.check_user(self, ctx, user) is not True:
            try:
                return await ctx.author.send(
                    "You don't have a character, get started with {}cmanage create".format(
                        ctx.prefix
                    )
                )
            except discord.Forbidden:
                return await ctx.send(
                    "You don't have a character, get started with {}cmanage create".format(
                        ctx.prefix
                    )
                )

    async def rpg_end(self, ctx, user: discord.Member):
        """End the rpg."""
        if await PlayerData.check_user(self, ctx, user) is not True:
            try:
                return await ctx.author.send(
                    "You don't have a character, get started with {}cmanage create".format(
                        ctx.prefix
                    )
                )
            except discord.Forbidden:
                return await ctx.send(
                    "You don't have a character, get started with {}cmanage create".format(
                        ctx.prefix
                    )
                )
        if not self.config.user(user).current_adventure.status == "active":
            return await ctx.send(
                "You are not currently on an adventure. Use `{}adventure` to start one.".format(
                    ctx.prefix
                )
            )

        async with self.config.user(user).current_adventure.ended() as adv:
            adv["reward"]
