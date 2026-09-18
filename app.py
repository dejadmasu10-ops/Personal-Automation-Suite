import os
import shutil
import tempfile
import zipfile

import streamlit as st

from personal_automation import (
    organize_files,
    log_weather,
    send_email,
    EMAIL
)


# ── PAGE CONFIGURATION ────────────────────────────

st.set_page_config(
    page_title="Personal Automation Suite",
    page_icon="⚙️",
    layout="wide"
)


# ── TITLE ─────────────────────────────────────────

st.title("⚙️ Personal Automation Suite")

st.write(
    "Automate file organization, weather logging, "
    "and email notifications from one web app."
)


# ── TABS ──────────────────────────────────────────

tab1, tab2, tab3 = st.tabs([
    "📁 File Organizer",
    "🌤️ Weather Logger",
    "📧 Email"
])


# ══════════════════════════════════════════════════
# FILE ORGANIZER
# ══════════════════════════════════════════════════

with tab1:

    st.header("📁 File Organizer")

    st.write(
        "Upload files and automatically organize them "
        "into folders based on their file type."
    )

    uploaded_files = st.file_uploader(
        "Upload your files",
        accept_multiple_files=True
    )

    if uploaded_files:

        if st.button(
            "Organize Files",
            key="organize_button"
        ):

            try:

                with tempfile.TemporaryDirectory() as temp_folder:

                    # Save uploaded files
                    for uploaded_file in uploaded_files:

                        file_path = os.path.join(
                            temp_folder,
                            uploaded_file.name
                        )

                        with open(
                            file_path,
                            "wb"
                        ) as file:

                            file.write(
                                uploaded_file.getbuffer()
                            )

                    # Organize files
                    result = organize_files(
                        temp_folder
                    )

                    st.success(result)

                    # Create ZIP file
                    zip_path = os.path.join(
                        temp_folder,
                        "organized_files.zip"
                    )

                    with zipfile.ZipFile(
                        zip_path,
                        "w",
                        zipfile.ZIP_DEFLATED
                    ) as zip_file:

                        for root, folders, files in os.walk(
                            temp_folder
                        ):

                            for filename in files:

                                full_path = os.path.join(
                                    root,
                                    filename
                                )

                                if full_path == zip_path:
                                    continue

                                archive_path = os.path.relpath(
                                    full_path,
                                    temp_folder
                                )

                                zip_file.write(
                                    full_path,
                                    archive_path
                                )

                    with open(
                        zip_path,
                        "rb"
                    ) as file:

                        zip_data = file.read()

                    st.download_button(
                        label="⬇️ Download Organized Files",
                        data=zip_data,
                        file_name="organized_files.zip",
                        mime="application/zip"
                    )

            except Exception as e:

                st.error(
                    f"File organization error: {e}"
                )


# ══════════════════════════════════════════════════
# WEATHER LOGGER
# ══════════════════════════════════════════════════

with tab2:

    st.header("🌤️ Weather Logger")

    st.write(
        "Enter a city to retrieve its current weather "
        "and save the result to the weather log."
    )

    city = st.text_input(
        "Enter city name",
        placeholder="Example: Kanpur"
    )

    if st.button(
        "Get Weather",
        key="weather_button"
    ):

        if city.strip():

            result = log_weather(
                city.strip()
            )

            if result.startswith("Weather logged"):

                st.success(result)

            else:

                st.error(result)

        else:

            st.warning(
                "Please enter a city name."
            )

    # Show existing weather log
    if os.path.exists("weather_log.csv"):

        st.subheader("📊 Weather Log")

        try:

            import pandas as pd

            weather_data = pd.read_csv(
                "weather_log.csv"
            )

            st.dataframe(
                weather_data,
                use_container_width=True
            )

            with open(
                "weather_log.csv",
                "rb"
            ) as file:

                st.download_button(
                    label="⬇️ Download Weather Log",
                    data=file,
                    file_name="weather_log.csv",
                    mime="text/csv"
                )

        except Exception as e:

            st.error(
                f"Error reading weather log: {e}"
            )


# ══════════════════════════════════════════════════
# EMAIL
# ══════════════════════════════════════════════════

with tab3:

    st.header("📧 Email Status")

    st.write(
        "Send an automated status email using Gmail."
    )

    recipient = st.text_input(
        "Recipient email",
        value=EMAIL if EMAIL else ""
    )

    subject = st.text_input(
        "Subject",
        value="Automation Suite Status"
    )

    message = st.text_area(
        "Message",
        value="Hello from my automation suite."
    )

    if st.button(
        "Send Email",
        key="email_button"
    ):

        if not recipient:

            st.warning(
                "Please enter a recipient email."
            )

        elif not message:

            st.warning(
                "Please enter a message."
            )

        else:

            result = send_email(
                recipient,
                subject,
                message
            )

            if result == "Email sent successfully":

                st.success(result)

            else:

                st.error(result)


# ── FOOTER ────────────────────────────────────────

st.divider()

st.caption(
    "Personal Automation Suite | Python + Streamlit + APIs"
)