import { useEffect, useState } from "react";
import { apiFetch } from "../api/client.js";

export default function Historico() {

    const [page, setPage] = useState(1);
    const [dados, setDados] = useState(null);
    const [tipo, setTipo] = useState("")
    const [numerosVerificacao, setNumerosVerificacao] = useState("");
    const [resultadosVerificacao, setResultadosVerificacao] = useState([]);
    const [showResultados, setShowResultados] = useState(false);

    const totalPaginas = dados ? Math.ceil(dados.total / 10) : 1;

    useEffect(() => {
        apiFetch(`/api/listas/historico/?page=${page}&limit=10&tipo=${tipo}&ordenar=acuracia`)
            .then(res => res.json())
            .then(setDados);
    }, [page, tipo]);

    const verificarNumeros = () => {
        // Converter a string de entrada em array de números
        const numeros = numerosVerificacao
            .split(/[\s,]+/)
            .map(n => n.trim())
            .filter(n => n !== "")
            .map(n => parseInt(n))
            .filter(n => !isNaN(n));

        if (numeros.length === 0) {
            alert("Digite pelo menos um número");
            return;
        }

        // Buscar todas as ocorrências nos dados do histórico
        if (!dados?.results) {
            alert("Não há dados para verificar");
            return;
        }

        const ocorrencias = dados.results
            .map(item => {
                const numerosReais = item.numeros_reais || [];
                const encontrados = numeros.filter(num => numerosReais.includes(num));
                
                if (encontrados.length > 0) {
                    return {
                        id: item.id,
                        tipo: item.tipo,
                        numerosReais: numerosReais,
                        numerosEncontrados: encontrados,
                        quantidadeEncontrada: encontrados.length,
                        dataSorteio: item.data_sorteio || "N/A"
                    };
                }
                return null;
            })
            .filter(item => item !== null);

        setResultadosVerificacao(ocorrencias);
        setShowResultados(true);
    };

    return (
        <div>
            <h1>Historico</h1>
            
            {/* Seção de Verificação de Números */}
            <div style={{ 
                marginBottom: "30px", 
                padding: "15px", 
                backgroundColor: "#f5f5f5", 
                borderRadius: "8px",
                border: "1px solid #ddd"
            }}>
                <h2>Verificar Números</h2>
                <p style={{ fontSize: "12px", color: "#666" }}>
                    Digite até 10 números separados por espaço ou vírgula para verificar se já apareceram no histórico
                </p>
                <textarea
                    value={numerosVerificacao}
                    onChange={(e) => setNumerosVerificacao(e.target.value)}
                    placeholder="Ex: 1 2 3 4 5 6 7 8 9 10"
                    style={{
                        width: "100%",
                        padding: "10px",
                        borderRadius: "4px",
                        border: "1px solid #ccc",
                        fontSize: "14px",
                        height: "80px",
                        fontFamily: "monospace"
                    }}
                />
                <button 
                    onClick={verificarNumeros}
                    style={{
                        marginTop: "10px",
                        padding: "10px 20px",
                        backgroundColor: "#007bff",
                        color: "white",
                        border: "none",
                        borderRadius: "4px",
                        cursor: "pointer",
                        fontSize: "14px"
                    }}
                >
                    Verificar
                </button>

                {/* Resultados da Verificação */}
                {showResultados && (
                    <div style={{ marginTop: "20px" }}>
                        <h3>Resultados ({resultadosVerificacao.length} ocorrência(s) encontrada(s))</h3>
                        {resultadosVerificacao.length > 0 ? (
                            <table border="1" cellPadding="10" style={{ marginTop: "10px", width: "100%" }}>
                                <thead>
                                    <tr style={{ backgroundColor: "#e8f4f8" }}>
                                        <th>ID</th>
                                        <th>Tipo</th>
                                        <th>Números Reais</th>
                                        <th>Números Encontrados</th>
                                        <th>Quantidade</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {resultadosVerificacao.map(resultado => (
                                        <tr key={resultado.id}>
                                            <td>{resultado.id}</td>
                                            <td>{resultado.tipo}</td>
                                            <td>{resultado.numerosReais.join(", ")}</td>
                                            <td style={{ color: "#28a745", fontWeight: "bold" }}>
                                                {resultado.numerosEncontrados.join(", ")}
                                            </td>
                                            <td style={{ textAlign: "center", fontWeight: "bold" }}>
                                                {resultado.quantidadeEncontrada}/10
                                            </td>
                                        </tr>
                                    ))}
                                </tbody>
                            </table>
                        ) : (
                            <p style={{ color: "#999" }}>Nenhuma ocorrência encontrada para os números digitados</p>
                        )}
                    </div>
                )}
            </div>

            {/* Filtro de Tipo */}
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