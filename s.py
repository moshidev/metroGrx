import sys
import requests
import pandas as pd

def obten_horarios() -> pd.DataFrame:
    return requests.post("https://metropolitanogranada.es/MGhorariosreal.asp",
        headers={
            "Origin": "https://metropolitanogranada.es",
            "Referer": "https://metropolitanogranada.es/horariosreal",
            "TE": "trailers",
            },
    ).content

def imprime_tiempos(df: pd.DataFrame, parada: str) -> None:
    try:
        paradas = df["Parada"].to_list()
        i = paradas.index(parada)
        d = t.T[i].to_dict()
        print(f"A Albolote: {d['a Albolote']}")
        print(f"A Armilla: {d['a Armilla']}")
    except ValueError:
        print("No existe una parada con ese nombre")

if __name__ == '__main__':
    parada = None
    if len(sys.argv) != 2:
        parada = input("¿Qué parada quiere consultar? ")
    else:
        parada = sys.argv[1]

    try:
        t = pd.read_html(obten_horarios(), encoding='utf8')[0]
        imprime_tiempos(t, parada)
    except ConnectionError:
        print("No he conseguido establecer conexión con el servidor")
        exit(1)
    
    exit(0)
