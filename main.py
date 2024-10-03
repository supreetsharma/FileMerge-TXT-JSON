import streamlit as st
import json
import io
import zipfile

st.set_page_config(page_title="File Processor", page_icon="📄", layout="wide")

def process_file_pair(txt_file, json_file, selected_tags, custom_tags):
    txt_content = txt_file.getvalue().decode("utf-8")
    
    try:
        json_data = json.loads(json_file.getvalue().decode("utf-8"))
        
        # Handle both list and dictionary cases
        if isinstance(json_data, list):
            json_data = json_data[0] if json_data else {}
        elif not isinstance(json_data, dict):
            raise ValueError("JSON content must be either a list or a dictionary")

        new_content = ""
        for tag in selected_tags:
            if tag in json_data:
                new_content += f"{tag}: {json_data[tag]}\n"
        
        # Add custom tags to the content
        if custom_tags:
            new_content += f"Custom Tags: {', '.join(custom_tags)}\n"
        
        new_content += "\n" + txt_content
        
        return new_content
    except json.JSONDecodeError:
        st.error(f"Error parsing JSON file '{json_file.name}'. Please make sure it's a valid JSON.")
        return None
    except ValueError as e:
        st.error(str(e))
        return None

def process_multiple_file_pairs(txt_files, json_files, selected_tags, custom_tags):
    processed_files = []
    for txt_file, json_file in zip(txt_files, json_files):
        new_content = process_file_pair(txt_file, json_file, selected_tags, custom_tags)
        if new_content:
            # Include custom tags in the filename
            tags_string = "_".join(custom_tags).replace(" ", "-") if custom_tags else "no-tags"
            new_filename = f"processed_{tags_string}_{txt_file.name}"
            processed_files.append((new_filename, new_content))
    return processed_files

def match_file_pairs(txt_files, json_files):
    txt_dict = {file.name.split('.')[0]: file for file in txt_files}
    json_dict = {file.name.split('.')[0]: file for file in json_files}
    matched_pairs = []
    for name in set(txt_dict.keys()) & set(json_dict.keys()):
        matched_pairs.append((txt_dict[name], json_dict[name]))
    return matched_pairs

def main():
    st.title("📄 File Processor")
    st.write("Upload multiple .txt and .json file pairs, select tags, add custom tags, and generate new .txt files with combined content.")

    # File upload section
    txt_files = st.file_uploader("Upload .txt files", type="txt", accept_multiple_files=True)
    json_files = st.file_uploader("Upload .json files", type="json", accept_multiple_files=True)

    if txt_files or json_files:
        txt_count = len(txt_files) if txt_files else 0
        json_count = len(json_files) if json_files else 0

        if txt_count != json_count:
            st.error(f"Mismatched file counts: {txt_count} .txt files and {json_count} .json files.")
            if txt_count > json_count:
                st.warning(f"Please upload {txt_count - json_count} more .json file(s) to match the number of .txt files.")
            else:
                st.warning(f"Please upload {json_count - txt_count} more .txt file(s) to match the number of .json files.")
            st.info("You can remove files by clicking the 'X' next to their names in the file uploader.")
        elif txt_count == 0:
            st.warning("Please upload both .txt and .json files to proceed.")
        else:
            if txt_count > 0 and json_count > 0:
                matched_pairs = match_file_pairs(txt_files, json_files)
                if matched_pairs:
                    st.subheader("Matched File Pairs")
                    table_data = [{"Text File": txt.name, "JSON File": json.name} for txt, json in matched_pairs]
                    st.table(table_data)
                else:
                    st.warning("No matching file pairs found. Please ensure file names (excluding extensions) are the same for .txt and .json files.")

            try:
                # Process the first JSON file to get available tags
                json_data = json.loads(json_files[0].getvalue().decode("utf-8"))
                if isinstance(json_data, list):
                    json_data = json_data[0] if json_data else {}
                available_tags = list(json_data.keys())

                if available_tags:
                    st.write("Available tags:")
                    selected_tags = st.multiselect("Select tags to include:", available_tags)

                    # Add custom tags input
                    custom_tags_input = st.text_input("Add custom tags (comma-separated):")
                    custom_tags = [tag.strip() for tag in custom_tags_input.split(",")] if custom_tags_input else []

                    if selected_tags or custom_tags:
                        if st.button("Process Files"):
                            if matched_pairs:
                                # Process files and generate new content
                                processed_files = process_multiple_file_pairs([txt for txt, _ in matched_pairs], [json for _, json in matched_pairs], selected_tags, custom_tags)

                                if processed_files:
                                    # Preview section
                                    st.subheader("Preview of Processed Files")
                                    for idx, (filename, content) in enumerate(processed_files):
                                        with st.expander(f"Preview: {filename}"):
                                            st.text_area(f"Content of {filename}", content, height=200)

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
                            else:
                                st.error("No matching file pairs found. Please ensure file names (excluding extensions) are the same for .txt and .json files.")
                    else:
                        st.warning("Please select at least one tag or add custom tags.")
                else:
                    st.error("No tags found in the JSON files.")
            except json.JSONDecodeError:
                st.error("Error parsing JSON files. Please make sure they are valid JSON.")

if __name__ == "__main__":
    main()
