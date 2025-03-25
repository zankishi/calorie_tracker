import json

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

def track_intake(daily_goals):
    foods = load_food_data()
    total = {"Calories": 0, "Protein": 0, "Carbs": 0, "Fat": 0}
    
    print("\nAvailable Foods: ", ", ".join(foods.keys()))

    while True:
        food_name = input("Enter food eaten (or 'done' to finish): ").title()
        if food_name.lower() == "done":
            break
        if food_name in foods:
            count = input("How many servings?")
            for key in total:
                total[key] += int(foods[food_name][key])*int(count)
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
    daily_goals = set_goals()

    while True:
        print("\n1. Add Food\n2. Track Intake\n3. Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            add_food()
        elif choice == "2":
            track_intake(daily_goals)
        elif choice == "3":
            break
        else:
            print("Invalid choice, try again.")

if __name__ == "__main__":
    main()
