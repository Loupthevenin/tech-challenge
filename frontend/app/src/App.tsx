import { useState, useEffect, useCallback } from "react";
import { VITE_API_BASE_URL } from "./config";
import type { LogEntry, LogLevel } from "./types";
import axios from "axios";

import LogFilters from "./components/LogFilters";
import LogList from "./components/LogList";
import LogForm from "./components/LogForm";
import { useDebounce } from "./hooks/useDebounce";
import type { JSX } from "react/jsx-dev-runtime";

function App(): JSX.Element {
  const [logs, setLogs] = useState<LogEntry[]>([]);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  const [search, setSearch] = useState("");
  const [filterLevel, setFilterLevel] = useState<LogLevel | "">("");
  const [filterService, setFilterService] = useState<string>("");

  const debouncedSearch = useDebounce(search, 500);

  // Fetch GET logs
  const fetchLogs = useCallback(async () => {
    setLoading(true);
    setError(null);

    try {
      const params: Record<string, string> = {};
      if (debouncedSearch.trim()) params.q = debouncedSearch.trim();
      if (filterLevel) params.level = filterLevel;
      if (filterService) params.service = filterService;

      const response = await axios.get<LogEntry[]>(
        `${VITE_API_BASE_URL}/logs/search`,
        {
          params,
        },
      );
      console.log(response);
      setLogs(response.data);
    } catch (error) {
      setError("Failed to fetch logs: ");
      console.error("Failed to fetch logs: ", error);
    } finally {
      setLoading(false);
    }
  }, [debouncedSearch, filterLevel, filterService]);

  useEffect(() => {
    fetchLogs();
  }, [fetchLogs]);

  return (
    <div className="max-w-4xl mx-auto p-4 font-sans">
      <h1 className="text-3xl font-bold mb-4">Logs Viewer</h1>

      <LogFilters
        search={search}
        setSearch={setSearch}
        filterLevel={filterLevel}
        setFilterLevel={setFilterLevel}
        filterService={filterService}
        setFilterService={setFilterService}
      />

      <LogList logs={logs} loading={loading} error={error} />

      <LogForm onSubmitSuccess={fetchLogs} />
    </div>
  );
}

export default App;
