import discord
from am import ArlandaMAT
import asyncio
from discord.ext import commands
from discord.ext import tasks
from datetime import datetime

DISCORD_TOKEN = "MTA2MjY1MjQ4NDMwNjMzNzg0NA.G48p3M.JFPuY2jeuNTlJ7DJ6KdxWo3F_-EhtC-Yxid_sc"
bot = commands.Bot(command_prefix=".", intents=discord.Intents.all())
AF = ArlandaMAT()




@tasks.loop(seconds=1)
async def check():
    channel = await bot.fetch_channel(1068962730473693294)
    lastdatepinged = None
    nowdate = datetime.now().strftime("%d %B")
    if lastdatepinged != nowdate:
        if datetime.now().strftime("%H:%M") == "11:33":
            lastdatepinged = nowdate
            meal = AF.get_today()
            if meal != None:
                await channel.send("@everyone")
                embed=discord.Embed(title="Arlandagymnasiet maträtt", description="Här kommer den dagliga uppdateringen!", color=0x0cd611)
                embed.add_field(name="Dagens rätt", value=f"{meal[3]}", inline=True)
                embed.add_field(name="Dagens gröna", value=f"{meal[5]}", inline=True)
                allowed_mentions = discord.AllowedMentions(everyone = True)
                await channel.send(embed=embed, allowed_mentions=allowed_mentions)

@bot.event
async def on_ready():
    await check()

@bot.command()
async def help(ctx):
    embed=discord.Embed(title="Arlandagymnasiet maträtt", description="Här kommer alla kommandon!", color=0x0cd611)
    embed.add_field(name=".meal", value="Hämtar dagens maträtt", inline=True)
    embed.add_field(name=".meal -D -M", value="Hämtar maträtt för den dagen(-D -M) (ex. 20 jan)", inline=True)
    embed.add_field(name=".search -R", value="Söker efter en maträtt(-R)", inline=True)
    await ctx.send(embed=embed)


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