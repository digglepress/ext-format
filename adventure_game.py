#!/usr/bin/env python3
import os
import time
import random
from typing import Dict, List, Tuple, Any

class AdventureGame:
    def __init__(self):
        self.player = {
            "name": "",
            "health": 100,
            "inventory": [],
            "location": "forest_entrance"
        }
        
        self.locations = {
            "forest_entrance": {
                "description": "You stand at the entrance of a mysterious forest. The trees seem to whisper secrets.",
                "options": {
                    "1": ("Enter the forest", "forest_path"),
                    "2": ("Examine the strange mushrooms nearby", "mushroom_encounter"),
                    "3": ("Turn back home", "game_end")
                }
            },
            "forest_path": {
                "description": "You're on a winding path. To your left is a babbling brook, to your right, dense foliage.",
                "options": {
                    "1": ("Follow the brook", "brook_path"),
                    "2": ("Explore the dense foliage", "hidden_clearing"),
                    "3": ("Continue straight ahead", "mysterious_cabin")
                }
            },
            "mushroom_encounter": {
                "description": "The mushrooms glow with an otherworldly light. As you lean closer, they release a cloud of spores!",
                "options": {
                    "1": ("Hold your breath and back away", "forest_entrance"),
                    "2": ("Collect some mushrooms for later", "mushroom_collection"),
                    "3": ("Accidentally inhale the spores", "hallucination")
                }
            },
            "mushroom_collection": {
                "description": "You carefully collect some mushrooms. They might be useful later.",
                "inventory_add": "glowing mushrooms",
                "options": {
                    "1": ("Return to the forest entrance", "forest_entrance"),
                    "2": ("Enter the forest", "forest_path")
                }
            },
            "hallucination": {
                "description": "The world around you transforms into vivid colors and impossible shapes. The trees begin to dance!",
                "health_change": -10,
                "options": {
                    "1": ("Close your eyes and wait for it to pass", "forest_entrance"),
                    "2": ("Dance with the trees", "fairy_encounter")
                }
            },
            "brook_path": {
                "description": "The brook leads to a small waterfall with a cave behind it. The water sparkles with unusual clarity.",
                "options": {
                    "1": ("Drink from the brook", "magic_water"),
                    "2": ("Explore behind the waterfall", "hidden_cave"),
                    "3": ("Return to the forest path", "forest_path")
                }
            },
            "magic_water": {
                "description": "The water tastes sweet and rejuvenating. You feel your vitality returning!",
                "health_change": 20,
                "options": {
                    "1": ("Explore behind the waterfall", "hidden_cave"),
                    "2": ("Return to the forest path", "forest_path")
                }
            },
            "hidden_cave": {
                "description": "Behind the waterfall is a cave filled with glittering crystals. In the center lies an ancient sword!",
                "inventory_add": "crystal sword",
                "options": {
                    "1": ("Take the sword and leave", "brook_path"),
                    "2": ("Examine the cave walls more closely", "cave_drawings")
                }
            },
            "cave_drawings": {
                "description": "The walls are covered with ancient drawings depicting a battle between light and darkness. A prophecy?",
                "options": {
                    "1": ("Take the sword and leave", "brook_path"),
                    "2": ("Touch the drawings", "vision_sequence")
                }
            },
            "vision_sequence": {
                "description": "As your fingers brush the drawings, you're flooded with visions of an ancient evil awakening deep in the forest.",
                "options": {
                    "1": ("Take the sword and prepare to face the evil", "forest_path"),
                    "2": ("Flee the cave in terror", "brook_path")
                }
            },
            "hidden_clearing": {
                "description": "You discover a hidden clearing with a stone circle. Moonlight bathes the area despite it being daytime.",
                "options": {
                    "1": ("Step into the stone circle", "fairy_encounter"),
                    "2": ("Examine the strange symbols on the stones", "ancient_magic"),
                    "3": ("Return to the forest path", "forest_path")
                }
            },
            "fairy_encounter": {
                "description": "Tiny lights swirl around you, revealing themselves as mischievous fairies! They seem amused by your presence.",
                "options": {
                    "1": ("Ask them for guidance", "fairy_help"),
                    "2": ("Try to catch one", "fairy_anger"),
                    "3": ("Politely excuse yourself", "hidden_clearing")
                }
            },
            "fairy_help": {
                "description": "The fairies giggle and lead you to a secret path through the forest. They whisper secrets of hidden treasures!",
                "options": {
                    "1": ("Follow their guidance to treasure", "treasure_cache"),
                    "2": ("Ask about the ancient evil", "fairy_warning"),
                    "3": ("Thank them and return to exploring", "hidden_clearing")
                }
            },
            "fairy_anger": {
                "description": "The fairies don't appreciate your grabby hands! They swarm around you, pinching and pulling your hair!",
                "health_change": -15,
                "options": {
                    "1": ("Apologize profusely", "fairy_forgiveness"),
                    "2": ("Run away!", "forest_path")
                }
            },
            "fairy_forgiveness": {
                "description": "Your sincere apology seems to appease the fairies. They stop tormenting you and become curious instead.",
                "options": {
                    "1": ("Ask them for guidance", "fairy_help"),
                    "2": ("Thank them and leave", "hidden_clearing")
                }
            },
            "fairy_warning": {
                "description": "The fairies become serious, warning you of an ancient evil stirring in the heart of the forest. They offer a magical charm.",
                "inventory_add": "fairy charm",
                "options": {
                    "1": ("Accept the charm and seek the evil", "mysterious_cabin"),
                    "2": ("Thank them and continue exploring", "hidden_clearing")
                }
            },
            "treasure_cache": {
                "description": "The fairies lead you to a hollow tree containing a small chest. Inside you find a golden amulet!",
                "inventory_add": "golden amulet",
                "options": {
                    "1": ("Return to the fairy clearing", "hidden_clearing"),
                    "2": ("Continue deeper into the forest", "mysterious_cabin")
                }
            },
            "ancient_magic": {
                "description": "As you trace the symbols with your finger, they begin to glow. You feel ancient knowledge flowing into you.",
                "inventory_add": "spell of light",
                "options": {
                    "1": ("Step into the stone circle", "fairy_encounter"),
                    "2": ("Return to the forest path", "forest_path")
                }
            },
            "mysterious_cabin": {
                "description": "You come across a moss-covered cabin. Smoke rises from the chimney, but something feels... wrong.",
                "options": {
                    "1": ("Knock on the door", "witch_encounter"),
                    "2": ("Peek through the window", "cabin_window"),
                    "3": ("Circle around to the back", "cabin_garden")
                }
            },
            "cabin_window": {
                "description": "Through the grimy window, you see shelves filled with bottles, dried herbs, and... are those eyes floating in jars?",
                "options": {
                    "1": ("Knock on the door anyway", "witch_encounter"),
                    "2": ("Decide this is too creepy and leave", "forest_path"),
                    "3": ("Check the back of the cabin", "cabin_garden")
                }
            },
            "cabin_garden": {
                "description": "Behind the cabin is a garden of strange plants. Some seem to move on their own! There's a basket of freshly harvested herbs.",
                "options": {
                    "1": ("Take some herbs", "herb_theft"),
                    "2": ("Knock on the back door", "witch_encounter"),
                    "3": ("Return to the forest", "forest_path")
                }
            },
            "herb_theft": {
                "description": "As you reach for the herbs, a vine wraps around your wrist! The plants don't appreciate theft!",
                "health_change": -10,
                "options": {
                    "1": ("Apologize to the plants", "plant_forgiveness"),
                    "2": ("Cut yourself free and run", "forest_path")
                }
            },
            "plant_forgiveness": {
                "description": "Surprisingly, the plants seem to understand your apology. A different plant offers you a glowing fruit.",
                "inventory_add": "glowing fruit",
                "health_change": 15,
                "options": {
                    "1": ("Knock on the cabin door", "witch_encounter"),
                    "2": ("Return to the forest", "forest_path")
                }
            },
            "witch_encounter": {
                "description": "The door creaks open to reveal an old woman with knowing eyes. 'I've been expecting you,' she says.",
                "options": {
                    "1": ("Ask about the ancient evil", "witch_warning"),
                    "2": ("Ask for help", "witch_help"),
                    "3": ("Apologize for disturbing and leave", "forest_path")
                }
            },
            "witch_warning": {
                "description": "The witch tells you of a shadow growing in the heart of the forest, consuming all light and life. It must be stopped!",
                "options": {
                    "1": ("Ask how to stop it", "witch_quest"),
                    "2": ("Decline involvement", "forest_path")
                }
            },
            "witch_help": {
                "description": "The witch examines you thoughtfully. 'What sort of help does a wanderer like you seek in these woods?'",
                "options": {
                    "1": ("Ask about the forest's secrets", "witch_warning"),
                    "2": ("Ask for something to restore health", "witch_potion"),
                    "3": ("Ask for the way out", "witch_directions")
                }
            },
            "witch_potion": {
                "description": "The witch brews you a strange-smelling potion. 'Drink this, but be warned: my help always comes with a price.'",
                "options": {
                    "1": ("Drink the potion", "potion_effect"),
                    "2": ("Politely decline", "witch_encounter")
                }
            },
            "potion_effect": {
                "description": "The potion heals you but leaves you with a strange tingling sensation. The witch smiles mysteriously.",
                "health_change": 50,
                "options": {
                    "1": ("Ask about the ancient evil", "witch_warning"),
                    "2": ("Thank her and leave", "forest_path")
                }
            },
            "witch_directions": {
                "description": "'The way out? But you've only just arrived, and the forest has so much to show you...'",
                "options": {
                    "1": ("Insist on leaving", "forest_entrance"),
                    "2": ("Ask about the forest's secrets instead", "witch_warning")
                }
            },
            "witch_quest": {
                "description": "To defeat the shadow, you must collect items of power and bring them to the heart of darkness. Are you brave enough?",
                "options": {
                    "1": ("Accept the quest", "quest_accepted"),
                    "2": ("Ask for time to prepare", "forest_path")
                }
            },
            "quest_accepted": {
                "description": "The witch gives you a mysterious map. 'Find the items marked here. Return when you have them all.'",
                "inventory_add": "witch's map",
                "options": {
                    "1": ("Set out immediately", "forest_path"),
                    "2": ("Ask for more details", "witch_details")
                }
            },
            "witch_details": {
                "description": "You need the crystal sword, fairy charm, and the light spell. With these three, you can defeat the shadow.",
                "options": {
                    "1": ("Set out to find the items", "forest_path"),
                    "2": ("Thank the witch and leave", "forest_path")
                }
            },
            "game_end": {
                "description": "Your adventure ends here, but the forest's mysteries remain unsolved. Perhaps another day...",
                "game_over": True
            }
        }
        
        self.ascii_art = {
            "title": """
    _    _              _____                      _                   
   | |  | |            |  __ \\                    | |                  
   | |  | |_ __   ___  | |__) |__ _  ___ ___  ___| |_ ___  _ __  ___  
   | |  | | '_ \\ / _ \\ |  _  // _` |/ __/ _ \\/ __| __/ _ \\| '_ \\/ __| 
   | |__| | | | |  __/ | | \\ \\ (_| | (_|  __/ (__| || (_) | | | \\__ \\ 
    \\____/|_| |_|\\___| |_|  \\_\\__,_|\\___\\___|\\___|\\__\\___/|_| |_|___/ 
     /\\      | |              | |                                      
    /  \\   __| |_   _____ _ __ | |_ _   _ _ __ ___                     
   / /\\ \\ / _` \\ \\ / / _ \\ '_ \\| __| | | | '__/ _ \\                    
  / ____ \\ (_| |\\ V /  __/ | | | |_| |_| | | |  __/                    
 /_/    \\_\\__,_| \\_/ \\___|_| |_|\\__|\\__,_|_|  \\___|                    
     /\\                  (_) |                                         
    /  \\__      ____ _  _| |_ ___                                      
   / /\\ \\ \\ /\\ / / _` || | __/ __|                                     
  / ____ \\ V  V / (_| || | |_\\__ \\                                     
 /_/    \\_\\_/\\_/ \\__,_|/ |\\__|___/                                     
                     |__/                                              
            """,
            "forest": """
              ,@@@@@@@,
      ,,,.   ,@@@@@@/@@,  .oo8888o.
   ,&%%&%&&%,@@@@@/@@@@@@,8888\\88/8o
  ,%&\\%&&%&&%,@@@\\@@@/@@@88\\88888/88'
  %&&%&%&/%&&%@@\\@@/ /@@@88888\\88888'
  %&&%/ %&%%&&@@\\ V /@@' `88\\8 `/88'
  `&%\\ ` /%&'    |.|        \\ '|8'
      |o|        | |         | |
      |.|        | |         | |
   \\/ ._\\///_/__/  ,\\_//__\\/.  \\_//__/_
            """,
            "mushroom": """
            .-'~~~-.
          .'o  oOOOo`.
         :~~~-.oOo   o`.
          `. \\ ~-.  oOOo.
            `.; / ~.  OO:
            .'  ;-- `.o.'
           ,'  ; ~~--'~
           ;  ;
_______/\\/  ;
         /\\ ;
        / /\\;
       / / /\\\\
      / / /  \\\\
     / / /    \\\\
    / / /      \\\\
   / / /        \\\\
  / / /          \\\\
 / / /            \\\\
/ / /              \\\\
\\/                 \\\\
                    \\\\
                     \\\\
            """,
            "fairy": """
            .--.
          .'    '.
         /   __   \\
      ,  |   \\/   |  ,
     /|\\,|    |    |,/|\\
        \\|    |    |/
         |    |    |
         |    |    |
       \\/ \\__/\\__/ \\/
     _-=  OOOOOOOO  =-_
     -__=OOOOOOOOOO=__-
           ~~~~
           """,
            "cabin": """
                  (
                  )
             ____(_)____
            /__________\\
           /__|: ::|__\\
          (    |: :|    )
         (_____|: :|_____)
        (______}: :{______)
       /         :         \\
      /          :          \\
     /           :           \\
    /___________;:____________\\
            """,
            "witch": """
                   /\\
                  /  \\
                 / /\\ \\
                / /  \\ \\
               / /    \\ \\
              / / ,'`. \\ \\
             / / /     \\ \\ \\
            / / /       \\ \\ \\
           / / /         \\ \\ \\
          / / /           \\ \\ \\
       __/ / /             \\ \\ \\__
     /__/ / /               \\ \\ \\__\\
     \\__\\/,'                 `.\\/\\_/
            """
        }
        
    def clear_screen(self) -> None:
        """Clear the terminal screen."""
        os.system('cls' if os.name == 'nt' else 'clear')
        
    def type_text(self, text: str, speed: float = 0.03) -> None:
        """Display text with a typewriter effect."""
        for char in text:
            print(char, end='', flush=True)
            time.sleep(speed)
        print()
        
    def display_ascii(self, art_key: str) -> None:
        """Display ASCII art."""
        if art_key in self.ascii_art:
            print(self.ascii_art[art_key])
            
    def display_status(self) -> None:
        """Display player status."""
        print(f"\nHealth: {self.player['health']}")
        if self.player['inventory']:
            print("Inventory:", ", ".join(self.player['inventory']))
        print()
        
    def display_location(self) -> None:
        """Display current location description and options."""
        location = self.locations[self.player['location']]
        
        # Check for ASCII art for this location
        location_name = self.player['location'].split('_')[0]
        if location_name in self.ascii_art:
            self.display_ascii(location_name)
            
        self.type_text(location['description'])
        print("\nWhat would you like to do?")
        
        for key, (option_text, _) in location['options'].items():
            print(f"{key}: {option_text}")
            
    def process_location_effects(self, location_key: str) -> None:
        """Process any special effects of the current location."""
        location = self.locations[location_key]
        
        # Add item to inventory
        if 'inventory_add' in location:
            item = location['inventory_add']
            if item not in self.player['inventory']:
                self.player['inventory'].append(item)
                self.type_text(f"\nYou obtained: {item}!")
                
        # Change health
        if 'health_change' in location:
            change = location['health_change']
            self.player['health'] += change
            
            if change > 0:
                self.type_text(f"\nYou gained {change} health!")
            else:
                self.type_text(f"\nYou lost {abs(change)} health!")
                
            # Ensure health doesn't exceed 100
            self.player['health'] = min(self.player['health'], 100)
            
            # Check if player has died
            if self.player['health'] <= 0:
                self.player['health'] = 0
                self.type_text("\nYour health has fallen to zero! Game over.")
                return "game_over"
                
        return None
        
    def process_choice(self, choice: str) -> bool:
        """Process player choice and move to new location. Returns True if game should continue."""
        location = self.locations[self.player['location']]
        
        if choice in location['options']:
            _, next_location = location['options'][choice]
            self.player['location'] = next_location
            
            # Process any location effects
            result = self.process_location_effects(next_location)
            if result == "game_over":
                return False
                
            # Check if we've reached an ending
            if 'game_over' in self.locations[next_location] and self.locations[next_location]['game_over']:
                return False
                
            return True
        else:
            self.type_text("Invalid choice. Please try again.")
            return True
            
    def check_victory_conditions(self) -> bool:
        """Check if player has met victory conditions."""
        required_items = ["crystal sword", "fairy charm", "spell of light"]
        has_all_items = all(item in self.player['inventory'] for item in required_items)
        
        if has_all_items and self.player['location'] == "witch_quest":
            return True
            
        return False
        
    def start_game(self) -> None:
        """Start the adventure game."""
        self.clear_screen()
        self.display_ascii("title")
        
        self.type_text("\nWelcome to the Unexpected Adventure!", 0.05)
        self.type_text("You never know what surprises await in the magical forest...", 0.05)
        
        name = input("\nWhat is your name, brave adventurer? ")
        self.player['name'] = name if name else "Adventurer"
        
        self.type_text(f"\nWelcome, {self.player['name']}! Your journey begins now...", 0.05)
        time.sleep(1)
        
        game_running = True
        while game_running:
            self.clear_screen()
            self.display_status()
            self.display_location()
            
            if self.check_victory_conditions():
                self.clear_screen()
                self.type_text("\nCongratulations! With all three magical items, you have defeated the ancient evil!")
                self.type_text("The forest is saved, and you become a legend among the woodland creatures.")
                self.type_text(f"Thank you for playing, {self.player['name']}!")
                break
                
            choice = input("\nEnter your choice: ")
            game_running = self.process_choice(choice)
            
            if not game_running:
                self.type_text(f"\nThank you for playing, {self.player['name']}!")
                
            time.sleep(1)
            
if __name__ == "__main__":
    game = AdventureGame()
    game.start_game()