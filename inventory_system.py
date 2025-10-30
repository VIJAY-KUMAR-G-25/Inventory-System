"""
A simple inventory management system.

This module provides functions to add, remove, and query item quantities
in a simple dictionary-based inventory. It also supports saving to
and loading from a JSON file.
"""

import json
import logging


def add_item(stock_data, item, qty):
    """
    Adds a specified quantity of an item to the stock.

    Args:
        stock_data (dict): The inventory dictionary.
        item (str): The name of the item to add.
        qty (int): The quantity to add.
    """
    if not isinstance(item, str) or not item:
        logging.error("Invalid item: %s. Must be a non-empty string.", item)
        return
    if not isinstance(qty, int):
        logging.error("Invalid qty for %s: %s. Must be an integer.", item, qty)
        return

    stock_data[item] = stock_data.get(item, 0) + qty
    logging.info("Added %d of %s.", qty, item)


def remove_item(stock_data, item, qty):
    """
    Removes a specified quantity of an item from the stock.

    If the remaining quantity is zero or less, the item is removed.

    Args:
        stock_data (dict): The inventory dictionary.
        item (str): The name of the item to remove.
        qty (int): The quantity to remove.
    """
    if not isinstance(item, str) or not item:
        logging.error("Invalid item: %s. Must be a non-empty string.", item)
        return
    if not isinstance(qty, int):
        logging.error("Invalid qty for %s: %s. Must be an integer.", item, qty)
        return

    try:
        stock_data[item] -= qty
        logging.info("Removed %d of %s.", qty, item)
        if stock_data[item] <= 0:
            del stock_data[item]
            logging.info("Item %s removed (quantity <= 0).", item)
    except KeyError:
        logging.warning("Failed to remove '%s'. Item not in stock.", item)


def get_qty(stock_data, item):
    """
    Gets the current quantity of a specific item.

    Args:
        stock_data (dict): The inventory dictionary.
        item (str): The name of the item to query.

    Returns:
        int: The quantity of the item, or 0 if not found.
    """
    try:
        return stock_data[item]
    except KeyError:
        logging.warning("Item '%s' not found in stock.", item)
        return 0


def load_data(file="inventory.json"):
    """
    Loads the inventory data from a JSON file.

    Args:
        file (str): The name of the file to load from.

    Returns:
        dict: The loaded inventory data, or an empty dict if
              the file is not found or is empty/corrupt.
    """
    try:
        with open(file, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        logging.warning("Could not load %s. Returning empty inventory.", file)
        return {}


def save_data(stock_data, file="inventory.json"):
    """
    Saves the inventory data to a JSON file.

    Args:
        stock_data (dict): The inventory dictionary to save.
        file (str): The name of the file to save to.
    """
    try:
        with open(file, "w", encoding="utf-8") as f:
            json.dump(stock_data, f, indent=4)
        logging.info("Inventory saved to %s.", file)
    except IOError as e:
        logging.error("Could not save inventory to %s: %s", file, e)


def print_data(stock_data):
    """
    Prints a formatted report of all items and their quantities.

    Args:
        stock_data (dict): The inventory dictionary.
    """
    print("\n--- Items Report ---")
    if not stock_data:
        print("Inventory is empty.")
    else:
        for item, qty in stock_data.items():
            print(f"{item} -> {qty}")
    print("--------------------")


def check_low_items(stock_data, threshold=5):
    """
    Finds all items with a quantity below the threshold.

    Args:
        stock_data (dict): The inventory dictionary.
        threshold (int): The quantity threshold.

    Returns:
        list: A list of item names that are low in stock.
    """
    return [item for item, qty in stock_data.items() if qty < threshold]


def main():
    """
    Main function to run the inventory system operations.
    """
    # Configure logging
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s')

    # Load data, perform operations, and save
    stock_data = load_data()
    print_data(stock_data)

    add_item(stock_data, "apple", 10)
    add_item(stock_data, "banana", 15)
    add_item(stock_data, "orange", 3)  # This item will be low
    add_item(stock_data, "apple", 5)

    # These will now log errors instead of crashing
    add_item(stock_data, 123, "ten")
    remove_item(stock_data, "grape", 1)  # Will log a warning

    remove_item(stock_data, "apple", 3)

    print(f"\nApple stock: {get_qty(stock_data, 'apple')}")
    print(f"Grape stock: {get_qty(stock_data, 'grape')}")

    print(f"Low items: {check_low_items(stock_data)}")

    print_data(stock_data)
    save_data(stock_data)


if __name__ == "__main__":
    main()
