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
_DEBUG_KIT = {
    "chest_armor": "Debuggers Migthy Chest Piece",
    "chest_armor_id": -1,
    "head_armor": "Debuggers Mighty Head Armor",
    "head_armor_id": -1,
    "leg_armor": "Debuggers Mighty Leg Armor",
    "leg_armor_id": -1,
    "woodcutting_tool": "Debuggers Migthy Axe",
    "woodcutting_tool_id": -1,
    "mining_tool": "Debuggers Migthy Pickaxe",
    "mining_tool_id": -1,
    "hunting_tool": "Debuggers Migthy Bow",
    "hunting_tool_id": -1,
    "melee_tool": "Debuggers Migthy Sword",
    "melee_tool_id": -1,
}

LOAD_INV_DATA = {
    "materials": {
        "material_lvl1_wood": 1,
        "metal_lvl1_ore": 1,
    },
    "food": {
        "food_lvl1_apple": 1,
        "food_lvl1_bread": 1,
    },
    "items": {
        "item_starter_text": 1,
        "item_lvl1_expgem": 1,
        "tools": {},
    },
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
    },
    {
        "id": "biom_rocky_mountains",
        "name": "Rocky Mountains",
        "description": "some text",
        "req_level": 3,
        "entities": [
            {
                "id": "entity_level1_rock",
                "name": "Rock",
                "health": 100,
                "description": "A basic Rock",
                "yields": {"exp_yield": 10, "coin_yield": 10},
                "req_tool_type": "mining_tool",
                "req_skill_type": "mining_skill",
                "drops": {
                    "common_drops": ["material_lvl1_stone"],
                    "uncommon_drops": ["material_lvl1_ore"],
                },
            }
        ],
    },
]

TOOL_DATA = {
    "woodcutting_tool": [
        {
            "id": -1,
            "name": "Debuggers Woodcutting Axe",
            "description": "The mighty debugger",
            "damage": 100,
            "durability": 100000,
            "type": "item_woodcutting_tool",
        },
        {
            "id": 0,
            "name": "Broken Axe",
            "description": "An old woodcutting tool",
            "damage": 1,
            "durability": 10,
            "type": "item_woodcutting_tool",
        },
    ],
    "mining_tool": [
        {
            "id": -1,
            "name": "Debuggers Mining Pickaxe",
            "description": "The mighty debugger",
            "damage": 100,
            "durability": 100000,
            "type": "item_mining_tool",
        },
        {
            "id": 0,
            "name": "Rusty Pickaxe",
            "description": "An old mining tool",
            "damage": 1,
            "durability": 10,
            "type": "item_mining_tool",
        },
    ],
    "hunting_tool": [
        {
            "id": -1,
            "name": "Debuggers Hunting Bow",
            "description": "The mighty debugger",
            "damage": 100,
            "durability": 100000,
            "type": "item_hunting_tool",
        }
    ],
}


class Utils:
    @staticmethod
    def fetch_tool_data(tool_category, tool_id):
        if tool_category not in TOOL_DATA:
            print(f"No tools found for category: {tool_category}")
            return None

        for tool in TOOL_DATA[tool_category]:
            if tool["id"] == tool_id:
                return tool

        print(f"No tool found with ID: {tool_id} in category: {tool_category}")
        return None

    @staticmethod
    def log(message):
        log_message = f"[{time.strftime('%Y-%m-%d %H:%M:%S')}], {message}"
        print(log_message)
        return log_message

    @staticmethod
    def sign_up_player(user_id):
        is_registered = False
        while not is_registered:
            print("Welcome to GrindStone!")
            print(
                f"Welcome {user_id}, we see that you didn't registered for the GrindStone lets write your name in to the guild book ! "
            )
            user_name = input("What is your name adventurer ? ")
            return user_id, user_name

    def fetch_biom_data(biom_id):
        for biome in BIOM_DATA:
            if biome["id"] == biom_id:
                return biome
        print(f"No biome found with ID: {biom_id}")
        return None

    def fetch_entity_data(biom_id, entity_id):
        biome = Utils.fetch_biom_data(biom_id)
        if biome is None:
            return None
        for entity in biome["entities"]:
            if entity["id"] == entity_id:
                return entity
        print(f"No entity found with ID: {entity_id} in biome: {biom_id}")
        return None


class GameManager:
    def __init__(self):
        self.player = Player(user_id=1)
        self.biomes = BIOM_DATA
        self.items = []
        self.current_action = ""
        self.biome = None
        self.stamps = []
        self.logger = Utils.log
        self.logs = []

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
        self.current_action = f"harvesting_woodcutting_{entity_id}"
        entity_data = self._get_entities_data(entity_id)
        req_tool = entity_data["req_tool_type"]
        player_tool_id = self.player.equipment[req_tool + "_id"]
        tool = Utils.fetch_tool_data(req_tool, player_tool_id)

        if 0 >= entity_data["health"] / tool["damage"]:
            time_to_harvest = 0
        else:
            time_to_harvest = entity_data["health"] / tool["damage"]

        time.sleep(time_to_harvest)
        self._entity_yields(entity_data)

    def _entity_yields(self, entity_data):
        self.player.gain_coin(entity_data["yields"]["coin_yield"])
        self.player.gain_exp(entity_data["yields"]["exp_yield"])

        for drop_type, drop_items in entity_data["drops"].items():
            self.player.inventory.extend(drop_items)

    def create_stamp(self):
        if not self.current_action:
            return None

        stamp = {
            "id": len(self.stamps) + 1,  # Or use a proper DB auto-increment
            "timestamp": time.time(),
            "action_data": {
                "action_type": self.current_action["action_type"],
                "biome_id": self.current_action["biome_id"],
                "target_id": self.current_action["target_id"],
                "target_type": self.current_action["target_type"],
                "player_id": self.current_action["player_id"],
            },
            "player_state": {
                "level": self.player.level,
                "exp": self.player.exp,
                "coins": self.player.coin,
            },
        }

        self.stamps.append(stamp)
        return stamp

    def fetch_stamps(self):
        # TODO do a persistent database for it
        return self.stamps

    def set_current_action(self, action_type, biom_id, target_id):
        self.current_action = {
            "action_type": action_type,
            "biome_id": biom_id,
            "target_type": "un_initialized",
            "target_id": target_id,
            "player_id": self.player.id,
            "timestamp": time.time(),
        }

        # Add target_type based on action
        if action_type == "harvesting":
            self.current_action["target_type"] = "entity"
        elif action_type == "pickup":
            self.current_action["target_type"] = "item"
        elif action_type in ["crafting", "cooking"]:
            self.current_action["target_type"] = "recipe"


class Player:
    def __init__(self, user_id):
        self._bounded_account = user_id
        self.id = 1
        self.name = "PLACEHOLDER"
        self.coin = 1000
        self.premium_coin = 0
        self.level = 0
        self.exp = 0
        self.equipment = _DEBUG_KIT
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

    def _swap_equipment(self, equipment_type, equipment_id):
        _equipment_data = Utils.fetch_tool_data(equipment_type, equipment_id)
        if not _equipment_data:
            print("A problem happened while fetching tool data please try again")
            return None
        self.equipment[equipment_type + "_id"] = equipment_id
        self.equipment[equipment_type + "_name"] = _equipment_data["name"]

    def check_inventory(self, equipment_type, equipment_id):
        pass


class Biom:
    def __init__(self, biom_data):
        self.id = biom_data["id"]
        self.name = biom_data["name"]
        self.description = biom_data["description"]
        self.entities = biom_data["entities"]

    def create_entity(self):
        pass


class GameInterface:
    def __init__(self):
        self.gm = GameManager()

    def int_game_session(self, user_id):
        pass

    def _get_player_name(self):
        pass

    def _get_player_id(self):
        pass
