from main import GameManager, fetch_tool_data


def test_game_initialization():
    """Test that the game manager initializes properly"""
    game = GameManager()
    print("Game Manager initialized successfully")
    print(f"Player starting coin: {game.player.coin}")
    print(f"Number of biomes available: {len(game.biomes)}")
    return game


def test_biome_loading(game):
    """Test loading a biome"""
    biome_id = "biom_dark_woods"
    game.load_biom(biome_id)
    if game.biome:
        print(f"Successfully loaded biome: {game.biome.name}")
        print(f"Number of entities in biome: {len(game.biome.entities)}")
    else:
        print(f"Failed to load biome: {biome_id}")
    return game


def test_entity_harvesting(game):
    """Test harvesting an entity"""
    entity_id = "entity_level1_tree"

    player_tool_type = "woodcutting_tool"
    player_tool_id = game.player.equipment[player_tool_type + "_id"]
    tool = fetch_tool_data(player_tool_type, player_tool_id)

    print(f"Player is using: {tool['name']} with {tool['damage']} damage")

    # Save initial state
    initial_exp = game.player.exp
    initial_coin = game.player.coin
    initial_inventory_size = len(game.player.inventory)

    print("Starting harvest...")
    game.harvest_entities(entity_id)

    # Check results
    exp_gained = game.player.exp - initial_exp
    coin_gained = game.player.coin - initial_coin
    items_gained = len(game.player.inventory) - initial_inventory_size

    print(f"EXP gained: {exp_gained}")
    print(f"Coins gained: {coin_gained}")
    print(f"Items gained: {items_gained}")
    print(f"Current inventory: {game.player.inventory}")


def run_tests():
    """Run all tests in sequence"""
    print("===== STARTING TESTS =====")

    game = test_game_initialization()
    print("\n----- Biome Loading Test -----")
    game = test_biome_loading(game)
    print("\n----- Entity Harvesting Test -----")
    test_entity_harvesting(game)

    print("\n===== TESTS COMPLETED =====")


if __name__ == "__main__":
    run_tests()
