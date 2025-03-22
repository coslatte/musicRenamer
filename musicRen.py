import os
import re
import platform
import argparse
from mutagen import File


def get_os():
    """Determina el sistema operativo actual."""
    return platform.system()


def sanitize_filename(filename, os_type):
    """Sanitiza el nombre del archivo según el sistema operativo."""
    if os_type == "Windows":
        invalid_chars = r'[<>:"/\\|?*\x00-\x1f]'
        sanitized = re.sub(invalid_chars, "", filename)
        forbidden_names = {
            "CON",
            "PRN",
            "AUX",
            "NUL",
            "COM1",
            "COM2",
            "COM3",
            "COM4",
            "COM5",
            "COM6",
            "COM7",
            "COM8",
            "COM9",
            "LPT1",
            "LPT2",
            "LPT3",
            "LPT4",
            "LPT5",
            "LPT6",
            "LPT7",
            "LPT8",
            "LPT9",
        }
        if sanitized.upper() in forbidden_names:
            sanitized = "_" + sanitized
    else:
        sanitized = re.sub(r"/", "-", filename)
        sanitized = sanitized.strip(".")

    sanitized = sanitized.strip()
    max_length = 255
    base, ext = os.path.splitext(sanitized)
    if len(sanitized) > max_length:
        base = base[: max_length - len(ext) - 1]
        sanitized = base + ext

    if not base:
        sanitized = f"audio_file{ext}"

    return sanitized


def get_audio_files(directory):
    """Obtiene todos los archivos de audio en el directorio especificado."""
    audio_extensions = (".mp3", ".wav", ".flac", ".m4a")
    return [f for f in os.listdir(directory) if f.lower().endswith(audio_extensions)]


def safe_rename(old_name, new_name, os_type, directory):
    """Renombra un archivo de forma segura, evitando conflictos de nombres."""
    old_path = os.path.join(directory, old_name)
    new_path = os.path.join(directory, new_name)

    if old_path == new_path:
        return old_name, False

    new_name = sanitize_filename(new_name, os_type)
    new_path = os.path.join(directory, new_name)
    base, extension = os.path.splitext(new_name)
    counter = 1
    while os.path.exists(new_path):
        new_name = f"{base} ({counter}){extension}"
        new_path = os.path.join(directory, new_name)
        counter += 1

    try:
        os.rename(old_path, new_path)
        return new_name, True
    except OSError as e:
        print(f"No se pudo renombrar '{old_name}' a '{new_name}'. Error: {e}")
        return old_name, False


def rename_files(files, os_type, directory):
    """Renombra los archivos de audio y devuelve un diccionario con los cambios."""
    changes = {}

    for file in files:
        try:
            file_path = os.path.join(directory, file)
            audio = File(file_path, easy=True)
            artist = (
                audio.get("artist", ["Unknown Artist"])[0]
                if audio
                else "Unknown Artist"
            )
            title = (
                audio.get("title", ["Unknown Title"])[0] if audio else "Unknown Title"
            )
            new_name = f"{artist} - {title}{os.path.splitext(file)[1]}"

            actual_new_name, changed = safe_rename(file, new_name, os_type, directory)
            if changed:
                changes[actual_new_name] = file
                print(f"Renombrado: {file} -> {actual_new_name}")
        except Exception as e:
            print(f"Error al procesar {file}: {str(e)}")

    return changes


def revert_changes(changes, os_type, directory):
    """Revierte los cambios de nombre realizados."""
    for new_name, original_name in changes.items():
        try:
            safe_rename(new_name, original_name, os_type, directory)
            print(f"Revertido: {new_name} -> {original_name}")
        except OSError as e:
            print(f"Error al revertir {new_name}: {str(e)}")


def main():
    parser = argparse.ArgumentParser(
        description="Renombra archivos de audio basándose en sus metadatos."
    )
    parser.add_argument(
        "-d",
        "--directory",
        help="Directorio donde se encuentran los archivos de audio",
        default=".",
    )
    args = parser.parse_args()

    directory = os.path.abspath(args.directory)
    os_type = get_os()

    print(f"Sistema operativo detectado: {os_type}")
    print(f"Directorio de trabajo: {directory}")

    if not os.path.isdir(directory):
        print(f"El directorio especificado no existe: {directory}")
        input("Presiona Enter para salir...")
        return

    files = get_audio_files(directory)

    if not files:
        print("No se encontraron archivos de audio en este directorio.")
        input("Presiona Enter para salir...")
        return

    print(f"Se encontraron {len(files)} archivos de audio.")
    start = input("Comenzar renombramiento (Y/N): ").lower()
    if start != "y":
        print("Operación cancelada.")
        input("Presiona Enter para salir...")
        return

    changes = rename_files(files, os_type, directory)

    if changes:
        keep_changes = input("¿Desea mantener los cambios? (Y/N): ").lower()
        if keep_changes != "y":
            revert_changes(changes, os_type, directory)
            print("Todos los cambios han sido revertidos.")
        else:
            print("Los cambios se han mantenido.")
    else:
        print("No se realizaron cambios.")

    print("El proceso ha concluido correctamente.")
    input("Presiona Enter para salir...")


if __name__ == "__main__":
    main()
