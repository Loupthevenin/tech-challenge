import type { JSX } from "react/jsx-dev-runtime";
import type { LogLevel, LogListProps } from "../types";

export default function LogList({
  logs,
  loading,
  error,
}: LogListProps): JSX.Element {
  if (loading)
    return <p className="text-center text-gray-500 italic">Loading logs...</p>;
  if (error)
    return <p className="text-center text-red-600 font-semibold">{error}</p>;
  if (logs.length === 0)
    return <p className="text-center text-gray-400">No logs found</p>;

  const levelStyles: Record<LogLevel, string> = {
    ERROR: "bg-red-100 text-red-800",
    WARNING: "bg-yellow-100 text-yellow-800",
    INFO: "bg-green-100 text-green-800",
    DEBUG: "bg-blue-100 text-blue-800",
  };

  return (
    <ul className="space-y-2 mb-10">
      {logs.map((log, i) => (
        <li
          key={i}
          className="bg-white border rounded-lg shadow-sm p-4 flex flex-col sm:flex-row sm:items-center sm:justify-between space-y-2 sm:space-y-0 flex-wrap"
        >
          <div className="flex flex-col sm:flex-row sm:items-center sm:gap-4 flex-wrap">
            <span className="font-mono text-sm text-gray-500">
              {new Date(log.timestamp).toISOString().replace("T", " ")}
            </span>
            <span
              className={`text-xs font-semibold px-2 py-1 rounded ${levelStyles[log.level]}`}
            >
              {log.level}
            </span>
            <span className="italic text-sm text-gray-700">{log.service}</span>
          </div>
          <p className="text-gray-900">{log.message}</p>
        </li>
      ))}
    </ul>
  );
}
