import os
from dotenv import load_dotenv
load_dotenv(override=True)

TOKEN = os.environ.get("DISCORD_TOKEN")

import discord
from discord.ext import commands

from logic import Pokemon, Fighter, Wizard

intents = discord.Intents.all()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print("Bot hazır")

@bot.command()
async def go(ctx, tür: str = "normal"):
    author = ctx.author.name
    if author not in Pokemon.pokemons:
        if tür == "fighter":
            pokemon = Fighter(author)
        elif tür == "wizard":
            pokemon = Wizard(author)
        else:
            pokemon = Pokemon(author)
        await pokemon.set_stats()
        Pokemon.pokemons[author] = pokemon
        await ctx.send(await pokemon.info())
        image_url = await pokemon.show_img()
        if image_url:
            embed = discord.Embed()
            embed.set_image(url=image_url)
            await ctx.send(embed=embed)
    else:
        await ctx.send("Zaten bir Pokémon'un var!")

@bot.command()
async def pokebilgi(ctx):
    author = ctx.author.name
    if author in Pokemon.pokemons:
        pokemon = Pokemon.pokemons[author]
        await ctx.send(await pokemon.info())
    else:
        await ctx.send("Henüz bir Pokémon'un yok.")

@bot.command()
async def attack(ctx):
    target = ctx.message.mentions[0] if ctx.message.mentions else None
    if target:
        if target.name in Pokemon.pokemons and ctx.author.name in Pokemon.pokemons:
            enemy = Pokemon.pokemons[target.name]
            attacker = Pokemon.pokemons[ctx.author.name]
            result = await attacker.perform_attack(enemy)
            await ctx.send(result)
        else:
            await ctx.send("Her iki oyuncunun da Pokémon'u olmalı!")
    else:
        await ctx.send("Bir kullanıcıyı etiketlemelisin!")

@bot.command()
async def feed(ctx):
    author = ctx.author.name
    if author in Pokemon.pokemons:
        pokemon = Pokemon.pokemons[author]
        result = await pokemon.feed()
        await ctx.send(result)
    else:
        await ctx.send("Beslemek için önce bir Pokémon'un olmalı!")

bot.run(TOKEN)
