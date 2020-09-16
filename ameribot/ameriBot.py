import discord
from discord.ext import commands
import os
from dotenv import load_dotenv, find_dotenv
import random
import sys
import datetime

# loading in the token, setting up randomness, etc
load_dotenv(find_dotenv())
random.seed()

token = os.getenv("TOKEN")
mediiServerID = os.getenv("MEDIISERVERID")
honorsServerID = os.getenv("HONORSSERVERID")
happyServerID = os.getenv("HAPPYSERVERID")

bot = commands.Bot(command_prefix = "!")
semEnds = [2020, 12, 13]

@bot.command()
async def hi(ctx):
    await ctx.send("hi, {0.mention} it's nice to meet you :blush:".format(ctx.author))

@bot.command()
async def goodbye(ctx):
    if commands.is_owner():
        await ctx.send("so long world, see you again soon! :wave:")
        await bot.change_presence(status=discord.Status.offline)
        await bot.logout()
    else:
        await ctx.send("You can't control me :triumph:")

@bot.event
async def on_ready():
    print("------------------------------------")
    print("Bot Name: ", bot.user.name)
    print("Bot ID: ", bot.user.id)
    print("Discord Version: ", discord.__version__)
    print("------------------------------------")
    print("")
    print("hello world, ameriBot speaking!")

"""
@bot.event
async def on_message(ctx):
    # use this area to server lock some commands

    if ctx.author == bot.user:
        return
    print("beep boop {} {}".format(ctx.guild, ctx.guild.id))
"""

@bot.command()
async def color(ctx):
    colors = list(range(6))

    for i in colors:
        colors[i] = random.randint(0,15)
    
    await ctx.send("Here ya go! https://www.colorhexa.com/{}{}{}{}{}{}".format(colorHandle(colors[0]), colorHandle(colors[1]),
                    colorHandle(colors[2]), colorHandle(colors[3]), colorHandle(colors[4]), colorHandle(colors[5])))

@bot.command()
async def set_email(ctx, email):
    emailSet = setToFile(ctx, "emails.txt", email)

    if emailSet == -1:
        await ctx.send("You already set your email!")
    elif emailSet == 0:
        await ctx.send("Got it down!")
        
    """
    # if emails.txt doesn't exist, make it
    if os.path.exists(os.path.join(sys.path[0], "emails.txt")) == False:
        f = open(os.path.join(sys.path[0], "emails.txt"), "x")
        f.close()
    
    # check if user already created an email
    f = open(os.path.join(sys.path[0], "emails.txt"), "r")
    datafile = f.readlines()

    # check if file has contents, if so, scan through it for duplicates
    if os.path.getsize(os.path.join(sys.path[0], "emails.txt")) != 0:
        for line in datafile:
            if str(ctx.author.id) in line:
                f.close()
                await ctx.send("You already set your email!")
                return
    
    f.close()
    # add user email to the list if not present or if file empty
    f = open(os.path.join(sys.path[0], "emails.txt"), "a")
    f.write("{}: {}\n".format(ctx.author.id, email))
    f.close()
    await ctx.send("Got it down!")
    """

@bot.command()
async def getemail(ctx, user: discord.User):
    emailGet = getFromFile("emails.txt", user)

    if emailGet == -1:
        await ctx.send("Sorry, no one's set their email yet!")
    elif emailGet == 0:
        await ctx.send("{0.mention} hasn't set their email yet :sob:".format(user))
    else:
        await ctx.send("{0.mention}'s email is: {1}".format(user, emailGet))

@bot.command()
async def howmuchlonger(ctx):
    dday = datetime.datetime(semEnds[0], semEnds[1], semEnds[2])
    ddayCount = dday - datetime.datetime.now()

    await ctx.send("{} days until the semester is over {}".format(ddayCount.days, daysLeftEmote(ddayCount.days)))



# Helper Functions --------------------
def colorHandle(color):
    letters = ["a", "b", "c", "d", "e", "f"]
    letterFind = color - 10

    if letterFind >= 0:
        return letters[letterFind]
    else:
        return str(color)
    
def daysLeftEmote(days):
    if days <= 7:
        return ":partying_face:"
    else:
        return ":sob:"

def getFromFile(filename, user):
    # no things to get if file doesn't exist or is empty
    if os.path.exists(os.path.join(sys.path[0], filename)) == False or os.path.getsize(os.path.join(sys.path[0], filename)) == 0:
        return -1

    # extract file contents for further scanning
    f = open(os.path.join(sys.path[0], filename), "r")
    datafile = f.readlines()
    f.close()

    # search each line for the user's discord id, if you find it, take the thing next to it and return it
    for line in datafile:
        if "{}: ".format(str(user.id)) in line:
            junkID, got = line.split()
            return got
        else:
            return 0

def setToFile(ctx, filename, whatSet):
    # if emails.txt doesn't exist, make it
    if os.path.exists(os.path.join(sys.path[0], filename)) == False:
        f = open(os.path.join(sys.path[0], filename), "x")
        f.close()
    
    # check if user already created an email
    f = open(os.path.join(sys.path[0], filename), "r")
    datafile = f.readlines()

    # check if file has contents, if so, scan through it for duplicates
    if os.path.getsize(os.path.join(sys.path[0], filename)) != 0:
        for line in datafile:
            if str(ctx.author.id) in line:
                f.close()
                return -1
    
    f.close()
    # add user email to the list if not present or if file empty
    f = open(os.path.join(sys.path[0], filename), "a")
    f.write("{}: {}\n".format(ctx.author.id, whatSet))
    f.close()
    return 0


bot.run(token)