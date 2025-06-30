import aiohttp
import random

class Pokemon:
    pokemons = {}
    achievements = {}

    # Nadir Pokémon listesi (örnek efsaneler)
    rare_pokemons = [150, 151, 249, 250, 251]  # Mewtwo, Mew, Lugia, Ho-oh, Celebi

    def __init__(self, pokemon_trainer_id):
        self.pokemon_trainer_id = pokemon_trainer_id
        self.pokemon_number = self.select_pokemon_number()
        self.name = None
        self.types = []
        self.img = None
        self.stats = {}
        self.abilities = []
        self.level = 1
        self.experience = 0
        self.xp_to_next_level = 100
        self.is_rare = self.pokemon_number in Pokemon.rare_pokemons

    def select_pokemon_number(self):
        chance = random.random()
        if chance < 0.05:  # %5 nadir Pokémon şansı
            return random.choice(Pokemon.rare_pokemons)
        else:
            # Normal Pokémonlar (1-1025 arası)
            # Nadir listeden çıkarmak için filtre de koyabilirsin ama zorunlu değil
            return random.randint(1, 1025)

    async def fetch_data(self):
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    self.name = data['forms'][0]['name'].capitalize()
                    self.types = [t['type']['name'] for t in data['types']]
                    self.img = data["sprites"]["front_default"]
                    self.stats = {stat['stat']['name']: stat['base_stat'] for stat in data['stats']}
                    self.abilities = [a['ability']['name'] for a in data['abilities']]
                else:
                    self.name = f"Unknown (Error {response.status})"
                    self.types = []
                    self.img = None
                    self.stats = {}
                    self.abilities = []

    async def info(self):
        if not self.name:
            await self.fetch_data()
        types_str = ", ".join(self.types) if self.types else "Bilinmiyor"
        abilities_str = ", ".join(self.abilities) if self.abilities else "Yok"
        stats_str = ", ".join(f"{k}: {v}" for k, v in self.stats.items()) if self.stats else "Yok"
        rare_str = "⭐ **Nadir Pokémon!**" if self.is_rare else ""
        return (f"🎮 Eğitmen ID: {self.pokemon_trainer_id}\n"
                f"🐾 Pokémon: {self.name} (Lv. {self.level}) {rare_str}\n"
                f"🌪️ Tür(ler)i: {types_str}\n"
                f"✨ Yetenekler: {abilities_str}\n"
                f"📊 Statlar: {stats_str}\n"
                f"⭐ XP: {self.experience}/{self.xp_to_next_level}")

    async def show_img(self):
        if not self.img:
            await self.fetch_data()
        return self.img

    async def feed(self):
        base_xp = random.randint(10, 30)
        bonus_xp = 20 if self.is_rare else 0  # Nadir Pokémonlara bonus XP
        gained_xp = base_xp + bonus_xp
        self.experience += gained_xp
        leveled_up = False
        level_up_msgs = []
        while self.experience >= self.xp_to_next_level:
            self.experience -= self.xp_to_next_level
            self.level += 1
            self.xp_to_next_level = int(self.xp_to_next_level * 1.5)
            leveled_up = True
            level_up_msgs.append(f"🎉 Seviye atladı! Yeni seviye: {self.level}")
            await self.check_achievements()
        return leveled_up, gained_xp, level_up_msgs

    async def check_achievements(self):
        user_id = self.pokemon_trainer_id
        if user_id not in Pokemon.achievements:
            Pokemon.achievements[user_id] = set()
        levels_to_check = [5, 10, 15, 20, 25]
        for lvl in levels_to_check:
            if self.level >= lvl and f"Level {lvl} Ulaştı" not in Pokemon.achievements[user_id]:
                Pokemon.achievements[user_id].add(f"Level {lvl} Ulaştı")

    @classmethod
    async def get_achievements(cls, user_id):
        return cls.achievements.get(user_id, set())
