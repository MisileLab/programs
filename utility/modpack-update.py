import os
from sys import exit
from simple_term_menu import TerminalMenu
from tqdm import tqdm
import requests

os.chdir(input("input path: "))
print(f"current path: {os.getcwd()}")

menu = TerminalMenu(
    ["BasicCraft", "SomeMechanics"],
    title="What modpack?"
)

menu.show()

a = os.listdir()
b = requests.get(f"https://gitea.misilelaboratory.xyz/api/v1/repos/misilelaboratory/modpack/contents/modpacks%2F{menu.chosen_menu_entry}%2Fmods").json()

for i in tqdm(requests.get(f"https://gitea.misilelaboratory.xyz/api/v1/repos/misilelaboratory/modpack/contents/modpacks%2F{menu.chosen_menu_entry}%2Fmods").json()):
    if a.__contains__(i["name"]):
        a.remove(i["name"])
        b.remove(i)

for i in tqdm(a):
    os.remove(i)
    print(f"removed: {i}")

for i in tqdm(b):
    name = i["name"]
    with requests.get(i["download_url"]) as r:
        with open(name, 'wb') as f:
            for chunk in tqdm(r.iter_content(chunk_size=8192)):
                f.write(chunk)
    print(f"downloaded: {name}")