import { useState } from "react";

// ---------------------------------------------------------------------------
// Diet Plan Settings Form
// Self-contained, dependency-free (besides React) form for configuring a
// user's diet plan: calorie target, macro split, meals per day, goal,
// activity level, and dietary restrictions/allergies — with full validation.
// Drop this file into any React project (Vite, Next.js, CRA, etc.).
// ---------------------------------------------------------------------------

const GOALS = [
  { value: "lose", label: "Lose weight" },
  { value: "maintain", label: "Maintain weight" },
  { value: "gain", label: "Gain weight" },
];

const ACTIVITY_LEVELS = [
  { value: "sedentary", label: "Sedentary (little to no exercise)" },
  { value: "light", label: "Light (1–3 days/week)" },
  { value: "moderate", label: "Moderate (3–5 days/week)" },
  { value: "active", label: "Active (6–7 days/week)" },
  { value: "athlete", label: "Athlete (2x/day, intense training)" },
];

const DIET_TYPES = [
  { value: "none", label: "No specific diet" },
  { value: "vegetarian", label: "Vegetarian" },
  { value: "vegan", label: "Vegan" },
  { value: "keto", label: "Keto" },
  { value: "paleo", label: "Paleo" },
  { value: "mediterranean", label: "Mediterranean" },
];

const DEFAULTS = {
  calorieTarget: "2000",
  mealsPerDay: "3",
  goal: "maintain",
  activityLevel: "moderate",
  dietType: "none",
  proteinPct: "30",
  carbsPct: "40",
  fatPct: "30",
  allergies: "",
};

function validate(values) {
  const errors = {};

  const calories = Number(values.calorieTarget);
  if (values.calorieTarget.trim() === "") {
    errors.calorieTarget = "Enter a daily calorie target.";
  } else if (!Number.isFinite(calories) || calories <= 0) {
    errors.calorieTarget = "Calorie target must be a positive number.";
  } else if (calories < 1000 || calories > 6000) {
    errors.calorieTarget = "Enter a value between 1,000 and 6,000 kcal.";
  }

  const meals = Number(values.mealsPerDay);
  if (values.mealsPerDay.trim() === "") {
    errors.mealsPerDay = "Enter how many meals per day.";
  } else if (!Number.isInteger(meals) || meals < 1 || meals > 8) {
    errors.mealsPerDay = "Meals per day must be a whole number from 1 to 8.";
  }

  if (!GOALS.some((g) => g.value === values.goal)) {
    errors.goal = "Choose a goal.";
  }

  if (!ACTIVITY_LEVELS.some((a) => a.value === values.activityLevel)) {
    errors.activityLevel = "Choose an activity level.";
  }

  const protein = Number(values.proteinPct);
  const carbs = Number(values.carbsPct);
  const fat = Number(values.fatPct);
  const macroFields = [
    ["proteinPct", protein, "Protein"],
    ["carbsPct", carbs, "Carbs"],
    ["fatPct", fat, "Fat"],
  ];
  for (const [key, val, label] of macroFields) {
    if (values[key].trim() === "" || !Number.isFinite(val)) {
      errors[key] = `${label} % is required.`;
    } else if (val < 0 || val > 100) {
      errors[key] = `${label} % must be between 0 and 100.`;
    }
  }
  if (!errors.proteinPct && !errors.carbsPct && !errors.fatPct) {
    const sum = protein + carbs + fat;
    if (Math.round(sum) !== 100) {
      const msg = `Protein, carbs, and fat must add up to 100% (currently ${sum}%).`;
      errors.proteinPct = errors.proteinPct || msg;
      errors.macroSum = msg;
    }
  }

  if (values.allergies.length > 200) {
    errors.allergies = "Keep allergies/exclusions under 200 characters.";
  }

  return errors;
}

export default function DietPlanSettingsForm({ onSave } = {}) {
  const [values, setValues] = useState(DEFAULTS);
  const [errors, setErrors] = useState({});
  const [touched, setTouched] = useState({});
  const [savedAt, setSavedAt] = useState(null);

  const setField = (name) => (e) => {
    const val = e.target.value;
    setValues((v) => ({ ...v, [name]: val }));
    setSavedAt(null);
  };

  const markTouched = (name) => () =>
    setTouched((t) => ({ ...t, [name]: true }));

  const handleSubmit = (e) => {
    e.preventDefault();
    const nextErrors = validate(values);
    setErrors(nextErrors);
    setTouched({
      calorieTarget: true,
      mealsPerDay: true,
      goal: true,
      activityLevel: true,
      proteinPct: true,
      carbsPct: true,
      fatPct: true,
      allergies: true,
    });

    if (Object.keys(nextErrors).length === 0) {
      const payload = {
        ...values,
        calorieTarget: Number(values.calorieTarget),
        mealsPerDay: Number(values.mealsPerDay),
        proteinPct: Number(values.proteinPct),
        carbsPct: Number(values.carbsPct),
        fatPct: Number(values.fatPct),
      };
      setSavedAt(new Date());
      if (typeof onSave === "function") onSave(payload);
    }
  };

  const showError = (name) => touched[name] && errors[name];

  return (
    <form onSubmit={handleSubmit} noValidate style={styles.form}>
      <div style={styles.header}>
        <h2 style={styles.title}>Diet plan settings</h2>
        <p style={styles.subtitle}>
          Set your targets once — meals and macros adjust to match.
        </p>
      </div>

      <div style={styles.grid}>
        <Field
          label="Daily calorie target"
          suffix="kcal"
          error={showError("calorieTarget")}
        >
          <input
            type="number"
            value={values.calorieTarget}
            onChange={setField("calorieTarget")}
            onBlur={markTouched("calorieTarget")}
            style={styles.input}
            min="1000"
            max="6000"
          />
        </Field>

        <Field label="Meals per day" error={showError("mealsPerDay")}>
          <input
            type="number"
            value={values.mealsPerDay}
            onChange={setField("mealsPerDay")}
            onBlur={markTouched("mealsPerDay")}
            style={styles.input}
            min="1"
            max="8"
          />
        </Field>

        <Field label="Goal" error={showError("goal")}>
          <select
            value={values.goal}
            onChange={setField("goal")}
            onBlur={markTouched("goal")}
            style={styles.input}
          >
            {GOALS.map((g) => (
              <option key={g.value} value={g.value}>
                {g.label}
              </option>
            ))}
          </select>
        </Field>

        <Field label="Activity level" error={showError("activityLevel")}>
          <select
            value={values.activityLevel}
            onChange={setField("activityLevel")}
            onBlur={markTouched("activityLevel")}
            style={styles.input}
          >
            {ACTIVITY_LEVELS.map((a) => (
              <option key={a.value} value={a.value}>
                {a.label}
              </option>
            ))}
          </select>
        </Field>

        <Field label="Diet type">
          <select
            value={values.dietType}
            onChange={setField("dietType")}
            style={styles.input}
          >
            {DIET_TYPES.map((d) => (
              <option key={d.value} value={d.value}>
                {d.label}
              </option>
            ))}
          </select>
        </Field>
      </div>

      <fieldset style={styles.fieldset}>
        <legend style={styles.legend}>Macro split (% of calories)</legend>
        <div style={styles.macroRow}>
          <Field label="Protein" compact error={showError("proteinPct")}>
            <input
              type="number"
              value={values.proteinPct}
              onChange={setField("proteinPct")}
              onBlur={markTouched("proteinPct")}
              style={styles.input}
              min="0"
              max="100"
            />
          </Field>
          <Field label="Carbs" compact error={showError("carbsPct")}>
            <input
              type="number"
              value={values.carbsPct}
              onChange={setField("carbsPct")}
              onBlur={markTouched("carbsPct")}
              style={styles.input}
              min="0"
              max="100"
            />
          </Field>
          <Field label="Fat" compact error={showError("fatPct")}>
            <input
              type="number"
              value={values.fatPct}
              onChange={setField("fatPct")}
              onBlur={markTouched("fatPct")}
              style={styles.input}
              min="0"
              max="100"
            />
          </Field>
        </div>
        {touched.carbsPct && errors.macroSum && (
          <p style={styles.errorText}>{errors.macroSum}</p>
        )}
      </fieldset>

      <Field label="Allergies / foods to exclude" error={showError("allergies")}>
        <textarea
          value={values.allergies}
          onChange={setField("allergies")}
          onBlur={markTouched("allergies")}
          placeholder="e.g. peanuts, shellfish, dairy"
          style={{ ...styles.input, ...styles.textarea }}
          maxLength={200}
        />
      </Field>

      <div style={styles.footer}>
        <button type="submit" style={styles.button}>
          Save diet plan
        </button>
        {savedAt && (
          <span style={styles.savedNote}>
            Saved at {savedAt.toLocaleTimeString()}
          </span>
        )}
      </div>
    </form>
  );
}

function Field({ label, children, error, suffix, compact }) {
  return (
    <label style={{ ...styles.field, ...(compact ? styles.fieldCompact : {}) }}>
      <span style={styles.label}>{label}</span>
      <div style={styles.inputWrap}>
        {children}
        {suffix && <span style={styles.suffix}>{suffix}</span>}
      </div>
      {error && <span style={styles.errorText}>{error}</span>}
    </label>
  );
}

const styles = {
  form: {
    maxWidth: 640,
    margin: "0 auto",
    padding: 28,
    fontFamily:
      "-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif",
    background: "#F7F6F2",
    border: "1px solid #E3E0D6",
    borderRadius: 10,
    color: "#26312B",
  },
  header: { marginBottom: 20 },
  title: { fontSize: 22, fontWeight: 600, margin: 0, color: "#1E3A2E" },
  subtitle: { fontSize: 14, color: "#5B6A61", marginTop: 6 },
  grid: {
    display: "grid",
    gridTemplateColumns: "repeat(auto-fit, minmax(220px, 1fr))",
    gap: 16,
    marginBottom: 20,
  },
  fieldset: {
    border: "1px solid #E3E0D6",
    borderRadius: 8,
    padding: "14px 16px 18px",
    marginBottom: 20,
  },
  legend: { fontSize: 13, fontWeight: 600, color: "#3E4C44", padding: "0 4px" },
  macroRow: { display: "flex", gap: 12 },
  field: { display: "flex", flexDirection: "column", fontSize: 13 },
  fieldCompact: { flex: 1 },
  label: { fontWeight: 500, marginBottom: 6, color: "#3E4C44" },
  inputWrap: { position: "relative", display: "flex", alignItems: "center" },
  input: {
    width: "100%",
    padding: "8px 10px",
    fontSize: 14,
    border: "1px solid #CBC6B8",
    borderRadius: 6,
    background: "#FFFFFF",
    color: "#26312B",
    boxSizing: "border-box",
  },
  textarea: { minHeight: 64, resize: "vertical", fontFamily: "inherit" },
  suffix: {
    position: "absolute",
    right: 10,
    fontSize: 12,
    color: "#8A8577",
    pointerEvents: "none",
  },
  errorText: {
    color: "#B3413A",
    fontSize: 12,
    marginTop: 6,
  },
  footer: {
    display: "flex",
    alignItems: "center",
    gap: 12,
    marginTop: 8,
  },
  button: {
    padding: "10px 20px",
    fontSize: 14,
    fontWeight: 600,
    color: "#F7F6F2",
    background: "#1E3A2E",
    border: "none",
    borderRadius: 6,
    cursor: "pointer",
  },
  savedNote: { fontSize: 13, color: "#5B6A61" },
};