import aiohttp
import random

class Pokemon:
    pokemons = {}

    def __init__(self, pokemon_trainer):
        self.pokemon_trainer = pokemon_trainer
        self.pokemon_number = random.randint(1, 1025)
        self.img = None
        self.name = None
        self.types = []

    async def get_name_and_types(self):
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    self.name = data['forms'][0]['name']
                    self.types = [t['type']['name'] for t in data['types']]
                else:
                    self.name = f"Unknown (Error {response.status})"
                    self.types = []

    async def info(self):
        if not self.name:
            await self.get_name_and_types()

        if self.types:
            types_str = ", ".join(self.types)
        else:
            types_str = "Bilinmiyor"

        return f"🎮 Eğitmen: {self.pokemon_trainer}\n🐾 Pokémon: {self.name}\n🌪️ Tür(ler)i: {types_str}"

    async def get_image_url(self):
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    self.img = data["sprites"]["front_default"]
                    return self.img
                else:
                    return None

    async def show_img(self):
        return await self.get_image_url()
