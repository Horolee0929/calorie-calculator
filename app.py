import streamlit as st

st.set_page_config(page_title="卡路里计算器", layout="centered")
st.title("🥗 卡路里计算器")

# 每100g的营养数据
foods = {
    "Cottage Cheese": {"kcal": 87, "protein": 10, "carbs": 2.7, "fat": 4, "sugar": 1.7},
    "Protein Bread": {"kcal": 280, "protein": 11, "carbs": 20, "fat": 15, "sugar": 0.6},
    "Salmon (raw)": {"kcal": 188, "protein": 20, "carbs": 0.5, "fat": 12, "sugar": 0},
    "Beef Steak": {"kcal": 172, "protein": 20, "carbs": 0.5, "fat": 10, "sugar": 0},
    "Chicken Breast": {"kcal": 125, "protein": 22, "carbs": 2.7, "fat": 2.8, "sugar": 0},
    "Shrimp": {"kcal": 85, "protein": 20, "carbs": 0, "fat": 0.5, "sugar": 0},
    "Greek Yogurt 2": {"kcal": 58, "protein": 11, "carbs": 3.5, "fat": 0, "sugar": 3.4},
    "Sandwich Cracks": {"kcal": 483, "protein": 10, "carbs": 55, "fat": 23, "sugar": 3.1},
    "Mixed Vegetables": {"kcal": 30, "protein": 2, "carbs": 5, "fat": 0.3, "sugar": 2},
    "Oats": {"kcal": 379, "protein": 13.5, "carbs": 68, "fat": 6.5, "sugar": 1},
    "Steamed Sweet Potato": {"kcal": 86, "protein": 1.6, "carbs": 20.1, "fat": 0.1, "sugar": 4.2}
}

st.subheader("输入各食物的摄入量（克）")

quantities = {}
totals = {"kcal": 0, "protein": 0, "carbs": 0, "fat": 0, "sugar": 0}

with st.form("nutrition_form"):
    for food, nutrients in foods.items():
        qty = st.number_input(f"{food}（g）", min_value=0.0, step=10.0, key=food)
        quantities[food] = qty
    submitted = st.form_submit_button("计算")

if submitted:
    for food, qty in quantities.items():
        nutrients = foods[food]
        for key in totals:
            totals[key] += nutrients[key] * qty / 100

    st.markdown("### 🧾 结果")
    st.write(f"🔸 **总热量**: {totals['kcal']:.1f} kcal")
    st.write(f"💪 **蛋白质**: {totals['protein']:.1f} g")
    st.write(f"🥖 **碳水化合物**: {totals['carbs']:.1f} g")
    st.write(f"🧈 **脂肪**: {totals['fat']:.1f} g")
    st.write(f"🍬 **糖**: {totals['sugar']:.1f} g")
