import aiohttp
import random
from datetime import datetime, timedelta

class Pokemon:
    pokemons = {}

    def __init__(self, pokemon_trainer):
        self.pokemon_trainer = pokemon_trainer
        self.pokemon_number = random.randint(1, 1000)
        self.img = None
        self.name = None
        self.attack = None
        self.defense = None
        self.hp = None
        self.last_feed_time = datetime.now() - timedelta(seconds=100)  # Başta hemen beslenebilsin

    async def get_name(self):
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    return data['forms'][0]['name']
                else:
                    return "Pikachu"

    async def fetch_stats(self):
        stats = {"attack": 0, "defense": 0, "hp": 0}
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    for stat in data["stats"]:
                        name = stat["stat"]["name"]
                        if name == "attack":
                            stats["attack"] = stat["base_stat"]
                        elif name == "defense":
                            stats["defense"] = stat["base_stat"]
                        elif name == "hp":
                            stats["hp"] = stat["base_stat"]
        return stats

    async def set_stats(self):
        stats = await self.fetch_stats()
        self.attack = stats["attack"]
        self.hp = stats["hp"]
        self.defense = stats["defense"]
        if not self.name:
            self.name = await self.get_name()

    async def info(self):
        if not self.name:
            self.name = await self.get_name()
        return f"Pokémon'un ismi: {self.name}\nSaldırı: {self.attack}\nSavunma: {self.defense}\nCan: {self.hp}"

    async def show_img(self):
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    return data["sprites"]["front_default"]
                else:
                    return None

    async def perform_attack(self, enemy):
        if isinstance(enemy, Pokemon):
            if enemy.hp > self.attack:
                enemy.hp -= self.attack
                return f"@{self.pokemon_trainer}, @{enemy.pokemon_trainer}'a saldırdı!\n@{enemy.pokemon_trainer}'ın sağlık durumu: {enemy.hp}"
            else:
                enemy.hp = 0
                return f"@{self.pokemon_trainer}, @{enemy.pokemon_trainer}'ı yendi!"
        else:
            return "Geçersiz rakip!"

    async def feed(self, feed_interval=20, hp_increase=10):
        current_time = datetime.now()
        delta_time = timedelta(seconds=feed_interval)
        if (current_time - self.last_feed_time) > delta_time:
            self.hp += hp_increase
            self.last_feed_time = current_time
            return f"Pokémon beslendi. Yeni sağlık: {self.hp}"
        else:
            kalan = self.last_feed_time + delta_time - current_time
            return f"Şu kadar sonra besleyebilirsin: {round(kalan.total_seconds())} saniye"

class Fighter(Pokemon):
    async def feed(self, feed_interval=20, hp_increase=10):
        return await super().feed(feed_interval, hp_increase + 10)

class Wizard(Pokemon):
    async def feed(self, feed_interval=10, hp_increase=10):
        return await super().feed(feed_interval, hp_increase)
