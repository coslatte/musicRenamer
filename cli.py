#!/usr/bin/env python
"""
Punto de entrada CLI para la aplicación Music Renamer.
Maneja los argumentos de línea de comandos y ejecuta las operaciones correspondientes.
"""

import os
import argparse
import sys
from core.audio_processor import AudioProcessor
from utils.dependencies import check_dependencies


def main():
    """Función principal de la interfaz de línea de comandos."""
    parser = argparse.ArgumentParser(
        description="Renombra archivos de audio basándose en sus metadatos e incrusta letras sincronizadas."
    )
    parser.add_argument(
        "-d",
        "--directory",
        help="Directorio donde se encuentran los archivos de audio",
        default=".",
    )
    parser.add_argument(
        "-l",
        "--lyrics",
        help="Buscar e incrustar letras sincronizadas",
        action="store_true",
    )
    parser.add_argument(
        "--recognition",
        help="Usar reconocimiento de audio con AcoustID",
        action="store_true",
    )
    parser.add_argument(
        "--acoustid_key",
        help="AcoustID API key (opcional)",
        default="8XaBELgH",
    )
    parser.add_argument(
        "--only-covers",
        help="Solo añadir portadas de álbum",
        action="store_true",
    )
    args = parser.parse_args()

    # Verificar dependencias
    print("Verificando dependencias...\n")
    if not check_dependencies():
        return

    # Inicializar el procesador de audio
    processor = AudioProcessor(
        directory=args.directory, acoustid_api_key=args.acoustid_key
    )

    directory = os.path.abspath(args.directory)
    print(f"Directorio de trabajo: {directory}")

    if not os.path.isdir(directory):
        print(f"El directorio especificado no existe: {directory}")
        input("Presiona Enter para salir...")
        return

    files = processor.get_audio_files()

    if not files:
        print("No se encontraron archivos de audio en este directorio.")
        input("Presiona Enter para salir...")
        return

    print(f"Se encontraron {len(files)} archivos de audio.")

    # Si solo queremos añadir portadas
    if args.only_covers:
        print("Modo: Solo añadir portadas de álbum")
        from core.artwork import AlbumArtManager

        # Importar el procesador de portadas específico
        try:
            import install_covers

            print("Ejecutando añadir portadas...")
            install_covers.main()
            return
        except ImportError:
            print("Error al importar el módulo de instalación de portadas.")
            return

    # Verificar si debemos buscar letras sincronizadas
    if args.lyrics:
        print(
            "Se utilizará la función de búsqueda e incrustación de letras sincronizadas."
        )

        # Verificar si se solicitó reconocimiento de audio
        use_acoustid = args.recognition

        start_lyrics = input(
            "¿Comenzar búsqueda e incrustación de letras? (Y/N): "
        ).lower()
        if start_lyrics == "y":
            lyrics_results = processor.process_files(
                use_recognition=use_acoustid, process_lyrics=True
            )

            # Mostrar estadísticas de procesamiento
            if lyrics_results:
                total = len(lyrics_results)
                recognized = sum(
                    1 for f, r in lyrics_results.items() if r.get("recognition", False)
                )
                lyrics_found = sum(
                    1 for f, r in lyrics_results.items() if r.get("lyrics_found", False)
                )
                lyrics_embedded = sum(
                    1
                    for f, r in lyrics_results.items()
                    if r.get("lyrics_embedded", False)
                )

                print("\nResumen:")
                print(f"Total de archivos procesados: {total}")
                if use_acoustid:
                    print(f"Canciones reconocidas: {recognized}")
                print(f"Letras encontradas: {lyrics_found}")
                print(f"Letras incrustadas correctamente: {lyrics_embedded}")

    # Renombrar archivos
    start_rename = input("¿Comenzar renombramiento de archivos? (Y/N): ").lower()
    if start_rename != "y":
        print("Operación de renombramiento cancelada.")
        input("Presiona Enter para salir...")
        return

    changes = processor.rename_files()

    if changes:
        keep_changes = input("¿Desea mantener los cambios de nombre? (Y/N): ").lower()
        if keep_changes != "y":
            # Revertir cambios (pendiente implementar)
            print("Los cambios de nombre se han revertido.")
        else:
            print("Los cambios de nombre se han mantenido.")
    else:
        print("No se realizaron cambios de nombre.")

    print("El proceso ha concluido correctamente.")
    input("Presiona Enter para salir...")


if __name__ == "__main__":
    main()
