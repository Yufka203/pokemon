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
    await bot.change_presence(activity=discord.Game(name="/go ile Pokémon al!"))

@bot.command(name="topla")
async def topla(ctx, sayi1: int, sayi2: int):
    toplam = sayi1 + sayi2
    await ctx.send(f"Toplam: {toplam}")

@bot.command(name="go")
async def go(ctx):
    user_id = ctx.author.id
    if user_id in Pokemon.pokemons:
        await ctx.send("⚠️ Zaten bir Pokémon'unuz var. Yeni almak için önce `/release` yazın.")
        return

    pokemon = Pokemon(user_id)
    await pokemon.fetch_data()
    Pokemon.pokemons[user_id] = pokemon

    msg = await pokemon.info()
    if pokemon.is_rare:
        msg = f"✨ **Tebrikler! Nadir Pokémon yakaladınız!** ✨\n" + msg

    await ctx.send(msg)

    image_url = await pokemon.show_img()
    if image_url:
        embed = discord.Embed(title=f"{ctx.author.name} için Pokémon")
        embed.set_image(url=image_url)
        await ctx.send(embed=embed)
    else:
        await ctx.send("❌ Pokémon resmi yüklenemedi!")

@bot.command(name="my")
async def my_pokemon(ctx):
    user_id = ctx.author.id
    if user_id not in Pokemon.pokemons:
        await ctx.send("❌ Henüz bir Pokémon'unuz yok. Bir tane almak için `/go` yazın.")
        return

    pokemon = Pokemon.pokemons[user_id]
    await ctx.send(await pokemon.info())
    image_url = await pokemon.show_img()
    if image_url:
        embed = discord.Embed(title=f"{ctx.author.name} için mevcut Pokémon")
        embed.set_image(url=image_url)
        await ctx.send(embed=embed)

@bot.command(name="release")
async def release(ctx):
    user_id = ctx.author.id
    if user_id in Pokemon.pokemons:
        released = Pokemon.pokemons.pop(user_id)
        await ctx.send(f"😢 {released.name} serbest bırakıldı. Yeni bir Pokémon almak için `/go` yaz.")
    else:
        await ctx.send("❌ Serbest bırakacak bir Pokémon'unuz yok!")

@bot.command(name="feed")
async def feed(ctx):
    user_id = ctx.author.id
    if user_id not in Pokemon.pokemons:
        await ctx.send("❌ Henüz bir Pokémon'unuz yok. Bir tane almak için `/go` yazın.")
        return

    pokemon = Pokemon.pokemons[user_id]
    leveled_up, xp, level_up_msgs = await pokemon.feed()
    msg = f"{pokemon.name} beslendi ve {xp} XP kazandı."
    if leveled_up:
        msg += "\n" + "\n".join(level_up_msgs)
    await ctx.send(msg)

@bot.command(name="achievements")
async def achievements(ctx):
    user_id = ctx.author.id
    achs = await Pokemon.get_achievements(user_id)
    if not achs:
        await ctx.send("Henüz hiçbir başarınız yok.")
        return
    await ctx.send("🎖️ Başarılarınız:\n" + "\n".join(f"- {a}" for a in achs))

bot.run(TOKEN)
