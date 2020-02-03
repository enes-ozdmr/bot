import discord,requests,bs4
import bjack
import datetime
from discord.ext import commands

with open("test-bot.txt","r") as f:
    token=f.read()

client=commands.Bot(command_prefix=".",help_command=None,activity=discord.Game(name="FOREX | .help"))
embed=discord.Embed(title="Güncel Döviz Kurları için",
                    description=".dollar\n.euro\n.bitcoin\n.sterlin")
@client.event
async def on_ready():
    print("Bot is ready")

@client.command()
async def help(ctx):
    await ctx.send(embed=embed)


@client.command()
async def whois(ctx, *membr):
    if len(membr)>0:
        string=" ".join(membr)
        if isinstance(ctx.guild.get_member_named(string), discord.Member):
            membr=ctx.guild.get_member_named(string)
        else:
            await ctx.send(f":skull_crossbones: Couldn't find user {string}")
            return


    elif len(membr)==0:
        membr=ctx.author

    embed=discord.Embed(description=f"{membr.mention}")
    embed.set_author(name=str(membr), icon_url=membr.avatar_url)
    # embed.set_thumbnail(url=ctx.author.avatar_url)
    date=membr.joined_at.strftime("%a, %b %d, %Y %I:%M \n%p")
    embed.add_field(name="Joined", value=date, inline=True)
    regis=membr.created_at.strftime("%a, %b %d, %Y %I:%M \n%p")
    embed.add_field(name="Registered", value=regis ,inline=True)

    await ctx.send(embed=embed)
    #day, month, digit day, year, hour
    #title @author, On the right the picture

@client.command()
async def bj(ctx):
    await bjack.play(ctx,client)


@client.command(aliases=["dollar","euro","bitcoin","pound","sterlin"])
async def dovizkuru(ctx):
    currencies={
    "dollar": "TRY",
    "euro": "EURTRY",
    "bitcoin":"BTCUSD",
    "pound":"GBPTRY",
    "sterlin":"GBPTRY",
    }
    crr=currencies[ctx.invoked_with]
    #bitcoin value is displayed in terms of us dollar in order to avoid volatility issues.

    usdobject=requests.get(f"https://finance.yahoo.com/quote/{crr}=X")
    usdobject.raise_for_status()
    usdBS=bs4.BeautifulSoup(usdobject.text)
    result=usdBS.find_all("h1")
    # result[0].text  cr name
    resultvalue=usdBS.find_all("span")
    # resultvalue[0].text  cr value
    embed=discord.Embed(title=result[0].text,
            description=resultvalue[5].text,
            colour= discord.Colour.blue()
    )
    await ctx.send(embed=embed)



client.run(token)
