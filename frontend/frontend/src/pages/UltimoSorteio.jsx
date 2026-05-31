import { useEffect, useState } from "react";
import { apiFetch, readApiError } from "../api/client.js";

export default function UltimoSorteio() {
  const [dados, setDados] = useState(null);
  const [erro, setErro] = useState(null);

  useEffect(() => {
    async function fetchDados() {
      try {
        const response = await apiFetch("/api/listas/ultimo_sorteio_por_numero/");
        if (!response.ok) {
          throw new Error(await readApiError(response));
        }
        const json = await response.json();
        setDados(json);
      } catch (err) {
        setErro(err.message || "Erro ao carregar dados.");
      }
    }

    fetchDados();
  }, []);

  if (erro) {
    return (
      <div className="page-container">
        <h1 className="page-title">Último sorteio por número</h1>
        <p className="page-subtitle">
          Mostra quando cada número de 0 a 99 apareceu pela última vez.
        </p>
        <div className="alert alert-error">{erro}</div>
      </div>
    );
  }

  if (!dados) {
    return <div className="loading-block">Carregando último sorteio por número…</div>;
  }

  return (
    <div className="page-container">
      <h1 className="page-title">Último sorteio por número</h1>
      <p className="page-subtitle">
        Mostra quando cada número de 0 a 99 apareceu pela última vez.
      </p>

      <div className="table-card">
        <table className="data-table" cellPadding="8">
          <thead>
            <tr>
              <th>Número</th>
              <th>Última vez sorteado</th>
            </tr>
          </thead>
          <tbody>
            {dados.map((item) => (
              <tr key={item.numero}>
                <td>{item.numero}</td>
                <td>
                  {item.ultima_sorteado_em
                    ? new Date(item.ultima_sorteado_em).toLocaleString()
                    : "Nunca"
                  }
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
