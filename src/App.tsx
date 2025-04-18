import { useState } from "react";
import { invoke } from "@tauri-apps/api/core";
import { open } from "@tauri-apps/plugin-dialog";
import { call, registerJs } from "tauri-plugin-python-api";

function App() {
  const [selectedPath, setSelectedPath] = useState<string>("");
  const [renamedFiles, setRenamedFiles] = useState<string[]>([]);

  const [pythonText, setPythonText] = useState<string>("");

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

  const handlePythonTest = async () => {
    registerJs("main");

    const text = await call.main();
    setPythonText(text);
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

        <div className="bg-amber-100">
          <button
            onClick={handlePythonTest}
            className="bg-teal-50 border-sky-100"
          >
            Press Me
          </button>
          <p className="text-sm">{pythonText}</p>
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
