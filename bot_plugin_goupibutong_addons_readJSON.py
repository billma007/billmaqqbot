def readjson():
    import json
    with open(r"data/goupibutongdata.json","r",encoding="utf-8") as datajson:
        l=json.load(datajson)
        datajson.close()
    return l
