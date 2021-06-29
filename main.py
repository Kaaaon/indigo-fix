# original by gowixx i just removed all the unnecessary shit cuz his worked for roughly 10% of people
# the code here is pretty trash i just wanted to make it as simple as possible cuz gowixx always overcomplicates stuff
# dont let this be a reflection on me as a dev lol i hate python
import base64
import ctypes
import discord
import discum
import json
import os
import time
from colorama import Fore
from discord.ext import commands

config = json.load(open('config.json'))
token = config.get('Discord Token')
prefix = config.get('Command Prefix')

embed_color = 0x3964c3

client = commands.Bot(command_prefix=prefix, case_insensitive=True, self_bot=True, help_command=None)


def printmain():
    os.system('cls; clear')
    logo = f'''{Fore.LIGHTCYAN_EX}
    ██╗███╗   ██╗██████╗ ██╗ ██████╗  ██████╗ 
    ██║████╗  ██║██╔══██╗██║██╔════╝ ██╔═══██╗
    ██║██╔██╗ ██║██║  ██║██║██║  ███╗██║   ██║
    ██║██║╚██╗██║██║  ██║██║██║   ██║██║   ██║
    ██║██║ ╚████║██████╔╝██║╚██████╔╝╚██████╔╝
    ╚═╝╚═╝  ╚═══╝╚═════╝ ╚═╝ ╚═════╝  ╚═════╝'''
    for line in logo.split('\n'):
        print(line.center(100))
    print(f'''
    {Fore.LIGHTBLUE_EX}Account: {Fore.RESET}{client.user}
    {Fore.LIGHTBLUE_EX}Status: {Fore.LIGHTGREEN_EX}Connected
    {Fore.BLUE}{'_' * 100}
        ''')


def changetitle(title):
    if os.name == "nt":
        try:
            ctypes.windll.kernel32.SetConsoleTitleW(title)
        except:
            print("\33]0;" + title)


@client.event
async def on_connect():
    os.system('cls')
    printmain()
    changetitle('Indigo | Developed by Gowixx | Kaon Patch')


@client.command(name='help', description='Show help menu', usage='')
async def help(ctx):
    embed = discord.Embed(
        title='Help',
        description=f'''
        Arguments in `[]` are required, arguments in `()` are optional.

        **`{prefix}`massmention(amount)** » Mention lots of users in a guild
        **`{prefix}`whattimeisit (amount)** » Alias for Mass mention''',
        color=embed_color
    )
    await ctx.message.edit(content='', embed=embed)


@client.command(name="massmention", description="Ghost mention every user in the guild that can see the channel",
                usage="", aliases=['WhatTimeIsIt, massping'])
@commands.guild_only()
async def massmention(ctx, amount: int = 1):
    try:
        await ctx.message.delete()
    except:
        pass
    print(f'\n{Fore.LIGHTBLUE_EX}[Indigo] {Fore.RESET}Starting to Scrape members')
    discum_client = discum.Client(token=token, log=True)
    message = ""
    discum_client.gateway.fetchMembers(str(ctx.guild.id), str(ctx.channel.id))

    @discum_client.gateway.command
    def massmentiondef(this_is_needed_dont_remove):
        if discum_client.gateway.finishedMemberFetching(str(ctx.guild.id)):
            discum_client.gateway.removeCommand(massmentiondef)
            discum_client.gateway.close()

    discum_client.gateway.run()
    # Create a list so that you send the messages faster and ping the most people
    tosend = []
    for memberID in discum_client.gateway.session.guild(str(ctx.guild.id)).members:
        print(f'{Fore.LIGHTBLUE_EX}[Indigo] {Fore.RESET}Fetched user {Fore.LIGHTBLUE_EX}{memberID}')
        if len(message) < 1950:
            message += f"<@!{str(memberID)}>ඞ"
        else:
            tosend.append(message)
            message = ""
    tosend.append(message)
    # Send all the messages and instantly delete them
    for i in range(amount):
        for item in tosend:
            print(f'\n{Fore.LIGHTBLUE_EX}[Indigo] {Fore.RESET}Sending new message with more pings')
            m = await ctx.send(item)
            print(f'{Fore.LIGHTBLUE_EX}[Indigo] {Fore.RESET}Sent new message with more pings')
            try:
                print(f'{Fore.LIGHTBLUE_EX}[Indigo] {Fore.RESET}Deleting message')
                # Would use delete_after but this looks better
                await m.delete()
                print(f'{Fore.LIGHTBLUE_EX}[Indigo] {Fore.RESET}Deleted message')
            except:
                print(f'{Fore.LIGHTBLUE_EX}[Indigo] {Fore.RESET}Failed to delete message')
    # Ask who pinged you and delete the message instantly to look like you're innocent and make it unsnipable
    whopinged = await ctx.send("who pinged me")
    # had to it this way as delete_after doesnt work well with time.sleep
    await whopinged.delete()
    print(f'{Fore.LIGHTBLUE_EX}[Indigo] {Fore.RESET}Done :)')
    print(f'{Fore.LIGHTBLUE_EX}[Indigo] {Fore.RESET}Clearing in 5s')
    time.sleep(5)
    os.system('cls')
    printmain()


try:
    client.run(token, bot=False)
except Exception as e:
    print("Invalid token or smth fucked up when logging in")
    print(e)
