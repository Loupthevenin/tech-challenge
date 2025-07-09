import type { JSX } from "react/jsx-dev-runtime";
import { useState } from "react";
import axios from "axios";
import { VITE_API_BASE_URL } from "../config";
import {
  LEVELS,
  type LogEntry,
  type NewLog,
  type LogFormProps,
} from "../types";

const INITIAL_LOG: NewLog = {
  level: "INFO",
  message: "",
  service: "",
};

export default function LogForm({
  onSubmitSuccess,
}: LogFormProps): JSX.Element {
  const [newLog, setNewLog] = useState<NewLog>(INITIAL_LOG);

  // POST logs
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newLog.message || !newLog.service)
      return alert("Please fill message and service");

    try {
      await axios.post(`${VITE_API_BASE_URL}/logs`, newLog);
      alert("Log submitted");
      setNewLog({
        ...INITIAL_LOG,
      });
      onSubmitSuccess();
    } catch (error) {
      console.error("Failed to submit log:", error);
      alert("Failed to submit log");
    }
  };

  return (
    <form
      onSubmit={handleSubmit}
      className="border p-4 rounded space-y-4 max-w-md"
    >
      <h2 className="text-xl font-semibold mb-3">Submit a new log</h2>

      <label className="block">
        Message
        <input
          type="text"
          value={newLog.message}
          onChange={(e) => setNewLog({ ...newLog, message: e.target.value })}
          className="w-full border rounded px-3 py-2 mt-1"
          required
        />
      </label>

      <label className="block">
        Service
        <input
          type="text"
          value={newLog.service}
          onChange={(e) => setNewLog({ ...newLog, service: e.target.value })}
          className="w-full border rounded px-3 py-2 mt-1"
          required
        />
      </label>

      <label className="block">
        Level
        <select
          value={newLog.level}
          onChange={(e) =>
            setNewLog({ ...newLog, level: e.target.value as LogEntry["level"] })
          }
          className="w-full border rounded px-3 py-2 mt-1"
        >
          {LEVELS.map((level) => (
            <option key={level} value={level}>
              {level}
            </option>
          ))}
        </select>
      </label>

      <button
        type="submit"
        className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
      >
        Submit
      </button>
    </form>
  );
}
