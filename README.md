# metroGrx

Tiempo restante para el próximo tranvía del metropolitano
dado el nombre de una parada.

## Ejecución

`make`

## .zshrc

alias tram='(cd # metroGrx && make .venv/bin/activate > /dev/null && source .venv/bin/activate && python3 tram.py "Caleta")'
