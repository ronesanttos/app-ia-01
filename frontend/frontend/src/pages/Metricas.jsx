import { useEffect, useState, useMemo } from "react";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  ResponsiveContainer,
} from "recharts";
import { apiFetch } from "../api/client.js";

function cssVar(name, fallback) {
  if (typeof window === "undefined") return fallback;
  const v = getComputedStyle(document.documentElement).getPropertyValue(name).trim();
  return v || fallback;
}

export default function Metricas() {
  const [dados, setDados] = useState(null);
  const [historico, setHistorico] = useState([]);

  useEffect(() => {
    apiFetch(`/api/listas/metricas/`)
      .then((res) => res.json())
      .then(setDados);

    apiFetch(`/api/listas/historico/`)
      .then((res) => res.json())
      .then((data) => setHistorico(data.results || []));
  }, []);

  const top5 = useMemo(() => {
    const raw = dados?.top_5;
    if (!Array.isArray(raw) || raw.length === 0) return [];
    return raw.map((item) => {
      const v = item.acuracia ?? item.taxa_acerto;
      const num = v == null || Number.isNaN(Number(v)) ? null : Number(v);
      return {
        id: `#${item.id}`,
        idRaw: item.id,
        acuracia: num,
        acuraciaBar: num == null ? 0 : num,
      };
    });
  }, [dados]);

  const accent = cssVar("--accent", "#aa3bff");
  const text = cssVar("--text", "#6b6375");
  const border = cssVar("--border", "#e5e4e7");
  const grid = `${border}80`;

  if (!dados) {
    return <div className="loading-block">Carregando métricas…</div>;
  }

  const acuraciaMedia = dados.acuracia == null ? null : Number(dados.acuracia);
  return (
    <div>
      <h1 className="page-title">Métricas</h1>
      <p className="page-subtitle">
        Visão rápida da performance e do histórico recente.
      </p>

      <div className="grid-cards">
        <div className="stat-card">
          <h3>Acurácia média</h3>
          <p className="value">
            {acuraciaMedia == null || Number.isNaN(acuraciaMedia)
              ? "—"
              : `${(acuraciaMedia * 100).toFixed(1)}%`}
          </p>
        </div>
        <div className="stat-card">
          <h3>Total de previsões</h3>
          <p className="value">{dados.total_previsoes ?? "—"}</p>
        </div>
        <div className="stat-card">
          <h3>Itens no histórico (amostra)</h3>
          <p className="value">{historico.length}</p>
        </div>
      </div>

      <section className="chart-card">
        <h2>Top 5 previsões (por acurácia)</h2>
        {top5.length === 0 ? (
          <p className="loading-block" style={{ margin: 0 }}>
            Sem previsões no banco. Gere previsões e valide algumas para ver acurácia
            no gráfico.
          </p>
        ) : (
          <div className="chart-wrap" style={{ height: 300 }}>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={top5} margin={{ top: 8, right: 12, left: 0, bottom: 8 }}>
                <CartesianGrid strokeDasharray="3 3" stroke={grid} vertical={false} />
                <XAxis dataKey="id" tick={{ fill: text, fontSize: 12 }} />
                <YAxis
                  domain={[0, 1]}
                  tick={{ fill: text, fontSize: 12 }}
                  tickFormatter={(v) => `${(v * 100).toFixed(0)}%`}
                />
                <Tooltip
                  contentStyle={{
                    background: "rgba(22, 23, 29, 0.95)",
                    border: `1px solid ${border}`,
                    borderRadius: 8,
                    color: "#f3f4f6",
                  }}
                  formatter={(_value, _name, entry) => {
                    const raw = entry?.payload?.acuracia;
                    return raw == null ? "— (sem validação)" : `${(Number(raw) * 100).toFixed(1)}%`;
                  }}
                  labelFormatter={(_, p) => {
                    const id = p?.[0]?.payload?.idRaw;
                    return id != null ? `Previsão #${id}` : "";
                  }}
                />
                <Bar
                  dataKey="acuraciaBar"
                  name="Acurácia"
                  fill={accent}
                  radius={[6, 6, 0, 0]}
                  maxBarSize={56}
                />
              </BarChart>
            </ResponsiveContainer>
          </div>
        )}
      </section>
    </div>
  );
}
