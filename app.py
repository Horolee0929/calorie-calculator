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

    # 碳水来源
    "Protein Bread": {"kcal": 280, "protein": 11, "carbs": 20, "fat": 15, "sugar": 0.6, "category": "碳水来源"},
    "Oats": {"kcal": 379, "protein": 13.5, "carbs": 68, "fat": 6.5, "sugar": 1, "category": "碳水来源"},
    "Steamed Sweet Potato": {"kcal": 86, "protein": 1.6, "carbs": 20.1, "fat": 0.1, "sugar": 4.2, "category": "碳水来源"},
    "Sandwich Cracks": {"kcal": 483, "protein": 10, "carbs": 55, "fat": 23, "sugar": 3.1, "category": "碳水来源"},

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

st.subheader("输入各食物的摄入量（克）")

quantities = {}
totals = {"kcal": 0, "protein": 0, "carbs": 0, "fat": 0, "sugar": 0}

with st.form("nutrition_form"):
    for food, nutrients in foods.items():
        qty = st.number_input(f"{food}（g）", min_value=0.0, step=10.0, key=food)
        quantities[food] = qty
    selected_plan = st.selectbox("选择你的饮食计划", list(plans.keys()))
    submitted = st.form_submit_button("计算")

if submitted:
    for food, qty in quantities.items():
        nutrients = foods[food]
        for key in totals:
            totals[key] += nutrients[key] * qty / 100

    totals["kcal"] = totals["carbs"] * 4 + totals["fat"] * 9 + totals["protein"] * 4

    st.markdown("### 🧾 总结果")
    st.write(f"🔥 **总热量**: {totals['kcal']:.1f} kcal")
    st.write(f"🥖 **总碳水**: {totals['carbs']:.1f} g")
    st.write(f"🧈 **总脂肪**: {totals['fat']:.1f} g")
    st.write(f"💪 **总蛋白质**: {totals['protein']:.1f} g")

    st.markdown("### 🎯 与目标值对比：")
    plan = plans[selected_plan]
    comparison = {}
    for key in ["carbs", "protein", "fat"]:
        actual_kcal = totals[key] * calories_per_gram[key]
        target_kcal = plan[key]
        diff = actual_kcal - target_kcal
        status = "✅ 正常"
        if diff > 20:
            status = "🔺 超出"
        elif diff < -20:
            status = "🔻 不足"
        comparison[key] = {
            "实际 (kcal)": actual_kcal,
            "目标 (kcal)": target_kcal,
            "差值": diff,
            "状态": status
        }

    df_compare = pd.DataFrame(comparison).T
    st.dataframe(df_compare.style.format({"实际 (kcal)": "{:.0f}", "目标 (kcal)": "{:.0f}", "差值": "{:+.0f}"}))

    st.markdown("### 📊 热量来源比例 (饼图)")
    labels = ["碳水 (kcal)", "脂肪 (kcal)", "蛋白质 (kcal)"]
    values = [totals["carbs"] * 4, totals["fat"] * 9, totals["protein"] * 4]

    df_pie = pd.DataFrame({"来源": labels, "热量 (kcal)": values})
    fig = px.pie(df_pie, names="来源", values="热量 (kcal)", title="各营养素对总热量的贡献", hole=0.4)
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("### 📋 可复制结果")
    summary_text = (
        f"📋 今日总摄入：\n"
        f"🥖 碳水：{totals['carbs']:.1f} g\n"
        f"🧈 脂肪：{totals['fat']:.1f} g\n"
        f"💪 蛋白质：{totals['protein']:.1f} g\n"
        f"🔥 热量：{totals['kcal']:.1f} kcal"
    )
    st.text_area("📎 ", summary_text)
