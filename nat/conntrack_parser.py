from pathlib import Path
def parse_conntrack(conntrack_content):
    lines = conntrack_content.split("\n")
    entries=[]
    for line in lines:
        if "src" not in line:
            continue
        words = line.split()
        orig_src=words[3].split("=")[1]
        orig_dst=words[4].split("=")[1]
        reply_src=words[10].split("=")[1]
        reply_dst=words[11].split("=")[1]
        entry={
            "protocol":words[0],
            "orig_src" : orig_src,
            "orig_dst" : orig_dst,
            "reply_src" : reply_src,
            "reply_dst" : reply_dst

        }
        entries.append(entry)
    return entries

def is_natted(entry):
        if entry["orig_src"] != entry["reply_dst"]:
           return True
        else:
            return False   
            
