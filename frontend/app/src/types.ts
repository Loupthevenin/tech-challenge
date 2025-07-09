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
