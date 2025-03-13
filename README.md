# AGENT RESPONSE:

## PROMPT:Create an immersive space adventure game using Object-Oriented Programming with comprehensive error handling.



### OUTPUT:

```python
import random
from typing import List, Dict, Optional

# Custom Exceptions for the Space Adventure Game
class SpaceGameError(Exception):
    """Base exception for the space adventure game."""
    pass

class InvalidCommandError(SpaceGameError):
    """Raised when an invalid command is entered."""
    pass

class InsufficientFuelError(SpaceGameError):
    """Raised when the spaceship doesn't have enough fuel to travel."""
    pass

class ShipDestroyedError(SpaceGameError):
    """Raised when the spaceship is destroyed."""
    pass

# Alien Class representing hostile entities on planets
class Alien:
    def __init__(self, name: str, health: int, attack: int):
        if health <= 0:
            raise ValueError("Alien health must be positive.")
        if attack < 0:
            raise ValueError("Alien attack must be non-negative.")
        self.name = name
        self.health = health
        self.attack = attack

    def take_damage(self, damage: int):
        if damage < 0:
            raise ValueError("Damage cannot be negative.")
        self.health = max(self.health - damage, 0)

    def is_defeated(self) -> bool:
        return self.health == 0

    def __str__(self):
        return f"{self.name} (HP: {self.health}, ATK: {self.attack})"

# Planet Class representing different worlds in the game
class Planet:
    def __init__(self, name: str, description: str):
        if not name:
            raise ValueError("Planet name cannot be empty.")
        if not description:
            raise ValueError("Planet description cannot be empty.")
        self.name = name
        self.description = description
        self.aliens: List[Alien] = []
        self.items: List[str] = []  # Simplified items as strings.
        self.connections: Dict[str, 'Planet'] = {}

    def add_connection(self, direction: str, planet: 'Planet'):
        if not direction:
            raise ValueError("Direction cannot be empty.")
        self.connections[direction.lower()] = planet

    def add_alien(self, alien: Alien):
        self.aliens.append(alien)

    def remove_alien(self, alien: Alien):
        if alien not in self.aliens:
            raise ValueError("Alien not found on this planet.")
        self.aliens.remove(alien)

    def add_item(self, item: str):
        self.items.append(item)

    def remove_item(self, item: str):
        if item not in self.items:
            raise ValueError("Item not found on this planet.")
        self.items.remove(item)

    def __str__(self):
        connections = ", ".join(self.connections.keys()) if self.connections else "None"
        aliens = ", ".join(str(alien) for alien in self.aliens) if self.aliens else "None"
        items = ", ".join(self.items) if self.items else "None"
        return (f"Planet: {self.name}\n"
                f"Description: {self.description}\n"
                f"Connections: {connections}\n"
                f"Aliens: {aliens}\n"
                f"Items: {items}")

# SpaceShip Class representing the player's vessel
class SpaceShip:
    def __init__(self, name: str, fuel: int, health: int):
        if fuel <= 0:
            raise ValueError("Fuel must be positive.")
        if health <= 0:
            raise ValueError("Health must be positive.")
        self.name = name
        self.fuel = fuel
        self.health = health
        self.inventory: List[str] = []

    def travel(self, fuel_cost: int):
        if fuel_cost < 0:
            raise ValueError("Fuel cost cannot be negative.")
        if self.fuel < fuel_cost:
            raise InsufficientFuelError("Not enough fuel to travel.")
        self.fuel -= fuel_cost

    def repair(self, amount: int):
        if amount < 0:
            raise ValueError("Repair amount cannot be negative.")
        self.health += amount

    def take_damage(self, damage: int):
        if damage < 0:
            raise ValueError("Damage cannot be negative.")
        self.health = max(self.health - damage, 0)
        if self.health == 0:
            raise ShipDestroyedError("Your spaceship has been destroyed!")

    def add_item(self, item: str):
        self.inventory.append(item)

    def __str__(self):
        return f"SpaceShip: {self.name} (Fuel: {self.fuel}, Health: {self.health}, Inventory: {self.inventory})"

# Main Game Class for the Space Adventure
class SpaceAdventureGame:
    def __init__(self):
        self.planets: Dict[str, Planet] = {}
        self.current_planet: Optional[Planet] = None
        self.ship: Optional[SpaceShip] = None

    def setup(self):
        # Create Planets
        earth = Planet("Earth", "The blue planet, home to humanity.")
        mars = Planet("Mars", "A desolate red planet with hidden dangers.")
        jupiter = Planet("Jupiter", "A giant planet with violent storms and secrets.")
        saturn = Planet("Saturn", "Known for its rings, a place of mystery and relics.")

        # Connect Planets
        earth.add_connection("mars", mars)
        mars.add_connection("earth", earth)
        mars.add_connection("jupiter", jupiter)
        jupiter.add_connection("mars", mars)
        jupiter.add_connection("saturn", saturn)
        saturn.add_connection("jupiter", jupiter)

        # Add aliens to planets
        alien1 = Alien("Martian Raider", 50, 15)
        alien2 = Alien("Jovian Guardian", 70, 20)
        mars.add_alien(alien1)
        jupiter.add_alien(alien2)

        # Add items to planets
        earth.add_item("Fuel Cell")
        saturn.add_item("Ancient Artifact")

        self.planets = {
            "earth": earth,
            "mars": mars,
            "jupiter": jupiter,
            "saturn": saturn
        }
        self.current_planet = earth

    def create_ship(self, name: str, fuel: int = 100, health: int = 100):
        if self.ship is not None:
            raise ValueError("Ship already exists!")
        self.ship = SpaceShip(name, fuel, health)

    def travel_to(self, destination: str) -> str:
        if self.current_planet is None:
            raise SpaceGameError("Current planet is not set.")
        destination = destination.lower()
        if destination not in self.current_planet.connections:
            raise InvalidCommandError("No such destination from here.")
        fuel_cost = random.randint(10, 30)
        self.ship.travel(fuel_cost)
        self.current_planet = self.current_planet.connections[destination]
        return f"Traveled to {self.current_planet.name} using {fuel_cost} fuel."

    def scan_planet(self) -> str:
        if self.current_planet is None:
            raise SpaceGameError("Current planet is not set.")
        return str(self.current_planet)

    def collect_item(self, item: str) -> str:
        if self.current_planet is None:
            raise SpaceGameError("Current planet is not set.")
        if item not in self.current_planet.items:
            raise ValueError("Item not found on this planet.")
        self.ship.add_item(item)
        self.current_planet.remove_item(item)
        return f"Collected item: {item}"

    def engage_alien(self, alien_name: str) -> str:
        if self.current_planet is None:
            raise SpaceGameError("Current planet is not set.")
        for alien in self.current_planet.aliens:
            if alien.name.lower() == alien_name.lower():
                # Combat: spaceship attacks alien, then alien retaliates
                player_damage = random.randint(20, 40)
                alien.take_damage(player_damage)
                result = f"Attacked {alien.name} for {player_damage} damage. "
                if alien.is_defeated():
                    self.current_planet.remove_alien(alien)
                    result += f"{alien.name} has been defeated!"
                else:
                    alien_damage = alien.attack
                    try:
                        self.ship.take_damage(alien_damage)
                        result += f"{alien.name} retaliated for {alien_damage} damage."
                    except ShipDestroyedError as e:
                        result += f"{alien.name} retaliated for {alien_damage} damage. {e}"
                return result
        raise InvalidCommandError(f"No alien named '{alien_name}' found here.")

    def ship_status(self) -> str:
        if self.ship is None:
            raise SpaceGameError("Ship is not created.")
        return str(self.ship)

def main():
    game = SpaceAdventureGame()
    game.setup()
    
    try:
        ship_name = input("Enter the name of your spaceship: ").strip()
        if not ship_name:
            raise ValueError("Spaceship name cannot be empty.")
        game.create_ship(ship_name)
        print(f"Spaceship '{game.ship.name}' created successfully!")
    except Exception as e:
        print(f"Error: {e}")
        return

    print("\nWelcome to the Space Adventure Game!")
    print("Available commands: travel, scan, collect, attack, status, quit")
    
    while True:
        try:
            command = input("\nEnter command: ").strip().lower()
            if command == "quit":
                print("Exiting game. Safe travels!")
                break
            elif command == "travel":
                destination = input("Enter destination (e.g., Mars, Jupiter): ").strip()
                print(game.travel_to(destination))
            elif command == "scan":
                print(game.scan_planet())
            elif command == "collect":
                item = input("Enter the name of the item to collect: ").strip()
                print(game.collect_item(item))
            elif command == "attack":
                alien_name = input("Enter the name of the alien to attack: ").strip()
                print(game.engage_alien(alien_name))
                if game.ship.health == 0:
                    print("Your spaceship has been destroyed. Game Over!")
                    break
            elif command == "status":
                print(game.ship_status())
            else:
                print("Invalid command. Please try again.")
        except SpaceGameError as ge:
            print(f"Space Game Error: {ge}")
        except ValueError as ve:
            print(f"Value Error: {ve}")
        except Exception as ex:
            print(f"Unexpected error: {ex}")

if __name__ == "__main__":
    main()

```