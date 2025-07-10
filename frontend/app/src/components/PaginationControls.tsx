import type { JSX } from "react";
import type { PaginationControlsProps } from "../types";

export function PaginationControls({
  currentPage,
  setCurrentPage,
}: PaginationControlsProps): JSX.Element {
  return (
    <div className="flex justify-center gap-4 my-4">
      <button
        onClick={() => setCurrentPage((prev) => Math.max(prev - 1, 1))}
        disabled={currentPage === 1}
        className="px-4 py-2 bg-gray-200 rounded disabled:opacity-50"
      >
        ← Précédent
      </button>

      <span>Page {currentPage}</span>

      <button
        onClick={() => setCurrentPage((prev) => prev + 1)}
        className="px-4 py-2 bg-gray-200 rounded"
      >
        Suivant →
      </button>
    </div>
  );
}
