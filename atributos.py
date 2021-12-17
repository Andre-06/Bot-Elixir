from functions import *
from data_base import *


@client.command(aliases=['str', 'for', 'força'])
async def stre(ctx, tokenOp: discord.Member = None):
    if tokenOp == None:
        token = idPersonagem(ctx.author.id)
    else:
        token = idPersonagem(tokenOp.id)
    if token[1] == '0':
        await rolagemAtributo(ctx, token[0], 'STR', 'o')
    if token[1] == 1:
        await ctx.send(token[0])


@client.command(aliases=['des', 'destreza'])
async def dex(ctx, tokenOp: discord.Member = None):
    if tokenOp == None:
        token = idPersonagem(ctx.author.id)
    else:
        token = idPersonagem(tokenOp.id)
    if token[1] == '0':
        await rolagemAtributo(ctx, token[0], 'DEX', 'o')
    if token[1] == 1:
        await ctx.send(token[0])


@client.command(aliases=['carisma', 'car'])
async def cha(ctx, tokenOp: discord.Member = None):
    if tokenOp == None:
        token = idPersonagem(ctx.author.id)
    else:
        token = idPersonagem(tokenOp.id)
    if token[1] == '0':
        await rolagemAtributo(ctx, token[0], 'cha', 'o')
    if token[1] == 1:
        await ctx.send(token[0])


@client.command(aliases=['sab', 'sabedoria'])
async def wis(ctx, tokenOp: discord.Member = None):
    if tokenOp == None:
        token = idPersonagem(ctx.author.id)
    else:
        token = idPersonagem(tokenOp.id)
    if token[1] == '0':
        await rolagemAtributo(ctx, token[0], 'wis', 'o')
    if token[1] == 1:
        await ctx.send(token[0])


@client.command(aliases=['int', 'inteligencia'])
async def inte(ctx, tokenOp: discord.Member = None):
    if tokenOp == None:
        token = idPersonagem(ctx.author.id)
    else:
        token = idPersonagem(tokenOp.id)
    if token[1] == '0':
        await rolagemAtributo(ctx, token[0], 'inte', 'o')
    if token[1] == 1:
        await ctx.send(token[0])


@client.command(aliases=['habilidade', 'poder', 'pod'])
async def hab(ctx, tokenOp: discord.Member = None):
    if tokenOp == None:
        token = idPersonagem(ctx.author.id)
    else:
        token = idPersonagem(tokenOp.id)
    if token[1] == '0':
        await rolagemAtributo(ctx, token[0], 'hab', 'o')
    if token[1] == 1:
        await ctx.send(token[0])


@client.command(aliases=['constituição'])
async def con(ctx, tokenOp: discord.Member = None):
    if tokenOp == None:
        token = idPersonagem(ctx.author.id)
    else:
        token = idPersonagem(tokenOp.id)
    if token[1] == '0':
        await rolagemAtributo(ctx, token[0], 'con', 'o')
    if token[1] == 1:
        await ctx.send(token[0])
