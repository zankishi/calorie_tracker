import json

def load_user_data():
    try:
        with open("users.json", "r") as file:
            content = file.read().strip()
            return json.loads(content) if content else {}
    except (FileNotFoundError, json.JSONDecodeError):
        return {}
    
def save_user_data(users):
    with open("users.json", "w") as file:
        json.dump(users, file, indent =4)

def select_user():
    users = load_user_data()

    if users:
        print("\nExisting Users:", ", ".join(users.keys()))

    username = input("Enter your name (or type 'new' to create a new profile): ").title()

    if username.lower() == "new":
        username = input("Enter a new username: ").title()
        if username in users:
            print("User already exists! Logging in.")
        else:
            users[username] = set_goals()
            save_user_data(users)
            print(f"New profile created for {username}!")
    
    elif username not in users:
        print("User not found! Creating a new profile.")
        users[username] = set_goals()
        save_user_data(users)

    return username, users[username]

def load_food_data():
    try: 
        with open("foods.json","r") as file:
            content = file.read().strip()
            data = json.loads(content) if content else {}
            
            return data
    except (FileNotFoundError, json.JSONDecodeError):
        print("Error: foods.json is missing or corrupted.")
        return{}
    
def save_food_data(data):
    with open("foods.json","w") as file:
        json.dump(data, file, indent=4)

def add_food():
    food_name = input("Enter Food Name: ").title()
    calories = int(input("Enter Calories: "))
    protein = float(input("Enter Protein (g): "))
    carbs = float(input("Enter Carbs (g): "))
    fat = float(input("Enter Fat (g): "))

    foods = load_food_data()
    foods[food_name] = {"Calories": calories, "Protein": protein, "Carbs": carbs, "Fat": fat,}
    save_food_data(foods)
    print(f"{food_name} added successfully!\n")

def add_meal():
    foods = load_food_data()

    if "Meals" not in foods:
        foods["Meals"] = {}

    meal_name = input("Enter Meal Name: ").title()
    meal_components = {}

    print("\nAvailable Foods:")
    for food in foods.keys():
        if food != "Meals":
            print(f"- {food}")

    while True:
        food_name = input("Add a food (or type 'done' to finish): ").title()
        if food_name.lower() == "done":
            break
        if food_name in foods:
            servings = int(input(f"How many servings of {food_name}? "))
            meal_components[food_name] = servings
        else:
            print(f"{food_name} not found. Please add it first.")

    foods["Meals"][meal_name] = meal_components
    save_food_data(foods)
    print(f"{meal_name} added successfully as a preset meal!\n")

def track_intake(daily_goals):
    foods = load_food_data()
    total = {"Calories": 0, "Protein": 0, "Carbs": 0, "Fat": 0}
    
    food_items = [food for food in foods.keys() if food != "Meals"]
    meal_items = list(foods.get("Meals", {}).keys())

    print("\nAvailable Foods:")
    print(", ".join(food_items) if food_items else "No foods available.")

    print("\nAvailable Meals:")
    print(", ".join(meal_items) if meal_items else "No meals available.")

    while True:
        food_name = input("\nEnter food or meal eaten (or 'done' to finish): ").title()
        if food_name.lower() == "done":
            break

        if food_name in foods:
            count = int(input("How many servings of {food_name}?"))
            for key in total:
                total[key] += foods[food_name][key] * count

        elif food_name in foods.get("Meals", {}):
            count = int(input(f"How many servings of {food_name}? "))
            for ingredient, qty in foods["Meals"][food_name].items():
                for key in total:
                    total[key] += foods[ingredient][key] * qty * count
        else:
                print("Food not found. Please add it to the system.")
        
        print("\nDaily Intake:")
        for key, value in total.items():
            print(f"{key}: {value} (Goal: {daily_goals[key]})")

def set_goals():
    return {
        "Calories": int(input("Enter daily Calorie goal: ")),
        "Protein": float(input("Enter daily Protein goal (g): ")),
        "Carbs": float(input("Enter daily Carbs goal (g): ")),
        "Fat": float(input("Enter daily Fat goal (g): "))
    }

def main():
    print("Calorie Tracker")
    username, daily_goals = select_user()

    while True:
        print(f"\nUser: {username}")
        print("\n1. Add Food\n2. Add Meal\n3 Track Intake\n4. Change goals\n5. Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            add_food()
        elif choice == "2":
            add_meal()
        elif choice == "3":
            track_intake(load_user_data().get(username, {}))
        elif choice == "4":
            daily_goals = set_goals()
            users = load_user_data()
            users[username] = daily_goals
            save_user_data(users)
            print("Goals updated successfully!")
        elif choice == "5":
            break
        else:
            print("Invalid choice, try again.")

if __name__ == "__main__":
    main()

### Notes To Achieve:
### Make user profiles, make combinations of regularly used foods(Breakfast, Protein Shake, etc,), Add more macros such as sodium values