def is_bot_dev(ctx):
    guild = ctx.bot.get_guild(852094131047104593)
    dev_role = guild.get_role(852094131231522819)
    return ctx.author.id in ctx.bot.owner_ids or dev_role in ctx.author.roles


def is_premium(ctx):
    guild = ctx.bot.get_guild(852094131047104593)
    premium_role = guild.get_role(852094131233890816)
    return premium_role in ctx.author.roles
