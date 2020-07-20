import discord
import asyncio
import json
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()

with open('AutoExStaff/guilds.json') as json_file:
    guilds = json.load(json_file)

# Logging startup
@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

    for guild in client.guilds:
        print(f'{client.user} is in {guild}')

        # New guild setup
        if guild.name not in guilds:
            print(f'Adding {guild} to guilds')

            # Number of staff roles
            try:
                numStaffRoles = int(input('Number of staff roles:'))
            except:
                print('Please input an integer')
                numStaffRoles = int(input('Number of staff roles:'))

            # Number of retired roles
            try:
                numRetiredRoles = int(input('Number of retired roles:'))
            except:
                print('Please input an integer')
                numRetiredRoles = int(input('Number of retired roles:'))
                
            staffRoles = []
            retiredRoles = []

            # Staff role name input
            for i in range(numStaffRoles):
                try:
                    staffRoles.append(input(f'Staff role {i+1} name: '))
                except:
                    print('strs only')
                    staffRoles.append(input(f'Staff role {i+1} name: '))
            
            # Retired role name input
            for i in range(numRetiredRoles):
                try:
                    retiredRoles.append(input(f'Retired role {i+1} name: '))
                except:
                    print('strs only')
                    retiredRoles.append(input(f'Retired role {i+1} name: '))

            # Add to dictionary
            guilds[guild.name] = {
                'staffRoles' : staffRoles,
                'retiredRoles' : retiredRoles,
                'staff' : [],
                'retired' : []
            }

            # Save to JSON
            with open('AutoExStaff/guilds.json', 'w') as outfile:
                json.dump(guilds, outfile, indent=4)

            # Not necessary, but make it look cooler
            for i in range(3):
                print('...')

            print('done')

# Message processing
@client.event
async def on_message(message):
    if message.author == client.user:
        return

    # Retire command
    if message.content == '^retire':
        wasStaffRole = None
        hasRetiredRole = None
        for role in message.author.roles:
            if str(role) in guilds[message.guild.name]['staffRoles']:
                wasStaffRole = True
                await message.author.remove_roles(role, reason='retire')

            if str(role) in guilds[message.guild.name]['retiredRoles']: hasRetiredRole = True

        if wasStaffRole and not hasRetiredRole:
            for retiredRoleName in guilds[message.guild.name]['retiredRoles']:
                retireRole = discord.utils.get(message.guild.roles, name=retiredRoleName)
                await message.author.add_roles(retireRole, reason='retire')

@client.event
async def on_member_update(before, after):
    if before.roles != after.roles:
        isStaff = False
        isRetired = False
        for roleName in guilds[after.guild.name]['staffRoles']:
            if discord.utils.get(after.roles, name=roleName) != None:
                isStaff = True
        for roleName in guilds[after.guild.name]['retiredRoles']:
            if discord.utils.get(after.roles, name=roleName) != None:
                isRetired = True

        # Add to list
        if after.id not in guilds[after.guild.name]['staff'] and isStaff: guilds[after.guild.name]['staff'].append(after.id)
        if after.id not in guilds[after.guild.name]['retired'] and isRetired: guilds[after.guild.name]['retired'].append(after.id)

        # Remove from list
        if after.id in guilds[after.guild.name]['staff'] and not isStaff: guilds[after.guild.name]['staff'].remove(after.id)
        if after.id in guilds[after.guild.name]['retired'] and not isRetired: guilds[after.guild.name]['retired'].remove(after.id)

        # Save to file
        with open('AutoExStaff/guilds.json', 'w') as outfile:
            json.dump(guilds, outfile, indent=4)

client.run(TOKEN)

with open('AutoExStaff/guilds.json', 'w') as outfile:
    json.dump(guilds, outfile, indent=4)