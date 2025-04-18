import { useState } from "react";
import { invoke } from "@tauri-apps/api/core";
import { open } from "@tauri-apps/plugin-dialog";

function App() {
  const [selectedPath, setSelectedPath] = useState<string>("");
  const [renamedFiles, setRenamedFiles] = useState<string[]>([]);

  const handleSelectDirectory = async () => {
    const selected = await open({
      title: "Seleccionar Directorio",
      directory: true,
      multiple: false,
      canCreateDirectories: true,
    });

    if (selected === null) {
      console.log("User cancelled the selection");
      return;
    }

    console.log(selected);
    setSelectedPath(selected);
  };

  const runRename = async () => {
    if (!selectedPath) {
      console.error("No directory selected");
      return;
    }

    try {
      const result = await invoke("rename_music", { path: selectedPath });
      console.log(result);
    } catch (error) {
      console.error("Error renaming music:", error);
    }
  };

  return (
    <>
      <div className="flex flex-col space-y-1 items-center justify-center h-screen bg-gray-100">
        <h1 className="italic">musicRenamer</h1>

        <div className="directory-selector">
          <button onClick={handleSelectDirectory}>
            Seleccionar Directorio
          </button>
          {selectedPath && (
            <p className="selected-path">
              Ruta seleccionada: {selectedPath || selectedPath}{" "}
            </p>
          )}
        </div>

        <div className="flex flex-col space-y-1 items-center justify-center h-screen bg-gray-100">
          <button
            onClick={runRename}
            className="bg-blue-500 text-white px-4 py-2 rounded"
          >
            Renombrar Música
          </button>
          <div className="bg-blue-300">
            <p className="text-sm text-shadow-indigo-50">
              {renamedFiles.length > 0
                ? `Archivos renombrados: ${renamedFiles.join(", ")}`
                : "No se han renombrado archivos."}
            </p>
          </div>
        </div>
      </div>
    </>
  );
}

export default App;
