# import streamlit as st
# import pandas as pd
# import numpy as np
import time
import re
import xml.dom.minidom


def extract_text(file: str) -> str:
	with open(file, "r") as f:
		return f.read()


def parse_custom_syntax(text):
    """
    Parse recursively a string in the format 'tag:<content>' to transform it into XML.
    """
    # Pattern to find 'mot:<'
    token_pattern = re.compile(r'(\w+):<')
    
    cursor = 0
    output_parts = []
    
    while cursor < len(text):
        match = token_pattern.search(text, cursor)
        
        # If we can't find any opening tag, we add the rest of the text
        if not match:
            remaining_text = text[cursor:]
            if remaining_text.strip():
                output_parts.append(remaining_text)
            break
        
        # Add the text that is before the tag (ex: "macOS 26.1, ")
        if match.start() > cursor:
            pre_text = text[cursor:match.start()]
            if pre_text.strip():
                output_parts.append(pre_text)
        
        tag_name = match.group(1)
        start_content_index = match.end()
        
        # Find the corresponding closing '>' tag while handling nesting
        nesting_level = 1
        end_content_index = start_content_index
        found_closing = False
        
        while end_content_index < len(text):
            char = text[end_content_index]
            if char == '<':
                nesting_level += 1
            elif char == '>':
                nesting_level -= 1
                if nesting_level == 0:
                    found_closing = True
                    break
            end_content_index += 1
        
        if found_closing:
            # Recursive call for the content inside
            inner_content = text[start_content_index:end_content_index]
            parsed_inner = parse_custom_syntax(inner_content)
            
            # Construction of the XML tag
            output_parts.append(f"<{tag_name}>{parsed_inner}</{tag_name}>")
            cursor = end_content_index + 1
        else:
            # If there is no closing (syntax error), we treat it as text
            output_parts.append(text[cursor:])
            break
            
    return "".join(output_parts)

def format_xml(xml_string):
    """Format a raw XML string with correct indentation."""
    try:
        # We wrap in a fake root if necessary for the initial parsing if the XML is not valid
        # But here, the output is usually fragmented. We try to parse directly.
        # Trick: minidom needs a unique root. If the user enters multiple roots, we wrap.
        xml_string = f"<root>{xml_string}</root>"
        dom = xml.dom.minidom.parseString(xml_string)
        pretty_xml = dom.toprettyxml(indent="  ")
        
        # We remove the <root> wrapper and the XML declaration to comply with the request
        lines = pretty_xml.split('\n')
        cleaned_lines = []
        for line in lines:
            if "<?xml" in line or "<root>" in line or "</root>" in line:
                continue
            if line.strip():
                # We unindent one level because we removed root
                cleaned_lines.append(line[2:] if line.startswith("  ") else line)
        
        return "\n".join(cleaned_lines)
    except Exception as e:
        return f"XML formatting error: {str(e)}\nRaw XML: {xml_string}"

# --- Configuration Streamlit ---
# st.set_page_config(
#     page_title="App Python & XML",
#     page_icon="🐍",
#     layout="wide"
# )

# # --- Sidebar ---
# st.sidebar.title("Configuration")
# st.sidebar.info("Control panel")

# nom_utilisateur = st.sidebar.text_input("Your name", "User")
# option_choisie = st.sidebar.selectbox(
#     "Selected tool",
#     ["Data analysis", "Smart XML converter", "Image processing"]
# )

# if st.sidebar.button("Execute"):
#     with st.spinner('Processing...'):
#         time.sleep(0.5)
#     st.sidebar.success("Done!")

# # --- Corps Principal ---
# st.title("Python Tools Box")
# st.markdown(f"Hello **{nom_utilisateur}**, welcome to your workspace.")

# col1, col2 = st.columns([2, 1])

# with col1:
#     if option_choisie == "Data analysis":
#         st.subheader("Data visualization")
#         chart_data = pd.DataFrame(np.random.randn(20, 3), columns=['A', 'B', 'C'])
#         st.line_chart(chart_data)
        
#     elif option_choisie == "Smart XML converter":
#         st.subheader("Custom syntax converter to XML")
#         st.markdown("Transform `tag:<content>` into `<tag>content</tag>` intelligently.")
        
#         # Zone de texte avec l'exemple par défaut
#         default_text = "context:<macOS 26.1, machine:<Macbook Pro> puce:<Silicon Apple M4 Pro>>"
#         input_text = st.text_area("Input (Custom syntax)", default_text, height=100)
        
#         if input_text:
#             # 1. Parsing
#             raw_xml = parse_custom_syntax(input_text)
            
#             # 2. Light cleaning (removal of parasitic separation commas if desired)
#             # For the strict example, we keep the text as is, but the pretty print will help.
            
#             # 3. Formatting
#             formatted_xml = format_xml(raw_xml)
            
#             st.code(formatted_xml, language='xml')
            
#             # Copy button (handled natively by st.code but we can add a download)
#             st.download_button("Download the result .xml", formatted_xml, file_name="output.xml")

#     elif option_choisie == "Image processing":
#         st.info("Module under construction. Come back later.")

# with col2:
#     st.subheader("Logs / Info")
#     st.markdown("System status : **Online**")
    
#     if option_choisie == "Smart XML converter":
#         st.info("""
#         **Parsing rules :**
#         - `tag:<...>` becomes a tag.
#         - Tags can be nested.
#         - The text between tags is preserved.
#         """)
#     else:
#         st.metric(label="CPU usage", value="12%", delta="-2%")

# # Footer
# st.markdown("---")
# st.caption("Generated via Streamlit")