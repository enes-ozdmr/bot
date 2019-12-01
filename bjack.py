#! python3
import random
import time
import os
import discord




def generator(hands):
    value=0
    k=len(hands)
    for i in range(k):
        if hands[i] in "JQK":
            value+=10
        elif hands[i] not in "JQKA":
            value+=int(hands[i])
        elif hands[i] == "A":
            value+=1

    if value<12 and "A" in hands:
        value+=10

    return value


async def play(ctx, client):
    cards= [ "2","3","4","5","6","7","8","9","10","J","Q","K","A"]*4

    dealer_hand=[]
    your_hand=[]

    random.shuffle(cards)

    dealer_hand.append(cards.pop())
    dealer_hand.append(cards.pop())
    your_hand.append(cards.pop())
    your_hand.append(cards.pop())
    embed=discord.Embed(title=f"Blackjack | {ctx.message.author.display_name}",
        description="Type `hit` to draw another card or  `stay` to pass."
    )
    embed.add_field(name="Your hand: ",value=f"{'  -  '.join(your_hand)} \nValue: {generator(your_hand)}", inline=True)
    embed.add_field(name="Dealer hand: ",value=f"{dealer_hand[0]}  -  `XX` \nValue: {generator(dealer_hand[0])}", inline=True)
    # await ctx.send("Your hand:  {} value {}".format( "-".join(your_hand),generator(your_hand)))
    # await ctx.send("Dealer's hand: {}-xx value {} ".format(dealer_hand[0], generator(dealer_hand[0])))
    await ctx.send(embed=embed)

    while True:
        if generator(your_hand)==21:
            await ctx.send("You Win!")
            break
        if generator(your_hand)>21:
            await ctx.send("You Lose!")
            break
        def check(m):
            return m.content=="hit" or m.content=="stay"



        answer=await client.wait_for("message", timeout=60.0, check=check)

        if answer.content.lower()=="stay":
            while generator(dealer_hand) <17 or generator(your_hand)>=generator(dealer_hand) :
                dealer_hand.append(cards.pop())
            if generator(dealer_hand)<=21:
                embed=discord.Embed(title=f"Blackjack | {ctx.message.author.display_name}",description="You Lost!.", color=0xf90000)
                embed.add_field(name="Your hand: ",value=f"{'  -  '.join(your_hand)} \nValue: {generator(your_hand)}", inline=False)
                embed.add_field(name="Dealer hand: ",value=f"{'  -  '.join(dealer_hand)} \nValue: {generator(dealer_hand)}", inline=False)
                await ctx.send(embed=embed)
            else:
                embed=discord.Embed(title=f"Blackjack | {ctx.message.author.display_name}",description="You Win!.", color=0x0000ff)
                embed.add_field(name="Your hand: ",value=f"{'  -  '.join(your_hand)} \nValue: {generator(your_hand)}", inline=False)
                embed.add_field(name="Dealer hand: ",value=f"{'  -  '.join(dealer_hand)} \nValue: {generator(dealer_hand)}", inline=False)
                await ctx.send(embed=embed)
            break
        elif answer.content.lower()=="hit":
            your_hand.append(cards.pop())
            embed=discord.Embed(title=f"Blackjack | {ctx.message.author.display_name}",description="Type `hit` to draw another card or  `stay` to pass.!.")
            embed.add_field(name="Your hand: ",value=f"{'  -  '.join(your_hand)} \nValue: {generator(your_hand)}", inline=True)
            embed.add_field(name="Dealer hand: ",value=f"{'  -  '.join(dealer_hand)} \nValue: {generator(dealer_hand)}", inline=True)
            await ctx.send(embed=embed)
            continue
        else:
            continue


