import { useState } from "react";
import { invoke } from "@tauri-apps/api/core";
import { open } from "@tauri-apps/plugin-dialog";

function App() {
  const [greetMsg, setGreetMsg] = useState("");
  const [msgActivated, setMsgActivated] = useState<boolean>(false);
  const [name, setName] = useState("");
  const [selectedPath, setSelectedPath] = useState<string>("");

  async function greet() {
    setGreetMsg(await invoke("greet", { name }));
  }

  async function toggleMessage() {
    try {
      const newValue = (await invoke("switch_stuff", {
        value: msgActivated,
      })) as boolean;
      setMsgActivated(newValue);
    } catch (error) {
      console.error("Error toggling message:", error);
    }
  }

  async function handleSelectDirectory() {
    try {
      const selected = await open({
        directory: true,
        multiple: false,
        title: "Seleccionar Directorio",
        canCreateDirectories: true,
      });

      if (selected === null) {
        return;
      }

      setSelectedPath(selected);
    } catch (error) {
      console.error("Error selecting directory:", error);
    }
  }

  return (
    <>
      <div>
        <h1>Welcome to Tauri + React</h1>

        <form
          className="row"
          onSubmit={(e) => {
            e.preventDefault();
            greet();
          }}
        >
          <input
            id="greet-input"
            onChange={(e) => setName(e.currentTarget.value)}
            placeholder="Enter a name..."
          />
          <button type="submit">Greet</button>
        </form>
        <p>{greetMsg}</p>

        <p className={msgActivated ? "text-rose-800" : "text-blue-800"}>
          {msgActivated ? "¡Activado!" : "¡Desactivado!"}
        </p>

        <button
          className={`toggle-button ${msgActivated ? "active" : ""}`}
          onClick={toggleMessage}
        >
          Cambiar Estado
        </button>

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
      </div>
    </>
  );
}

export default App;
