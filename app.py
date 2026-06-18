# ============================================================
# BÀI TẬP TRỰC QUAN HÓA DỮ LIỆU
# Chủ đề: AI Agent JobFit Lab
# Mục tiêu: Xây dựng bản đồ lựa chọn nhiệm vụ phù hợp
# để giao cho AI Agent trong ngành Khoa học máy tính
# ============================================================

import streamlit as st
import pandas as pd
import plotly.express as px


# ============================================================
# 1. CẤU HÌNH TRANG
# ============================================================

st.set_page_config(
    page_title="AI Agent JobFit Lab",
    layout="wide"
)

st.title("AI Agent JobFit Lab")

st.markdown("""
### Bản đồ lựa chọn nhiệm vụ phù hợp để giao cho AI Agent trong ngành Khoa học máy tính

Dashboard này tập trung trả lời một câu hỏi chính:

> **Nhiệm vụ nào nên giao cho AI Agent, nhiệm vụ nào chỉ nên để AI hỗ trợ, và nhiệm vụ nào vẫn cần con người kiểm soát?**

Dữ liệu được phân tích từ các nhóm nghề thuộc lĩnh vực **Khoa học máy tính**, kết hợp giữa
đánh giá của chuyên gia, mong muốn tự động hóa của người lao động và đặc điểm của từng nhiệm vụ.
""")


# ============================================================
# 2. ĐỌC DỮ LIỆU
# Ghi chú:
# - app.py nằm ngoài thư mục data
# - 4 file CSV nằm trong thư mục data
# ============================================================

@st.cache_data
def load_data():
    task_df = pd.read_csv("data/task_statement_with_metadata.csv")
    expert_df = pd.read_csv("data/expert_rated_technological_capability.csv")
    worker_df = pd.read_csv("data/domain_worker_desires.csv")
    meta_df = pd.read_csv("data/domain_worker_metadata.csv")
    return task_df, expert_df, worker_df, meta_df


try:
    task_df, expert_df, worker_df, meta_df = load_data()
except FileNotFoundError:
    st.error("""
    Không tìm thấy file dữ liệu. Hãy kiểm tra lại cấu trúc thư mục:

    BÀI TẬP TRỰC QUAN HÓA DỮ LIỆU/
    ├── app.py
    └── data/
        ├── domain_worker_desires.csv
        ├── domain_worker_metadata.csv
        ├── expert_rated_technological_capability.csv
        └── task_statement_with_metadata.csv
    """)
    st.stop()


# ============================================================
# 3. LỌC NHÓM NGHỀ KHOA HỌC MÁY TÍNH
# Ghi chú:
# Chỉ chọn các nghề liên quan đến lập trình, web,
# dữ liệu, hệ thống, bảo mật, kiểm thử và quản trị CNTT.
# ============================================================

cs_jobs = [
    "Business Intelligence Analysts",
    "Computer Network Support Specialists",
    "Computer Programmers",
    "Computer Systems Analysts",
    "Computer Systems Engineers/Architects",
    "Computer User Support Specialists",
    "Computer and Information Research Scientists",
    "Computer and Information Systems Managers",
    "Database Administrators",
    "Information Security Analysts",
    "Information Technology Project Managers",
    "Network and Computer Systems Administrators",
    "Software Quality Assurance Analysts and Testers",
    "Web Administrators",
    "Web Developers"
]

task_cs = task_df[task_df["Occupation (O*NET-SOC Title)"].isin(cs_jobs)]
expert_cs = expert_df[expert_df["Occupation (O*NET-SOC Title)"].isin(cs_jobs)]
worker_cs = worker_df[worker_df["Occupation (O*NET-SOC Title)"].isin(cs_jobs)]
meta_cs = meta_df[meta_df["Occupation (O*NET-SOC Title)"].isin(cs_jobs)]


# ============================================================
# 4. SIDEBAR BỘ LỌC
# ============================================================

st.sidebar.header("Bộ lọc phân tích")

selected_jobs = st.sidebar.multiselect(
    "Chọn nhóm nghề:",
    options=cs_jobs,
    default=cs_jobs
)

top_n = st.sidebar.slider(
    "Số nhiệm vụ hiển thị trong Top nhiệm vụ:",
    min_value=5,
    max_value=20,
    value=10
)

if len(selected_jobs) == 0:
    st.warning("Vui lòng chọn ít nhất một nhóm nghề để phân tích.")
    st.stop()


# ============================================================
# 5. ÁP DỤNG BỘ LỌC
# ============================================================

task_filter = task_cs[task_cs["Occupation (O*NET-SOC Title)"].isin(selected_jobs)]
expert_filter = expert_cs[expert_cs["Occupation (O*NET-SOC Title)"].isin(selected_jobs)]
worker_filter = worker_cs[worker_cs["Occupation (O*NET-SOC Title)"].isin(selected_jobs)]
meta_filter = meta_cs[meta_cs["Occupation (O*NET-SOC Title)"].isin(selected_jobs)]


# ============================================================
# 6. KPI TỔNG QUAN
# ============================================================

st.subheader("1. Tổng quan dữ liệu phân tích")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Nhóm nghề",
    task_filter["Occupation (O*NET-SOC Title)"].nunique()
)

col2.metric(
    "Nhiệm vụ",
    task_filter["Task ID"].nunique()
)

col3.metric(
    "Đánh giá chuyên gia",
    len(expert_filter)
)

col4.metric(
    "Đánh giá người lao động",
    len(worker_filter)
)

st.info("""
Bộ dữ liệu sau khi lọc tập trung vào các nhóm nghề thuộc lĩnh vực Khoa học máy tính.
Các chỉ số tổng quan cho thấy dữ liệu có đủ thông tin về nhiệm vụ, đánh giá chuyên gia và mong muốn tự động hóa của người lao động để phân tích mức độ phù hợp với AI Agent.
""")

with st.expander("Xem nhanh 4 bộ dữ liệu gốc"):
    st.write("1. Dữ liệu nhiệm vụ nghề nghiệp")
    st.dataframe(task_df.head(), use_container_width=True)

    st.write("2. Dữ liệu đánh giá khả năng tự động hóa từ chuyên gia")
    st.dataframe(expert_df.head(), use_container_width=True)

    st.write("3. Dữ liệu mong muốn tự động hóa từ người lao động")
    st.dataframe(worker_df.head(), use_container_width=True)

    st.write("4. Dữ liệu thông tin và mức độ sử dụng LLM/AI")
    st.dataframe(meta_df.head(), use_container_width=True)


# ============================================================
# 7. TỔNG HỢP DỮ LIỆU THEO NGHỀ
# ============================================================

expert_summary = expert_filter.groupby("Occupation (O*NET-SOC Title)").agg(
    expert_capacity=("Automation Capacity Rating", "mean"),
    human_agency=("Human Agency Scale Rating", "mean"),
    uncertainty=("Involved Uncertainty", "mean"),
    domain_expertise=("Domain Expertise Requirement", "mean"),
    interpersonal=("Interpersonal Communication Requirement", "mean")
).reset_index()

worker_summary = worker_filter.groupby("Occupation (O*NET-SOC Title)").agg(
    worker_desire=("Automation Desire Rating", "mean"),
    enjoyment=("Enjoyment Rating", "mean"),
    core_skill=("Core Skill Rating", "mean"),
    job_security=("Job Security Rating", "mean")
).reset_index()

task_summary = task_filter.groupby("Occupation (O*NET-SOC Title)").agg(
    total_tasks=("Task ID", "nunique"),
    avg_importance=("Importance", "mean"),
    avg_relevance=("Relevance", "mean"),
    avg_wage=("Occupation Mean Annual Wage", "mean"),
    employment=("Occupation Employment", "mean")
).reset_index()

summary = task_summary.merge(
    expert_summary,
    on="Occupation (O*NET-SOC Title)",
    how="left"
)

summary = summary.merge(
    worker_summary,
    on="Occupation (O*NET-SOC Title)",
    how="left"
)


# ============================================================
# 8. TÍNH ĐIỂM JOBFIT CHO TỪNG NHÓM NGHỀ
# Ghi chú:
# Điểm JobFit càng cao nghĩa là nghề đó càng có nhiều nhiệm vụ
# phù hợp để AI Agent tham gia xử lý.
# ============================================================

summary["JobFit Score"] = (
    (summary["expert_capacity"] / 5) * 0.35 +
    (summary["worker_desire"] / 5) * 0.25 +
    ((6 - summary["human_agency"]) / 5) * 0.15 +
    ((6 - summary["uncertainty"]) / 5) * 0.10 +
    ((6 - summary["interpersonal"]) / 5) * 0.10 +
    (summary["avg_importance"] / 5) * 0.05
) * 100


# ============================================================
# 9. HÀM PHÂN LOẠI KHUYẾN NGHỊ
# ============================================================

def classify_recommendation(score, human_agency, uncertainty):
    if score >= 75 and human_agency <= 2.8 and uncertainty <= 2.8:
        return "Ưu tiên giao cho AI Agent"
    elif score >= 60:
        return "AI hỗ trợ, con người kiểm tra"
    else:
        return "Con người kiểm soát chính"


summary["Recommendation"] = summary.apply(
    lambda row: classify_recommendation(
        row["JobFit Score"],
        row["human_agency"],
        row["uncertainty"]
    ),
    axis=1
)

summary = summary.sort_values("JobFit Score", ascending=False)


# ============================================================
# 10. KPI SAU KHI TÍNH ĐIỂM
# ============================================================

avg_jobfit = summary["JobFit Score"].mean()
best_job = summary.iloc[0]["Occupation (O*NET-SOC Title)"]
best_score = summary.iloc[0]["JobFit Score"]

col1, col2, col3 = st.columns(3)

col1.metric("Điểm JobFit trung bình", f"{avg_jobfit:.2f}")
col2.metric("Nghề phù hợp nhất", best_job)
col3.metric("Điểm cao nhất", f"{best_score:.2f}")


# ============================================================
# 11. BIỂU ĐỒ 1: BẢN ĐỒ NGHỀ NGHIỆP PHÙ HỢP VỚI AI AGENT
# ============================================================

st.subheader("2. Bản đồ nghề nghiệp phù hợp với AI Agent")

color_map = {
    "Ưu tiên giao cho AI Agent": "#2E86AB",
    "AI hỗ trợ, con người kiểm tra": "#F6C85F",
    "Con người kiểm soát chính": "#E07A5F"
}

fig1 = px.bar(
    summary,
    x="JobFit Score",
    y="Occupation (O*NET-SOC Title)",
    orientation="h",
    color="Recommendation",
    title="Xếp hạng mức độ phù hợp để ứng dụng AI Agent theo nhóm nghề",
    color_discrete_map=color_map
)

fig1.update_layout(
    yaxis={"categoryorder": "total ascending"},
    height=650,
    xaxis_title="JobFit Score",
    yaxis_title="Nhóm nghề"
)

st.plotly_chart(fig1, use_container_width=True)

st.info("""
Biểu đồ cho thấy các nhóm nghề có điểm JobFit cao thường là những nghề có nhiều nhiệm vụ kỹ thuật, quy trình rõ ràng và dễ kiểm tra kết quả.
Các nhóm nghề này phù hợp để AI Agent tham gia hỗ trợ hoặc tự động hóa một phần công việc.
""")


# ============================================================
# 12. BIỂU ĐỒ 2: MA TRẬN JOBFIT
# ============================================================

st.subheader("3. Ma trận JobFit: Khả năng tự động hóa và mong muốn tự động hóa")

fig2 = px.scatter(
    summary,
    x="expert_capacity",
    y="worker_desire",
    size="total_tasks",
    color="Recommendation",
    hover_name="Occupation (O*NET-SOC Title)",
    title="Ma trận lựa chọn nhóm nghề ưu tiên triển khai AI Agent",
    color_discrete_map=color_map
)

fig2.update_layout(
    height=600,
    xaxis_title="Khả năng tự động hóa theo chuyên gia",
    yaxis_title="Mong muốn tự động hóa của người lao động"
)

st.plotly_chart(fig2, use_container_width=True)

st.info("""
Ma trận JobFit giúp xác định nhóm nghề vừa có khả năng tự động hóa cao, vừa có nhu cầu tự động hóa từ người lao động.
Những nhóm nghề nằm ở vùng có cả hai chỉ số cao nên được ưu tiên triển khai AI Agent trước.
""")


# ============================================================
# 13. PHÂN TÍCH NHIỆM VỤ CỤ THỂ
# ============================================================

expert_task = expert_filter.groupby(
    ["Task ID", "Occupation (O*NET-SOC Title)", "Task"]
).agg(
    expert_capacity=("Automation Capacity Rating", "mean"),
    human_agency=("Human Agency Scale Rating", "mean"),
    uncertainty=("Involved Uncertainty", "mean"),
    domain_expertise=("Domain Expertise Requirement", "mean"),
    interpersonal=("Interpersonal Communication Requirement", "mean")
).reset_index()

worker_task = worker_filter.groupby(
    ["Task ID", "Occupation (O*NET-SOC Title)", "Task"]
).agg(
    worker_desire=("Automation Desire Rating", "mean")
).reset_index()

task_meta = task_filter[
    [
        "Task ID",
        "Occupation (O*NET-SOC Title)",
        "Importance",
        "Relevance",
        "Frequency",
        "Task Type"
    ]
].drop_duplicates(["Task ID", "Occupation (O*NET-SOC Title)"])

task_detail = expert_task.merge(
    worker_task,
    on=["Task ID", "Occupation (O*NET-SOC Title)", "Task"],
    how="left"
)

task_detail = task_detail.merge(
    task_meta,
    on=["Task ID", "Occupation (O*NET-SOC Title)"],
    how="left"
)


# ============================================================
# 14. TÍNH ĐIỂM JOBFIT CHO TỪNG NHIỆM VỤ
# ============================================================

task_detail["Task JobFit Score"] = (
    (task_detail["expert_capacity"] / 5) * 0.40 +
    (task_detail["worker_desire"].fillna(3) / 5) * 0.25 +
    ((6 - task_detail["human_agency"]) / 5) * 0.15 +
    ((6 - task_detail["uncertainty"]) / 5) * 0.10 +
    ((6 - task_detail["interpersonal"]) / 5) * 0.05 +
    (task_detail["Importance"].fillna(3) / 5) * 0.05
) * 100

task_detail["Recommendation"] = task_detail.apply(
    lambda row: classify_recommendation(
        row["Task JobFit Score"],
        row["human_agency"],
        row["uncertainty"]
    ),
    axis=1
)

top_tasks = task_detail.sort_values(
    "Task JobFit Score",
    ascending=False
).head(top_n)


# ============================================================
# 15. KPI PHÂN LOẠI NHIỆM VỤ
# ============================================================

st.subheader("4. Phân loại nhiệm vụ theo mức độ nên giao cho AI Agent")

task_count_by_recommendation = task_detail["Recommendation"].value_counts().reset_index()
task_count_by_recommendation.columns = ["Recommendation", "Count"]

col1, col2, col3 = st.columns(3)

count_ai = task_count_by_recommendation[
    task_count_by_recommendation["Recommendation"] == "Ưu tiên giao cho AI Agent"
]["Count"].sum()

count_hybrid = task_count_by_recommendation[
    task_count_by_recommendation["Recommendation"] == "AI hỗ trợ, con người kiểm tra"
]["Count"].sum()

count_human = task_count_by_recommendation[
    task_count_by_recommendation["Recommendation"] == "Con người kiểm soát chính"
]["Count"].sum()

col1.metric("Ưu tiên giao cho AI Agent", int(count_ai))
col2.metric("AI hỗ trợ + người kiểm tra", int(count_hybrid))
col3.metric("Con người kiểm soát chính", int(count_human))

fig3 = px.pie(
    task_count_by_recommendation,
    names="Recommendation",
    values="Count",
    title="Tỷ trọng nhiệm vụ theo nhóm khuyến nghị",
    color="Recommendation",
    color_discrete_map=color_map
)

st.plotly_chart(fig3, use_container_width=True)

st.info("""
Biểu đồ phân loại cho thấy không phải nhiệm vụ nào cũng nên giao hoàn toàn cho AI Agent.
Cách chia thành ba nhóm giúp việc ứng dụng AI Agent thực tế hơn: nhiệm vụ phù hợp thì ưu tiên giao cho AI, nhiệm vụ rủi ro hơn thì cần con người kiểm tra hoặc kiểm soát chính.
""")


# ============================================================
# 16. BIỂU ĐỒ 4: TOP NHIỆM VỤ NÊN GIAO CHO AI AGENT
# ============================================================

st.subheader("5. Top nhiệm vụ phù hợp nhất để giao cho AI Agent")

fig4 = px.bar(
    top_tasks.sort_values("Task JobFit Score"),
    x="Task JobFit Score",
    y="Task",
    color="Recommendation",
    orientation="h",
    title=f"Top {top_n} nhiệm vụ có điểm JobFit cao nhất",
    color_discrete_map=color_map
)

fig4.update_layout(
    height=750,
    xaxis_title="Task JobFit Score",
    yaxis_title="Nhiệm vụ"
)

st.plotly_chart(fig4, use_container_width=True)

st.info("""
Các nhiệm vụ có điểm JobFit cao là nhóm nên được chọn để thử nghiệm AI Agent trước.
Đây thường là các nhiệm vụ có quy trình rõ ràng như kiểm thử phần mềm, sao lưu dữ liệu, giám sát hệ thống hoặc hỗ trợ xử lý lỗi kỹ thuật.
""")


# ============================================================
# 17. BIỂU ĐỒ 5: MỨC ĐỘ CẦN CON NGƯỜI KIỂM SOÁT
# ============================================================

st.subheader("6. Mức độ cần con người kiểm soát theo nhóm nghề")

human_control = summary.sort_values("human_agency", ascending=False)

fig5 = px.bar(
    human_control,
    x="human_agency",
    y="Occupation (O*NET-SOC Title)",
    orientation="h",
    color="human_agency",
    color_continuous_scale="Reds",
    title="Nhóm nghề có mức độ cần con người kiểm soát cao"
)

fig5.update_layout(
    yaxis={"categoryorder": "total ascending"},
    height=650,
    xaxis_title="Human Agency Rating",
    yaxis_title="Nhóm nghề"
)

st.plotly_chart(fig5, use_container_width=True)

st.info("""
Những nhóm nghề có mức độ cần con người kiểm soát cao thường liên quan đến phán đoán chuyên môn, bảo mật, quản lý hoặc ra quyết định.
Với các nhóm nghề này, AI Agent nên đóng vai trò hỗ trợ thay vì tự động quyết định hoàn toàn.
""")


# ============================================================
# 18. BIỂU ĐỒ 6: LÝ DO NGƯỜI LAO ĐỘNG MUỐN TỰ ĐỘNG HÓA
# ============================================================

st.subheader("7. Vì sao người lao động muốn có AI Agent?")

reason_cols = [
    "Reasons for Automation Desire - Free Time",
    "Reasons for Automation Desire - Repetitive",
    "Reasons for Automation Desire - Human Error",
    "Reasons for Automation Desire - Stress",
    "Reasons for Automation Desire - Difficulty",
    "Reasons for Automation Desire - Scale"
]

reason_data = worker_filter[reason_cols].sum().reset_index()
reason_data.columns = ["Reason", "Count"]

reason_data["Reason"] = reason_data["Reason"].str.replace(
    "Reasons for Automation Desire - ",
    "",
    regex=False
)

reason_data = reason_data.sort_values("Count", ascending=True)

fig6 = px.bar(
    reason_data,
    x="Count",
    y="Reason",
    orientation="h",
    color="Count",
    color_continuous_scale="Purples",
    title="Các lý do chính khiến người lao động muốn tự động hóa"
)

fig6.update_layout(
    height=500,
    xaxis_title="Số lượt chọn",
    yaxis_title="Lý do"
)

st.plotly_chart(fig6, use_container_width=True)

st.info("""
Lý do người lao động muốn tự động hóa chủ yếu liên quan đến tiết kiệm thời gian, giảm công việc lặp lại và hạn chế lỗi do con người.
Điều này cho thấy AI Agent có giá trị lớn trong việc hỗ trợ các nhiệm vụ thường xuyên, tốn thời gian và có thể chuẩn hóa.
""")


# ============================================================
# 19. BIỂU ĐỒ 7: AI/LLM ĐANG ĐƯỢC DÙNG VÀO VIỆC GÌ?
# ============================================================

st.subheader("8. AI/LLM đang được dùng vào việc gì?")

usage_cols = [
    "LLM Usage by Type - Information Access",
    "LLM Usage by Type - Edit",
    "LLM Usage by Type - Idea Generation",
    "LLM Usage by Type - Communication",
    "LLM Usage by Type - Analysis",
    "LLM Usage by Type - Decision",
    "LLM Usage by Type - Coding",
    "LLM Usage by Type - System Design",
    "LLM Usage by Type - Data Processing"
]

usage_result = []

for col in usage_cols:
    usage_result.append({
        "Usage Type": col.replace("LLM Usage by Type - ", ""),
        "Weekly or Daily Use (%)": meta_filter[col].isin(["Weekly", "Daily"]).mean() * 100
    })

usage_df = pd.DataFrame(usage_result)
usage_df = usage_df.sort_values("Weekly or Daily Use (%)", ascending=True)

fig7 = px.bar(
    usage_df,
    x="Weekly or Daily Use (%)",
    y="Usage Type",
    orientation="h",
    color="Weekly or Daily Use (%)",
    color_continuous_scale="Greens",
    title="Tỷ lệ sử dụng AI/LLM hằng tuần hoặc hằng ngày theo mục đích"
)

fig7.update_layout(
    height=550,
    xaxis_title="Tỷ lệ sử dụng hằng tuần hoặc hằng ngày (%)",
    yaxis_title="Mục đích sử dụng"
)

st.plotly_chart(fig7, use_container_width=True)

st.info("""
AI/LLM đang được sử dụng nhiều trong các hoạt động như tìm kiếm thông tin, chỉnh sửa nội dung, phân tích, giao tiếp và lập trình.
Đây là cơ sở cho thấy AI Agent có thể mở rộng vai trò từ công cụ hỗ trợ đơn lẻ sang trợ lý xử lý nhiệm vụ nhiều bước.
""")


# ============================================================
# 20. BẢNG KHUYẾN NGHỊ THEO NHÓM NGHỀ
# ============================================================

st.subheader("9. Bảng khuyến nghị theo nhóm nghề")

job_table_cols = [
    "Occupation (O*NET-SOC Title)",
    "total_tasks",
    "expert_capacity",
    "worker_desire",
    "human_agency",
    "uncertainty",
    "interpersonal",
    "JobFit Score",
    "Recommendation"
]

st.dataframe(
    summary[job_table_cols].round(2),
    use_container_width=True
)

st.info("""
Bảng khuyến nghị giúp xác định nhóm nghề nào nên ưu tiên ứng dụng AI Agent và nhóm nghề nào cần thận trọng hơn.
Các nhóm có điểm JobFit cao có thể được chọn làm phạm vi thử nghiệm ban đầu khi triển khai AI Agent.
""")


# ============================================================
# 21. BẢNG KHUYẾN NGHỊ THEO NHIỆM VỤ
# ============================================================

st.subheader("10. Bảng khuyến nghị theo nhiệm vụ")

task_table_cols = [
    "Occupation (O*NET-SOC Title)",
    "Task",
    "expert_capacity",
    "worker_desire",
    "human_agency",
    "uncertainty",
    "interpersonal",
    "Task JobFit Score",
    "Recommendation"
]

st.dataframe(
    top_tasks[task_table_cols].round(2),
    use_container_width=True
)

st.info("""
Bảng nhiệm vụ cho thấy cụ thể những công việc nào có thể giao cho AI Agent hoặc để AI hỗ trợ.
Cách phân tích theo nhiệm vụ giúp khuyến nghị trở nên thực tế hơn so với chỉ đánh giá ở cấp độ nghề nghiệp.
""")


# ============================================================
# 22. KẾT LUẬN NGẮN TRÊN DASHBOARD
# ============================================================

st.subheader("11. Kết luận ngắn")

st.success("""
Kết quả trực quan hóa cho thấy AI Agent phù hợp nhất với các nhiệm vụ có quy trình rõ ràng, khả năng tự động hóa cao và ít cần sự can thiệp trực tiếp của con người.

Các nhiệm vụ như kiểm thử phần mềm, sao lưu dữ liệu, giám sát hệ thống, hỗ trợ viết mã và xử lý lỗi kỹ thuật nên được ưu tiên thử nghiệm với AI Agent.

Tuy nhiên, với các nhiệm vụ liên quan đến bảo mật, quản lý dự án, thiết kế hệ thống hoặc ra quyết định quan trọng, AI Agent chỉ nên đóng vai trò hỗ trợ; con người vẫn cần kiểm tra và phê duyệt kết quả cuối cùng.
""")


# ============================================================
# 23. TẢI FILE KẾT QUẢ
# ============================================================

csv_job_summary = summary.to_csv(index=False).encode("utf-8-sig")
csv_task_summary = task_detail.to_csv(index=False).encode("utf-8-sig")

col1, col2 = st.columns(2)

with col1:
    st.download_button(
        label="Tải bảng JobFit theo nhóm nghề",
        data=csv_job_summary,
        file_name="jobfit_by_occupation.csv",
        mime="text/csv"
    )

with col2:
    st.download_button(
        label="Tải bảng JobFit theo nhiệm vụ",
        data=csv_task_summary,
        file_name="jobfit_by_task.csv",
        mime="text/csv"
    )