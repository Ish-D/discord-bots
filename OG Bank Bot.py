from discord.ext import commands, tasks
import discord
import requests,json,asyncio
import random,math
import matplotlib.pyplot as plt
import gspread, re
from oauth2client.service_account import ServiceAccountCredentials

task = discord.ext.tasks
bot = commands.Bot(command_prefix='!', description='', case_insensitive=True)
bot.remove_command('help')

scope = ['https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('Griffith Pierce Banking-59c60c5719ea.json', scope)
client = gspread.authorize(creds)
sheet = client.open("Griffith Pierce Banking Co. Public").sheet1
deposits = client.open("Griffith Pierce Checking Accounts").sheet1
codes = client.open("Griffith Pierce Banking Co. - Document of Ownership").sheet1


@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))
    await fluc.start()

    #await bot.change_presence(status=discord.Status.online)

'''
@bot.command()
async def displayembed(ctx):
    embed = discord.Embed(
        title='Title',
        description='Description',
        colour=discord.Colour.blue()
    )

    embed.set_footer(text = 'Footer')
    embed.set_image(url='https://crafatar.com/renders/body/56ae9d68-fe21-47c9-a0bc-9edbc3687f4b.png')
    embed.set_thumbnail(url='https://crafatar.com/renders/body/56ae9d68-fe21-47c9-a0bc-9edbc3687f4b.png')
    embed.set_author(name='Author Name', icon_url='https://crafatar.com/renders/body/56ae9d68-fe21-47c9-a0bc-9edbc3687f4b.png')
    embed.add_field(name='Field Name', value='Field Value', inline=False)
    embed.add_field(name='Field Name', value='Field Value', inline=True)
    embed.add_field(name='Field Name', value='Field Value', inline=True)

    await ctx.send(embed=embed)


@bot.command()
async def player(ctx, name: str):
    response = requests.get('https://api.mojang.com/users/profiles/minecraft/' + name)
    if (response.status_code == 200):
        str = json.loads(response.text)

        embed = discord.Embed(
            title=str['name'],
            description=str['id'],
            colour=discord.Colour.orange()
        )
        embed.set_footer(text='Griffith Pierce Banking Co.')
        embed.set_thumbnail(url='https://crafatar.com/avatars/' + str['id'] + '.png')
        embed.set_image(url='https://crafatar.com/renders/body/' + str['id'] + '.png')

        await ctx.send(embed=embed)
    else:
        await ctx.send('Please enter a valid player name.')
'''

realePrice = 7
graph = []
plt.axes(xlabel='Time (Hours)', ylabel='Price (Diamonds)', title='Reale Price Over Time')

@tasks.loop(seconds=3600)
async def fluc():
    global realePrice

    diff = random.normalvariate(0, 1)
    if (diff > 0):
        diff = math.floor(diff)
    else:
        diff = math.ceil(diff)

    realePrice += diff

    if (realePrice < 4):
        realePrice = 4
    elif (realePrice > 27):
        realePrice = 27

    graph.append(realePrice)

    channel = bot.get_channel(721488958214897695)
    embed = discord.Embed(
        title='Reale',
        description='The current value of a Reale is ' + str(realePrice) + ' diamonds.',
        colour=discord.Colour.orange()
    )
    embed.set_thumbnail(url='https://vignette.wikia.nocookie.net/minecraft/images/7/7c/Honeycomb.png/revision/latest?cb=20190823083553.png')
    embed.set_footer(text='Griffith Pierce Banking Co.')
    #await channel.send(embed=embed)
    await bot.get_user(169248301143687168).send(embed = embed)
    await bot.get_user(282741403363049477).send(embed = embed)

        #await asyncio.sleep(3600)

'''

@bot.command()
async def forceupdate(ctx):
    await fluc()

@bot.command()
async def pricegraph(ctx):
    plt.plot(graph)
    plt.savefig('graph')
    await ctx.send(file=discord.File('graph.png'))
'''

@bot.command()
async def reale(ctx):
    global realePrice
    embed = discord.Embed(
        title='Reale',
        description='The current value of a Reale is ' + str(realePrice) + ' diamonds.',
        colour=discord.Colour.orange()
    )
    embed.set_thumbnail(url='https://vignette.wikia.nocookie.net/minecraft/images/7/7c/Honeycomb.png/revision/latest?cb=20190823083553.png')
    embed.set_footer(text='Griffith Pierce Banking Co.')
    await ctx.author.send(embed=embed)

bankers = ['169248301143687168', "282741403363049477", "576221715936313354", "525440100407181322", "378666989188677652"]

@bot.command()
async def sell(ctx):
    global realePrice
    for id in bankers:
        await bot.get_user(int(id)).send(str(ctx.author.name) + " (" + str(ctx.author) + ') wants to sell at ' + str(realePrice) + ' diamonds.')
    await ctx.send("Your request has been recieved. Please confirm the details of the transaction with a banker on the server when available.")


@bot.command()
async def buy(ctx):
    global realePrice
    for id in bankers:
        await bot.get_user(int(id)).send(str(ctx.author.name) + " (" + str(ctx.author) + ') wants to buy at ' + str(realePrice) + ' diamonds.')
    await ctx.send("Your request has been recieved. Please confirm the details of the transaction with a banker on the server when available.")


@bot.command()
async def closetransaction(ctx, name :str):
    for id in bankers:
        await bot.get_user(int(id)).send(str(ctx.author) + " has closed the transaction with " + name)

@bot.command()
async def help(ctx):
    global realePrice
    embed = discord.Embed(
        title='Griffith Pierce Banking Company',
        #description='Description',
        colour=discord.Colour.orange()
    )

    embed.set_footer(text='Griffith Pierce Banking Co.')
    embed.set_thumbnail(url='https://i.imgur.com/tsFCe0z.png')
    embed.add_field(name='**About Us**', value='Welcome to Griffith Pierce Banking Company. Griffith Pierce is an investment bank and financial services company based in Brightsville. Here, you can purchase, trade, and sell our exclusive Reales. Our interactive Griffith Pierce Banking Bot will display the current value of the Reale every hour.', inline=False)
    embed.add_field(name='**Reale**', value='You may be wondering, what is a Reale? Reale is a new currency, represented by a honeycomb in game. Each and every Reale has its own unique code to ensure the safety of your diamonds. '
                                            'Reale are redeemable at well-known establishments such as Stav Industries. The price of reale will randomly fluctuate once every hour.'
                                            ' Reales are limited to 100 units and an individual may buy at most 10 per day. \n The current price of a reale is  **' + str(realePrice) + '** diamonds.' , inline=False)
    embed.add_field(name='**Commands**', value='**!reale** Allows you to see the current value of the reale at any time.'
                                           '\n **!buy** Allows you to request the purchase of Reale at the current price.'
                                           '\n **!sell** Allows you to request the sale of Reale at the current price.'
                                           '\n **!help** Brings up this menu.'
                                           '\n **!ign** **<Discord Tag>** Allows you to see the in-game name of another user. Ex: !ign Username#0000'
                                           '\n **!tag** **<In Game Name>** Allows you to see the discord tag of another user. Ex: !tag Username'
                                           '\n **!transfer <Discord Tag> <Reale ID>** Allows you to transfer Reales to another user. Ex: !transfer Username#0000 0000'
                                           '\n **!confirm** Confirms the transfer of reales to another user.'
                                           '\n **!cancel** Cancels the tranfer of reales to another user.', inline=False)
    embed.add_field(name = '**Other Services**', value='Griffith Pierce also offers a currency exchange service.\n **Selling Rate**:'
                                                       '\n32 Gold: 12 Emerald: 8 Iron: 1 Dia '
                                                       '\n**Buying Rate:**'
                                                       '\n40 Gold: 16 Emerald: 10 Iron: 1 Dia.')

    await ctx.author.send(embed=embed)

@bot.command()
async def helpadmin(ctx):
    if str(ctx.author.id) in bankers:
        embed = discord.Embed(
            title='Griffith Pierce Banking Company',
            # description='Description',
            colour=discord.Colour.orange()
        )

        embed.set_footer(text='Griffith Pierce Banking Co.')
        embed.set_thumbnail(url='https://i.imgur.com/tsFCe0z.png')
        embed.add_field(name='**Administrator**',
                        value='As an administrator/banker, your job is to ensure that the bank\'s customers have the best possible experience.',
                        inline=False)
        embed.add_field(name='**Admin Commands**',
                        value='**!register <IGN> <Discord Tag> <Discord ID>** Registers a player into our system, allowing them  to use the Bot\'s commands.'
                              '\n **!admin <Discord ID>** Allows another user to use admin commands.'
                              '\n **!closetransaction <name>** Notifies the other bankers that a transaction with a certain person has been closed.'
                              '\n **!pricegraph** Displays a graph of the Reale price.'
                              '\n **!helpadmin** Brings up this embed.', inline=False)

        await ctx.author.send(embed=embed)
    else:
        await ctx.author.send("You do not have permission to use this command.")

@bot.command()
async def register(ctx, name: str, tag: str, id: str):

    if str(ctx.author.id) in bankers:
        response = requests.get('https://api.mojang.com/users/profiles/minecraft/' + name)

        if (response.status_code == 200):
            data = json.loads(response.text)

            try:
                sheet.find(str(data['name']))
                await ctx.author.send('There is already someone by this name registered.')
            except gspread.exceptions.CellNotFound:
                try:
                    sheet.find(str(tag))
                    await ctx.author.send('You have already signed up using this discord account.')
                except gspread.exceptions.CellNotFound:
                    str_list = list(filter(None, sheet.col_values(1)))
                    sheet.update_cell(len(str_list) + 1, 1, str(data['name']))
                    sheet.update_cell(len(str_list) + 1, 2, str(tag))
                    sheet.update_cell(len(str_list) + 1, 3, str(id))
                    sheet.update_cell(len(str_list) + 1, 4, '0')

                    await ctx.author.send('You have successfully registered ' + name +".")

                    global realePrice
                    embed = discord.Embed(
                        title='Griffith Pierce Banking Company',
                        # description='Description',
                        colour=discord.Colour.orange()
                    )

                    embed.set_footer(text='Griffith Pierce Banking Co.')
                    embed.set_thumbnail(url='https://i.imgur.com/tsFCe0z.png')
                    embed.add_field(name='**About Us**',
                                    value='Welcome to Griffith Pierce Banking Company. Griffith Pierce is an investment bank and financial services company based in Brightsville. Here, you can purchase, trade, and sell our exclusive Reales. Our interactive Griffith Pierce Banking Bot will display the current value of the Reale every hour.',
                                    inline=False)
                    embed.add_field(name='**Reale**',
                                    value='You may be wondering, what is a Reale? Reale is a new currency, represented by a honeycomb in game. Each and every Reale has its own unique code to ensure the safety of your diamonds. '
                                          'Reale are redeemable at well-known establishments such as Stav Industries. The price of reale will randomly fluctuate once every hour.'
                                          ' Reales are limited to 100 units and an individual may buy at most 10 per day. \n The current price of a reale is  **' + str(
                                        realePrice) + '** diamonds.', inline=False)
                    embed.add_field(name='**Commands**',
                                    value='**!reale** Allows you to see the current value of the reale at any time.'
                                          '\n **!buy** Allows you to request the purchase of Reale at the current price.'
                                          '\n **!sell** Allows you to request the sale of Reale at the current price.'
                                          '\n **!help** Brings up this menu.'
                                          '\n **!ign** **<Discord Tag>** Allows you to see the in-game name of another user. Ex: !ign Username#0000'
                                          '\n **!tag** **<In Game Name>** Allows you to see the discord tag of another user. Ex: !tag Username'
                                          '\n **!transfer <Discord Tag> <Reale ID>** Allows you to transfer Reales to another user. Ex: !transfer Username#0000 0000'
                                          '\n **!confirm** Confirms the transfer of reales to another user.'
                                          '\n **!cancel** Cancels the tranfer of reales to another user.', inline=False)
                    embed.add_field(name='**Other Services**',
                                    value='Griffith Pierce also offers a currency exchange service.\n **Selling Rate**:'
                                          '\n32 Gold: 12 Emerald: 8 Iron: 1 Dia '
                                          '\n**Buying Rate:**'
                                          '\n40 Gold: 16 Emerald: 10 Iron: 1 Dia.')

                    await bot.get_user(int(id)).send(embed=embed)

        else:
            await ctx.author.send('Please enter a valid name.')
    else:
        await ctx.author.send("You do not have permission to use this command.")


senders = ['']
recievers = ['']
idlist = ['']


@bot.command()
async def transfer(ctx, name: str, id: int):
    global senders
    global recievers
    global idlist

    if str(ctx.author) in senders:
        await ctx.author.send('You already have a pending transfer.')
    else:
        try:
            sheet.find(str(ctx.author))
            nameNew = re.compile("^" + name + "$", re.IGNORECASE)
            try:
                sheet.find(nameNew)
                try:
                    codes.find(str(id))

                    codecell = codes.find(str(id))

                    try:
                        if (codes.row_values(codecell.row)[1] == str(ctx.author)):
                            cell = sheet.find(nameNew)
                            cell2 = sheet.find(str(ctx.author))
                            if (str(sheet.row_values(cell.row)[2]) == str(ctx.author)):
                                await ctx.send('You must enter a valid transfer recipient.')
                            else:
                                if (int(sheet.row_values(cell2.row)[3]) >= 1):
                                    await ctx.author.send('Are you sure you would like to transfer Reale#' + str(id) + ' to ' + name + '?')
                                    await ctx.author.send('To proceed, type !confirm. To cancel the transfer, type !cancel')
                                    senders.append(str(ctx.author))
                                    recievers.append(int(sheet.row_values(cell.row)[2]))
                                    idlist.append(id)
                                else:
                                    await ctx.send('You do not have enough reales.')
                        else:
                            await ctx.send('You do not own this reale.')
                    except IndexError:
                        await ctx.send("You do not own this reale.")
                except gspread.exceptions.CellNotFound:
                    await ctx.send("Please enter a valid Reale ID.")
            except gspread.exceptions.CellNotFound:
                await ctx.send(name + ' is not registered.')
        except gspread.exceptions.CellNotFound:
            await ctx.send('You must first register.')

senderConf = False

@bot.command()
async def confirm(ctx):

    global senders
    global recievers
    global idlist

    if str(ctx.author) in senders:

        authorIndex = senders.index(str(ctx.author))
        cell = sheet.find(str(recievers[authorIndex]))
        cell2 = sheet.find(senders[authorIndex])
        coderow = codes.find(str(idlist[authorIndex]))

        sheet.update_cell(cell.row, cell.col + 1, int(sheet.row_values(cell.row)[3]) + 1)
        sheet.update_cell(cell2.row, cell2.col + 2, int(sheet.row_values(cell2.row)[3]) - 1)
        codes.update_cell(coderow.row, coderow.col + 1, sheet.row_values(cell.row)[1])

        await ctx.send('Trade confirmed.')
        await bot.get_user(int(sheet.row_values(cell.row)[2])).send(senders[authorIndex] + ' has transferred Reale#' + str(idlist[authorIndex]) + ' to you.')

        senders.remove(str(ctx.author))
        recievers.remove(recievers[authorIndex])
        idlist.remove(idlist[authorIndex])
    else:
        await ctx.author.send('You do not have any pending transfers.')


@bot.command()
async def cancel(ctx):
    global senders
    global recievers
    global transferAmount

    if str(ctx.author) in senders:
        transferAmount.remove(transferAmount[senders.index(str(ctx.author))])
        recievers.remove(recievers[senders.index(str(ctx.author))])
        senders.remove(str(ctx.author))
        await ctx.author.send('Transfer cancelled.')
    else:
        await ctx.author.send('You do not have any pending transfers.')


@bot.command()
async def ign(ctx, name :str):
    try:
        cell = sheet.find(name)
        await ctx.author.send(name + "'s in game name is " + str(sheet.row_values(cell.row)[0]))
    except gspread.exceptions.CellNotFound:
        await ctx.author.send('The player must first be registered.')

@bot.command()
async def tag(ctx, name :str):
    try:
        cell = sheet.find(name)
        await ctx.author.send(name + "'s discord tag is " + str(sheet.row_values(cell.row)[1]))
    except gspread.exceptions.CellNotFound:
        await ctx.author.send('The player must first be registered.')

@bot.command()
async def admin(ctx, id :str):
    if str(ctx.author.id) in bankers:
        if id not in bankers:
            bankers.append(id)
            await ctx.send("Person has been added as an admin.")
        else:
            await ctx.author.send("This person is already an admin.")
    else:
        await ctx.author.send("You do not have permission to use this command.")


'''@bot.command()
async def forceupdate(ctx):
    if (int(ctx.author.id) == 169248301143687168):
        await fluc()
    else:
        await ctx.author.send("You do not have permission to use this command.")'''

@bot.command()
async def pricegraph(ctx):
    if (int(ctx.author.id) == 169248301143687168):
        plt.plot(graph)
        plt.savefig('graph')
        await ctx.send(file=discord.File('graph.png'))
    else:
        await ctx.author.send("You do not have permission to use this command.")

@bot.command()
async def welcome(ctx, msg :str):
    if (int(ctx.author.id) == 282741403363049477 or int(ctx.author.id) == 169248301143687168):
        await bot.get_channel(733939009105035295).send(msg)
    else:
        await ctx.author.send("You do not have permission to use this command.")
'''
@bot.command()
async def deposit(ctx, type : str, name :str, amount):
    if str(ctx.author.id) in bankers:
        if (type == "create"):
            str_list = list(filter(None, deposits.col_values(1)))
            deposits.update_cell(len(str_list) + 1, 1, name)
            deposits.update_cell(len(str_list) + 1, 2, amount)
            deposits.update_cell(len(str_list) + 1, 3, '0')
            deposits.update_cell(len(str_list) + 1, 4, '=floor( product(indirect(ADDRESS(row(),column()-2)), indirect(ADDRESS(row(),column()-1)), 0.005))')
            deposits.update_cell(len(str_list) + 1, 5, '=floor(sum(indirect(ADDRESS(row(),column()-1)), indirect(ADDRESS(row(),column()-3))))')
    else:
        await ctx.author.send("You do not have permission to use this command.")
        '''


'''
@bot.command()
async def wallet(ctx):
    cell = sheet.find(str(ctx.author))
    await ctx.send('You have ' + sheet.row_values(cell.row)[2] + ' reales in your wallet.')
'''


#bot.loop.create_task(fluc())
bot.run('token')
