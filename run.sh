#!/bin/bash

if [[ "$(pwd)" =~ /panfit_api$ ]]; then
    export PYTHONPATH=$(pwd)
    echo "Variável PYTHONPATH definida como: $PYTHONPATH"
else
    echo "Este script deve ser executado dentro do diretório /panfit_api para definir PYTHONPATH."
fi

cd src && python app.py