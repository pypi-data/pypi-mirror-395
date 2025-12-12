#!/bin/bash

# Limpa diretório dist anterior se existir
rm -rf dist/*

# Gera os arquivos de distribuição usando uv
uv build

# Faz upload para o PyPI usando uv
uv publish

echo "Pacote publicado com sucesso!"
