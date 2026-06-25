
# ─────────────────────────────────────────────
#  INFERENCE ENGINE — Diet & Meal Plan Expert System
#  Uses: Forward Chaining on RULES from knowledge_base.py
# ─────────────────────────────────────────────

import random
from knowledge_base import (
    BMI_CATEGORIES,
    FOOD_DATABASE,
    AVOID_FOODS,
    RULES,
    VALID_GOALS,
    VALID_DISEASES,
    VALID_ACTIVITY,
    VALID_GENDERS,
)


# ─────────────────────────────────────────────
#  STEP 1: CALCULATE BMI
# ─────────────────────────────────────────────

def calculate_bmi(weight_kg: float, height_cm: float) -> float:
    if height_cm <= 0 or weight_kg <= 0:
        raise ValueError("Height and weight must be positive numbers.")
    height_m = height_cm / 100
    return round(weight_kg / (height_m ** 2), 2)


def classify_bmi(bmi: float) -> str:
    for category, (low, high) in BMI_CATEGORIES.items():
        if low <= bmi <= high:
            return category
    return "unknown"


# ─────────────────────────────────────────────
#  STEP 2: CALCULATE TDEE
# ─────────────────────────────────────────────

ACTIVITY_MULTIPLIERS = {
    "sedentary": 1.2,
    "light":     1.375,
    "moderate":  1.55,
    "active":    1.725,
}

def calculate_tdee(weight_kg, height_cm, age, gender, activity_level) -> int:
    if gender == "male":
        bmr = 88.36 + (13.4 * weight_kg) + (4.8 * height_cm) - (5.7 * age)
    else:
        bmr = 447.6 + (9.2 * weight_kg) + (3.1 * height_cm) - (4.3 * age)
    return round(bmr * ACTIVITY_MULTIPLIERS[activity_level])


# ─────────────────────────────────────────────
#  STEP 3: FORWARD CHAINING ENGINE
# ─────────────────────────────────────────────

def run_forward_chaining(facts: dict) -> dict:
    conclusions = {
        "calorie_change": 0,
        "recommended_categories": [],
        "avoid_keywords": [],
        "foods_to_avoid": [],
    }

    goal     = facts.get("goal", "").lower()
    diseases = [d.lower() for d in facts.get("diseases", [])]

    for rule in RULES:
        condition = rule["if"]
        action    = rule["then"]
        matched   = False

        if "goal" in condition:
            if condition["goal"] == goal:
                matched = True

        elif "disease" in condition:
            rule_disease = condition["disease"]
            if isinstance(rule_disease, list):
                if all(d in diseases for d in rule_disease):
                    matched = True
            else:
                if rule_disease in diseases:
                    matched = True

        if matched:
            if "calorie_change" in action:
                conclusions["calorie_change"] += action["calorie_change"]
            if "recommend" in action:
                for cat in action["recommend"]:
                    if cat not in conclusions["recommended_categories"]:
                        conclusions["recommended_categories"].append(cat)
            if "avoid" in action:
                avoided = action["avoid"]
                if isinstance(avoided, list):
                    conclusions["avoid_keywords"].extend(avoided)
                else:
                    conclusions["avoid_keywords"].append(avoided)

    for disease in diseases:
        if disease in AVOID_FOODS:
            conclusions["foods_to_avoid"].extend(AVOID_FOODS[disease])

    conclusions["recommended_categories"] = list(dict.fromkeys(conclusions["recommended_categories"]))
    conclusions["avoid_keywords"]         = list(set(conclusions["avoid_keywords"]))
    conclusions["foods_to_avoid"]         = list(set(conclusions["foods_to_avoid"]))

    return conclusions


# ─────────────────────────────────────────────
#  STEP 4: MEAL PLAN GENERATOR
# ─────────────────────────────────────────────

MEAL_SLOTS = ["Breakfast", "Morning Snack", "Lunch", "Evening Snack", "Dinner"]

def build_meal_plan(recommended_categories, foods_to_avoid) -> dict:
    pool = []
    for cat in recommended_categories:
        if cat in FOOD_DATABASE:
            for item in FOOD_DATABASE[cat]:
                if item["name"] not in foods_to_avoid:
                    pool.append({**item, "category": cat})

    if len(pool) < len(MEAL_SLOTS):
        for item in FOOD_DATABASE.get("high_protein", []):
            if item["name"] not in foods_to_avoid and item not in pool:
                pool.append({**item, "category": "high_protein"})

    random.shuffle(pool)

    meal_plan = {}
    for i, slot in enumerate(MEAL_SLOTS):
        meal_plan[slot] = pool[i % len(pool)]

    return meal_plan


def calculate_meal_plan_calories(meal_plan) -> int:
    return sum(item["calories"] for item in meal_plan.values())


# ─────────────────────────────────────────────
#  STEP 5: MASTER ENGINE
# ─────────────────────────────────────────────

def generate_diet_plan(user_input: dict) -> dict:
    goal     = user_input.get("goal", "").lower()
    diseases = [d.lower() for d in user_input.get("diseases", ["none"])]

    bmi          = calculate_bmi(user_input["weight_kg"], user_input["height_cm"])
    bmi_category = classify_bmi(bmi)
    tdee         = calculate_tdee(
                       user_input["weight_kg"],
                       user_input["height_cm"],
                       user_input["age"],
                       user_input["gender"],
                       user_input["activity_level"]
                   )

    facts        = {"goal": goal, "diseases": diseases}
    conclusions  = run_forward_chaining(facts)

    target_calories    = tdee + conclusions["calorie_change"]
    meal_plan          = build_meal_plan(conclusions["recommended_categories"],
                                         conclusions["foods_to_avoid"])
    meal_plan_calories = calculate_meal_plan_calories(meal_plan)

    return {
        "user_name":              user_input.get("name", "User"),
        "bmi":                    bmi,
        "bmi_category":           bmi_category,
        "tdee":                   tdee,
        "target_calories":        target_calories,
        "calorie_change":         conclusions["calorie_change"],
        "recommended_categories": conclusions["recommended_categories"],
        "avoid_keywords":         conclusions["avoid_keywords"],
        "foods_to_avoid":         conclusions["foods_to_avoid"],
        "meal_plan":              meal_plan,
        "meal_plan_calories":     meal_plan_calories,
    }


# ─────────────────────────────────────────────
#  STEP 6: PRINT OUTPUT
# ─────────────────────────────────────────────

def print_diet_plan(result: dict):
    print("\n" + "═" * 50)
    print(f"   🥗  DIET PLAN FOR: {result['user_name'].upper()}")
    print("═" * 50)

    print(f"\n📊 BMI            : {result['bmi']}  ({result['bmi_category'].capitalize()})")
    print(f"🔥 TDEE           : {result['tdee']} kcal/day")
    print(f"🎯 Target Calories: {result['target_calories']} kcal/day", end="")
    change = result['calorie_change']
    if change != 0:
        sign = "+" if change > 0 else ""
        print(f"  ({sign}{change} adjustment)")
    else:
        print()

    if result["avoid_keywords"]:
        print(f"\n⚠️  Avoid          : {', '.join(result['avoid_keywords'])}")
    if result["foods_to_avoid"]:
        print(f"🚫 Foods to Avoid : {', '.join(result['foods_to_avoid'])}")

    print(f"\n✅ Recommended Food Categories:")
    for cat in result["recommended_categories"]:
        print(f"   • {cat.replace('_', ' ').title()}")

    print(f"\n🍽️  MEAL PLAN  (≈ {result['meal_plan_calories']} kcal total):")
    print("─" * 42)
    for slot, food in result["meal_plan"].items():
        print(f"  {slot:<18}: {food['name']:<25} ({food['calories']} kcal)")
    print("─" * 42)
    print()


# ─────────────────────────────────────────────
#  STEP 7: GET USER INPUT (Interactive Terminal)
# ─────────────────────────────────────────────

def get_user_input() -> dict:
    print("\n" + "═" * 50)
    print("      🥗  DIET PLAN EXPERT SYSTEM")
    print("═" * 50)
    print("  Please enter your details below:\n")

    # ── Name ──────────────────────────────────────
    name = input("  Your name                 : ").strip()

    # ── Age ───────────────────────────────────────
    while True:
        try:
            age = int(input("  Age (years)               : ").strip())
            if 1 <= age <= 120:
                break
            print("  ⚠  Enter a valid age (1–120).")
        except ValueError:
            print("  ⚠  Age must be a whole number.")

    # ── Gender ────────────────────────────────────
    while True:
        gender = input("  Gender (male / female)    : ").strip().lower()
        if gender in VALID_GENDERS:
            break
        print(f"  ⚠  Choose from: {VALID_GENDERS}")

    # ── Weight ────────────────────────────────────
    while True:
        try:
            weight = float(input("  Weight (kg)               : ").strip())
            if weight > 0:
                break
            print("  ⚠  Weight must be greater than 0.")
        except ValueError:
            print("  ⚠  Enter a numeric value e.g. 70 or 65.5")

    # ── Height ────────────────────────────────────
    while True:
        try:
            height = float(input("  Height (cm)               : ").strip())
            if height > 0:
                break
            print("  ⚠  Height must be greater than 0.")
        except ValueError:
            print("  ⚠  Enter a numeric value e.g. 170 or 162.5")

    # ── Activity Level ────────────────────────────
    print()
    print("  Activity levels:")
    print("    sedentary → little/no exercise")
    print("    light     → exercise 1–3 days/week")
    print("    moderate  → exercise 3–5 days/week")
    print("    active    → exercise 6–7 days/week")
    while True:
        activity = input("\n  Activity level            : ").strip().lower()
        if activity in VALID_ACTIVITY:
            break
        print(f"  ⚠  Choose from: {VALID_ACTIVITY}")

    # ── Goal ──────────────────────────────────────
    print()
    print("  Goals:")
    print("    1. lose weight")
    print("    2. gain weight")
    print("    3. maintain weight")
    while True:
        goal = input("\n  Your goal                 : ").strip().lower()
        if goal in VALID_GOALS:
            break
        print(f"  ⚠  Type exactly one of: {VALID_GOALS}")

    # ── Diseases ──────────────────────────────────
    print()
    print("  Medical conditions:")
    print("    Options : diabetes | hypertension | none")
    print("    Multiple: type  diabetes, hypertension")
    print("    Healthy : type  none")
    while True:
        raw      = input("\n  Your condition(s)         : ").strip().lower()
        diseases = [d.strip() for d in raw.split(",")]
        if all(d in VALID_DISEASES for d in diseases):
            break
        print(f"  ⚠  Valid options: {VALID_DISEASES}")

    return {
        "name":           name,
        "age":            age,
        "gender":         gender,
        "weight_kg":      weight,
        "height_cm":      height,
        "activity_level": activity,
        "goal":           goal,
        "diseases":       diseases,
    }


# ─────────────────────────────────────────────
#  MAIN — Entry Point
# ─────────────────────────────────────────────

if __name__ == "__main__":
    user_input = get_user_input()
    result     = generate_diet_plan(user_input)
    print_diet_plan(result)
