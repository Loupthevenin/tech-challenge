import type { JSX } from "react/jsx-dev-runtime";
import { LEVELS, SERVICES, type LogLevel } from "../types";
import type { LogFiltersProps } from "../types";

export default function LogFilters({
  search,
  setSearch,
  filterLevel,
  setFilterLevel,
  filterService,
  setFilterService,
}: LogFiltersProps): JSX.Element {
  return (
    <div className="flex gap-4 mb-6">
      <input
        type="text"
        placeholder="Search messages..."
        value={search}
        onChange={(e) => setSearch(e.target.value)}
        className="flex-grow border rounded px-3 py-2"
      />

      <select
        value={filterLevel}
        onChange={(e) => setFilterLevel(e.target.value as LogLevel | "")}
        className="border rounded px-3 py-2"
      >
        <option value="">All levels</option>
        {LEVELS.map((level) => (
          <option key={level} value={level}>
            {level}
          </option>
        ))}
      </select>

      <select
        value={filterService}
        onChange={(e) => setFilterService(e.target.value)}
        className="border rounded px-3 py-2"
      >
        <option value="">All services</option>
        {SERVICES.map((s) => (
          <option key={s} value={s}>
            {s}
          </option>
        ))}
      </select>
    </div>
  );
}
