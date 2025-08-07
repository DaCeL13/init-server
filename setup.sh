#!/bin/bash

# Solicita nombre de carpeta
read -p "📁 Ingresa el nombre de la carpeta donde montar el servidor (Enter: backend): " directory

# Determina ruta de destino
path="."
if [ -z "$directory" ]; then
  directory="backend"
fi
path="$path/$directory"
echo "🗺️ Ruta de destino: $path"
# Verifica si la carpeta ya existe
if [ -d "$path" ]; then
  echo "📂 La carpeta '$directory' ya existe. Usándola..."
else
  echo "📦 Creando carpeta '$directory'..."
  mkdir -p "$path"
fi

# Moverse al destino
cd "$path" || { echo "❌ Error al acceder a la carpeta '$path'"; exit 1; }

# Crear entorno virtual
echo "🔧 Creando entorno virtual..."
python3 -m venv .venv

# Instalar FastAPI y Uvicorn
echo "📦 Instalando FastAPI y Uvicorn..."
pip install --upgrade pip
pip install "fastapi[standard]" uvicorn

# Pedir nombre del usuario
read -p "👤 Ingresa tu nombre: " name

# Pedir nombre del archivo
read -p "📄 Ingresa el nombre del archivo de servidor (sin .py): " file
file_name="${file}.py"

# Crear archivo si no existe
if [ ! -f "$file_name" ]; then
  echo "📝 Creando '$file_name' con saludo para $name..."
  cat <<EOF > "$file_name"
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hola $name, tu API '$file_name' está viva"}
EOF
else
  echo "✅ El archivo '$file_name' ya existe. No se modifica."
fi

# Mensaje final
echo "🚀 Todo listo en '$path'. Ejecuta tu app con:"
# Activar entorno virtual
echo "🖥️ Cambia al directorio '$path' y activa el entorno virtual:"
echo "cd $path"
echo "🖥️ Ejecuta para activar el entorno virtual..."
echo "source .venv/bin/activate"
echo "🖥️ Luego inicia tu app con:"
echo "uvicorn $file:app --reload"