import streamlit as st
import pandas as pd

from CGMT_engine import calculate_fatigue_life
from Cfatigue_engine import run_fatigue_analysis

# ==========================================================
# PAGE SETTINGS
# ==========================================================

st.set_page_config(
    page_title="Bridge Fatigue Assessment Tool",
    layout="wide"
)

st.title("Bridge Fatigue Assessment Tool")

# ==========================================================
# SELECT APPROACH
# ==========================================================

approach = st.selectbox(
    "Select Fatigue Assessment Approach",
    [
        "IRS Simplified Fatigue Assessment",
        "Stress-Time History Fatigue Assessment"
    ]
)

# ==========================================================
# IRS SIMPLIFIED FATIGUE ASSESSMENT
# ==========================================================

if approach == "IRS Simplified Fatigue Assessment":

    st.header("IRS Simplified Fatigue Assessment")

    loading_type = st.selectbox(
        "Loading Type",
        ["25T", "32.5T"]
    )

    if loading_type == "25T":
        train = st.selectbox(
            "Train Type",
            [f"Train-{i}" for i in range(1, 12)]
        )
    else:
        train = st.selectbox(
            "Train Type",
            [f"Train-{i}" for i in range(1, 8)]
        )

    span = st.number_input(
        "Span (m)",
        min_value=0.1,
        value=10.0
    )

    annual_gmt = st.number_input(
        "Annual Traffic (GMT/Year)",
        min_value=0.0,
        value=25.0
    )

    stress_range = st.number_input(
        "Stress Range (MPa)",
        min_value=0.0,
        value=50.0
    )

    detail_category = st.selectbox(
        "Detail Category",
        ["36", "50", "56", "63", "71", "80",
         "90", "100", "112", "125", "140", "160"]
    )

    consumed_gmt_years = st.number_input(
        "Consumed GMT",
        min_value=0.0,
        value=1000.0
    )

    track_type = st.radio(
        "Track Type",
        ["Single Track", "Double Track"]
    )

    single_track = track_type == "Single Track"

    delta_sigma1 = None
    delta_sigma12 = None

    if not single_track:

        delta_sigma1 = st.number_input(
            "Δσ1 (MPa)",
            min_value=0.0,
            value=80.0
        )

        delta_sigma12 = st.number_input(
            "Δσ1+2 (MPa)",
            min_value=0.0,
            value=100.0
        )

    if st.button("Calculate IRS Fatigue Life"):

        result = calculate_fatigue_life(
            loading_type=loading_type,
            span=span,
            train=train,
            annual_gmt=annual_gmt,
            stress_range=stress_range,
            detail_category=detail_category,
            consumed_gmt_years=consumed_gmt_years,
            single_track=single_track,
            delta_sigma1=delta_sigma1,
            delta_sigma12=delta_sigma12
        )

        st.subheader("Results")

        for key, value in result.items():
            st.write(f"**{key}** : {value}")

# ==========================================================
# STRESS HISTORY FATIGUE ASSESSMENT
# ==========================================================

elif approach == "Stress-Time History Fatigue Assessment":

    st.header("Stress-Time History Fatigue Assessment")

    uploaded_file = st.file_uploader(
        "Upload Stress-Time Excel File",
        type=["xlsx"]
    )

    detail_category_excel = st.selectbox(
        "Select Detail Category",
        [160, 140, 125, 112, 100, 90, 80,
         71, 63, 56, 50, 45, 40, 36]
    )

    if uploaded_file:

        st.success("File Uploaded Successfully")

        df = pd.read_excel(uploaded_file)

        st.subheader("Input Data Preview")
        st.dataframe(df.head())

        if st.button("Run Fatigue Assessment"):

            with open("uploaded.xlsx", "wb") as f:
                f.write(uploaded_file.getbuffer())

            summary_df = run_fatigue_analysis(
                "uploaded.xlsx",
                detail_category_excel
            )

            st.success("Analysis Completed")

            st.subheader("Fatigue Assessment Summary")
            st.dataframe(summary_df)