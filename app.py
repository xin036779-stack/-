import streamlit as st
import pandas as pd
import plotly.express as px

# ==================== 页面配置 ====================
st.set_page_config(
    page_title="省域数字经济发展水平分析平台",
    page_icon="📊",
    layout="wide"
)

# ==================== 深色科技风样式 ====================
st.markdown("""
<style>
.stApp {
    background-color: #08111f;
    color: #e6f1ff;
}

.block-container {
    padding-top: 1.5rem;
    padding-bottom: 2rem;
    max-width: 1500px;
}

h1, h2, h3 {
    color: #e6f1ff !important;
}

p, label {
    color: #b8c7dc;
}

[data-testid="stMetric"] {
    background: linear-gradient(135deg, #13243b, #102d42);
    border: 1px solid #1e5773;
    padding: 20px;
    border-radius: 12px;
}

[data-testid="stMetricLabel"] {
    color: #9eb9d3 !important;
}

[data-testid="stMetricValue"] {
    color: #43d9ff !important;
}

div[data-testid="stPlotlyChart"] {
    background-color: #0d1b2d;
    border-radius: 12px;
    padding: 8px;
}

hr {
    border-color: #24415d;
}
</style>
""", unsafe_allow_html=True)

# ==================== 页面标题 ====================
st.markdown(
    "<h1 style='text-align:center;color:#43d9ff !important;'>"
    "省域数字经济发展水平分析平台</h1>",
    unsafe_allow_html=True
)

st.markdown(
    "<p style='text-align:center;color:#8daac8;'>"
    "PROVINCIAL DIGITAL ECONOMY ANALYSIS PLATFORM</p >",
    unsafe_allow_html=True
)

st.divider()

# ==================== 侧边栏 ====================
st.sidebar.title("📊 系统导航")
page = st.sidebar.radio(
    "请选择功能",
    ["数据总览", "省域排名", "数据说明"]
)

st.sidebar.divider()
st.sidebar.caption("毕业设计演示原型")
st.sidebar.caption("当前展示数据为模拟数据")

# ==================== 模拟数据 ====================
# 注意：以下数值仅用于页面展示，不代表真实统计结果。
df = pd.DataFrame({
    "省份": ["广东", "江苏", "浙江", "山东", "北京",
             "上海", "福建", "四川", "湖北", "安徽"],
    "综合得分": [89, 85, 83, 77, 76, 75, 69, 66, 64, 61],
    "数字基础设施": [92, 87, 85, 79, 88, 90, 72, 67, 66, 62],
    "数字产业发展": [91, 86, 84, 78, 80, 82, 70, 68, 65, 63],
    "数字应用水平": [84, 82, 80, 74, 69, 67, 65, 63, 61, 58]
})

# ==================== 数据总览 ====================
if page == "数据总览":

    st.subheader("📈 数字经济发展概况")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("评价省份数量", "10")

    with col2:
        st.metric("评价指标维度", "3")

    with col3:
        st.metric("最高综合得分", "89.0")

    with col4:
        st.metric("平均综合得分", f"{df['综合得分'].mean():.1f}")

    st.write("")

    left, right = st.columns([1.5, 1])

    with left:
        st.markdown("### 各省数字经济综合得分")

        fig = px.bar(
            df.sort_values("综合得分", ascending=True),
            x="综合得分",
            y="省份",
            orientation="h",
            color="综合得分",
            color_continuous_scale=["#17466b", "#1cb8d9", "#73f5ff"],
            text="综合得分"
        )

        fig.update_layout(
            paper_bgcolor="#0d1b2d",
            plot_bgcolor="#0d1b2d",
            font_color="#dcecff",
            xaxis_title="综合得分（模拟）",
            yaxis_title="",
            coloraxis_showscale=False,
            margin=dict(l=10, r=20, t=20, b=20),
            height=420
        )

        fig.update_traces(textposition="outside")
        st.plotly_chart(fig, use_container_width=True)

    with right:
        st.markdown("### 评价指标维度")

        radar_df = pd.DataFrame({
            "指标": ["数字基础设施", "数字产业发展", "数字应用水平"],
            "示例得分": [
                df["数字基础设施"].mean(),
                df["数字产业发展"].mean(),
                df["数字应用水平"].mean()
            ]
        })

        fig2 = px.bar(
            radar_df,
            x="指标",
            y="示例得分",
            color="示例得分",
            color_continuous_scale=["#17466b", "#1cb8d9", "#73f5ff"],
            text_auto=".1f"
        )

        fig2.update_layout(
            paper_bgcolor="#0d1b2d",
            plot_bgcolor="#0d1b2d",
            font_color="#dcecff",
            xaxis_title="",
            yaxis_title="平均得分（模拟）",
            coloraxis_showscale=False,
            margin=dict(l=10, r=10, t=20, b=50),
            height=420
        )

        st.plotly_chart(fig2, use_container_width=True)

    st.markdown("### 🏆 省域综合评价预览")

    display_df = df[["省份", "综合得分"]].copy()
    display_df.insert(0, "排名", range(1, len(display_df) + 1))

    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True
    )

# ==================== 省域排名 ====================
elif page == "省域排名":

    st.subheader("🏆 省域数字经济综合排名")

    st.caption("以下为模拟数据，仅用于测试排名展示功能。")

    ranked_df = df.sort_values(
        "综合得分",
        ascending=False
    ).reset_index(drop=True)

    ranked_df.insert(0, "排名", range(1, len(ranked_df) + 1))

    st.dataframe(
        ranked_df,
        use_container_width=True,
        hide_index=True
    )

    selected_province = st.selectbox(
        "选择省份查看指标",
        df["省份"].tolist()
    )

    selected_data = df[df["省份"] == selected_province].iloc[0]

    st.markdown(f"### {selected_province}省指标展示")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("综合得分", selected_data["综合得分"])
    c2.metric("数字基础设施", selected_data["数字基础设施"])
    c3.metric("数字产业发展", selected_data["数字产业发展"])
    c4.metric("数字应用水平", selected_data["数字应用水平"])

# ==================== 数据说明 ====================
elif page == "数据说明":

    st.subheader("📋 数据与评价方法说明")

    st.info(
        "当前页面使用的是模拟数据，"
        "仅用于验证页面布局、图表显示和排名功能。"
        "正式研究时需要替换为有明确来源的真实统计数据。"
    )

    st.markdown("""
    **计划建设的系统功能**

    1. 省域数字经济数据导入。
    2. 数据缺失、重复及异常值检查。
    3. 数字经济评价指标体系构建。
    4. 省域数字经济发展水平综合评价。
    5. 省域排名及图表可视化。
    6. 评价结果查询与导出。

    **后续计划**

    在数据准备完成后，进一步实现真实数据读取、
    数据预处理、综合评价计算和结果展示。
    """)

st.divider()

st.markdown(
    "<p style='text-align:center;color:#617d99;'>"
    "省域数字经济发展水平综合评价系统 · 毕业设计原型"
    "</p >",
    unsafe_allow_html=True
)