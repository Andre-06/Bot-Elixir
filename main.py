import discord
from discord.ext import commands
from discord.utils import get
from discord import  member
import os
import key
import bot_commands
# coding: utf-8


eu_nao_sei_pq_dessa_variavel_mas_sei_que_sem_ela_o_bot_quebra = discord.Intents.all()
client = commands.Bot(command_prefix=".", case_insensitive=True, intents=eu_nao_sei_pq_dessa_variavel_mas_sei_que_sem_ela_o_bot_quebra, help_command=None)
