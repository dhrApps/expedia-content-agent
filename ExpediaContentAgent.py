
import streamlit as st
import pandas as pd
from bs4 import BeautifulSoup
from io import BytesIO
import streamlit.components.v1 as components

st.set_page_config(page_title="Expedia Content Generator", page_icon="🌍")
st.title("🌍 Expedia Travel Content Generator")

st.write("""
Welcome to the Expedia Content Generator! ✈️🏝️

Create stunning content for your next travel campaign — fast and formatted perfectly.

📂 **How it works:**
1. Enter content details using visual editor.
2. Download a ready-to-upload Excel file.
""")

correct_columns = [
    "NAME (*)", "CONTENT_TYPE (*)", "PAGE_TYPE (*)", "TITLE", "SUBTITLE", "LANGUAGE (*)", "BODY",
    "EFFECTIVE_DATE_START", "EFFECTIVE_DATE_END", "POS_LOCALES (*)", "PUBLISHABLE (*)", "LOCATION",
    "ORIGIN", "DESTINATION", "MEDIA_ASSETS", "CAR_SUPPLIERS", "TOPICS", "AIR_SUPPLIERS", "AFFINITY",
    "HOTEL_ID_LIST", "HOTEL_BRAND", "IS_DEFAULT", "STARS", "SOURCE", "CONTENT_PURPOSE (*)",
    "ACCOMMODATIONS", "URL_LIST", "IMAGE_USAGE", "USE_POS_TIMEZONE", "CAR_SUPPLIER_IDS",
    "CRUISE_THEMES", "CRUISE_LINES", "CRUISE_SHIPS", "FLIGHT_NUMBER_LIST", "CAR_CLASS",
    "CAR_SUPPLIER_LOCATIONS", "POINT_OF_INTEREST_TYPE"
]

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
        st.warning(f"⚠️ Invalid PUBLISHABLE value '{value}'. Defaulting to 'false'. Please enter 'true' or 'false'.")
        return "false"

num_entries = st.number_input("How many content pieces would you like to add?", min_value=1, step=1)

content_entries = []

for i in range(num_entries):
    st.markdown(f"### Content Item {i + 1}")
    name = st.text_input("NAME (*)", key=f"name_{i}")
    content_type = st.text_input("CONTENT_TYPE (*)", key=f"ctype_{i}").upper()
    content_purpose = st.text_input("CONTENT_PURPOSE (*)", key=f"cpurpose_{i}")
    page_type = st.text_input("PAGE_TYPE (*)", value="Url-Mapping", key=f"ptype_{i}")
    pos_locales = st.text_input("POS_LOCALES (*)", key=f"pos_{i}")
    language = st.text_input("LANGUAGE (*)", key=f"lang_{i}")
    publishable = st.text_input("PUBLISHABLE (*) (true/false)", key=f"pub_{i}")
    title = st.text_input("TITLE", key=f"title_{i}")
    subtitle = st.text_input("SUBTITLE", key=f"subtitle_{i}")
    media_assets = st.text_input("MEDIA_ASSETS", key=f"media_{i}")
    url_list = st.text_input("URL_LIST", key=f"url_{i}")

    st.markdown("**BODY (use the rich text editor below):**")
    editor_id = f"editor_{i}"
    components.html(f'''
    <link href="https://cdn.jsdelivr.net/npm/summernote@0.8.18/dist/summernote-lite.min.css" rel="stylesheet">
    <script src="https://code.jquery.com/jquery-3.5.1.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/summernote@0.8.18/dist/summernote-lite.min.js"></script>
    <div id="{editor_id}"></div>
    <textarea id="{editor_id}_input" style="display:none;"></textarea>
    <script>
    const textarea = document.getElementById('{editor_id}_input');
    $('#{editor_id}').summernote({{
        height: 200,
        callbacks: {{
            onChange: function(contents) {{
                textarea.value = contents;
            }}
        }}
    }});
    </script>
    ''', height=300)

    body = st.text_area("Paste BODY HTML from above editor here:", key=f"body_{i}")

    content_entries.append({
        "NAME (*)": name,
        "CONTENT_TYPE (*)": content_type,
        "PAGE_TYPE (*)": page_type,
        "TITLE": title,
        "SUBTITLE": subtitle,
        "LANGUAGE (*)": language,
        "BODY": body,
        "EFFECTIVE_DATE_START": "",
        "EFFECTIVE_DATE_END": "",
        "POS_LOCALES (*)": pos_locales,
        "PUBLISHABLE (*)": publishable,
        "LOCATION": "",
        "ORIGIN": "",
        "DESTINATION": "",
        "MEDIA_ASSETS": media_assets,
        "CAR_SUPPLIERS": "",
        "TOPICS": "",
        "AIR_SUPPLIERS": "",
        "AFFINITY": "",
        "HOTEL_ID_LIST": "",
        "HOTEL_BRAND": "",
        "IS_DEFAULT": "",
        "STARS": "",
        "SOURCE": "",
        "CONTENT_PURPOSE (*)": content_purpose,
        "ACCOMMODATIONS": "",
        "URL_LIST": url_list,
        "IMAGE_USAGE": "",
        "USE_POS_TIMEZONE": "",
        "CAR_SUPPLIER_IDS": "",
        "CRUISE_THEMES": "",
        "CRUISE_LINES": "",
        "CRUISE_SHIPS": "",
        "FLIGHT_NUMBER_LIST": "",
        "CAR_CLASS": "",
        "CAR_SUPPLIER_LOCATIONS": "",
        "POINT_OF_INTEREST_TYPE": ""
    })

if st.button("Generate Excel File"):
    df = pd.DataFrame(content_entries)
    df = df[correct_columns]
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

