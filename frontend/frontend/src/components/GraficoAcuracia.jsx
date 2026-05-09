import { useMemo } from "react";
import {
  Chart as ChartJS,
  LineElement,
  CategoryScale,
  LinearScale,
  PointElement,
  Tooltip,
  Legend,
  Filler,
} from "chart.js";
import { Line } from "react-chartjs-2";

ChartJS.register(
  LineElement,
  CategoryScale,
  LinearScale,
  PointElement,
  Tooltip,
  Legend,
  Filler
);

function cssVar(name, fallback) {
  if (typeof window === "undefined") return fallback;
  const v = getComputedStyle(document.documentElement).getPropertyValue(name).trim();
  return v || fallback;
}

function formatarData(val) {
  if (!val) return "";
  const s = String(val);
  const d = new Date(s);
  if (!Number.isNaN(d.getTime())) {
    return d.toLocaleDateString("pt-BR", {
      day: "2-digit",
      month: "short",
    });
  }
  return s.slice(0, 10);
}

export default function GraficoAcuracia({ dados = [] }) {
  const chartData = useMemo(() => {
    const rows = Array.isArray(dados) ? dados : [];
    const accent = cssVar("--accent", "#aa3bff");
    const border = cssVar("--border", "#e5e4e7");

    return {
      labels: rows.map((d) => formatarData(d.data)),
      datasets: [
        {
          label: "Acurácia média (por dia)",
          data: rows.map((d) =>
            d.media == null ? null : Number(d.media)
          ),
          borderColor: accent,
          backgroundColor: `${accent}33`,
          borderWidth: 2,
          tension: 0.35,
          fill: true,
          pointRadius: 4,
          pointHoverRadius: 6,
          pointBackgroundColor: accent,
          pointBorderColor: border,
          spanGaps: true,
        },
      ],
    };
  }, [dados]);

  const options = useMemo(() => {
    const text = cssVar("--text", "#6b6375");
    const textH = cssVar("--text-h", "#08060d");
    const border = cssVar("--border", "#e5e4e7");

    return {
      responsive: true,
      maintainAspectRatio: false,
      interaction: { mode: "index", intersect: false },
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
          callbacks: {
            label(ctx) {
              const v = ctx.parsed.y;
              if (v == null) return " — ";
              return ` ${(v * 100).toFixed(1)}%`;
            },
          },
        },
      },
      scales: {
        x: {
          grid: { color: `${border}99` },
          ticks: { color: text, maxRotation: 45, minRotation: 0 },
        },
        y: {
          min: 0,
          max: 1,
          grid: { color: `${border}99` },
          ticks: {
            color: text,
            callback: (value) => `${(Number(value) * 100).toFixed(0)}%`,
          },
          title: {
            display: true,
            text: "Acurácia",
            color: textH,
            font: { size: 11, weight: "600" },
          },
        },
      },
    };
  }, []);

  if (!dados?.length) {
    return (
      <p className="loading-block" style={{ margin: 0 }}>
        Ainda não há pontos de evolução (acurácia por dia). Valide algumas
        previsões para preencher o gráfico.
      </p>
    );
  }

  return (
    <div className="chart-wrap">
      <Line data={chartData} options={options} />
    </div>
  );
}
