import streamlit as st
import plotly.express as px

from resume_parser import extract_resume_text
from text_cleaner import clean_resume_text

from skill_extractor import (
    load_skill_dictionary,
    extract_skills
)

from job_matcher import (
    load_job_roles,
    rank_job_roles,
    analyze_skill_gap
)

from roadmap_generator import (
    generate_learning_roadmap
)

from io import BytesIO

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)
from reportlab.lib import colors


# =========================================
# PAGE CONFIGURATION
# =========================================

st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide"
)


# =========================================
# TITLE
# =========================================

st.title(
    "📄 AI Resume Analyzer & Job Recommendation System"
)

st.write(
    "Upload your resume to analyze your skills, "
    "find suitable job roles, identify skill gaps, "
    "and generate a personalized learning roadmap."
)

st.divider()


# =========================================
# RESUME UPLOAD
# =========================================

st.header("📤 Upload Your Resume")

uploaded_file = st.file_uploader(
    "Upload your resume",
    type=["pdf", "docx"],
    help="Supported formats: PDF and DOCX"
)


# =========================================
# PROCESS RESUME
# =========================================

if uploaded_file is not None:

    st.success(
        f"Uploaded successfully: {uploaded_file.name}"
    )

    st.write(
        f"File size: "
        f"{uploaded_file.size / 1024:.2f} KB"
    )

    try:

        # =====================================
        # 1. EXTRACT RESUME TEXT
        # =====================================

        extracted_text = extract_resume_text(
            uploaded_file
        )


        # =====================================
        # 2. CLEAN RESUME TEXT
        # =====================================

        cleaned_text = clean_resume_text(
            extracted_text
        )


        # =====================================
        # 3. EXTRACT SKILLS
        # =====================================

        skill_dictionary = load_skill_dictionary()

        resume_skills = extract_skills(
            cleaned_text,
            skill_dictionary
        )


        # =====================================
        # 4. DISPLAY RESUME TEXT
        # =====================================

        st.divider()

        st.header("📄 Extracted Resume Text")

        with st.expander("View extracted text"):

            st.text(cleaned_text)


        # =====================================
        # 5. DISPLAY DETECTED SKILLS
        # =====================================

        st.header("🧠 Detected Skills")

        if resume_skills:

            skill_columns = st.columns(3)

            for index, skill in enumerate(resume_skills):

                with skill_columns[index % 3]:

                    st.success(
                        f"✓ {skill['skill']}"
                    )

        else:

            st.warning(
                "No technical skills were detected "
                "from this resume."
            )


        # =====================================
        # 6. LOAD JOB ROLES
        # =====================================

        job_roles = load_job_roles()


        # =====================================
        # 7. RECOMMENDED JOB ROLES
        # =====================================

        st.divider()

        st.header("🎯 Recommended Job Roles")

        results = rank_job_roles(
            cleaned_text,
            resume_skills,
            job_roles
        )


        # -------------------------------------
        # Top 3 Roles
        # -------------------------------------

        st.subheader("🏆 Top 3 Suitable Roles")

        top_roles = results.head(3)

        for index, row in top_roles.iterrows():

            st.write(
                f"**{index + 1}. {row['job_role']}**"
            )

            st.progress(
                min(
                    int(row["match_score"]),
                    100
                )
            )

            st.write(
                f"Match Score: "
                f"**{row['match_score']}%**"
            )

            st.write(
                f"Skill Coverage: "
                f"{row['skill_coverage']}%"
            )

            st.write(
                f"Text Similarity: "
                f"{row['tfidf_similarity']}%"
            )

            st.divider()


        # -------------------------------------
        # Match Score Chart
        # -------------------------------------

        st.subheader("📊 Job Role Match Scores")

        chart_data = results.sort_values(
            by="match_score",
            ascending=True
        )

        fig = px.bar(
            chart_data,
            x="match_score",
            y="job_role",
            orientation="h",
            text="match_score",
            labels={
                "match_score": "Match Score (%)",
                "job_role": "Job Role"
            },
            title="Resume Match Score by Job Role"
        )

        fig.update_traces(
            texttemplate="%{text:.2f}%",
            textposition="outside"
        )

        fig.update_layout(
            xaxis_range=[0, 100],
            height=500
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


        # =====================================
        # 8. TARGET ROLE SELECTION
        # =====================================

        st.header("🎯 Analyze a Target Role")

        role_names = job_roles[
            "job_role"
        ].tolist()

        selected_role_name = st.selectbox(
            "Select the job role you want to analyze:",
            ["Choose a job role"] + role_names
        )


        # =====================================
        # 9. SKILL GAP ANALYSIS
        # =====================================

        if selected_role_name == "Choose a job role":

            st.info(
                "Please choose a job role to see "
                "the skill-gap analysis."
            )


        else:

            selected_role = job_roles[
                job_roles["job_role"] == selected_role_name
            ].iloc[0]

            st.subheader(
                f"Analysis for: {selected_role_name}"
            )


            # -------------------------------------
            # Compare Skills
            # -------------------------------------

            matched_skills, missing_skills = analyze_skill_gap(
                resume_skills,
                selected_role
            )


            # -------------------------------------
            # Skills Found
            # -------------------------------------

            st.write("### ✅ Skills Found")

            if matched_skills:

                found_columns = st.columns(3)

                for index, skill in enumerate(
                    matched_skills
                ):

                    with found_columns[index % 3]:

                        st.success(
                            f"✓ {skill.title()}"
                        )

            else:

                st.info(
                    "No required skills for this role "
                    "were detected in the resume."
                )


            # -------------------------------------
            # Missing Skills
            # -------------------------------------

            st.write(
                "### ⚠️ Missing / Not Detected Skills"
            )

            if missing_skills:

                missing_columns = st.columns(3)

                for index, skill in enumerate(
                    missing_skills
                ):

                    with missing_columns[index % 3]:

                        st.warning(
                            f"⚠ {skill.title()}"
                        )

            else:

                st.success(
                    "All required skills were detected!"
                )


            # =====================================
            # 10. LEARNING ROADMAP
            # =====================================

            st.divider()

            st.header(
                "📚 Personalized Learning Roadmap"
            )

            if missing_skills:

                roadmap = generate_learning_roadmap(
                    missing_skills
                )

                for item in roadmap:

                    with st.expander(
                        f"Week {item['week']}: "
                        f"{item['topic']}"
                    ):

                        st.write(
                            item["resource"]
                        )

            else:

                st.success(
                    "No major skill gaps detected. "
                    "Continue strengthening your existing skills!"
                )


            # =====================================
            # 11. DOWNLOAD PDF ANALYSIS REPORT
            # =====================================

            st.divider()

            st.header(
                "📥 Download Analysis Report"
            )

            # -------------------------------------
            # Create PDF in memory
            # -------------------------------------

            pdf_buffer = BytesIO()

            pdf = SimpleDocTemplate(
                pdf_buffer,
                pagesize=A4,
                rightMargin=40,
                leftMargin=40,
                topMargin=40,
                bottomMargin=40
            )

            styles = getSampleStyleSheet()

            title_style = styles["Title"]

            title_style.alignment = TA_CENTER

            heading_style = styles["Heading2"]

            normal_style = styles["BodyText"]

            story = []


            # -------------------------------------
            # PDF Title
            # -------------------------------------

            story.append(
                Paragraph(
                    "AI Resume Analyzer and "
                    "Job Recommendation System",
                    title_style
                )
            )

            story.append(
                Spacer(1, 20)
            )


            # -------------------------------------
            # Resume Information
            # -------------------------------------

            story.append(
                Paragraph(
                    "Resume Information",
                    heading_style
                )
            )

            story.append(
                Paragraph(
                    f"<b>File Name:</b> "
                    f"{uploaded_file.name}",
                    normal_style
                )
            )

            story.append(
                Spacer(1, 15)
            )


            # -------------------------------------
            # Detected Skills
            # -------------------------------------

            story.append(
                Paragraph(
                    "Detected Skills",
                    heading_style
                )
            )

            if resume_skills:

                for skill in resume_skills:

                    story.append(
                        Paragraph(
                            f"- {skill['skill']}",
                            normal_style
                        )
                    )

            else:

                story.append(
                    Paragraph(
                        "No skills detected.",
                        normal_style
                    )
                )

            story.append(
                Spacer(1, 15)
            )


            # -------------------------------------
            # Recommended Job Roles
            # -------------------------------------

            story.append(
                Paragraph(
                    "Recommended Job Roles",
                    heading_style
                )
            )

            role_table_data = [
                [
                    "Rank",
                    "Job Role",
                    "Skill Coverage",
                    "TF-IDF Similarity",
                    "Match Score"
                ]
            ]

            for index, row in results.iterrows():

                role_table_data.append(
                    [
                        str(index + 1),
                        row["job_role"],
                        f"{row['skill_coverage']:.2f}%",
                        f"{row['tfidf_similarity']:.2f}%",
                        f"{row['match_score']:.2f}%"
                    ]
                )

            role_table = Table(
                role_table_data,
                repeatRows=1
            )

            role_table.setStyle(
                TableStyle(
                    [
                        (
                            "BACKGROUND",
                            (0, 0),
                            (-1, 0),
                            colors.lightgrey
                        ),
                        (
                            "TEXTCOLOR",
                            (0, 0),
                            (-1, 0),
                            colors.black
                        ),
                        (
                            "GRID",
                            (0, 0),
                            (-1, -1),
                            0.5,
                            colors.grey
                        ),
                        (
                            "ALIGN",
                            (0, 0),
                            (-1, -1),
                            "CENTER"
                        ),
                        (
                            "VALIGN",
                            (0, 0),
                            (-1, -1),
                            "MIDDLE"
                        ),
                        (
                            "FONTSIZE",
                            (0, 0),
                            (-1, -1),
                            8
                        )
                    ]
                )
            )

            story.append(
                role_table
            )

            story.append(
                Spacer(1, 20)
            )


            # -------------------------------------
            # Target Role
            # -------------------------------------

            story.append(
                Paragraph(
                    "Target Role Analysis",
                    heading_style
                )
            )

            story.append(
                Paragraph(
                    f"<b>Target Role:</b> "
                    f"{selected_role_name}",
                    normal_style
                )
            )

            story.append(
                Spacer(1, 10)
            )


            # -------------------------------------
            # Skills Found
            # -------------------------------------

            story.append(
                Paragraph(
                    "Skills Found",
                    heading_style
                )
            )

            if matched_skills:

                for skill in matched_skills:

                    story.append(
                        Paragraph(
                            f"- {skill.title()}",
                            normal_style
                        )
                    )

            else:

                story.append(
                    Paragraph(
                        "No required skills detected.",
                        normal_style
                    )
                )

            story.append(
                Spacer(1, 15)
            )


            # -------------------------------------
            # Missing Skills
            # -------------------------------------

            story.append(
                Paragraph(
                    "Missing / Not Detected Skills",
                    heading_style
                )
            )

            if missing_skills:

                for skill in missing_skills:

                    story.append(
                        Paragraph(
                            f"- {skill.title()}",
                            normal_style
                        )
                    )

            else:

                story.append(
                    Paragraph(
                        "No major skill gaps detected.",
                        normal_style
                    )
                )

            story.append(
                Spacer(1, 15)
            )


            # -------------------------------------
            # Learning Roadmap
            # -------------------------------------

            story.append(
                Paragraph(
                    "Personalized Learning Roadmap",
                    heading_style
                )
            )

            if missing_skills:

                roadmap = generate_learning_roadmap(
                    missing_skills
                )

                for item in roadmap:

                    story.append(
                        Paragraph(
                            f"<b>Week {item['week']}: "
                            f"{item['topic']}</b>",
                            normal_style
                        )
                    )

                    story.append(
                        Paragraph(
                            item["resource"],
                            normal_style
                        )
                    )

                    story.append(
                        Spacer(1, 8)
                    )

            else:

                story.append(
                    Paragraph(
                        "No major skill gaps detected. "
                        "Continue strengthening your existing skills!",
                        normal_style
                    )
                )

            story.append(
                Spacer(1, 20)
            )


            # -------------------------------------
            # Responsible AI Disclaimer
            # -------------------------------------

            story.append(
                Paragraph(
                    "Responsible AI Disclaimer",
                    heading_style
                )
            )

            story.append(
                Paragraph(
                    "This analysis is an educational estimate "
                    "based on job-related skills and text "
                    "similarity. It is not an automatic hiring "
                    "or rejection decision. Missing keywords do "
                    "not necessarily mean that the candidate "
                    "lacks the underlying ability. The system "
                    "does not evaluate protected personal "
                    "information.",
                    normal_style
                )
            )


            # -------------------------------------
            # Build PDF
            # -------------------------------------

            pdf.build(story)

            pdf_buffer.seek(0)


            # -------------------------------------
            # Download Button
            # -------------------------------------

            st.download_button(
                label="📥 Download PDF Analysis Report",
                data=pdf_buffer,
                file_name="resume_analysis_report.pdf",
                mime="application/pdf"
            )


    # =========================================
    # ERROR HANDLING
    # =========================================

    except Exception as e:

        st.error(
            f"Unable to process the resume: {e}"
        )