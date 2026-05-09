import { useMemo } from "react";
import {
  Chart as ChartJS,
  BarElement,
  CategoryScale,
  LinearScale,
  Tooltip,
  Legend,
} from "chart.js";
import { Bar } from "react-chartjs-2";

ChartJS.register(BarElement, CategoryScale, LinearScale, Tooltip, Legend);

function cssVar(name, fallback) {
  if (typeof window === "undefined") return fallback;
  const v = getComputedStyle(document.documentElement).getPropertyValue(name).trim();
  return v || fallback;
}

/** Tons de cor por intensidade (compatível com todos os browsers) */
function coresBarras(frequencias, hue = 270) {
  const max = Math.max(...frequencias, 1);
  return frequencias.map((f) => {
    const ratio = Math.min(1, f / max);
    const L = 78 - ratio * 38;
    const s = 55 + ratio * 25;
    return `hsl(${hue} ${s}% ${L}%)`;
  });
}

export default function GraficoTopNumeros({ dados = [] }) {
  const rows = Array.isArray(dados) ? dados : [];
  const accent = cssVar("--accent", "#aa3bff");
  const hue = 270;

  const labels = rows.map((d) => String(d.numero));
  const values = rows.map((d) => Number(d.frequencia) || 0);
  const chartData = {
    labels,
    datasets: [
      {
        label: "Frequência",
        data: values,
        backgroundColor: coresBarras(values, hue),
        borderColor: values.map(() => accent),
        borderWidth: 1,
        borderRadius: 6,
        borderSkipped: false,
      },
    ],
  };

  const options = useMemo(() => {
    const text = cssVar("--text", "#6b6375");
    const textH = cssVar("--text-h", "#08060d");
    const border = cssVar("--border", "#e5e4e7");

    return {
      responsive: true,
      maintainAspectRatio: false,
      indexAxis: "y",
      plugins: {
        legend: {
          display: true,
          labels: { color: text, font: { size: 12 } },
        },
        tooltip: {
          backgroundColor: "rgba(22, 23, 29, 0.92)",
          titleColor: "#f3f4f6",
          bodyColor: "#e5e7eb",
          borderColor: border,
          borderWidth: 1,
          padding: 10,
        },
      },
      scales: {
        x: {
          beginAtZero: true,
          grid: { color: `${border}99` },
          ticks: { color: text, precision: 0 },
          title: {
            display: true,
            text: "Ocorrências",
            color: textH,
            font: { size: 11, weight: "600" },
          },
        },
        y: {
          grid: { display: false },
          ticks: { color: text, font: { weight: "500" } },
          title: {
            display: true,
            text: "Número",
            color: textH,
            font: { size: 11, weight: "600" },
          },
        },
      },
    };
  }, []);

  if (!rows.length) {
    return (
      <p className="loading-block" style={{ margin: 0 }}>
        Sem dados de frequência para exibir.
      </p>
    );
  }

  return (
    <div className="chart-wrap">
      <Bar data={chartData} options={options} />
    </div>
  );
}
