


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
        {"name": "Mixed Sabzi (Low Oil)", "calories": 120},
        {"name": "Kachumbar Salad", "calories": 40},
        {"name": "Chicken Yakhni", "calories": 80},
        {"name": "Ghia Kaddu", "calories": 90},
        {"name": "Sliced Guava (Amrood)", "calories": 60},
        {"name": "Papaya", "calories": 70},
    ],

    "high_protein": [
        {"name": "Boiled Eggs", "calories": 155},
        {"name": "Chicken Tikka ", "calories": 165},
        {"name": "Dal Chana (Cooked)", "calories": 180},
        {"name": "Beef Shami Kabab (Grilled)", "calories": 200},
        {"name": "Greek Yogurt / Hung Curd", "calories": 100},
        {"name": "Grilled Fish (Rahu/Mahseer)", "calories": 150},
    ],

    "low_sugar": [
        {"name": "Whole Wheat Roti (Chakki)", "calories": 120},
        {"name": "Bhindi Masala", "calories": 110},
        {"name": "Handful of Walnuts", "calories": 180},
        {"name": "Spinach (Palak)", "calories": 40},
        {"name": "Bitter Gourd (Karela)", "calories": 50},
        {"name": "Grapefruit", "calories": 52},
    ],

    "low_sodium": [
        {"name": "Boiled Basmati Rice", "calories": 205},
        {"name": "Boiled Sweet Potato (Shakarkandi)", "calories": 110},
        {"name": "Banana", "calories": 89},
        {"name": "Unsalted Almonds", "calories": 170},
        {"name": "Plain Dalia (Porridge)", "calories": 150},
        {"name": "Fresh Pomegranate Juice", "calories": 120},
    ],

    "high_calorie": [
        {"name": "Peanut Butter & Roti", "calories": 320},
        {"name": "Egg Paratha (Low Oil)", "calories": 350},
        {"name": "Buffalo Milk (1 Cup)", "calories": 200},
        {"name": "Dates (Khajur) with Milk", "calories": 250},
        {"name": "Desi Ghee Choori (Small)", "calories": 400},
        {"name": "Almond & Raisin Mix", "calories": 280},
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