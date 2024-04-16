import os
import os

for folder in os.listdir("Mappers"):
    folder_path = os.path.join("Mappers", folder)
    if os.path.isdir(folder_path):
        for file in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file)
            if os.path.isfile(file_path):
                with open(file_path, "w") as f:
                    f.write("")

for file in os.listdir("Reducers"):
    with open(f"Reducers/{file}", "w") as f:
        f.write("")

with open("dump.txt", "w") as f:
    f.write("")