import os
import sys
import time

from main import GameManager, Player, Utils

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import Logger

# Create a test logger instance
logger = Logger()


def test_game_initialization():
    """Test that the game manager initializes properly"""
    logger.system_event("TEST", "Starting game initialization test")
    game = GameManager()

    logger.info(logger.SYSTEM, "\n=== Game Manager Initialization ===")
    logger.info(logger.SYSTEM, f"Player starting coin: {game.player.coin}")
    logger.info(logger.SYSTEM, f"Number of biomes available: {len(game.biomes)}")
    logger.info(
        logger.SYSTEM,
        f"Available biomes: {', '.join([biome['name'] for biome in game.biomes])}",
    )

    logger.success(logger.SYSTEM, "Game manager initialized successfully")
    return game


def test_biome_loading(game, desired_biome_id="biom_dark_woods"):
    """Test loading a biome"""
    logger.system_event(
        "TEST", f"Starting biome loading test with biome: {desired_biome_id}"
    )

    logger.info(logger.SYSTEM, f"\n=== Loading Biome: {desired_biome_id} ===")
    game.load_biom(desired_biome_id)

    if game.biome:
        logger.success(logger.SYSTEM, f"Successfully loaded biome: {game.biome.name}")
        logger.info(logger.SYSTEM, f"Biome description: {game.biome.description}")
        logger.info(
            logger.SYSTEM, f"Number of entities in biome: {len(game.biome.entities)}"
        )

        for i, entity in enumerate(game.biome.entities):
            logger.info(
                logger.SYSTEM,
                f"  Entity {i + 1}: {entity['name']} (Health: {entity['health']})",
            )
    else:
        logger.error(logger.SYSTEM, f"Failed to load biome: {desired_biome_id}")

    return game


def test_entity_harvesting(game, test_entity_id="entity_level1_tree"):
    """Test harvesting an entity"""
    logger.system_event(
        "TEST", f"Starting entity harvesting test with entity: {test_entity_id}"
    )

    logger.info(logger.SYSTEM, f"\n=== Harvesting Entity: {test_entity_id} ===")

    if not game.biome:
        logger.warning(logger.SYSTEM, "No biome loaded. Loading default biome first...")
        game = test_biome_loading(game)

    entity_data = None
    for entity in game.biome.entities:
        if entity["id"] == test_entity_id:
            entity_data = entity
            break

    if not entity_data:
        logger.error(
            logger.SYSTEM,
            f"Entity {test_entity_id} not found in current biome. Stopping test.",
        )
        return

    player_tool_type = entity_data["req_tool_type"]
    player_tool_id = game.player.equipment[player_tool_type + "_id"]
    tool = Utils.fetch_tool_data(player_tool_type, player_tool_id)

    logger.info(
        logger.SYSTEM,
        f"Entity to harvest: {entity_data['name']} (Health: {entity_data['health']})",
    )
    logger.info(
        logger.SYSTEM, f"Player is using: {tool['name']} with {tool['damage']} damage"
    )
    logger.info(logger.SYSTEM, f"Required tool type: {player_tool_type}")

    # Save initial state
    initial_exp = game.player.exp
    initial_coin = game.player.coin
    initial_inventory_size = len(game.player.inventory)
    initial_level = game.player.level

    logger.info(logger.SYSTEM, "\nStarting harvest...")
    start_time = time.time()
    game.harvest_entities(test_entity_id)
    harvest_time = time.time() - start_time

    # Check results
    exp_gained = game.player.exp - initial_exp
    coin_gained = game.player.coin - initial_coin
    items_gained = len(game.player.inventory) - initial_inventory_size
    levels_gained = game.player.level - initial_level

    logger.info(logger.SYSTEM, f"Harvest completed in {harvest_time:.2f} seconds")

    # Log detailed results
    result_data = {
        "exp_gained": exp_gained,
        "coin_gained": coin_gained,
        "items_gained": items_gained,
        "harvest_time": f"{harvest_time:.2f}s",
    }

    logger.success(logger.SYSTEM, "Harvest results", result_data)

    if levels_gained > 0:
        logger.success(
            logger.SYSTEM,
            f"LEVEL UP! Gained {levels_gained} level(s). Current level: {game.player.level}",
        )

    logger.info(logger.SYSTEM, f"Current inventory: {game.player.inventory}")

    # Check stamp creation
    if len(game.stamps) > 0:
        logger.info(logger.SYSTEM, f"Stamp created: #{game.stamps[-1]['id']}")


def test_player_level_up():
    """Test the player level up mechanism"""
    logger.system_event("TEST", "Starting player level-up test")

    logger.info(logger.SYSTEM, "\n=== Testing Player Level-Up System ===")

    player = Player(user_id=999)
    logger.info(logger.SYSTEM, f"Initial level: {player.level}")
    logger.info(logger.SYSTEM, f"Initial XP: {player.exp}")

    # Check XP requirement for next level
    next_level_req = player._get_required_exp_for_next_level()
    logger.info(logger.SYSTEM, f"XP required for next level: {next_level_req}")

    # Add almost enough XP to level up
    almost_level_xp = next_level_req - 1
    player.gain_exp(almost_level_xp)
    logger.info(logger.SYSTEM, f"Added {almost_level_xp} XP. Current XP: {player.exp}")
    logger.info(logger.SYSTEM, f"Current level: {player.level}")

    # Add just enough XP to level up
    player.gain_exp(1)
    logger.info(logger.SYSTEM, f"Added 1 more XP. Current XP: {player.exp}")
    logger.info(logger.SYSTEM, f"Current level: {player.level}")

    # Check skill improvements after level up
    logger.info(logger.SYSTEM, "Skills after level up:")
    for skill, level in player.skills.items():
        logger.info(logger.SYSTEM, f"  {skill}: {level}")

    # Add enough XP for multiple level ups
    player.gain_exp(1000)
    logger.info(logger.SYSTEM, f"Added 1000 more XP. Current XP: {player.exp}")
    logger.info(logger.SYSTEM, f"Current level: {player.level}")


def test_equipment_swap():
    """Test swapping player equipment"""
    logger.system_event("TEST", "Starting equipment swap test")

    logger.info(logger.SYSTEM, "\n=== Testing Equipment Swapping ===")

    player = Player(user_id=999)

    # Show initial equipment
    logger.info(logger.SYSTEM, "Initial equipment:")
    for item_type, item_id in {
        k: v for k, v in player.equipment.items() if k.endswith("_id")
    }.items():
        item_name = player.equipment.get(item_type.replace("_id", ""), "Unknown")
        tool_data = Utils.fetch_tool_data(item_type.replace("_id", ""), item_id)
        if tool_data:
            logger.info(
                logger.SYSTEM,
                f"  {item_type}: {tool_data['name']} (ID: {item_id}, Damage: {tool_data.get('damage', 'N/A')})",
            )
        else:
            logger.info(logger.SYSTEM, f"  {item_type}: {item_name} (ID: {item_id})")

    # Try to swap to a different tool
    tool_category = "woodcutting_tool"
    new_tool_id = 0  # Basic Axe

    logger.info(logger.SYSTEM, f"\nSwapping {tool_category} to ID {new_tool_id}...")
    swap_result = player.swap_equipment(tool_category, new_tool_id)

    # Check result
    if swap_result:
        logger.success(
            logger.SYSTEM,
            f"Successfully swapped to {player.equipment[tool_category]} (ID: {player.equipment[tool_category + '_id']})",
        )
    else:
        logger.error(logger.SYSTEM, "Failed to swap equipment")

    # Try to swap to an invalid tool
    logger.info(logger.SYSTEM, "\nTrying to swap to an invalid tool...")
    invalid_result = player.swap_equipment(tool_category, 999)
    if not invalid_result:
        logger.success(logger.SYSTEM, "Correctly failed to swap to invalid tool")


def print_menu():
    """Print the test menu options"""
    menu = """
========== GRINDSTONE TEST MENU ==========
1. Test Game Initialization
2. Test Biome Loading
3. Test Entity Harvesting (Woodcutting)
4. Test Entity Harvesting (Mining)
5. Test Player Level Up
6. Test Equipment Swap
7. Test Action Stamps
8. Run All Tests
0. Exit
=========================================="""

    logger.info(logger.SYSTEM, menu)
    return input("Enter your choice (0-8): ")


def test_action_stamps():
    """Test creating and fetching action stamps"""
    logger.system_event("TEST", "Starting action stamps test")

    logger.info(logger.SYSTEM, "\n=== Testing Action Stamps ===")

    game = GameManager()

    # Create a stamp manually
    game.load_biom("biom_dark_woods")
    game.set_current_action("test_action", game.biome.id, "test_target")

    logger.info(logger.SYSTEM, "Creating an action stamp...")
    stamp = game.create_stamp()

    if stamp:
        logger.success(
            logger.SYSTEM,
            "Stamp created successfully",
            {
                "id": stamp["id"],
                "timestamp": stamp["timestamp"],
                "action_type": stamp["action_data"]["action_type"],
                "target": stamp["action_data"]["target_id"],
            },
        )
    else:
        logger.error(logger.SYSTEM, "Failed to create stamp")

    # Create a few more stamps
    logger.info(logger.SYSTEM, "Creating additional stamps...")
    game.set_current_action("harvesting", game.biome.id, "entity_level1_tree")
    game.create_stamp()

    game.set_current_action("travel", "biom_rocky_mountains", None)
    game.create_stamp()

    # Fetch all stamps
    all_stamps = game.fetch_stamps()
    logger.info(logger.SYSTEM, f"\nTotal stamps created: {len(all_stamps)}")
    logger.info(logger.SYSTEM, "Stamp history:")

    for i, s in enumerate(all_stamps):
        logger.info(
            logger.SYSTEM,
            f"  {i + 1}. {s['action_data']['action_type']} at {s['timestamp']}",
        )


def test_logger():
    """Test the logging system itself"""
    logger.system_event("TEST", "Starting logger test")

    logger.info(logger.SYSTEM, "\n=== Testing Logger System ===")

    # Test different log levels
    logger.info(logger.SYSTEM, "This is an info message")
    logger.success(logger.SYSTEM, "This is a success message")
    logger.warning(logger.SYSTEM, "This is a warning message")
    logger.error(logger.SYSTEM, "This is an error message")
    logger.critical(logger.SYSTEM, "This is a critical message")

    # Test different sources
    logger.info(logger.PLAYER, "This is a player message")
    logger.info(logger.GAME, "This is a game message")
    logger.info(logger.SERVER, "This is a server message")
    logger.info(logger.SYSTEM, "This is a system message")

    # Test with data
    logger.info(
        logger.SYSTEM,
        "Message with data",
        {"player_id": 123, "action": "test", "value": 42},
    )

    # Test convenience methods
    logger.player_action(
        "MOVE", "Player moved to new location", {"from": "Town", "to": "Forest"}
    )
    logger.game_event("SPAWN", "Entity spawned", {"entity_id": "monster_1", "level": 5})
    logger.server_event(
        "REQUEST", "API request received", {"endpoint": "/api/game", "method": "GET"}
    )
    logger.system_event("STARTUP", "System initialized", {"version": "1.0.0"})

    # Get stored logs
    logs = logger.get_logs()
    logger.info(logger.SYSTEM, f"Total logs stored: {len(logs)}")

    logger.success(logger.SYSTEM, "Logger test completed successfully")


def run_tests():
    """Run tests based on user selection"""
    logger.system_event("TEST_SUITE", "GrindStone test suite started")

    while True:
        choice = print_menu()

        if choice == "0":
            logger.system_event("TEST_SUITE", "Exiting test suite")
            logger.info(logger.SYSTEM, "Exiting test suite. Goodbye!")
            break

        elif choice == "1":
            logger.system_event("TEST_SUITE", "Running game initialization test")
            test_game_initialization()

        elif choice == "2":
            logger.system_event("TEST_SUITE", "Running biome loading test")
            game = test_game_initialization()
            biome_id = input("Enter biome ID to load (default: biom_dark_woods): ")
            if not biome_id:
                biome_id = "biom_dark_woods"
            test_biome_loading(game, biome_id)

        elif choice == "3":
            logger.system_event("TEST_SUITE", "Running woodcutting test")
            game = test_game_initialization()
            test_biome_loading(game, "biom_dark_woods")
            test_entity_harvesting(game, "entity_level1_tree")

        elif choice == "4":
            logger.system_event("TEST_SUITE", "Running mining test")
            game = test_game_initialization()
            test_biome_loading(game, "biom_rocky_mountains")
            test_entity_harvesting(game, "entity_level1_rock")

        elif choice == "5":
            logger.system_event("TEST_SUITE", "Running player level up test")
            test_player_level_up()

        elif choice == "6":
            logger.system_event("TEST_SUITE", "Running equipment swap test")
            test_equipment_swap()

        elif choice == "7":
            logger.system_event("TEST_SUITE", "Running action stamps test")
            test_action_stamps()

        elif choice == "8":
            logger.system_event("TEST_SUITE", "Running all tests")
            logger.info(logger.SYSTEM, "\n===== RUNNING ALL TESTS =====")

            # Initialize game
            game = test_game_initialization()

            # Test biome loading
            game = test_biome_loading(game, "biom_dark_woods")

            # Test woodcutting
            test_entity_harvesting(game, "entity_level1_tree")

            # Test biome change
            game = test_biome_loading(game, "biom_rocky_mountains")

            # Test mining
            test_entity_harvesting(game, "entity_level1_rock")

            # Test player level up
            test_player_level_up()

            # Test equipment swap
            test_equipment_swap()

            # Test action stamps
            test_action_stamps()

            # Test the logger itself
            test_logger()

            logger.success(logger.SYSTEM, "ALL TESTS COMPLETED SUCCESSFULLY")

        elif choice == "9":  # Hidden option for testing the logger
            test_logger()

        else:
            logger.warning(logger.SYSTEM, f"Invalid choice: {choice}")
            logger.info(logger.SYSTEM, "Please select a number from 0-8.")

        input("\nPress Enter to continue...")


if __name__ == "__main__":
    run_tests()
