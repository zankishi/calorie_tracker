import json
import random

def load_characters(filename="marvel_rivals_characters.json"):
        with open("MarvelRivalsRoulette/" + filename, "r") as file:
            data = json.load(file)
        
        return data["marvel_rivals_characters"]

def get_balanced_roster(num_players):
     marvel_rival_characters = load_characters()

     
     
     categorized = {"Vanguard": [], "Duelist": [], "Strategist": []}

     for char in marvel_rival_characters:
        categorized[char["class"]].append(char["name"])
          
     selected = []
     chosen_classes = set()

     while len(selected) < num_players:
        available_classes = [c for c in categorized if c not in chosen_classes and categorized[c]]
        
               
        if not available_classes or available_classes==[]:
            available_classes = [c for c in categorized if categorized[c]]
        print(chosen_classes)

        
        chosen_class = random.choice(available_classes)
        chosen_character = random.choice(categorized[chosen_class])

        selected.append((chosen_class, chosen_character))
        categorized[chosen_class].remove(chosen_character)
        chosen_classes.add(chosen_class)
        if len(chosen_classes) > 2:
            chosen_classes = set()
    
     class_order = {"Vanguard": 0, "Duelist": 1, "Strategist": 2}
     selected.sort(key=lambda x: class_order[x[0]])

     return [char[1] for char in selected]

def main():
    player_names = input("Enter player names (comma-separated): ").split(",")
    player_names = [name.strip() for name in player_names]
    num_players = len(player_names)

    if not (1<= num_players <= 6):
        print("Please enter between 1 and 6 players.")
        return
    
    while True:
        selected_characters = get_balanced_roster(num_players)

        print("\nCharacter Assignments:")
        for player, character in zip(player_names, selected_characters):
            print(f"{player}, {character}")

        again = input("\nReroll characters? (yes/no): ").strip().lower()
        if again != "yes":
            break
    

if __name__ == "__main__":
    main()

