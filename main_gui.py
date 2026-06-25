import customtkinter as ctk
from tkinter import messagebox

# Import logic from your Inference Engine file 
# (Assuming your file is named inference_engine.py)
from inference_engine import generate_diet_plan

# Import constants from your Knowledge Base file
# (Assuming your file is named knowledge_base.py)
from knowledge_base import VALID_GOALS, VALID_ACTIVITY, VALID_GENDERS

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class DietExpertGUI(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("AI Diet Expert System")
        self.geometry("650x900")

        # --- Header ---
        self.header = ctk.CTkLabel(self, text="🥗 Diet Plan Expert System", font=("Roboto", 24, "bold"))
        self.header.pack(pady=20)

        # --- Main Container ---
        self.scroll_frame = ctk.CTkScrollableFrame(self, width=600, height=800)
        self.scroll_frame.pack(pady=10, padx=20, fill="both", expand=True)

        # User Inputs
        self.name_entry = self.add_input("Full Name:", "Enter your name")
        self.age_entry = self.add_input("Age:", "e.g. 25")
        
        # Dropdowns
        self.gender_var = self.add_dropdown("Gender:", VALID_GENDERS)
        self.weight_entry = self.add_input("Weight (kg):", "e.g. 70")
        self.height_entry = self.add_input("Height (cm):", "e.g. 175")
        self.activity_var = self.add_dropdown("Activity Level:", VALID_ACTIVITY)
        self.goal_var = self.add_dropdown("Primary Goal:", VALID_GOALS)

        # Checkboxes for Diseases
        ctk.CTkLabel(self.scroll_frame, text="Medical Conditions:", font=("Roboto", 14, "bold")).pack(anchor="w", padx=20, pady=(15, 5))
        self.diabetes_var = ctk.BooleanVar()
        self.hypertension_var = ctk.BooleanVar()
        
        cb_frame = ctk.CTkFrame(self.scroll_frame, fg_color="transparent")
        cb_frame.pack(fill="x", padx=20)
        ctk.CTkCheckBox(cb_frame, text="Diabetes", variable=self.diabetes_var).pack(side="left", padx=10)
        ctk.CTkCheckBox(cb_frame, text="Hypertension", variable=self.hypertension_var).pack(side="left", padx=10)

        # Submit Button
        self.submit_btn = ctk.CTkButton(self.scroll_frame, text="GENERATE DIET PLAN", 
                                        command=self.process_input, height=45, font=("Roboto", 14, "bold"))
        self.submit_btn.pack(pady=30, padx=20, fill="x")

        # Result Display
        self.result_box = ctk.CTkTextbox(self.scroll_frame, height=350, font=("Consolas", 13))
        self.result_box.pack(pady=10, padx=20, fill="x")

    def add_input(self, label, placeholder):
        ctk.CTkLabel(self.scroll_frame, text=label, font=("Roboto", 12, "bold")).pack(anchor="w", padx=20, pady=(10, 0))
        entry = ctk.CTkEntry(self.scroll_frame, placeholder_text=placeholder)
        entry.pack(fill="x", padx=20, pady=5)
        return entry

    def add_dropdown(self, label, values):
        ctk.CTkLabel(self.scroll_frame, text=label, font=("Roboto", 12, "bold")).pack(anchor="w", padx=20, pady=(10, 0))
        var = ctk.StringVar(value=values[0])
        menu = ctk.CTkOptionMenu(self.scroll_frame, values=values, variable=var)
        menu.pack(fill="x", padx=20, pady=5)
        return var

    def process_input(self):
        try:
            # Collect health conditions
            diseases = []
            if self.diabetes_var.get(): diseases.append("diabetes")
            if self.hypertension_var.get(): diseases.append("hypertension")
            if not diseases: diseases = ["none"]

            # Prepare data for the Inference Engine
            user_data = {
                "name": self.name_entry.get(),
                "age": int(self.age_entry.get()),
                "gender": self.gender_var.get(),
                "weight_kg": float(self.weight_entry.get()),
                "height_cm": float(self.height_entry.get()),
                "activity_level": self.activity_var.get(),
                "goal": self.goal_var.get(),
                "diseases": diseases
            }

            # Call the function from your inference_engine.py
            report = generate_diet_plan(user_data)
            self.show_report(report)

        except ValueError:
            messagebox.showerror("Input Error", "Please check that Age, Weight, and Height are numbers.")

    def show_report(self, r):
        self.result_box.delete("1.0", "end")
        
        text = f"📋 DIET REPORT FOR: {r['user_name'].upper()}\n"
        text += "═" * 45 + "\n"
        text += f"Status  : {r['bmi_category'].upper()} (BMI: {r['bmi']})\n"
        text += f"Daily Burn (TDEE): {r['tdee']} kcal\n"
        text += f"Target Intake    : {r['target_calories']} kcal/day\n"
        
        if r['foods_to_avoid']:
            text += f"\n🚫 AVOID: {', '.join(r['foods_to_avoid'])}\n"
        
        text += "\n🍽️ GENERATED MEAL PLAN:\n"
        text += "─" * 45 + "\n"
        for slot, food in r['meal_plan'].items():
            text += f"{slot:15}: {food['name']} ({food['calories']} kcal)\n"
        
        text += "─" * 45 + "\n"
        text += f"Total Calories: ~{r['meal_plan_calories']} kcal"
        
        self.result_box.insert("0.0", text)

if __name__ == "__main__":
    app = DietExpertGUI()
    app.mainloop()