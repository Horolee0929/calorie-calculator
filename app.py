import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

st.set_page_config(page_title="卡路里计算器", layout="centered")
st.title("🥗 卡路里计算器")

# 每100g的营养数据（示例）
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
    "Pork Ribs (1块/45g)": {"kcal": 262, "protein": 17, "carbs": 0, "fat": 21, "sugar": 0, "category": "蛋白质来源"},
    "Magerquark (100g)": {"kcal": 65, "protein": 11, "carbs": 4, "fat": 0.5, "sugar": 4, "category": "蛋白质来源"},
    "Chicken Drumstick (去皮, 1个/90g)": {"kcal": 155, "protein": 10, "carbs": 0, "fat": 9, "sugar": 0, "category": "蛋白质来源"},

    # 碳水来源
    "Protein Bread": {"kcal": 280, "protein": 11, "carbs": 20, "fat": 15, "sugar": 0.6, "category": "碳水来源"},
    "Oats": {"kcal": 379, "protein": 13.5, "carbs": 68, "fat": 6.5, "sugar": 1, "category": "碳水来源"},
    "Steamed Sweet Potato": {"kcal": 86, "protein": 1.6, "carbs": 20.1, "fat": 0.1, "sugar": 4.2, "category": "碳水来源"},
    "Cooked Rice": {"kcal": 130, "protein": 2.7, "carbs": 28, "fat": 0.3, "sugar": 0.1, "category": "碳水来源"},
    "Musli": {"kcal": 453, "protein": 23, "carbs": 45, "fat": 18, "sugar": 5, "category": "碳水来源"},
    "Chickpeas": {"kcal": 128, "protein": 9, "carbs": 15, "fat": 2.7, "sugar": 0.5, "category": "碳水来源"},  
    "Bread (100g)": {"kcal": 274, "protein": 11, "carbs": 45, "fat": 4.4, "sugar": 0.9, "category": "碳水来源"},
    "Banana": {"kcal": 89, "protein": 1.1, "carbs": 22.8, "fat": 0.3, "sugar": 12, "category": "碳水来源"},

    # 脂肪来源
    "Olive Oil": {"kcal": 884, "protein": 0, "carbs": 0, "fat": 100, "sugar": 0, "category": "脂肪来源"},
    "Avocado": {"kcal": 160, "protein": 2, "carbs": 8.5, "fat": 15, "sugar": 0.7, "category": "脂肪来源"},
    
    # 蔬菜
    "Mixed Vegetables": {"kcal": 30, "protein": 2, "carbs": 5, "fat": 0.3, "sugar": 2, "category": "蔬菜"},

    # snack
    "Sesam-Cracker (4块/19g)": {"kcal": 468, "protein": 13, "carbs": 53, "fat": 20, "sugar": 3, "category": "snack"},
    "Sandwich Cracks (1块/16.25g)": {"kcal": 479, "protein": 10, "carbs": 56, "fat": 23, "sugar": 4, "category": "snack"},
    "Dark Chocolate (90%)": {"kcal": 592, "protein": 10, "carbs": 14, "fat": 55, "sugar": 7, "category": "snack"},
    "Mixed Raw Nuts (Almonds, Macadamia, Cashew)": {"kcal": 657, "protein": 19, "carbs": 10, "fat": 59, "sugar": 4, "category": "snack"},
    "玉米片 (100g)": {"kcal": 421, "protein": 4.3, "carbs": 71.2, "fat": 11.3, "sugar": 0.7, "category": "snack"},
}


calories_per_gram = {"carbs": 4, "fat": 9, "protein": 4}



# 计算过程
plans = {
    "低碳日": {"carbs": 160, "protein": 500, "fat": 495},
    "中碳日": {"carbs": 240, "protein": 500, "fat": 450},
    "高碳日": {"carbs": 360, "protein": 460, "fat": 405},
}

carb_options = [f for f, v in foods.items() if v["category"] == "碳水来源"]
protein_options = [f for f, v in foods.items() if v["category"] == "蛋白质来源"]
fat_options = [f for f, v in foods.items() if v["category"] == "脂肪来源"]
veggie_options = [f for f, v in foods.items() if v["category"] == "蔬菜"]
snack_options = [f for f, v in foods.items() if v["category"] == "snack"]

selected_carbs = st.multiselect("🌾 选择碳水来源", carb_options)
selected_proteins = st.multiselect("🥚 选择蛋白质来源", protein_options)
selected_fats = st.multiselect("🥑 选择脂肪来源", fat_options)
selected_veggies = st.multiselect("🥦 选择蔬菜", veggie_options)
selected_snacks = st.multiselect("🥨 选择零食/小吃", snack_options)

selected_foods = selected_carbs + selected_proteins + selected_fats + selected_veggies + selected_snacks
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

    st.subheader("🧾 结果")
    target_range_min = 1150
    target_range_max = 1250
    st.write(f"🎯 **建议热量区间**: {target_range_min}–{target_range_max} kcal")
    st.write(f"🔥 **实际摄入热量**: {totals['kcal']:.1f} kcal")
    if totals['kcal'] < target_range_min:
        st.write(f"📉 **与建议区间差值**: {totals['kcal'] - target_range_min:.1f} kcal 🔻 不足")
    elif totals['kcal'] > target_range_max:
        st.write(f"📈 **与建议区间差值**: {totals['kcal'] - target_range_max:+.1f} kcal 🔺 过高")
    else:
        st.write("✅ 热量在建议区间内")
  
    st.write(f"🌾 **总碳水**: {totals['carbs']:.1f} g")
    st.write(f"🥑 **总脂肪**: {totals['fat']:.1f} g")
    st.write(f"🥚 **总蛋白质**: {totals['protein']:.1f} g")

    plan = plans[selected_plan]
    total_target_kcal = plan["carbs"] + plan["fat"] + plan["protein"]
    total_diff_kcal = totals["kcal"] - total_target_kcal

    
 
    st.subheader("📊 营养素差值")
    df_diff = pd.DataFrame({
        "营养素": ["碳水", "脂肪", "蛋白质"],
        "实际 (g)": [totals["carbs"], totals["fat"], totals["protein"]],
        "目标 (g)": [plan["carbs"] / 4, plan["fat"] / 9, plan["protein"] / 4],
        "差值 (g)": [
            totals["carbs"] - plan["carbs"] / 4,
            totals["fat"] - plan["fat"] / 9,
            totals["protein"] - plan["protein"] / 4
        ]
    }).set_index("营养素")

    def status(diff):
        if diff < -5:
            return "🔻 不足"
        elif diff > 5:
            return "🔺 过高"
        else:
            return "✅ 正常"

    df_diff["状态"] = df_diff["差值 (g)"].apply(status)
    st.dataframe(df_diff)

   
    st.subheader(" 热量占比图")
    pie_data = pd.DataFrame({
        "来源": ["碳水 (kcal)", "脂肪 (kcal)", "蛋白质 (kcal)"],
        "热量": [totals["carbs"] * 4, totals["fat"] * 9, totals["protein"] * 4],
    })
    fig = px.pie(pie_data, names="来源", values="热量", hole=0.3)
    st.plotly_chart(fig)


    # 💡 汇总 
    st.subheader("📋 Summary")
    st.write(f"🔥 总摄入热量：{totals['kcal']:.1f} kcal")
    st.write(f"🥖 总碳水：{totals['carbs']:.1f} g")
    st.write(f"🧈 总脂肪：{totals['fat']:.1f} g")
    st.write(f"💪 总蛋白质：{totals['protein']:.1f} g")
    st.write(f"💪 热量差值：{total_diff_kcal :.1f} kcal")
    food_details = "\n".join([
    f"{food}：{quantities[food]:.1f}g" for food in selected_foods if quantities[food] > 0
    ])


    output_text = f"""📊 今日总摄入：
   🥖 碳水：{totals['carbs']:.1f} g
   🧈 脂肪：{totals['fat']:.1f} g
   💪 蛋白质：{totals['protein']:.1f} g
   🔥 热量：{totals['kcal']:.1f} kcal
   📉 热量差值：{kcal total_diff_kcal:+.1f} kcal

   🥣 食物明细：
    {food_details}"""

    st.text_area("📎 可复制文本：", output_text)
    st.download_button(
        label="📥 下载今日饮食日志",
        data=output_text,
        file_name=f"log_{datetime.now().strftime('%Y-%m-%d')}.txt",
        mime="text/plain"
    )

    # 保存累积饮食日志（每天仅一条，覆盖同一天的旧记录）
    import os
    from datetime import datetime

    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)
    log_path = os.path.join(log_dir, "diet_log.txt")

    # 读取旧日志
    if os.path.exists(log_path):
        with open(log_path, "r", encoding="utf-8") as f:
            lines = f.read().split("\n\n📅 ")
            
        logs = {l[:10]: l for l in lines if len(l) > 10 and l[0].isdigit()}
    else:
        logs = {}

    # 更新今日记录
    today_str = datetime.now().strftime("%Y-%m-%d")
    logs[today_str] = f"📅 {today_str}\n" + output_text


    # 写入回日志
    all_dates = pd.date_range(start=min(logs.keys()), end=today_str).strftime("%Y-%m-%d")
    with open(log_path, "w", encoding="utf-8") as f:
        for d in all_dates:
            if d in logs:
                
                f.write(f"\n\n{logs[d]}")
            else: 
                f.write(f"\n\n📅 {d}\nNA")


 




    
 # 💡 推荐补充建议
    st.subheader("🔄 推荐补充")
    suggestions = []

    nutrient_map = {"carbs": "碳水", "fat": "脂肪", "protein": "蛋白质"}

    for nutrient, label in nutrient_map.items():
        try:
            diff = df_diff.loc[label, "差值 (g)"]
        except KeyError:
            continue

        if diff < -5:
            deficit = abs(diff)
            candidates = [
                (food, data) for food, data in foods.items()
                if data["category"] == {
                    "carbs": "碳水来源",
                    "fat": "脂肪来源",
                    "protein": "蛋白质来源"
                }[nutrient]
            ]
            candidates = sorted(candidates, key=lambda x: x[1][nutrient], reverse=True)
            if candidates:
                top_food, top_nutri = candidates[0]
                amount_needed = round(deficit / (top_nutri[nutrient] / 100), 1)
                suggestions.append(f"👉 {label}不足，建议补充 {amount_needed}g {top_food}")

    if suggestions:
        for s in suggestions:
            st.write(s)
    else:
        st.write("✅ 所有营养素均已达标，无需补充")
