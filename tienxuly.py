import re

with open("D:\\DoAn2\\data\\all_text_raw.txt", encoding="utf-8") as f:
    lines = f.readlines()

clean = []
for l in lines:
    l = l.strip()
    l = re.sub(r'\s+', ' ', l)
    if len(l) > 10:
        clean.append(l)

with open("all_text.txt", "w", encoding="utf-8") as f:
    for l in clean:
        f.write(l+"\n")

print("Saved", len(clean), "lines")
print("✅ Saved data/all_text.txt")