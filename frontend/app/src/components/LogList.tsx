import type { JSX } from "react/jsx-dev-runtime";
import type { LogListProps } from "../types";

export default function LogList({
  logs,
  loading,
  error,
}: LogListProps): JSX.Element {
  if (loading) return <p>Loading logs...</p>;
  if (error) return <p className="text-red-600">{error}</p>;
  if (logs.length === 0) return <p>No logs found</p>;

  return (
    <ul className="space-y-2 mb-10">
      {logs.map((log, i) => (
        <li
          key={i}
          className="border rounded p-3 flex flex-col sm:flex-row sm:justify-between bg-gray-50"
        >
          <span className="font-mono text-sm text-gray-600">
            {new Date(log.timestamp).toISOString().replace("T", " ")}
          </span>
          <span
            className={`font-bold px-2 rounded ${
              log.level === "ERROR"
                ? "bg-red-300"
                : log.level === "WARNING"
                  ? "bg-yellow-300"
                  : log.level === "INFO"
                    ? "bg-green-300"
                    : "bg-blue-300"
            }`}
          >
            {log.level}
          </span>
          <span className="italic text-gray-700">{log.service}</span>
          <p className="mt-1 sm:mt-0 sm:flex-grow text-black">{log.message}</p>
        </li>
      ))}
    </ul>
  );
}
