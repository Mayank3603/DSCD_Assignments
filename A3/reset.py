import os
for folders in os.listdir("Mappers"):
    for file in os.listdir(f"Mappers/{folders}"):
        with open(f"Mappers/{folders}/{file}", "w") as f:
            f.write("")