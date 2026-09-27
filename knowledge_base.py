


# ─────────────────────────────────────────────
#  SECTION 1: BMI FACTS
# ─────────────────────────────────────────────

BMI_CATEGORIES = {
    "underweight": (0, 18.4),
    "normal": (18.5, 24.9),
    "overweight": (25.0, 29.9),
    "obese": (30.0, float('inf'))
}


# ─────────────────────────────────────────────
#  SECTION 2: FOOD DATABASE
# ─────────────────────────────────────────────

FOOD_DATABASE = {

    "low_calorie": [
        {"name": "Boiled Vegetables", "calories": 50},
        {"name": "Garden Salad", "calories": 70},
        {"name": "Oats (plain)", "calories": 150},
        {"name": "Cucumber Slices", "calories": 20},
        {"name": "Apple", "calories": 95},
        {"name": "Watermelon", "calories": 85},
    ],

    "high_protein": [
        {"name": "Boiled Eggs", "calories": 155},
        {"name": "Grilled Chicken", "calories": 165},
        {"name": "Lentils (cooked)", "calories": 116},
        {"name": "Greek Yogurt", "calories": 100},
        {"name": "Tuna (canned)", "calories": 130},
        {"name": "Cottage Cheese", "calories": 110},
    ],

    "low_sugar": [
        {"name": "Whole Grain Bread", "calories": 120},
        {"name": "Broccoli", "calories": 55},
        {"name": "Mixed Berries", "calories": 70},
        {"name": "Almonds", "calories": 160},
        {"name": "Spinach", "calories": 23},
        {"name": "Cauliflower", "calories": 25},
    ],

    "low_sodium": [
        {"name": "Brown Rice", "calories": 215},
        {"name": "Sweet Potato", "calories": 103},
        {"name": "Banana", "calories": 89},
        {"name": "Unsalted Nuts", "calories": 170},
        {"name": "Homemade Oatmeal", "calories": 150},
        {"name": "Fresh Orange Juice", "calories": 112},
    ],

    "high_calorie": [
        {"name": "Peanut Butter", "calories": 190},
        {"name": "Avocado", "calories": 240},
        {"name": "Whole Milk", "calories": 149},
        {"name": "Quinoa", "calories": 222},
        {"name": "Banana Smoothie", "calories": 280},
        {"name": "Brown Bread + Eggs", "calories": 300},
    ],
}


# ─────────────────────────────────────────────
#  SECTION 3: DISEASE RESTRICTIONS
# ─────────────────────────────────────────────

AVOID_FOODS = {
    "diabetes": [
        "White Rice", "Sugary Drinks", "Candy",
        "White Bread", "Pastries", "Packaged Fruit Juice",
        "Ice Cream", "Sweetened Cereals"
    ],
    "hypertension": [
        "Salty Snacks", "Processed Meat", "Canned Soups",
        "Pickles", "Fast Food", "Salted Butter",
        "Frozen Meals", "Soy Sauce"
    ]
}


# ─────────────────────────────────────────────
#  SECTION 4: RULE BASE (IF–THEN RULES AS DATA)
# ─────────────────────────────────────────────

RULES = [

    # Weight Management Rules
    {
        "if": {"goal": "lose weight"},
        "then": {
            "calorie_change": -500,
            "recommend": ["low_calorie"]
        }
    },
    {
        "if": {"goal": "gain weight"},
        "then": {
            "calorie_change": +500,
            "recommend": ["high_calorie", "high_protein"]
        }
    },
    {
        "if": {"goal": "maintain weight"},
        "then": {
            "calorie_change": 0,
            "recommend": ["high_protein"]
        }
    },

    # Disease Rules
    {
        "if": {"disease": "diabetes"},
        "then": {
            "avoid": "sugar",
            "recommend": ["low_sugar"]
        }
    },
    {
        "if": {"disease": "hypertension"},
        "then": {
            "avoid": "salt",
            "recommend": ["low_sodium"]
        }
    },

    # Combined Disease Rule
    {
        "if": {"disease": ["diabetes", "hypertension"]},
        "then": {
            "avoid": ["processed_food", "packaged_food"]
        }
    }
]


# ─────────────────────────────────────────────
#  SECTION 5: VALID INPUTS
# ─────────────────────────────────────────────

VALID_GOALS = ["lose weight", "gain weight", "maintain weight"]

VALID_DISEASES = ["diabetes", "hypertension", "none"]

VALID_ACTIVITY = ["sedentary", "light", "moderate", "active"]

VALID_GENDERS = ["male", "female"]