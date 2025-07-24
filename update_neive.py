import requests, json
from datetime import datetime

STATION_CODE = "NIEV"
CSV_URL = "https://www.arpa.piemonte.it/export/dati-meteo/rete-meteo/dati.csv"

def get_latest():
    r = requests.get(CSV_URL, timeout=30)
    r.raise_for_status()
    lines = r.text.splitlines()
    headers = lines[0].split(";")
    idx = {h: i for i, h in enumerate(headers)}
    latest = None
    for l in lines[1:]:
        cols = l.split(";")
        if cols[idx["codice"]] == STATION_CODE:
            latest = {
                "rain": float(cols[idx["pioggia"]] or 0),
                "time": cols[idx["data_lettura"]]
            }
    if not latest:
        raise RuntimeError("Stazione NIEV non trovata")
    return latest

def main():
    d = get_latest()
    with open("neive.json", "w") as f:
        json.dump({"station": STATION_CODE, **d}, f, indent=2)
    print("✅ Updated:", d)

if __name__=="__main__":
    main()
