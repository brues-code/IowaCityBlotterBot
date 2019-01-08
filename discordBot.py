import discord

class BlotBot(discord.Client):
    def __init__(self, key, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.key = key
        self.dispatchMsg = ""

    async def on_ready(self):
        channel = discord.utils.get(self.get_all_channels(), name='general')
        await channel.send(self.dispatchMsg)
        await self.logout()

    def sendMessage(self, dispatchMsg):
        self.dispatchMsg = dispatchMsg
        self.login(self.key)