import re,string, json

def strip_links(text):
    link_regex    = re.compile('((http?):((//)|(\\\\))+([\w\d:#@%/;$()~_?\+-=\\\.&](#!)?)*)', re.DOTALL)
    links         = re.findall(link_regex, text)
    for link in links:
        text = text.replace(link[0], ', ')
        text = text.replace(link[1], ', ')
    link_regex    = re.compile('((https?):((//)|(\\\\))+([\w\d:#@%/;$()~_?\+-=\\\.&](#!)?)*)', re.DOTALL)
    links         = re.findall(link_regex, text)
    for link in links:
        text = text.replace(link[0], ', ')
        text = text.replace(link[1], ', ')
    text = text.replace("http/URL",", ")
    return text

def strip_all_entities(text):
    entity_prefixes = ['@','#']
    for separator in  string.punctuation:
        if separator not in entity_prefixes :
            text = text.replace(separator,' ')
    words = []
    for word in text.split():
        word = word.strip()
        if word:
            if word[0] not in entity_prefixes:
                words.append(word)
            elif word[0] == "#":
                words.append(word[1:])
            elif word[0] == "@":
                words.append("$USER")
    return ' '.join(words)

with open("codemixing_iiits.json") as rd:
    lines = json.load(rd)

cleaned_data = open("CODEMIXED_DATA.json","w")

finalt = []

for x in lines:
    f = x
    if type(f["text"])==type(1.0):
        continue
    cdata = strip_all_entities(strip_links(f["text"]))
    if len(cdata.split()) > 3:
        finalt.append({
            "text": f["text"],
            "lang_tagged_text": f["lang_tagged_text"],
            "sentiment": f["sentiment"],
            })

json.dump(finalt, cleaned_data, indent=4)
