def generate_profile(age):
    if 0 <= age <= 12:
        return "Child"
    if 13 <= age <= 19:
        return "Teenager"
    if age >= 20 :
        return "Adult"


 # Get user input
user_name = input("Enter your full name:")
birth_year_str = input("Enter your birth year:")

# Convert and calculate age
current_year = 2025
current_age = current_year - int(birth_year_str)

# Record hobbies
hobbies = []
while True:
    hobby=input("Enter a favorite hobby or type 'stop' to finish:")
    if hobby == 'stop':
        break
    hobbies.append(hobby)

# Process and generate profile
life_stage = generate_profile(current_age)

# Create profile dictionary
user_profile = {
    "name": user_name,
    "age": current_age,
    "stage": life_stage,
    "hobbies": hobbies
}

# Display output
print("\n","-"*10)
print("Profile Summary:")
print(f"Name: {user_profile['name']}")
print(f"Age: {user_profile['age']}")
print(f"Life Stage: {user_profile['stage']}")
if len(hobbies)==0:
    print("You didn't mention any hobbies.")
else:
    print(f"Favorite Hobbies ({len(hobbies)}):")
    for hobby in user_profile['hobbies']:
        print(f"- {hobby}")
print("\n","-"*10)

