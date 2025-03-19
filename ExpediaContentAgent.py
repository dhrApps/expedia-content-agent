
import streamlit as st
import pandas as pd
from bs4 import BeautifulSoup
from io import BytesIO

st.set_page_config(page_title="Expedia Content Generator", page_icon="🌍")
st.title("🌍 Expedia Travel Content Generator")

st.write("""Welcome to the Expedia Content Generator! ✈️🏝️

Create stunning content for your next travel campaign — fast and formatted perfectly.

📂 **How it works:**
1. Enter content details using visual editor.
2. Download a ready-to-upload Excel file.
""")

# Simulated content_entries for testing (you can replace this with actual user inputs)
content_entries = []

def fix_html_content(html_text):
    if not html_text:
        return html_text
    try:
        soup = BeautifulSoup(html_text, "html.parser")
        for tag in soup.find_all(href=True):
            tag['href'] = tag['href'].replace('\"', '').replace('"', '')
        return str(soup)
    except Exception:
        return html_text

def format_pos_locales(value):
    try:
        if not value or '.' not in value:
            return value
        before_dot, after_dot = value.split('.')
        locale_parts = after_dot.split('_')
        if len(locale_parts) != 2:
            return value
        formatted_before = before_dot.upper()
        formatted_after = f"{locale_parts[0].lower()}_{locale_parts[1].upper()}"
        return f"{formatted_before}.{formatted_after}"
    except Exception:
        return value

def validate_publishable(value):
    value_str = str(value).strip().lower()
    if value_str in ["true", "false"]:
        return value_str
    else:
        return "false"

# Simulate button to generate file
if st.button("Generate Excel File"):
    df = pd.DataFrame(content_entries)
    df["BODY"] = df["BODY"].apply(fix_html_content)
    df["POS_LOCALES (*)"] = df["POS_LOCALES (*)"].apply(format_pos_locales)
    df["PUBLISHABLE (*)"] = df["PUBLISHABLE (*)"].apply(validate_publishable)
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Content')
        worksheet = writer.sheets['Content']
        for cell in worksheet[1]:
            cell.font = cell.font.copy(bold=False)
    output.seek(0)
    st.success("✅ Excel file generated successfully!")
    st.download_button("📥 Download Excel File", data=output, file_name="expedia_content_upload.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    
    st.markdown("""
    ---
    🎯 **Next Step: Generate Your Landing Page Template**

    Once you've uploaded your content and received your Content IDs,  
    👉 [Click here to create your Landing Page Template](https://streamlit.io/)  
    *(Replace this link with your deployed Template Generator Agent URL)*
    """)

