import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="卡路里计算器", layout="centered")
st.title("🥗 卡路里计算器")

# 每100g的营养数据
foods = {
    # 蛋白质来源
    "Cottage Cheese": {"kcal": 87, "protein": 10, "carbs": 2.7, "fat": 4, "sugar": 1.7, "category": "蛋白质来源"},
    "Salmon (raw)": {"kcal": 188, "protein": 20, "carbs": 0.5, "fat": 12, "sugar": 0, "category": "蛋白质来源"},
    "Beef Steak": {"kcal": 172, "protein": 20, "carbs": 0.5, "fat": 10, "sugar": 0, "category": "蛋白质来源"},
    "Chicken Breast": {"kcal": 125, "protein": 22, "carbs": 2.7, "fat": 2.8, "sugar": 0, "category": "蛋白质来源"},
    "Shrimp": {"kcal": 85, "protein": 20, "carbs": 0, "fat": 0.5, "sugar": 0, "category": "蛋白质来源"},
    "Tofu": {"kcal": 126, "protein": 13, "carbs": 0, "fat": 7, "sugar": 0, "category": "蛋白质来源"},
    "Greek Yogurt 2": {"kcal": 58, "protein": 11, "carbs": 3.5, "fat": 0, "sugar": 3.4, "category": "蛋白质来源"},
    "Boiled Egg (1个/53g)": {"kcal": 75.8, "protein": 6.9, "carbs": 0.6, "fat": 5.3, "sugar": 0.3, "category": "蛋白质来源"},

    # 碳水来源
    "Protein Bread": {"kcal": 280, "protein": 11, "carbs": 20, "fat": 15, "sugar": 0.6, "category": "碳水来源"},
    "Oats": {"kcal": 379, "protein": 13.5, "carbs": 68, "fat": 6.5, "sugar": 1, "category": "碳水来源"},
    "Steamed Sweet Potato": {"kcal": 86, "protein": 1.6, "carbs": 20.1, "fat": 0.1, "sugar": 4.2, "category": "碳水来源"},
    "Sandwich Cracks": {"kcal": 483, "protein": 10, "carbs": 55, "fat": 23, "sugar": 3.1, "category": "碳水来源"},
    "Cooked Rice": {"kcal": 130, "protein": 2.7, "carbs": 28, "fat": 0.3, "sugar": 0.1, "category": "碳水来源"},

    # 脂肪来源
    "Olive Oil": {"kcal": 884, "protein": 0, "carbs": 0, "fat": 100, "sugar": 0, "category": "脂肪来源"},
    "Avocado": {"kcal": 160, "protein": 2, "carbs": 8.5, "fat": 15, "sugar": 0.7, "category": "脂肪来源"},
    "Mixed Raw Nuts (Almonds, Macadamia, Cashew)": {"kcal": 657, "protein": 19, "carbs": 10, "fat": 59, "sugar": 4, "category": "脂肪来源"},
    "Dark Chocolate (85%)": {"kcal": 592, "protein": 10, "carbs": 14, "fat": 55, "sugar": 7, "category": "脂肪来源"},

    # 蔬菜
    "Mixed Vegetables": {"kcal": 30, "protein": 2, "carbs": 5, "fat": 0.3, "sugar": 2, "category": "蔬菜"},
}

# 每克热量
calories_per_gram = {"carbs": 4, "fat": 9, "protein": 4}

# 目标摄入计划
plans = {
    "低碳日": {"carbs": 160, "protein": 500, "fat": 495},
    "中碳日": {"carbs": 240, "protein": 500, "fat": 450},
    "高碳日": {"carbs": 360, "protein": 460, "fat": 405},
}

st.subheader("选择食物并输入摄入量")

selected_foods = st.multiselect("选择今天吃过的食物", list(foods.keys()))
quantities = {}
totals = {"kcal": 0, "protein": 0, "carbs": 0, "fat": 0, "sugar": 0}

with st.form("nutrition_form"):
    for food in selected_foods:
        unit = "个" if "Boiled Egg" in food else "g"
        qty = st.number_input(f"{food}（{unit}）", min_value=0.0, step=1.0 if unit == "个" else 10.0, key=food)
        gram_qty = qty * 53 if unit == "个" else qty
        quantities[food] = gram_qty
    selected_plan = st.selectbox("选择你的饮食计划", list(plans.keys()))
    submitted = st.form_submit_button("计算")
