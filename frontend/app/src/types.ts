export const LEVELS = ["INFO", "WARNING", "ERROR", "DEBUG"];
export type LogLevel = (typeof LEVELS)[number];

export const SERVICES = ["api-gateway", "user-service", "auth-service"];
export type LogService = (typeof SERVICES)[number];

export interface LogEntry {
  timestamp: string;
  level: LogLevel;
  message: string;
  service: string;
}

export type NewLog = LogEntry;

export interface LogListProps {
  logs: LogEntry[];
  loading: boolean;
  error: string | null;
}

export interface LogFormProps {
  onSubmitSuccess: () => void;
}

export interface LogFiltersProps {
  search: string;
  setSearch: (val: string) => void;
  filterLevel: LogLevel | "";
  setFilterLevel: (val: LogLevel | "") => void;
  filterService: string;
  setFilterService: (val: string) => void;
}
