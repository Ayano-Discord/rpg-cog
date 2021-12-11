# Future Imports
from __future__ import annotations

# Dependency Imports
from redbot.core.utils.predicates import MessagePredicate
import discord


class Dropdown(discord.ui.Select):
    def __init__(self):

        # Set the options that will be presented inside the dropdown
        options = [
            discord.SelectOption(
                label="Level", description="Edit the users rpg level"
            ),
            discord.SelectOption(
                label="Health", description="Edit the users max health"
            ),
            discord.SelectOption(
                label="Mana", description="Edit the users max mana"
            ),
            discord.SelectOption(
                label="Finished", description="Finished editing"
            ),
        ]

        # The placeholder is what will be shown when no option is chosen
        # The min and max values indicate we can only pick one of the three options
        # The options parameter defines the dropdown options. We defined this above
        super().__init__(
            placeholder="Edit the user's stats",
            min_values=1,
            max_values=1,
            options=options,
        )

    async def callback(self, interaction: discord.Interaction):
        if interaction.data["values"] == "Level":
            await interaction.message.edit(
                "What level do you want to set the user to?"
            )
            pred = MessagePredicate.valid_int(self.ctx)
            await self.bot.wait_for("message", check=pred)
            if pred.result is True:
                await self.config.user(self.ctx.author).level.set(pred.result)
                await self.ctx.send("Level set!")
            else:
                await self.ctx.send("Invalid input!")

        elif interaction.data["values"] == "Health":
            await interaction.response.edit_message(
                "What is the users new max health?"
            )
            pred = MessagePredicate.valid_int(self.ctx)
            await self.bot.wait_for("message", check=pred)
            if pred.result is True:
                await self.config.user(self.ctx.author).health.set(pred.result)
                await self.ctx.send("Health set!")
            else:
                await self.ctx.send("Invalid input!")

        elif interaction.data["values"] == "Mana":
            await interaction.message.edit("What is the users new max mana?")
            pred = MessagePredicate.valid_int(self.ctx)
            await self.bot.wait_for("message", check=pred)
            if pred.result is True:
                await self.config.user(self.ctx.author).mana.set(pred.result)
                await self.ctx.send("Mana set!")
            else:
                await self.ctx.send("Invalid input!")

        elif interaction.data["values"] == "Finished":
            await interaction.message.edit("Finished editing!")
            await self.ctx.send("Finished editing!")
            return


class DropdownView(discord.ui.View):
    def __init__(self):
        super().__init__()

        # Adds the dropdown to our view object.
        self.add_item(Dropdown())
