import sys
import requests
from bs4 import BeautifulSoup

def obten_horarios() -> str:
    return requests.post("https://metropolitanogranada.es/MGhorariosreal.asp",
        headers={
            "Origin": "https://metropolitanogranada.es",
            "Referer": "https://metropolitanogranada.es/horariosreal",
            "TE": "trailers",
            },
    ).content

def imprime_tiempos(html_content : str, parada: str) -> None:
    soup = BeautifulSoup(html_content, 'html.parser')
    tabla = soup.find('table')

    # Extraer tiempos
    for row in tabla.find_all('tr')[1:]:  # Saltar el primer tr que contiene los encabezados
        fila = [col.get_text(strip=True) for col in row.find_all('td')]
        if parada in fila:
            # Formato de fila: ['Parada', "X'", "Y'", "Z'", "W'"]
            tiempos_albolote = fila[1:3]
            tiempos_armilla = fila[3:5]
            break
    
    if len(tiempos_albolote) > 0 and len(tiempos_armilla) > 0:
        print(f"\"{parada}\". Minutos faltantes.\n")
        rows = [
            ['Dirección', 'Tranvía Inminente', 'Siguiente'],
            ['Albolote', tiempos_albolote[0], tiempos_albolote[1]], 
            ['Armilla', tiempos_armilla[0], tiempos_armilla[1]],
        ]
        widths = [max(map(len, col)) for col in zip(*rows)]
        for row in rows:
            print("  ".join((val.ljust(width) for val, width in zip(row, widths))))
    else:        
        print("No existe una parada con ese nombre")
    
def run():
    parada = None
    if len(sys.argv) != 2:
        parada = input("¿Qué parada quiere consultar? ")
    else:
        parada = sys.argv[1]

    try:
        html_content = obten_horarios()
        imprime_tiempos(html_content, parada)
    except ConnectionError:
        print("No he conseguido establecer conexión con el servidor")
        exit(1)
    
    exit(0)

if __name__ == '__main__':
    run()