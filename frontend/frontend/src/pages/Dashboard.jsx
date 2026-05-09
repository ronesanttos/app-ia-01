import { useEffect, useState } from "react";
import GraficoAcuracia from "../components/GraficoAcuracia";
import GraficoTopNumeros from "../components/GraficoTopNumeros";
import Heatmap from "../components/Heatmap";
import { apiFetch } from "../api/client.js";

export default function Dashboard() {
  const [dados, setDados] = useState(null);

  useEffect(() => {
    apiFetch(`/api/listas/dashboard/`)
      .then((res) => res.json())
      .then(setDados);
  }, []);

  if (!dados) {
    return <div className="loading-block">Carregando dashboard…</div>;
  }

  const media = dados.resumo?.acuracia_media;

  return (
    <div>
      <h1 className="page-title">Dashboard</h1>
      <p className="page-subtitle">
        Resumo das previsões, evolução da acurácia e distribuição dos números.
      </p>

      <div className="grid-cards">
        <div className="stat-card">
          <h3>Total de previsões</h3>
          <p className="value">{dados.resumo?.total_previsoes ?? "—"}</p>
        </div>
        <div className="stat-card">
          <h3>Acurácia média</h3>
          <p className="value">
            {media == null || Number.isNaN(Number(media))
              ? "—"
              : `${(Number(media) * 100).toFixed(1)}%`}
          </p>
        </div>
      </div>

      <section className="chart-card">
        <h2>Evolução da acurácia</h2>
        <GraficoAcuracia dados={dados.evolucao} />
      </section>

      <section className="chart-card">
        <h2>Top números (frequência)</h2>
        <GraficoTopNumeros dados={dados.top_numeros} />
      </section>

      <section className="chart-card">
        <h2>Mapa de calor (0–99)</h2>
        <Heatmap items={dados.heatmap} />
      </section>
    </div>
  );
}
