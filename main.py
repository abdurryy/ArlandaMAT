import discord
from am import ArlandaMAT
import asyncio
from discord.ext import commands
from discord.ext import tasks
from datetime import datetime

DISCORD_TOKEN = ""
bot = commands.Bot(command_prefix=".", intents=discord.Intents.all())
AF = ArlandaMAT()
lastdatepinged = None

@tasks.loop(seconds=5)
async def check():
    global lastdatepinged
    channel = await bot.fetch_channel(1068962730473693294)
    nowdate = datetime.now().strftime("%d %B")
    print(nowdate, lastdatepinged)
    if lastdatepinged != nowdate:
        print("1")
        print(datetime.now().strftime("%H:%M"))
        if datetime.now().strftime("%H:%M") == "10:35":
            print("2")
            meal = AF.get_today()
            print(meal)
            if meal != None:
                print("3")
                lastdatepinged = nowdate
                await channel.send("@everyone")
                embed=discord.Embed(title="Arlandagymnasiet maträtt", description="Här kommer den dagliga uppdateringen!", color=0x0cd611)
                embed.add_field(name="Dagens rätt", value=f"{meal[3]}", inline=True)
                embed.add_field(name="Dagens gröna", value=f"{meal[5]}", inline=True)
                allowed_mentions = discord.AllowedMentions(everyone = True)
                await channel.send(embed=embed, allowed_mentions=allowed_mentions)

@bot.event
async def on_ready():
    check.start()


@bot.command()
async def meal(ctx, *, time = ""):
    if time == "":
        meal = AF.get_today()
        if meal == None:
            return await ctx.send("Det finns inga maträtter idag! Testa att skriva datumet i formatet D M (20 jan)")
        embed=discord.Embed(title="Arlandagymnasiet maträtt", description="Här kommer din sökning!", color=0x0cd611)
        embed.add_field(name="Dagens rätt", value=f"{meal[3]}", inline=True)
        embed.add_field(name="Dagens gröna", value=f"{meal[5]}", inline=True)
        return await ctx.send(embed=embed)
    meal = AF.get_day(time)
    print(time, meal)
    if meal == None:
            return await ctx.send("Det finns inga maträtter för den dagen! Testa att skriva datumet i formatet D M (20 jan)")
    embed=discord.Embed(title="Arlandagymnasiet maträtt", description="Här kommer din sökning!", color=0x0cd611)
    embed.add_field(name="Dagens rätt", value=f"{meal[3]}", inline=True)
    embed.add_field(name="Dagens gröna", value=f"{meal[5]}", inline=True)
    return await ctx.send(embed=embed)

@bot.command()
async def search(ctx, *, meal = " "):
    j = AF.get_search(meal)
    if j == None:
        return await ctx.send("Inga maträtter hittades!")
    embed=discord.Embed(title="Arlandagymnasiet maträtt", description="Här kommer din sökning!", color=0x0cd611)
    paginator = 0
    for i in range(0,len(j)):
        embed.add_field(name="Datum", value=f"{j[i][0]}", inline=True)
        embed.add_field(name="Dag", value=f"{j[i][1]}", inline=True)
        embed.add_field(name="Hittad rätt", value=f"{j[i][2]}", inline=True)
        paginator +=1
        if i+1 == len(j):
            await ctx.send(embed=embed) 
            break
        if paginator == 3:
            await ctx.send(embed=embed)
            embed=discord.Embed(title="Arlandagymnasiet maträtt", description="Här kommer din sökning!", color=0x0cd611)
            paginator = 0

bot.run(DISCORD_TOKEN)