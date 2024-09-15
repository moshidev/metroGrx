# Tiempo Parada

Tiempo restante para el próximo tranvía del metropolitano
dado el nombre de una parada.

## Ejecución

`make`

## .zshrc

alias tram='(cd tiempo-parada && make .venv/bin/activate > /dev/null && echo "Caleta." && source .venv/bin/activate && python3 s.py "Caleta")'
