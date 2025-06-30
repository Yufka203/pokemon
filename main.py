import os
from dotenv import load_dotenv
from logic import Pokemon

load_dotenv(override=True)
TOKEN = os.environ.get("DISCORD_TOKEN")

import discord
from discord.ext import commands

intents = discord.Intents.all()
intents.message_content = True

bot = commands.Bot(command_prefix="/", intents=intents)

@bot.event
async def on_ready():
    print("✅ Bot başarıyla başlatıldı!")

@bot.command(name="topla")
async def topla(ctx, sayi1: int, sayi2: int):
    toplam = sayi1 + sayi2
    await ctx.send(f"Toplam: {toplam}")

@bot.command(name="go")
async def go(ctx):
    username = ctx.author.name

    if username in Pokemon.pokemons:
        await ctx.send("⚠️ Zaten bir Pokémon'unuz var. Yeni bir tane almak için önce `/release` yazın.")
        return

    pokemon = Pokemon(username)
    await pokemon.get_name_and_types()
    Pokemon.pokemons[username] = pokemon

    await ctx.send(await pokemon.info())

    image_url = await pokemon.show_img()
    if image_url:
        embed = discord.Embed(title=f"{username} için Pokémon")
        embed.set_image(url=image_url)
        await ctx.send(embed=embed)
    else:
        await ctx.send("❌ Pokémon resmi yüklenemedi!")

@bot.command(name="my")
async def my_pokemon(ctx):
    username = ctx.author.name

    if username not in Pokemon.pokemons:
        await ctx.send("❌ Henüz bir Pokémon'unuz yok. Bir tane almak için `/go` yazın.")
        return

    pokemon = Pokemon.pokemons[username]
    await ctx.send(await pokemon.info())

    image_url = await pokemon.show_img()
    if image_url:
        embed = discord.Embed(title=f"{username} için mevcut Pokémon")
        embed.set_image(url=image_url)
        await ctx.send(embed=embed)

@bot.command(name="release")
async def release(ctx):
    username = ctx.author.name

    if username in Pokemon.pokemons:
        released = Pokemon.pokemons.pop(username)
        await ctx.send(f"😢 {released.name} serbest bırakıldı. Yeni bir Pokémon almak için `/go` yaz.")
    else:
        await ctx.send("❌ Serbest bırakacak bir Pokémon'unuz yok!")

bot.run(TOKEN)
