import time

# Related data for GrindStone
STARTER_KIT = {
    "chest_armor": "Old Adventurers Chest Plate",
    "chest_armor_id": 0,
    "head_armor": "Old cascate",
    "head_armor_id": 0,
    "leg_armor": "Old Miners Pants",
    "leg_armor_id": 0,
    "woodcutting_tool": "Basic Axe",
    "woodcutting_tool_id": 0,
    "mining_tool": "Basic Pickaxe",
    "mining_tool_id": 0,
    "hunting_tool": "Basic Bow",
    "hunting_tool_id": 0,
    "melee_tool": "Sword",
    "melee_tool_id": 0,
}


BIOM_DATA = [
    {
        "id": "biom_dark_woods",
        "name": "Dark Woods",
        "description": "some text",
        "req_level": 1,
        "entities": [
            {
                "id": "entity_level1_tree",
                "name": "Oak Tree",
                "health": 100,
                "description": "A basic Oak Tree",
                "yields": {"exp_yield": 10, "coin_yield": 10},
                "req_tool_type": "woodcutting_tool",
                "req_skill_type": "woodcutting_skill",
                "drops": {  # rarity's are common, uncommon, rare, legendary, uniq
                    "common_drops": ["material_lvl1_wood"],
                    "uncommon_drops": ["food_lvl1_apple", "seed_lvl1_oak"],
                },
            },
        ],
    }
]

TOOL_DATA = {
    "woodcutting_tool": [
        {
            "id": 0,
            "name": "Debuggers pickaxe",
            "description": "The mighty debugger",
            "damage": 100,
            "durability": 100000,
            "type": "item_woodcutting_tool",
        },
    ],
    "mining_tool": [
        {
            "id": 0,
            "name": "Rusty Pickaxe",
            "description": "An old mining tool",
            "damage": 1,
            "durability": 10,
            "type": "item_mining_tool",
        },
    ],
}


def fetch_tool_data(tool_category, tool_id):
    if tool_category not in TOOL_DATA:
        print(f"No tools found for category: {tool_category}")
        return None

    for tool in TOOL_DATA[tool_category]:
        if tool["id"] == tool_id:
            return tool

    print(f"No tool found with ID: {tool_id} in category: {tool_category}")
    return None


class GameManager:
    def __init__(self):
        self.player = Player(userId=1)
        self.biomes = BIOM_DATA
        self.items = []
        self.current_action = None
        self.biome = None

    def load_biom(self, destination):
        _desired_biom = self._find_desired_biom(destination)
        if _desired_biom:
            self.biome = Biom(_desired_biom)

    def _find_desired_biom(self, destination):
        for biome in self.biomes:
            if biome["id"] == destination:
                return biome
        print("There is no biome that matches desired id")
        return None

    def _get_entities_data(self, entity_id):
        if self.biome is None:
            return None

        for entity in self.biome.entities:
            if entity["id"] == entity_id:
                return entity

        return None

    def harvest_entities(self, entity_id):
        entity_data = self._get_entities_data(entity_id)
        req_tool = entity_data["req_tool_type"]
        player_tool_id = self.player.equipment[req_tool + "_id"]
        tool = fetch_tool_data(req_tool, player_tool_id)

        if 0 >= entity_data["health"] / tool["damage"]:
            time_to_harvest = 0
        else:
            # Make it so if it requires 3 hits it wont spend 3 sec it would spend 2 sec
            time_to_harvest = entity_data["health"] / tool["damage"] - 1

        time.sleep(time_to_harvest)
        self._entity_yields(entity_data)

    def _entity_yields(self, entity_data):
        self.player.gain_coin(entity_data["yields"]["coin_yield"])
        self.player.gain_exp(entity_data["yields"]["exp_yield"])

        for drop_type, drop_items in entity_data["drops"].items():
            self.player.inventory.extend(drop_items)


class Player:
    def __init__(self, userId):
        self._bounded_account = userId
        self.name = "PLACEHOLDER"
        self.coin = 1000
        self.premium_coin = 0
        self.level = 0
        self.exp = 0
        self.equipment = STARTER_KIT
        self.skills = {
            "woodcutting_skills": 1,
            "mining_skills": 1,
            "hunting_skills": 1,
            "crafting_skills": 1,
            "adventure_skills": 1,
            "cooking_skills": 1,
        }
        self.inventory = []

    def goto_biom(self):
        pass

    def create_stamp():
        pass

    def gain_exp(self, amount):
        self.exp += amount
        self.check_level_up()

    def gain_coin(self, amount):
        self.coin += amount

    def check_level_up(self):
        req_exp = self._get_required_exp_for_next_level()
        if self.exp >= req_exp:
            self._level_up()

    def _get_required_exp_for_next_level(self):
        return 100 * self.level

    def _level_up(self):
        self.level += 1
        for skill in self.skills:
            self.skills[skill] += 1


class Biom:
    def __init__(self, biom_data):
        self.name = biom_data["name"]
        self.description = biom_data["description"]
        self.entities = biom_data["entities"]

    def create_entity(self):
        pass
