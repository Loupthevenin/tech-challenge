import type { JSX } from "react";
import type { PaginationControlsProps } from "../types";

export function PaginationControls({
  currentPage,
  setCurrentPage,
}: PaginationControlsProps): JSX.Element {
  return (
    <div className="flex justify-center gap-4 my-6">
      <button
        onClick={() => setCurrentPage((prev) => Math.max(prev - 1, 1))}
        disabled={currentPage === 1}
        className="px-4 py-2 rounded-md bg-gray-200 text-gray-700 disabled:opacity-50 hover:bg-gray-300 transition"
      >
        ← Précédent
      </button>

      <span className="font-medium text-gray-700">Page {currentPage}</span>

      <button
        onClick={() => setCurrentPage((prev) => prev + 1)}
        className="px-4 py-2 rounded-md bg-gray-200 text-gray-700 hover:bg-gray-300 transition"
      >
        Suivant →
      </button>
    </div>
  );
}
