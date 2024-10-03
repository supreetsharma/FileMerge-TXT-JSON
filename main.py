import streamlit as st
import json
import io

st.set_page_config(page_title="File Processor", page_icon="📄", layout="wide")

def process_files(txt_file, json_file, selected_tags):
    # Read the content of the text file
    txt_content = txt_file.getvalue().decode("utf-8")
    
    try:
        # Parse the JSON file
        json_data = json.loads(json_file.getvalue().decode("utf-8"))
        
        # Create the new content with selected tags
        new_content = ""
        for tag in selected_tags:
            if tag in json_data:
                new_content += f"{tag}: {json_data[tag]}\n"
        new_content += "\n" + txt_content
        
        return new_content
    except json.JSONDecodeError:
        st.error("Error parsing JSON file. Please make sure it's a valid JSON.")
        return None

def main():
    st.title("📄 File Processor")
    st.write("Upload .txt and .json files, select tags, and generate new .txt files with combined content.")

    # File upload section
    col1, col2 = st.columns(2)
    with col1:
        txt_file = st.file_uploader("Upload .txt file", type="txt")
    with col2:
        json_file = st.file_uploader("Upload .json file", type="json")

    if txt_file and json_file:
        try:
            # Process JSON file and display tags
            json_data = json.loads(json_file.getvalue().decode("utf-8"))
            available_tags = list(json_data.keys())

            if available_tags:
                st.write("Available tags:")
                selected_tags = st.multiselect("Select tags to include:", available_tags)

                if selected_tags:
                    if st.button("Process Files"):
                        # Process files and generate new content
                        new_content = process_files(txt_file, json_file, selected_tags)

                        if new_content:
                            # Display preview of the new content
                            st.write("Preview of the new file:")
                            st.text_area("Content", new_content, height=300)

                            # Provide download option
                            st.download_button(
                                label="Download Processed File",
                                data=new_content,
                                file_name="processed_file.txt",
                                mime="text/plain"
                            )
                else:
                    st.warning("Please select at least one tag.")
            else:
                st.error("No tags found in the JSON file.")
        except json.JSONDecodeError:
            st.error("Error parsing JSON file. Please make sure it's a valid JSON.")
    else:
        st.info("Please upload both .txt and .json files to proceed.")

if __name__ == "__main__":
    main()
