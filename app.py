import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="卡路里计算器", layout="centered")
st.title("🥗 卡路里计算器")

# 每100g的营养数据（示例）
foods = {
    "Boiled Egg (1个/53g)": {"kcal": 75.8, "protein": 6.9, "carbs": 0.6, "fat": 5.3, "sugar": 0.3, "category": "蛋白质来源"},
    "Cooked Rice": {"kcal": 130, "protein": 2.7, "carbs": 28, "fat": 0.3, "sugar": 0.1, "category": "碳水来源"},
    "Olive Oil": {"kcal": 884, "protein": 0, "carbs": 0, "fat": 100, "sugar": 0, "category": "脂肪来源"},
    "Mixed Vegetables": {"kcal": 30, "protein": 2, "carbs": 5, "fat": 0.3, "sugar": 2, "category": "蔬菜"}
}

calories_per_gram = {"carbs": 4, "fat": 9, "protein": 4}

plans = {
    "低碳日": {"carbs": 160, "protein": 500, "fat": 495},
    "中碳日": {"carbs": 240, "protein": 500, "fat": 450},
    "高碳日": {"carbs": 360, "protein": 460, "fat": 405},
}

carb_options = [f for f, v in foods.items() if v["category"] == "碳水来源"]
protein_options = [f for f, v in foods.items() if v["category"] == "蛋白质来源"]
fat_options = [f for f, v in foods.items() if v["category"] == "脂肪来源"]
veggie_options = [f for f, v in foods.items() if v["category"] == "蔬菜"]

selected_carbs = st.multiselect("🥖 选择碳水来源", carb_options)
selected_proteins = st.multiselect("💪 选择蛋白质来源", protein_options)
selected_fats = st.multiselect("🧈 选择脂肪来源", fat_options)
selected_veggies = st.multiselect("🥦 选择蔬菜", veggie_options)

selected_foods = selected_carbs + selected_proteins + selected_fats + selected_veggies
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

if submitted and selected_foods:
    for food, qty in quantities.items():
        nutrients = foods[food]
        for key in totals:
            totals[key] += nutrients[key] * qty / 100
    totals["kcal"] = totals["carbs"] * 4 + totals["fat"] * 9 + totals["protein"] * 4

    st.subheader("🧾 总结果")
    st.write(f"🔥 **总热量**: {totals['kcal']:.1f} kcal")
    st.write(f"🥖 **总碳水**: {totals['carbs']:.1f} g")
    st.write(f"🧈 **总脂肪**: {totals['fat']:.1f} g")
    st.write(f"💪 **总蛋白质**: {totals['protein']:.1f} g")

    plan = plans[selected_plan]
    st.subheader("📊 营养素差值")
    df_diff = pd.DataFrame({
        "营养素": ["carbs", "fat", "protein"],
        "实际 (kcal)": [totals["carbs"] * 4, totals["fat"] * 9, totals["protein"] * 4],
        "目标 (kcal)": [plan["carbs"], plan["fat"], plan["protein"]],
        "差值 (kcal)": [
            totals["carbs"] * 4 - plan["carbs"],
            totals["fat"] * 9 - plan["fat"],
            totals["protein"] * 4 - plan["protein"]
        ],
        "实际 (g)": [totals["carbs"], totals["fat"], totals["protein"]],
        "目标 (g)": [plan["carbs"] / 4, plan["fat"] / 9, plan["protein"] / 4],
        "差值 (g)": [
            totals["carbs"] - plan["carbs"] / 4,
            totals["fat"] - plan["fat"] / 9,
            totals["protein"] - plan["protein"] / 4
        ],
        "差值 (%)": [
            (totals["carbs"] - plan["carbs"] / 4) / (plan["carbs"] / 4) * 100,
            (totals["fat"] - plan["fat"] / 9) / (plan["fat"] / 9) * 100,
            (totals["protein"] - plan["protein"] / 4) / (plan["protein"] / 4) * 100,
        ]
    })

    def status(diff):
        if diff < -5:
            return "🔻 不足"
        elif diff > 5:
            return "🔺 过高"
        else:
            return "✅ 正常"

    df_diff["状态"] = df_diff["差值 (g)"].apply(status)
    st.dataframe(df_diff.set_index("营养素"))

   
    st.subheader("🍰 热量占比图")
    pie_data = pd.DataFrame({
        "来源": ["碳水 (kcal)", "脂肪 (kcal)", "蛋白质 (kcal)"],
        "热量": [totals["carbs"] * 4, totals["fat"] * 9, totals["protein"] * 4],
    })
    fig = px.pie(pie_data, names="来源", values="热量", hole=0.3)
    st.plotly_chart(fig)

    st.subheader("📋 复制粘贴到 Notion")
    notion_text = (
        f"📊 今日总摄入：\n"
        f"🥖 碳水：{totals['carbs']:.1f} g\n"
        f"🧈 脂肪：{totals['fat']:.1f} g\n"
        f"💪 蛋白质：{totals['protein']:.1f} g\n"
        f"🔥 热量：{totals['kcal']:.1f} kcal\n"
        f"📉 热量差值：{total_diff_kcal:+.1f} kcal"
    )
    st.text_area("复制以下内容：", notion_text)
