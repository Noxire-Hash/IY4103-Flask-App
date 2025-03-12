import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import random
import time

from utils import Logger

# Game data structures
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
        "description": "A dense forest with ancient oak trees, perfect for woodcutting.",
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
                "drops": {
                    "common_drops": ["material_lvl1_wood"],
                    "uncommon_drops": ["food_lvl1_apple", "seed_lvl1_oak"],
                },
            },
            {
                "id": "entity_level2_tree",
                "name": "Hard Bench Tree",
                "health": 300,
                "description": "Hard Bench Tree",
                "yields": {"exp_yield": 30, "coin_yield": 30},
                "req_tool_type": "woodcutting_tool",
                "req_skill_type": "woodcutting_skill",
                "drops": {
                    "common_drops": ["metarial_lvl2_wood", "food_lvl1_apple"],
                    "uncommon_drops": ["seed_lvl2_hard_bench"],
                },
            },
        ],
    },
    {
        "id": "biom_rocky_mountains",
        "name": "Rocky Mountains",
        "description": "A rugged landscape filled with mineral-rich rocks and ores.",
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

# Create a global logger instance
logger = Logger()


class Utils:
    @staticmethod
    def fetch_tool_data(tool_category, tool_id):
        """Retrieve tool data from the tool database"""
        if tool_category not in TOOL_DATA:
            logger.error(logger.GAME, f"No tools found for category: {tool_category}")
            return None

        for tool in TOOL_DATA[tool_category]:
            if tool["id"] == tool_id:
                return tool

            logger.error(
                logger.GAME,
                f"No tool found with ID: {tool_id} in category: {tool_category}",
            )
        return None

    @staticmethod
    def sign_up_player(user_id):
        """Register a new player"""
        logger.game_event(
            "REGISTRATION", f"New player registration started for user_id: {user_id}"
        )
        print("Welcome to GrindStone!")
        print(
            f"Welcome {user_id}, we see that you didn't registered for the GrindStone lets write your name in to the guild book ! "
        )
        user_name = input("What is your name adventurer ? ")
        logger.success(
            logger.GAME,
            "Player registered successfully",
            {"user_id": user_id, "username": user_name},
        )
        return user_id, user_name

    @staticmethod
    def fetch_biom_data(biom_id):
        """Retrieve biome data from the biome database"""
        for biome in BIOM_DATA:
            if biome["id"] == biom_id:
                return biome
        logger.warning(logger.GAME, f"No biome found with ID: {biom_id}")
        return None

    @staticmethod
    def fetch_entity_data(biom_id, entity_id):
        """Retrieve entity data from a specific biome"""
        biome = Utils.fetch_biom_data(biom_id)
        if biome is None:
            return None
        for entity in biome["entities"]:
            if entity["id"] == entity_id:
                return entity
        logger.warning(
            logger.GAME, f"No entity found with ID: {entity_id} in biome: {biom_id}"
        )
        return None


class Player:
    def __init__(self, user_id):
        """Initialize a player with default values"""
        self._bounded_account = user_id
        self.id = 1
        self.name = "PLACEHOLDER"
        self.coin = 1000
        self.premium_coin = 0
        self.level = 0
        self.exp = 0
        self.equipment = _DEBUG_KIT.copy()  # Make a copy to avoid shared references
        self.skills = {
            "woodcutting_skills": 1,
            "mining_skills": 1,
            "hunting_skills": 1,
            "crafting_skills": 1,
            "adventure_skills": 1,
            "cooking_skills": 1,
        }
        self.inventory = []
        self.last_action_time = time.time()
        logger.game_event(
            "PLAYER_CREATION", "New player object initialized", {"user_id": user_id}
        )

    def gain_exp(self, amount):
        """Add experience points and check for level up"""
        self.exp += amount
        logger.game_event(
            "EXP_GAIN",
            f"Player gained {amount} experience points",
            {"player_id": self.id, "new_total": self.exp},
        )
        self.check_level_up()
        return amount

    def gain_coin(self, amount):
        """Add coins to player's wallet"""
        self.coin += amount
        logger.game_event(
            "COIN_GAIN",
            f"Player gained {amount} coins",
            {"player_id": self.id, "new_total": self.coin},
        )
        return amount

    def check_level_up(self):
        """Check if player has enough experience to level up"""
        req_exp = self._get_required_exp_for_next_level()
        if self.exp >= req_exp:
            self._level_up()
            return True
        return False

    def _get_required_exp_for_next_level(self):
        """Calculate required experience for next level"""
        # Exponential growth formula for level requirements
        base_exp = 100
        return int(base_exp * (self.level + 1) * 1.5)

    def _level_up(self):
        """Process level up and increase skills"""
        prev_level = self.level
        self.level += 1

        # Increase all skills by 1
        for skill in self.skills:
            self.skills[skill] += 1

        logger.success(
            logger.PLAYER,
            f"Player leveled up to level {self.level}",
            {"player_id": self.id, "previous_level": prev_level, "skills": self.skills},
        )

        # Calculate remaining experience
        next_level_exp = self._get_required_exp_for_next_level()
        if self.exp >= next_level_exp:
            # If still have enough exp for another level up, recurse
            self.check_level_up()

        return self.level - prev_level  # Return number of levels gained

    def swap_equipment(self, equipment_type, equipment_id):
        """Change a piece of equipment"""
        # Check if equipment exists
        if not equipment_type.endswith("_tool") and not equipment_type.endswith(
            "_armor"
        ):
            logger.error(
                logger.PLAYER,
                f"Invalid equipment type: {equipment_type}",
                {"player_id": self.id},
            )
            return False

        _equipment_data = Utils.fetch_tool_data(equipment_type, equipment_id)
        if not _equipment_data:
            logger.error(
                logger.PLAYER,
                "Failed to fetch tool data",
                {
                    "player_id": self.id,
                    "equipment_type": equipment_type,
                    "equipment_id": equipment_id,
                },
            )
            return False

        # Store old equipment for logging
        old_id = self.equipment.get(equipment_type + "_id")
        old_name = self.equipment.get(equipment_type, "None")

        # Update equipment
        self.equipment[equipment_type + "_id"] = equipment_id
        self.equipment[equipment_type] = _equipment_data["name"]

        logger.player_action(
            "EQUIPMENT_CHANGE",
            f"Player changed {equipment_type}",
            {
                "player_id": self.id,
                "old_item": f"{old_name} (ID: {old_id})",
                "new_item": f"{_equipment_data['name']} (ID: {equipment_id})",
            },
        )
        return True

    def use_item(self, item_id):
        """Use an item from the inventory"""
        if item_id in self.inventory:
            self.inventory.remove(item_id)
            logger.player_action(
                "ITEM_USE", f"Player used item {item_id}", {"player_id": self.id}
            )
            # TODO: Implement item effects
            return True
        else:
            logger.warning(
                logger.PLAYER,
                f"Item {item_id} not found in inventory",
                {"player_id": self.id},
            )
            return False


class Biom:
    def __init__(self, biom_data):
        """Initialize a biome from biome data"""
        self.id = biom_data["id"]
        self.name = biom_data["name"]
        self.description = biom_data["description"]
        self.entities = biom_data["entities"]
        self.req_level = biom_data.get("req_level", 1)
        logger.game_event(
            "BIOME_CREATION", f"Biome {self.name} initialized", {"biome_id": self.id}
        )

    def is_accessible(self, player_level):
        """Check if player has required level to access this biome"""
        accessible = player_level >= self.req_level
        if not accessible:
            logger.warning(
                logger.GAME,
                f"Player level {player_level} too low for biome {self.name}",
                {"required_level": self.req_level},
            )
        return accessible

    def get_entity(self, entity_id):
        """Get entity data by ID"""
        for entity in self.entities:
            if entity["id"] == entity_id:
                return entity
        logger.warning(
            logger.GAME, f"Entity {entity_id} not found in biome {self.name}"
        )
        return None


class GameManager:
    def __init__(self):
        """Initialize the game manager"""
        self.player = Player(user_id=1)
        self.biomes = BIOM_DATA
        self.items = []
        self.current_action = {}  # Dictionary to store current action details
        self.biome = None
        self.stamps = []
        self.logs = []
        logger.game_event("GAME_INIT", "Game Manager initialized")

    def load_biom(self, destination):
        """Load a biome by ID"""
        logger.game_event("BIOME_LOAD", f"Attempting to load biome: {destination}")
        _desired_biom = self._find_desired_biom(destination)
        if _desired_biom:
            self.biome = Biom(_desired_biom)
            logger.success(
                logger.GAME,
                f"Loaded biome: {self.biome.name}",
                {"biome_id": self.biome.id},
            )
            return True
        return False

    def _find_desired_biom(self, destination):
        """Find a biome by ID in the biome database"""
        for biome in self.biomes:
            if biome["id"] == destination:
                return biome
        logger.warning(logger.GAME, f"No biome found with ID: {destination}")
        return None

    def _get_entities_data(self, entity_id):
        """Get entity data from the current biome"""
        if self.biome is None:
            logger.error(logger.GAME, "No biome loaded")
            return None

        for entity in self.biome.entities:
            if entity["id"] == entity_id:
                return entity

        logger.warning(
            logger.GAME,
            f"No entity found with ID: {entity_id} in biome: {self.biome.id}",
        )
        return None

    def harvest_entities(self, entity_id):
        """Harvest an entity in the current biome"""
        # Set the current action
        if self.biome:
            self.set_current_action("harvesting", self.biome.id, entity_id)
        else:
            logger.error(logger.GAME, "Cannot harvest: No biome loaded")
            return False

        # Get entity data
        entity_data = self._get_entities_data(entity_id)
        if not entity_data:
            logger.error(
                logger.GAME, f"Cannot harvest entity: {entity_id}, entity not found"
            )
            return False

        # Get required tool
        req_tool = entity_data["req_tool_type"]
        player_tool_id = self.player.equipment[req_tool + "_id"]
        tool = Utils.fetch_tool_data(req_tool, player_tool_id)

        if not tool:
            logger.error(
                logger.GAME,
                f"Player does not have required tool for harvesting {entity_id}",
                {"required_tool": req_tool, "player_tool_id": player_tool_id},
            )
            return False

        # Calculate harvest time based on entity health and tool damage
        if tool["damage"] == 0:
            time_to_harvest = 0  # Avoid division by zero
        else:
            time_to_harvest = entity_data["health"] / tool["damage"]

        logger.player_action(
            "HARVEST",
            f"Harvesting {entity_data['name']} with {tool['name']}",
            {
                "entity_id": entity_id,
                "tool_id": player_tool_id,
                "time": f"{time_to_harvest:.2f}s",
            },
        )

        # Simulate harvesting time
        time.sleep(time_to_harvest)

        # Process harvesting results
        self._entity_yields(entity_data)

        # Create a stamp for this action
        self.create_stamp()

        return True

    def _entity_yields(self, entity_data):
        """Process the rewards from harvesting an entity"""
        # Award coins and experience
        coin_gained = self.player.gain_coin(entity_data["yields"]["coin_yield"])
        exp_gained = self.player.gain_exp(entity_data["yields"]["exp_yield"])

        # Process item drops
        drops = []

        # Process common drops (always drop)
        if "common_drops" in entity_data["drops"]:
            drops.extend(entity_data["drops"]["common_drops"])

        # Process uncommon drops (50% chance)
        if (
            "uncommon_drops" in entity_data["drops"]
            and len(entity_data["drops"]["uncommon_drops"]) > 0
        ):
            if random.random() < 0.5:  # 50% chance
                # Randomly select one of the uncommon drops
                selected_drop = random.choice(entity_data["drops"]["uncommon_drops"])
                drops.append(selected_drop)

        # Add drops to player inventory
        for item in drops:
            self.player.inventory.append(item)

        logger.success(
            logger.PLAYER,
            "Harvesting completed successfully",
            {
                "exp_gained": exp_gained,
                "coin_gained": coin_gained,
                "drops": drops,
                "inventory_size": len(self.player.inventory),
            },
        )

    def create_stamp(self):
        """Create a timestamp record of the current action and player state"""
        if not self.current_action:
            logger.error(logger.GAME, "Cannot create stamp: No current action")
            return None

        stamp = {
            "id": len(self.stamps) + 1,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "action_data": self.current_action,
            "player_state": {
                "level": self.player.level,
                "exp": self.player.exp,
                "coins": self.player.coin,
                "inventory_size": len(self.player.inventory),
            },
        }

        self.stamps.append(stamp)
        logger.game_event(
            "STAMP_CREATION",
            f"Created stamp #{stamp['id']}",
            {"action": self.current_action["action_type"]},
        )
        return stamp

    def fetch_stamps(self):
        """Retrieve all action stamps"""
        logger.game_event("STAMP_FETCH", f"Fetching {len(self.stamps)} stamps")
        return self.stamps

    def set_current_action(self, action_type, biom_id, target_id):
        """Set the current action being performed"""
        self.current_action = {
            "action_type": action_type,
            "biome_id": biom_id,
            "target_id": target_id,
            "player_id": self.player.id,
            "timestamp": time.time(),
        }

        # Add target_type based on action
        if action_type.startswith("harvesting"):
            self.current_action["target_type"] = "entity"
        elif action_type == "pickup":
            self.current_action["target_type"] = "item"
        elif action_type in ["crafting", "cooking"]:
            self.current_action["target_type"] = "recipe"
        else:
            self.current_action["target_type"] = "unknown"

        logger.game_event(
            "ACTION_SET",
            f"Set current action: {action_type}",
            {
                "biome_id": biom_id,
                "target_id": target_id,
                "target_type": self.current_action["target_type"],
            },
        )


class GameInterface:
    def __init__(self):
        """Initialize the game interface"""
        self.gm = GameManager()
        self.logs = []
        self.is_logged_in = False
        self.current_user_id = None
        logger.game_event("INTERFACE_INIT", "Game Interface initialized")

    def init_game_session(self, user_id):
        """Initialize a new game session for a user"""
        logger.server_event(
            "SESSION_INIT", f"Initializing game session for user {user_id}"
        )
        self.current_user_id = user_id

        # Set up a new player
        user_id, user_name = Utils.sign_up_player(user_id)
        self.gm.player.name = user_name
        self.gm.player.id = user_id

        # Load starter biome
        self.gm.load_biom("biom_dark_woods")

        self.is_logged_in = True
        logger.success(
            logger.SERVER,
            f"Game session initialized for user {user_id}",
            {"username": user_name},
        )
        return True

    def perform_action(self, action_type, target_id):
        """Perform a game action"""
        if not self.is_logged_in:
            logger.error(logger.SERVER, "Cannot perform action: Not logged in")
            return False

        if not self.gm.biome:
            logger.error(logger.SERVER, "Cannot perform action: No biome loaded")
            return False

        logger.player_action(
            action_type.upper(),
            f"Player attempting to {action_type} {target_id}",
            {"player_id": self.current_user_id, "biome_id": self.gm.biome.id},
        )

        # Set current action
        self.gm.set_current_action(action_type, self.gm.biome.id, target_id)

        # Perform the action
        result = False
        if action_type == "harvesting":
            result = self.gm.harvest_entities(target_id)
        elif action_type == "travel":
            result = self.gm.load_biom(target_id)
        # Add more action types as needed

        # Log the result
        if result:
            logger.success(
                logger.PLAYER,
                f"Action {action_type} on {target_id} completed successfully",
            )
        else:
            logger.error(logger.PLAYER, f"Action {action_type} on {target_id} failed")

        return result

    def get_player_data(self):
        """Get current player data"""
        if not self.is_logged_in:
            logger.warning(
                logger.SERVER, "Attempted to get player data without logging in"
            )
            return None

        logger.server_event(
            "DATA_REQUEST", "Player data requested", {"player_id": self.current_user_id}
        )
        return {
            "id": self.gm.player.id,
            "name": self.gm.player.name,
            "level": self.gm.player.level,
            "exp": self.gm.player.exp,
            "coin": self.gm.player.coin,
            "premium_coin": self.gm.player.premium_coin,
            "skills": self.gm.player.skills,
            "inventory": self.gm.player.inventory,
            "equipment": self.gm.player.equipment,
        }

    def get_biome_data(self):
        """Get current biome data"""
        if not self.is_logged_in or not self.gm.biome:
            logger.warning(
                logger.SERVER, "Attempted to get biome data when unavailable"
            )
            return None

        logger.server_event(
            "DATA_REQUEST",
            "Biome data requested",
            {"player_id": self.current_user_id, "biome_id": self.gm.biome.id},
        )
        return {
            "id": self.gm.biome.id,
            "name": self.gm.biome.name,
            "description": self.gm.biome.description,
            "entities": self.gm.biome.entities,
        }

    def end_game(self):
        """End the current game session"""
        if not self.is_logged_in:
            logger.warning(
                logger.SERVER, "Attempted to end game session when not logged in"
            )
            return False

        logger.server_event(
            "SESSION_END", "Game session ended", {"player_id": self.current_user_id}
        )
        self.is_logged_in = False
        self.current_user_id = None
        return True
