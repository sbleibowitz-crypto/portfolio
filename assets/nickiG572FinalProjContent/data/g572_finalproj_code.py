#part of GEOG 572 Final Project- parsing Nicki Minaj lyrics for geographies
#this code was written with assistance from Microsoft Copilot

import pandas as pd
import json
import re
import spacy


nlp = spacy.load("en_core_web_sm")

with open("/Users/sleibowitz/Downloads/datasets.json", "r") as f:
    data = json.load(f)

slang_map = {
    "philly": "Philadelphia",
    "nyc": "New York City",
    "bk": "Brooklyn",
    "queens": "Queens",
    "jersey": "New Jersey",
    "chi-town": "Chicago",
    "kc": "Kansas City",
    "stl": "St. Louis",
    "cali": "California",
    "la": "Los Angeles",
    "the bay": "Bay Area",
    "vegas": "Las Vegas",
    "nola": "New Orleans",
    "the a": "Atlanta",
    "mia": "Miami",
}

def extract_places(text):
    if not isinstance(text, str):
        return []
        
    doc = nlp(text)

    spacy_places = [ent.text for ent in doc.ents if ent.label_ in ("GPE", "LOC")]

    found_slang = [slang_map[word] for word in slang_map if re.search(rf"\b{re.escape(word)}\b", text.lower())]
    return list(set(spacy_places + found_slang))

results = []
for lyric in data["train"]:
    places = extract_places(lyric)
    results.append({"Lyrics": lyric, "Places Found": ", ".join(places)})

df = pd.DataFrame(results)
df.to_excel("lyrics_with_places_spacy.xlsx", index=False)




df = pd.read_excel("/Users/sleibowitz/Downloads/lyrics_with_places_spacy.xlsx")
df["Places Found"] = df["Places Found"].astype(str)
df_expanded = df.assign(Phrase=df["Places Found"].str.split(",")).explode("Places Found")
df_expanded["Places Found"] = df_expanded["Places Found"].str.strip()
df_final = df_expanded[["Places Found"]]
df_final.to_excel("phrases_column_expanded1.xlsx", index=False)