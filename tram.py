# MIT LICENSE
# Daniel Pedrosa © 2024
# Yeray López © 2024

import sys
import requests
from bs4 import BeautifulSoup
from cmd import Cmd

# Funciones relacionadas con la obtención de los horarios y paradas
def obten_horarios() -> str:
    return requests.post("https://metropolitanogranada.es/MGhorariosreal.asp",
        headers={
            "Origin": "https://metropolitanogranada.es",
            "Referer": "https://metropolitanogranada.es/horariosreal",
            "TE": "trailers",
            },
    ).content

def get_paradas(html_content: str) -> list:
    soup = BeautifulSoup(html_content, 'html.parser')
    tabla = soup.find('table')
    
    # Extraer las filas
    paradas = []
    for row in tabla.find_all('tr')[1:]:  # Saltar el primer tr que contiene los encabezados
        columnas = row.find_all('td')
        fila = [col.get_text().strip() for col in columnas]
        paradas.append(fila[0])  # Asumiendo que la primera columna es el nombre de la parada

    return paradas

def imprime_tiempos(html_content : str, parada: str) -> None:
    soup = BeautifulSoup(html_content, 'html.parser')
    tabla = soup.find('table')

    # Extraer tiempos
    tiempos_albolote, tiempos_armilla = [], []
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

# Clase interactiva basada en CMD
class TramCMD(Cmd):
    def __init__(self):
        super().__init__()
        self.prompt = 'metroGrx> '
        self.html_content = obten_horarios()
        self.parada_options = get_paradas(self.html_content)

    def do_parada(self, parada):
        """
        Consulta los tiempos para una parada específica.
        Uso: parada <nombre de la parada>
        """
        if parada in self.parada_options:
            imprime_tiempos(self.html_content, parada)
        else:
            print(f"Parada '{parada}' no encontrada. Prueba con una de las siguientes: {', '.join(self.parada_options)}")

    def complete_parada(self, text, line, start_index, end_index):
        if text: # Si ya he empezado a escribir la opción, filtrar las opciones existentes
            return [
                option for option in self.parada_options
                if option.startswith(text)
            ]
        else:
            return self.parada_options

    def do_salir(self, arg):
        """Salir del programa"""
        print("Saliendo del sistema de metroGrx...")
        return True

# Ejecución principal
if __name__ == '__main__':
    try:
        # Si se pasa el nombre de la parada como argumento en la línea de comandos
        if len(sys.argv) > 1:
            parada = sys.argv[1]
            html_content = obten_horarios()
            paradas = get_paradas(html_content)
            if parada in paradas:
                imprime_tiempos(html_content, parada)
            else:
                print(f"Parada '{parada}' no encontrada. Prueba con una de las siguientes: {', '.join(paradas)}")
        else:
            # Iniciar modo interactivo
            tram_cmd = TramCMD()
            tram_cmd.cmdloop()
    except ConnectionError:
        print("No se ha podido establecer conexión con el servidor.")