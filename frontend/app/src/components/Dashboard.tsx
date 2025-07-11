import { useCallback, useEffect, useState } from "react";
import { VITE_API_BASE_URL } from "../config";
import axios from "axios";
import { Pie } from "react-chartjs-2";
import {
  Chart as ChartJS,
  ArcElement,
  Tooltip,
  Legend,
  type ChartData,
} from "chart.js";

ChartJS.register(ArcElement, Tooltip, Legend);

export default function Dashboard() {
  const [data, setData] = useState<ChartData<"pie">>();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchStats = useCallback(async () => {
    setLoading(true);
    setError(null);

    try {
      const response = await axios.get<Record<string, number>>(
        `${VITE_API_BASE_URL}/logs/stats`,
      );
      const result = response.data;

      const labels = Object.keys(result);
      const values = Object.values(result);
      const colors = ["#4ade80", "#facc15", "#f87171", "#60a5fa"];
      setData({
        labels,
        datasets: [
          {
            label: "Nombre de logs",
            data: values,
            backgroundColor: colors.slice(0, labels.length),
          },
        ],
      });
    } catch (error) {
      setError("Failed to fetch stats");
      console.error("Failed to fetch stats", error);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchStats();
  }, [fetchStats]);

  if (loading) return <p>Loading...</p>;
  if (error) return <p className="text-red-500">{error}</p>;
  if (!data) return null;

  return (
    <div className="w-full p-4 max-w-md mx-auto">
      <h2 className="text-xl font-bold text-center mb-4">
        Répartition des logs
      </h2>
      <div className="flex justify-center">
        <Pie data={data} />
      </div>
    </div>
  );
}
