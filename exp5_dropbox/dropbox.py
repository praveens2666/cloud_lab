!pip install dropbox

import dropbox

# Connect to Dropbox
TOKEN = "YOUR_ACCESS_TOKEN"
dbx = dropbox.Dropbox(TOKEN)

while True:
    print("\n--- Dropbox Storage ---")
    print("1. Upload")
    print("2. Download")
    print("3. Exit")

    ch = input("Enter choice: ")

    # Upload file
    if ch == "1":
        name = input("Enter file name: ")

        try:
            with open(name, "rb") as f:
                dbx.files_upload(
                    f.read(),
                    "/" + name,
                    mode=dropbox.files.WriteMode.overwrite
                )

            print("Upload successful!")

        except Exception as e:
            print("Error:", e)

    # List and download file
    elif ch == "2":
        try:
            result = dbx.files_list_folder("")
            files_list = []

            print("\n--- Files in Dropbox ---")

            while True:
                for item in result.entries:
                    if isinstance(item, dropbox.files.FileMetadata):
                        files_list.append(item)
                        print(item.name)

                if not result.has_more:
                    break

                result = dbx.files_list_folder_continue(
                    result.cursor
                )

            if not files_list:
                print("No files found.")
                continue

            name = input("\nEnter file name to download: ")

            # Find the selected file
            selected = next(
                (item for item in files_list
                 if item.name == name),
                None
            )

            if selected is None:
                print("File not found.")
                continue

            metadata, response = dbx.files_download(
                selected.path_lower
            )

            with open("downloaded_" + name, "wb") as f:
                f.write(response.content)

            print("Download successful!")
            print("Saved as: downloaded_" + name)

        except Exception as e:
            print("Error:", e)

    # Exit
    elif ch == "3":
        print("Exiting program...")
        break

    else:
        print("Invalid choice. Try again.")
