import { useState, useEffect, useCallback } from "react";
import { VITE_API_BASE_URL } from "./config";
import type { LogEntry, LogLevel } from "./types";
import axios from "axios";

import LogFilters from "./components/LogFilters";
import LogList from "./components/LogList";
import LogForm from "./components/LogForm";
import { useDebounce } from "./hooks/useDebounce";
import type { JSX } from "react/jsx-dev-runtime";
import { DateRangeFilter } from "./components/DateRangeFilter";
import { PaginationControls } from "./components/PaginationControls";
import Dashboard from "./components/Dashboard";

function App(): JSX.Element {
  const [logs, setLogs] = useState<LogEntry[]>([]);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  const [search, setSearch] = useState<string>("");
  const debouncedSearch = useDebounce(search, 500);
  const [filterLevel, setFilterLevel] = useState<LogLevel | "">("");
  const [filterService, setFilterService] = useState<string>("");
  const [currentPage, setCurrentPage] = useState<number>(1);
  const [pageSize] = useState<number>(20);
  const [startDate, setStartDate] = useState<string>("");
  const [endDate, setEndDate] = useState<string>("");

  useEffect(() => {
    // TODO: var d'env ws !
    const socket = new WebSocket("ws://localhost:8000/ws/logs");

    socket.onopen = () => {
      console.log("✅ WebSocket connected");
    };

    socket.onmessage = (event) => {
      const newLog: LogEntry = JSON.parse(event.data);
      setLogs((prevLogs) => [newLog, ...prevLogs]);
    };

    socket.onerror = (error) => {
      console.error("WebSocket error:", error);
    };

    return () => {
      socket.close();
    };
  }, []);

  // Fetch GET logs
  const fetchLogs = useCallback(async () => {
    setLoading(true);
    setError(null);

    try {
      const params: Record<string, string | number> = {
        page: currentPage,
        size: pageSize,
      };
      if (debouncedSearch.trim()) params.q = debouncedSearch.trim();
      if (filterLevel) params.level = filterLevel;
      if (filterService) params.service = filterService;
      if (startDate) params.start_date = new Date(startDate).toISOString();
      if (endDate) params.end_date = new Date(endDate).toISOString();

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
  }, [
    debouncedSearch,
    filterLevel,
    filterService,
    currentPage,
    pageSize,
    startDate,
    endDate,
  ]);

  useEffect(() => {
    fetchLogs();
  }, [fetchLogs]);

  return (
    <div className="max-w-4xl mx-auto p-4 font-sans">
      {/* Main page title */}
      <h1 className="text-3xl font-bold mb-4">Logs Viewer</h1>

      {/* Filters for text search, log level, and service name */}
      <LogFilters
        search={search}
        setSearch={setSearch}
        filterLevel={filterLevel}
        setFilterLevel={setFilterLevel}
        filterService={filterService}
        setFilterService={setFilterService}
      />

      {/* Date range filter to filter logs between two dates */}
      <DateRangeFilter
        startDate={startDate}
        endDate={endDate}
        setStartDate={setStartDate}
        setEndDate={setEndDate}
      />

      {/* List of logs with loading and error handling */}
      <LogList logs={logs} loading={loading} error={error} />

      {/* Pagination controls to navigate through pages */}
      <PaginationControls
        currentPage={currentPage}
        setCurrentPage={setCurrentPage}
      />

      {/* Form to submit a new log entry */}
      <LogForm onSubmitSuccess={fetchLogs} />

      {/* Dashboard */}
      <Dashboard />
    </div>
  );
}

export default App;
