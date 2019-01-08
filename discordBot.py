import discord

class BlotBot(discord.Client):
    def __init__(self, dispatchMsg, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dispatchMsg = dispatchMsg

    async def on_ready(self):
        channel = discord.utils.get(self.get_all_channels(), name='general')
        await channel.send(self.dispatchMsg)
        await self.close()