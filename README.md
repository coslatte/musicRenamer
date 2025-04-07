# Music Renamer

Una herramienta para renombrar archivos de música basándose en sus metadatos e incrustar letras sincronizadas.

## Características Principales

- Renombra archivos de música basándose en los metadatos existentes (artista, título)
- Reconocimiento de canciones usando Chromaprint/AcoustID
- Completa automáticamente los metadatos para canciones reconocidas (fecha, género, número de pista, etc.)
- Descarga e incrusta portadas de álbum
- Busca e incrusta letras sincronizadas (formato LRC)
- Soporta formatos MP3, FLAC y M4A

## Instalación

### Prerrequisitos

- Python 3.6 o superior
- Las siguientes bibliotecas:
  - mutagen
  - requests
  - syncedlyrics
  - pyacoustid
  - musicbrainzngs (opcional, para obtener mejor información de álbumes)

Puede instalar las dependencias manualmente:

```bash
pip install mutagen requests syncedlyrics pyacoustid musicbrainzngs
```

O puede instalar el paquete completo que se encargará de las dependencias:

```bash
pip install -e .
```

### Chromaprint (fpcalc)

Para utilizar la funcionalidad de reconocimiento de canciones, necesitará Chromaprint (comando `fpcalc`).

- **Windows**: Descargue fpcalc.exe desde [Chromaprint releases](https://github.com/acoustid/chromaprint/releases) y colóquelo en el mismo directorio que este programa.
- **macOS**: `brew install chromaprint`
- **Linux**: `apt-get install libchromaprint-tools` o equivalente en su distribución

## Nueva Estructura del Proyecto

El proyecto ahora está organizado de manera encapsulada usando programación orientada a objetos:

```none
core/                   # Núcleo de funcionalidad
├── __init__.py
├── audio_processor.py  # Procesador principal de audio
└── artwork.py          # Manejo de portadas de álbum
utils/                  # Utilidades
├── __init__.py
└── dependencies.py     # Verificación de dependencias

cli.py                      # Interfaz de línea de comandos
app.py                      # Punto de entrada principal
install_covers.py           # Script para instalar portadas
setup.py                    # Configuración de instalación
```

## Uso

### Modo Básico

Para renombrar archivos de música en el directorio actual:

```bash
python app.py
```

### Con Letras Sincronizadas

Para buscar e incrustar letras sincronizadas:

```bash
python app.py -l
```

### Con Reconocimiento de Canciones

Para identificar canciones y obtener información completa:

```bash
python app.py -l --recognition
```

### Solo Añadir Portadas

Para añadir portadas a archivos existentes:

```bash
python install_covers.py
```

O usando el programa principal:

```bash
python app.py --only-covers
```

### Opciones Avanzadas

```bash
python app.py --help
```

## Resolución de Problemas

### Error de fpcalc no encontrado

Si recibe un error indicando que `fpcalc` no fue encontrado:

1. Descargue el ejecutable adecuado para su sistema desde [Chromaprint releases](https://github.com/acoustid/chromaprint/releases)
2. Coloque el archivo `fpcalc` o `fpcalc.exe` en el mismo directorio que este programa
3. Asegúrese de que tiene permisos de ejecución (en sistemas Unix: `chmod +x fpcalc`)
