import json
import requests
from discord.ext import commands
from pydactyl import PterodactylClient

"""

i know i could have made this code much more optimized with function parameters but eh

if you want to add them yourself, make a pull request :D

"""

with open('config.json') as configfile:
    configdata = json.load(configfile)

BOT = commands.Bot(command_prefix='$$')
panel_client = PterodactylClient(configdata["server_address"], configdata["ptero_api_key"])
server_id = configdata["ptero_server_id"]


class ServerError:
    """There was a server error during a power action"""
    pass


class PterodactylDiscordBot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.has_permissions(administrator=True)
    @commands.command
    async def httperrorresponse(ctx):
        await ctx.send(embed=discord.Embed(
            description='There was a server error while processing that power action, please try again later',
            color=0xb51818
        ))
        raise ServerError


    @commands.has_permissions(administrator=True)
    @commands.command
    async def start(self, ctx):
        try:
            response = panel_client.client.send_power_action(server_id, 'start')
            if response.status_code == 204:
                await ctx.send(embed=discord.Embed(
                    description=f"Starting the server {ctx.author.mention}, please wait while it starts!",
                    color=0x842899
                ))
            else:
                pass
        except requests.exceptions.HTTPError:
            httperrorresponse()

    @commands.has_permissions(administrator=True)
    @commands.command
    async def stop(self, ctx):
        try:
            response = panel_client.client.send_power_action(server_id, 'stop')
            if response.status_code == 204:
                await ctx.send(embed=discord.Embed(
                    description="Stopping the server, hope you had a great time!"
                ))
            else:
                pass
        except requests.exceptions.HTTPError:
            httperrorresponse()


    @commands.has_permissions(administrator=True)
    @commands.command
    async def restart(self, ctx):
        try:
            response = panel_client.client.send_power_action(server_id, 'restart')
            if response.status_code == 204:
                await ctx.send(embed=discord.Embed(
                    description="Restarting the server, give it a minute!"
                ))
            else:
                pass
        except requests.exceptions.HTTPError:
            httperrorresponse()
    
    @commands.command
    async def serverstatus(self, ctx):
        try:
            response = panel_client.client.get_server_utilization(server_id)
            if response['state'] == 'on':
                await ctx.send(embed=discord.Embed(
                    description='The server\'s online, get on there!'
                ))
            elif response['state'] == 'off':
                await ctx.send(embed=discord.Embed(
                    description='The server\'s offline, start it using `$$start`!'
                ))
            else:
                await ctx.send(embed=discord.Embed(
                    description='The server is either in the middle of a power action, or its not responding'
                ))
        except requests.exceptions.HTTPError:
            httperrorresponse()


def setup(bot):
    bot.add_cog(PterodactylClient(bot))
