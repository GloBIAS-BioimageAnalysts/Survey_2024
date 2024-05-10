import os

script_directory = str(os.path.dirname(os.path.abspath(__file__)))
file_path = "figures/README.md"
full_path=os.path.join(script_directory, "..", file_path)

print (f"Modifying file at: {full_path}")

# Updates the markdown file for the figures directory
folder_path = os.path.dirname(full_path)
with open(full_path, 'w') as md_file:
    
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.png') or file_name.endswith('.jpg') or file_name.endswith('.jpeg') or file_name.endswith('.gif'):
            image_path = os.path.join(folder_path, file_name)
            print (f"Adding {file_name}")
            md_file.write(f"## {os.path.splitext(file_name)[0]}\n")
            md_file.write(f"![{file_name}]({file_name})\n\n")