import { useEffect, useState } from "react";
import { apiFetch } from "../api/client.js";

/** Quantas listas recentes entram na referência automática (união dos números). */
const LISTAS_REFERENCIA = 6;

export default function ValidarPrevisao() {
    const [previsoes, setPrevisoes] = useState([]);
    const [input, setInput] = useState("");
    const [resultado, setResultado] = useState(null);
    const [selecionado, setSelecionado] = useState(null);
    const [validandoAuto, setValidandoAuto] = useState(false);

    // 🔹 carregar previsões
    useEffect(() => {
        apiFetch(`/api/listas/previsoes/?limit=50`)
            .then(res => res.json())
            .then(setPrevisoes);
    }, []);


    // 🔹 converter input → array
    function parseNumeros(texto) {
        return texto
            .split(/[\s,]+/)
            .map(Number)
            .filter(n => !isNaN(n));
    }

    async function validarComNumeros(numeros) {
        if (!selecionado) {
            alert("Selecione uma previsão");
            return;
        }
        if (!numeros.length) {
            alert("Nenhum número válido para validar");
            return;
        }

        const res = await apiFetch(`/api/listas/${selecionado}/validar/`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ numeros }),
        });

        const data = await res.json();
        if (data.erro) {
            alert(data.erro);
            return;
        }
        setResultado(data);
    }

    // 🔹 validar previsão
    async function validar() {
        await validarComNumeros(parseNumeros(input));
    }

    /**
     * Busca as últimas N listas cadastradas, monta a referência como união dos
     * números sorteados nelas, preenche o campo e valida a previsão selecionada.
     */
    async function validarAutomatico() {
        if (!selecionado) {
            alert("Selecione uma previsão");
            return;
        }
        setValidandoAuto(true);
        try {
            const res = await apiFetch(
                `/api/listas/ultimas_listas/?limite=${LISTAS_REFERENCIA}`
            );
            const data = await res.json().catch(() => ({}));
            if (!res.ok) {
                alert(
                    data.erro ||
                        "Não foi possível obter as listas de sorteio de referência"
                );
                return;
            }
            const numeros = Array.isArray(data.numeros_referencia)
                ? data.numeros_referencia
                : [];
            setInput(numeros.join(", "));
            await validarComNumeros(numeros);
        } finally {
            setValidandoAuto(false);
        }
    }

    // 🔹 destacar acertos
    function renderComparacao(previstos, reais) {
        return previstos.map((n, i) => {
            const acertou = reais.includes(n);

            return (
                <span
                    key={i}
                    style={{
                        color: acertou ? "limegreen" : "red",
                        marginRight: "6px",
                        fontWeight: "bold"
                    }}
                >
                    {n}
                </span>
            );
        });
    }

    return (
        <div>
            <h1>Validar Previsão</h1>

            {/* 🔹 selecionar previsão */}
            <select onChange={(e) => {setSelecionado(Number(e.target.value));setResultado(null)}}>
                
                <option value="">Selecione</option>
                {previsoes.map(p => (
                    <option key={p.id} value={p.id}>
                        #{p.id} | {p.tipo} | {p.numeros.slice(0, 3).join(", ")}...
                    </option>
                ))}
            </select>

            <br /><br />

            {/* 🔹 input números reais */}
            <textarea
                placeholder="Digite os números reais (ex: 10, 20, 30...)"
                value={input}
                onChange={(e) => setInput(e.target.value)}
            />

            <br /><br />

            <button onClick={validar} disabled={validandoAuto}>
                Validar
            </button>
            {" "}
            <button type="button" onClick={validarAutomatico} disabled={validandoAuto}>
                {validandoAuto
                    ? "Validando…"
                    : `Validar automaticamente (últimas ${LISTAS_REFERENCIA} listas)`}
            </button>
            <p style={{ fontSize: "0.9rem", color: "#555", maxWidth: "36rem" }}>
                Na validação automática, os números reais são a união (sem repetir) de
                todos os valores das {LISTAS_REFERENCIA} listas mais recentes: um
                palpite “acerta” se aparecer em qualquer uma dessas listas.
            </p>

            {/* 🔹 resultado */}
            {resultado && (
                <div>
                    <h2>Resultado</h2>

                    <p>Acertos: {resultado.acertos}</p>
                    <p>Total: {resultado.total}</p>
                    <p>
                        Acurácia: {(resultado.acuracia * 100).toFixed(1)}%
                    </p>
                    <p>Data da previsão: {resultado.data_previsao}</p>
                </div>
            )}

            {/* 🔹 comparação visual */}
            {resultado && selecionado && (
                <div>
                    <h3>Comparação</h3>

                    {renderComparacao(
                        previsoes.find(p => p.id == selecionado)
                            ?.numeros || [],
                        parseNumeros(input)
                    )}
                </div>
            )}
        </div>
    );
}
