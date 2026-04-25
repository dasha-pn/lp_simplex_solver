import { useState } from "react";
import axios from "axios";
import "./App.css";
import { tasks } from "./tasks";

const signSymbols = {
  LESS_OR_EQUAL: "≤",
  GREATER_OR_EQUAL: "≥",
  EQUAL: "=",
};

function formatExpression(coefs) {
  return coefs.map((coef, index) => (
    <span key={index}>
      {index > 0 && coef >= 0 ? " + " : ""}
      {coef < 0 ? " - " : ""}
      {Math.abs(coef)}x<sub>{index + 1}</sub>
    </span>
  ));
}

export default function App() {
  const [selectedTask, setSelectedTask] = useState(tasks[0]);
  const [editableTask, setEditableTask] = useState(structuredClone(tasks[0]));
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const updateObjective = (index, value) => {
    const newTask = structuredClone(editableTask);
    newTask.objective[index] = Math.max(0, Number(value));
    setEditableTask(newTask);
    setResult(null);
  };

  const updateConstraintCoef = (rowIndex, colIndex, value) => {
    const newTask = structuredClone(editableTask);
    newTask.constraints[rowIndex].coefs[colIndex] = Number(value);
    setEditableTask(newTask);
    setResult(null);
  };

  const updateConstraintSign = (rowIndex, value) => {
    const newTask = structuredClone(editableTask);
    newTask.constraints[rowIndex].sign = value;
    setEditableTask(newTask);
    setResult(null);
  };

  const updateConstraintRhs = (rowIndex, value) => {
    const newTask = structuredClone(editableTask);
    newTask.constraints[rowIndex].rhs = Math.max(0, Number(value));
    setEditableTask(newTask);
    setResult(null);
  };

  const resetTask = () => {
    setEditableTask(structuredClone(selectedTask));
    setResult(null);
  };

  const solve = async () => {
    setLoading(true);

    try {
      const res = await axios.post("http://127.0.0.1:8000/solve", {
        vars_cnt: editableTask.varsCnt,
        objective: editableTask.objective,
        target: editableTask.target,
        constraints: editableTask.constraints,
      });

      setResult(res.data);
    } catch (error) {
      console.error(error);
      setResult({
        status: "ERROR",
        variables: [],
        objective_value: null,
      });
    }

    setLoading(false);
  };

  return (
    <div className="app">
      <div className="hero">
        <span className="badge">Simplex Method</span>
        <h1>LP Simplex Solver</h1>
        <p>
          Choose a linear programming task, review its mathematical formulation,
          and solve it using our Python simplex implementation.
        </p>
      </div>

      <div className="layout">
        <div className="card task-card">
          <label>Select task</label>

          <select
            value={selectedTask.id}
            onChange={(e) => {
              const task = tasks.find((t) => t.id === e.target.value);
              setSelectedTask(task);
              setEditableTask(structuredClone(task));
              setResult(null);
            }}
          >
            {tasks.map((task) => (
              <option key={task.id} value={task.id}>
                {task.title}
              </option>
            ))}
          </select>

          <div className="task-description">
            <h3>{selectedTask.title}</h3>
            <p>{selectedTask.description}</p>

            <div className="formula-box">
              <strong>{selectedTask.formulation.objective}</strong>
              <ul>
                {selectedTask.formulation.constraints.map(
                  (constraint, index) => (
                    <li key={index}>{constraint}</li>
                  ),
                )}
              </ul>
            </div>

            <div className="explanation-box">
              <h4>What do the variables mean?</h4>
              <ul>
                {selectedTask.explanation.variables.map((variable, index) => (
                  <li key={index}>{variable}</li>
                ))}
              </ul>

              <h4>Objective explanation</h4>
              <p>{selectedTask.explanation.objective}</p>

              <h4>Constraints explanation</h4>
              <ul>
                {selectedTask.explanation.constraints.map(
                  (constraint, index) => (
                    <li key={index}>{constraint}</li>
                  ),
                )}
              </ul>
            </div>
          </div>
        </div>

        <div className="side-panel">
          <div className="card editor-card">
            <div className="editor-section">
              <div className="editor-header">
                <h4>Edit objective coefficients</h4>
                <span>{editableTask.target}</span>
              </div>

              <div className="coef-row">
                {editableTask.objective.map((coef, index) => (
                  <div className="input-with-label" key={index}>
                    <span>x{index + 1}</span>
                    <input
                      type="number"
                      min="0"
                      value={coef}
                      onChange={(e) => updateObjective(index, e.target.value)}
                    />
                  </div>
                ))}
              </div>
            </div>

            <div className="editor-section">
              <div className="editor-header">
                <h4>Edit constraints</h4>
                <span>Excel-style table</span>
              </div>

              <div className="constraints-table">
                {editableTask.constraints.map((constraint, rowIndex) => (
                  <div className="constraint-row" key={rowIndex}>
                    {constraint.coefs.map((coef, colIndex) => (
                      <div className="input-with-label" key={colIndex}>
                        <span>x{colIndex + 1}</span>
                        <input
                          type="number"
                          value={coef}
                          onChange={(e) =>
                            updateConstraintCoef(
                              rowIndex,
                              colIndex,
                              e.target.value,
                            )
                          }
                        />
                      </div>
                    ))}

                    <select
                      className="sign-select"
                      value={constraint.sign}
                      onChange={(e) =>
                        updateConstraintSign(rowIndex, e.target.value)
                      }
                    >
                      <option value="LESS_OR_EQUAL">≤</option>
                      <option value="GREATER_OR_EQUAL">≥</option>
                      <option value="EQUAL">=</option>
                    </select>

                    <div className="input-with-label">
                      <span>rhs</span>
                      <input
                        type="number"
                        min="0"
                        value={constraint.rhs}
                        onChange={(e) =>
                          updateConstraintRhs(rowIndex, e.target.value)
                        }
                      />
                    </div>
                  </div>
                ))}
              </div>
            </div>

            <div className="current-model">
              <h4>Current model</h4>
              <p>
                <strong>
                  {editableTask.target === "MAXIMIZE" ? "Maximize" : "Minimize"}
                  :
                </strong>{" "}
                z = <>{formatExpression(editableTask.objective)}</>
              </p>

              <ul>
                {editableTask.constraints.map((constraint, index) => (
                  <li key={index}>
                    {formatExpression(constraint.coefs)}{" "}
                    {signSymbols[constraint.sign]} {constraint.rhs}
                  </li>
                ))}
                <li>
                  {editableTask.objective.map((_, i) => (
                    <span key={i}>
                      {i > 0 ? ", " : ""}x<sub>{i + 1}</sub>
                    </span>
                  ))}{" "}
                  ≥ 0
                </li>
              </ul>
            </div>

            <div className="button-row">
              <button className="secondary-button" onClick={resetTask}>
                Reset
              </button>

              <button onClick={solve} disabled={loading}>
                {loading ? "Solving..." : "Solve problem"}
              </button>
            </div>
          </div>

          {result && (
            <div className={`result ${result.status}`}>
              <span className="result-label">Result</span>
              <h2>Status: {result.status}</h2>

              {result.variables.length > 0 && (
                <>
                  <h3>Variables</h3>

                  <div className="variables-grid">
                    {result.variables.map((value, index) => (
                      <div className="variable-item" key={index}>
                        <span>x{index + 1}</span>
                        <strong>{value.toFixed(3)}</strong>
                      </div>
                    ))}
                  </div>

                  <div className="objective-box">
                    <span>Objective value</span>
                    <strong>{result.objective_value.toFixed(3)}</strong>
                  </div>
                </>
              )}

              {result.status === "ERROR" && (
                <p className="error-text">
                  Something went wrong. Check if the backend is running.
                </p>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
