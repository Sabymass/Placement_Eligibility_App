import streamlit as st
import pandas as pd
from io import BytesIO
from db_config import db_config  # ✅ Import the config dictionary
from db_connector import DatabaseConnector
from student_manager import StudentDataManager
from exporter import ExcelExporter

st.set_page_config(page_title="Placement Eligibility App", layout="wide")
st.title("🎓 Placement Eligibility Streamlit App")

db = DatabaseConnector(db_config)  # ✅ Now config is defined


# ---------------------- View Student Details ------------------------ #
st.sidebar.header("🔍 Search Student")
options = db.get_student_names()
sel = st.sidebar.selectbox("Select student:", ["-- select --"] + list(options.keys()))

if sel != "-- select --":
    student_id = options[sel]
    student_info = db.get_student_info(student_id)
    programming_info = db.get_programming_info(student_id)
    soft_skills_info = db.get_soft_skills_info(student_id)
    placement_info = db.get_placement_info(student_id)

    st.subheader(f"📌 Details for: {student_info['name']}")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**🎓 Student Info:**")
        if isinstance(student_info, dict):
            df_student = pd.DataFrame(student_info.items(), columns=["Field", "Value"])
            st.table(df_student)
        else:
            st.write(student_info)

    with col2:
        st.markdown("**💻 Programming Skills:**")
        if isinstance(programming_info, dict):
            df_program = pd.DataFrame(programming_info.items(), columns=["Field", "Value"])
            st.table(df_program)
        else:
            st.write(programming_info)


    st.markdown("**🧠 Soft Skills:**")
    if isinstance(soft_skills_info, dict):
        df_soft = pd.DataFrame(soft_skills_info.items(), columns=["Field", "Value"])
        st.table(df_soft)
    else:
        st.write(soft_skills_info)

    st.markdown("**📈 Placement Info:**")
    if isinstance(placement_info, dict):  # Optional: convert placement_date to readable format
        if "placement_date" in placement_info and hasattr(placement_info["placement_date"], "isoformat"):
            placement_info["placement_date"] = placement_info["placement_date"].isoformat()
        df_place = pd.DataFrame(placement_info.items(), columns=["Field", "Value"])
        st.table(df_place)
    else:
        st.write(placement_info)
        
    if st.button("📥 Download This Student's Info as Excel"):
        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            # Convert each section to DataFrame and write to separate sheets
            pd.DataFrame(student_info.items(), columns=["Field", "Value"]).to_excel(writer, index=False, sheet_name="Student Info")
            pd.DataFrame(programming_info.items(), columns=["Field", "Value"]).to_excel(writer, index=False, sheet_name="Programming Skills")
            pd.DataFrame(soft_skills_info.items(), columns=["Field", "Value"]).to_excel(writer, index=False, sheet_name="Soft Skills")

            # Format placement_date if needed
            if "placement_date" in placement_info and hasattr(placement_info["placement_date"], "isoformat"):
                placement_info["placement_date"] = placement_info["placement_date"].isoformat()
            pd.DataFrame(placement_info.items(), columns=["Field", "Value"]).to_excel(writer, index=False, sheet_name="Placement Info")

        output.seek(0)

        st.download_button(
            label="⬇️ Click to Download Excel",
            data=output,
            file_name=f"{student_info['name'].replace(' ', '_')}_Details.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )


# ---------------------- Filter by Placement Status ------------------------ #
st.subheader("🎯 Filter by Placement Status")
placement_filter = st.selectbox("Select Placement Status:", ["-- select --", "Placed", "Not Placed"])

if placement_filter in ["Placed", "Not Placed"]:
    query = """
        SELECT s.student_id, s.name, p.company_name, p.placement_package, p.placement_date
        FROM Student_table s
        JOIN Placement_table p ON s.student_id = p.student_id
        WHERE p.placement_status = %s
    """
    result_df = db.execute_query(query, (placement_filter,))

    if result_df is not None and not result_df.empty:
        result_df.columns = ["ID", "Name", "Company", "Package", "Placement Date"]
        st.dataframe(result_df)

        # Download Excel
        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            result_df.to_excel(writer, index=False, sheet_name="Filtered Students")
        output.seek(0)

        st.download_button(
            label=f"📥 Download {placement_filter} Students as Excel",
            data=output,
            file_name=f"{placement_filter}_Students.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    else:
        st.info("No students found for selected placement status.")

# ---------------------- Top 10 Performers ---------------------- #
st.subheader("🏆 Top 10 Performers")
top_option = st.selectbox("Filter by:", [
    "-- select --", "Programming Score", "Communication Skill", "Mock Interview Score", "Overall Performance"
])

if top_option != "-- select --":
    query_map = {
        "Programming Score": ("""
            SELECT s.student_id, s.name, p.latest_project_score
            FROM Student_table s
            JOIN Programming_table p ON s.student_id = p.student_id
            ORDER BY p.latest_project_score DESC
            LIMIT 10
        """, ["ID", "Name", "Score"], "💻 Top 10 by Programming Score:"),

        "Communication Skill": ("""
            SELECT s.student_id, s.name, sk.communication
            FROM Student_table s
            JOIN Soft_skills sk ON s.student_id = sk.student_id
            ORDER BY sk.communication DESC
            LIMIT 10
        """, ["ID", "Name", "Score"], "🗣️ Top 10 by Communication Skill:"),

        "Mock Interview Score": ("""
            SELECT s.student_id, s.name, pl.mock_interview_score
            FROM Student_table s
            JOIN Placement_table pl ON s.student_id = pl.student_id
            ORDER BY pl.mock_interview_score DESC
            LIMIT 10
        """, ["ID", "Name", "Score"], "🎤 Top 10 by Mock Interview Score:"),

        "Overall Performance": ("""
            SELECT s.student_id, s.name,
                   p.latest_project_score,
                   sk.communication,
                   pl.mock_interview_score,
                   ROUND((IFNULL(p.latest_project_score, 0) +
                          IFNULL(sk.communication, 0) +
                          IFNULL(pl.mock_interview_score, 0)) / 3, 2) AS overall_score
            FROM Student_table s
            JOIN Programming_table p ON s.student_id = p.student_id
            JOIN Soft_skills sk ON s.student_id = sk.student_id
            JOIN Placement_table pl ON s.student_id = pl.student_id
            ORDER BY overall_score DESC
            LIMIT 10
        """, ["ID", "Name", "Programming", "Communication", "Mock Interview", "Overall Score"], "🌟 Top 10 Overall Performers:")
    }

    query, columns, title = query_map[top_option]
    result_df = db.execute_query(query)

    st.subheader(title)
    if result_df is not None and not result_df.empty:
        result_df.columns = columns
        st.dataframe(result_df)
    else:
        st.warning("No data found.")
