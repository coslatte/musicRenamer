#!/usr/bin/env python
"""
Script para añadir portadas a archivos de música existentes.
Usa las clases de la biblioteca encapsulada music_renamer.
"""

import os
import argparse
import concurrent.futures
from mutagen import File
from core.artwork import AlbumArtManager


def get_audio_files(directory):
    """Obtiene todos los archivos de audio en el directorio especificado."""
    audio_extensions = (".mp3", ".wav", ".flac", ".m4a")
    return [f for f in os.listdir(directory) if f.lower().endswith(audio_extensions)]


def process_file(file_path, art_manager):
    """Procesa un archivo individual añadiendo portada."""
    try:
        # Obtener metadatos actuales
        audio = File(file_path, easy=True)
        if not audio:
            return {"status": False, "error": "No se pudieron leer los metadatos"}

        artist = (
            audio.get("artist", ["Unknown Artist"])[0]
            if "artist" in audio
            else "Unknown Artist"
        )
        album = (
            audio.get("album", ["Unknown Album"])[0]
            if "album" in audio
            else "Unknown Album"
        )

        # Verificar si el archivo ya tiene portada
        has_cover = False
        if file_path.lower().endswith(".mp3"):
            from mutagen.id3 import ID3

            try:
                tags = ID3(file_path)
                has_cover = any(frame.startswith("APIC") for frame in tags.keys())
            except:
                has_cover = False
        elif file_path.lower().endswith(".flac"):
            from mutagen.flac import FLAC

            try:
                audio = FLAC(file_path)
                has_cover = len(audio.pictures) > 0
            except:
                has_cover = False
        elif file_path.lower().endswith(".m4a"):
            from mutagen.mp4 import MP4

            try:
                audio = MP4(file_path)
                has_cover = "covr" in audio
            except:
                has_cover = False

        # Si ya tiene portada, informar y saltar
        if has_cover:
            print(
                f"[INFO] El archivo ya tiene portada, saltando: {os.path.basename(file_path)}"
            )
            return {"status": True, "message": "El archivo ya tiene portada"}

        # Buscar portada
        print(f"Buscando portada para: {artist} - {album}")
        cover_url = art_manager.fetch_album_cover(artist, album)

        if not cover_url:
            return {"status": False, "error": "No se encontró portada"}

        # Descargar e incrustar portada
        image_data = art_manager.fetch_cover_image(cover_url)
        if not image_data:
            return {"status": False, "error": "No se pudo descargar la portada"}

        if art_manager.embed_album_art(file_path, image_data):
            print(f"[OK] Portada incrustada: {os.path.basename(file_path)}")
            return {"status": True, "message": "Portada incrustada correctamente"}
        else:
            return {"status": False, "error": "Error al incrustar la portada"}

    except Exception as e:
        print(f"[ERROR] Error procesando {os.path.basename(file_path)}: {str(e)}")
        return {"status": False, "error": str(e)}


def main():
    parser = argparse.ArgumentParser(
        description="Añade portadas a archivos de música existentes."
    )
    parser.add_argument(
        "-d",
        "--directory",
        help="Directorio donde se encuentran los archivos de audio",
        default=".",
    )
    parser.add_argument(
        "--max-workers",
        help="Número máximo de trabajadores concurrentes",
        type=int,
        default=4,
    )
    args = parser.parse_args()

    directory = os.path.abspath(args.directory)
    print(f"Directorio de trabajo: {directory}")

    # Obtener archivos de audio
    files = get_audio_files(directory)
    if not files:
        print("No se encontraron archivos de audio en este directorio.")
        return

    print(f"Se encontraron {len(files)} archivos de audio.")

    # Crear gestor de portadas
    art_manager = AlbumArtManager()

    # Procesar archivos en paralelo
    results = {"success": 0, "skipped": 0, "failed": 0}

    with concurrent.futures.ThreadPoolExecutor(
        max_workers=args.max_workers
    ) as executor:
        future_to_file = {
            executor.submit(
                process_file, os.path.join(directory, file), art_manager
            ): file
            for file in files
        }

        for future in concurrent.futures.as_completed(future_to_file):
            file = future_to_file[future]
            try:
                result = future.result()
                if result["status"]:
                    if "message" in result and "ya tiene portada" in result["message"]:
                        results["skipped"] += 1
                    else:
                        results["success"] += 1
                else:
                    results["failed"] += 1
                    print(f"[ERROR] {file}: {result.get('error', 'Error desconocido')}")
            except Exception as e:
                results["failed"] += 1
                print(f"[ERROR] Error procesando {file}: {str(e)}")

    # Mostrar resumen
    print("\nResumen:")
    print(f"Total de archivos procesados: {len(files)}")
    print(f"Portadas añadidas correctamente: {results['success']}")
    print(f"Archivos que ya tenían portada: {results['skipped']}")
    print(f"Archivos con errores: {results['failed']}")


if __name__ == "__main__":
    main()
