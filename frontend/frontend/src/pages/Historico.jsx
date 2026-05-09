import { useEffect, useState } from "react";
import { apiFetch } from "../api/client.js";

export default function Historico() {

    const [page, setPage] = useState(1);
    const [dados, setDados] = useState(null);
    const [tipo, setTipo] = useState("")

    const totalPaginas = dados ? Math.ceil(dados.total / 10) : 1;

    useEffect(() => {
        apiFetch(`/api/listas/historico/?page=${page}&limit=10&tipo=${tipo}&ordenar=acuracia`)
            .then(res => res.json())
            .then(setDados);
    }, [page, tipo]);

    
    return (
        <div>
            <h1>Historico</h1>
            <div>
                <select onChange={(e) => {
                    setTipo(e.target.value)
                    setPage(1)
                    }}>
                    <option value="">Todos</option>
                    <option value="ml">Machine Learning</option>
                    <option value="heuristica">Heurística</option>
                </select>
            </div>

            <table border="1" cellPadding="10">
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Tipo</th>
                        <th>Previstos</th>
                        <th>Reais</th>
                        <th>Acurácia</th>
                    </tr>
                </thead>

                <tbody>
                    {dados?.results?.map(item => (
                        <tr key={item.id}>
                            <td>{item.id}</td>
                            <td>{item.tipo}</td>
                            <td>{item.numeros_previstos.join(", ") || "-"}</td>
                            <td>{item.numeros_reais?.join(", ") || "-"}</td>
                            <td>
                                {item.acuracia
                                    ? (item.acuracia * 100).toFixed(1) + "%"
                                    : "-"}
                            </td>
                        </tr>
                    ))}
                </tbody>
            </table>
            <button onClick={() => setPage(page - 1)} disabled={page === 1}>
                Anterior
            </button>

            <button onClick={() => setPage(page + 1)}
                disabled={page >= totalPaginas}>
                Próxima
            </button>

            <p>Pagina: {page}</p>
        </div>
    );
}