import type { JSX } from "react";
import type { DateRangeFilterProps } from "../types";

export function DateRangeFilter({
  startDate,
  endDate,
  setStartDate,
  setEndDate,
}: DateRangeFilterProps): JSX.Element {
  return (
    <div className="flex gap-4 my-4">
      <div>
        <label className="block text-sm font-medium">Début</label>
        <input
          type="datetime-local"
          value={startDate}
          onChange={(e) => setStartDate(e.target.value)}
          className="border rounded px-2 py-1"
        />
      </div>

      <div>
        <label className="block text-sm font-medium">Fin</label>
        <input
          type="datetime-local"
          value={endDate}
          onChange={(e) => setEndDate(e.target.value)}
          className="border rounded px-2 py-1"
        />
      </div>
    </div>
  );
}
