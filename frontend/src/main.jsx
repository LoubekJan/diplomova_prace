import React, { useCallback, useEffect, useState } from "react";
import { createRoot } from "react-dom/client";
import "./styles.css";

function App() {
  const [tasks, setTasks] = useState([]);
  const [title, setTitle] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const loadTasks = useCallback(async () => {
    try {
      const response = await fetch("/api/tasks");
      if (!response.ok) throw new Error("Nepodařilo se načíst úkoly.");
      setTasks(await response.json());
      setError("");
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    loadTasks();
  }, [loadTasks]);

  async function addTask(event) {
    event.preventDefault();
    const value = title.trim();
    if (!value) return;

    const response = await fetch("/api/tasks", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ title: value }),
    });
    if (!response.ok) {
      setError("Úkol se nepodařilo vytvořit.");
      return;
    }
    setTitle("");
    await loadTasks();
  }

  async function toggleTask(task) {
    await fetch(`/api/tasks/${task.id}`, {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ completed: !task.completed }),
    });
    await loadTasks();
  }

  async function deleteTask(taskId) {
    await fetch(`/api/tasks/${taskId}`, { method: "DELETE" });
    await loadTasks();
  }

  const completed = tasks.filter((task) => task.completed).length;

  return (
    <main className="shell">
      <section className="card">
        <p className="eyebrow">Docker · Kubernetes · OKD</p>
        <h1>Diploma Task App</h1>
        <p className="intro">
          Jednoduchá třívrstvá aplikace pro ověření sestavení, nasazení, škálování,
          aktualizace a perzistence dat.
        </p>

        <form onSubmit={addTask} className="task-form">
          <label htmlFor="task-title">Nový úkol</label>
          <div className="form-row">
            <input
              id="task-title"
              value={title}
              onChange={(event) => setTitle(event.target.value)}
              maxLength={200}
              placeholder="Například otestovat rolling update"
            />
            <button type="submit">Přidat</button>
          </div>
        </form>

        <div className="summary">
          <span>Celkem: {tasks.length}</span>
          <span>Dokončeno: {completed}</span>
        </div>

        {error && <p className="error">{error}</p>}
        {loading ? (
          <p>Načítání…</p>
        ) : tasks.length === 0 ? (
          <p className="empty">Zatím zde nejsou žádné úkoly.</p>
        ) : (
          <ul className="task-list">
            {tasks.map((task) => (
              <li key={task.id} className={task.completed ? "done" : ""}>
                <button
                  type="button"
                  className="check"
                  aria-label="Změnit stav úkolu"
                  onClick={() => toggleTask(task)}
                >
                  {task.completed ? "✓" : ""}
                </button>
                <span>{task.title}</span>
                <button
                  type="button"
                  className="delete"
                  onClick={() => deleteTask(task.id)}
                >
                  Smazat
                </button>
              </li>
            ))}
          </ul>
        )}
      </section>
    </main>
  );
}

createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
);
