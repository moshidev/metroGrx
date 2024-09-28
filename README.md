# metroGrx

Tiempo restante para el próximo tranvía del metropolitano
dado el nombre de una parada.

## Tenga en cuenta

Este script no es oficial ni está asociado a ninguna empresa.

Este script es código libre, liberado con licencia MIT.

Depende en la información que proporciona la página web
[https://metropolitanogranada.es/horariosreal](https://metropolitanogranada.es/horariosreal).

## Ejecución

`make`, para la ejecución interactiva. Cortesía de [Yeray](https://github.com/yerasiito).

`python3 tram.py "Caleta"`, para la consulta de una parada, en el ejemplo la de de Caleta. Requiere instalar las dependencias del fichero `requirements.txt`. Recomiendo el uso propuesto en la sección [.zshrc](#.zshrc).

## .zshrc

`alias tram='(cd ~/MetroGrx && make .venv/bin/activate > /dev/null && source .venv/bin/activate && python3 tram.py "Caleta")'`
