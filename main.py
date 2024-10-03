import streamlit as st
import json
import io
import zipfile

st.set_page_config(page_title="File Processor", page_icon="📄", layout="wide")

def process_file_pair(txt_file, json_file, selected_tags):
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
        st.error(f"Error parsing JSON file '{json_file.name}'. Please make sure it's a valid JSON.")
        return None

def process_multiple_file_pairs(txt_files, json_files, selected_tags):
    processed_files = []
    for txt_file, json_file in zip(txt_files, json_files):
        new_content = process_file_pair(txt_file, json_file, selected_tags)
        if new_content:
            processed_files.append((f"processed_{txt_file.name}", new_content))
    return processed_files

def main():
    st.title("📄 File Processor")
    st.write("Upload multiple .txt and .json file pairs, select tags, and generate new .txt files with combined content.")

    # File upload section
    txt_files = st.file_uploader("Upload .txt files", type="txt", accept_multiple_files=True)
    json_files = st.file_uploader("Upload .json files", type="json", accept_multiple_files=True)

    if txt_files and json_files:
        if len(txt_files) != len(json_files):
            st.error("The number of .txt files must match the number of .json files.")
        else:
            try:
                # Process the first JSON file to get available tags
                json_data = json.loads(json_files[0].getvalue().decode("utf-8"))
                available_tags = list(json_data.keys())

                if available_tags:
                    st.write("Available tags:")
                    selected_tags = st.multiselect("Select tags to include:", available_tags)

                    if selected_tags:
                        if st.button("Process Files"):
                            # Process files and generate new content
                            processed_files = process_multiple_file_pairs(txt_files, json_files, selected_tags)

                            if processed_files:
                                # Create a zip file containing all processed files
                                zip_buffer = io.BytesIO()
                                with zipfile.ZipFile(zip_buffer, "w") as zip_file:
                                    for filename, content in processed_files:
                                        zip_file.writestr(filename, content)

                                # Provide download option for the zip file
                                st.download_button(
                                    label="Download Processed Files (ZIP)",
                                    data=zip_buffer.getvalue(),
                                    file_name="processed_files.zip",
                                    mime="application/zip"
                                )

                                # Display preview of the first processed file
                                st.write("Preview of the first processed file:")
                                st.text_area("Content", processed_files[0][1], height=300)
                    else:
                        st.warning("Please select at least one tag.")
                else:
                    st.error("No tags found in the JSON files.")
            except json.JSONDecodeError:
                st.error("Error parsing JSON files. Please make sure they are valid JSON.")
    else:
        st.info("Please upload both .txt and .json files to proceed.")

if __name__ == "__main__":
    main()
