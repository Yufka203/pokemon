import os
from dotenv import load_dotenv
from logic import Pokemon



load_dotenv(override=True)


TOKEN = os.environ.get("DISCORD_TOKEN")

import discord
from discord.ext import commands, tasks

imtiyazlar = discord.Intents.all()
imtiyazlar.message_content = True

piton = commands.Bot(command_prefix="/", intents= imtiyazlar)

@piton.event
async def on_ready():
    print("bot hazır")


@piton.command("topla")
async def topla(ctx, sayi1, sayi2):
    toplam = int(sayi1) + int(sayi2)
    await ctx.send(toplam)

@piton.command("pokebilgi")
async def go(ctx):
    author = ctx.author.name
    if author in Pokemon.pokemons:
        pokemon = Pokemon.pokemons[author]
        await ctx.send(pokemon.info())
    else:
        await ctx.send("Pokemonun yok")

@piton.command("go")
async def go(ctx):    
    user = ctx.author  
    username = user.name  
    
    if username not in Pokemon.pokemons:
        pokemon = Pokemon(username)
        await ctx.send(await pokemon.info())

        image_url = await pokemon.show_img()
        if image_url:
            embed = discord.Embed(title=f"{username}'in Pokémon'u")
            embed.set_image(url=image_url)
            await ctx.send(embed=embed)
        else:
            await ctx.send("Pokémonun görüntüsü yüklenemedi!")
    else:
        await ctx.send("Zaten kendi Pokémonunuzu oluşturdunuz!")

piton.run(TOKEN)


