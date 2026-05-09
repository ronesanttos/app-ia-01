import { useEffect, useState } from "react";
import BlocoPrevisao from "../components/BlocoPrevisao.jsx"
import { apiFetch, readApiError } from "../api/client.js";

export default function Previsao() {
    const [heuristica, setHeuristica] = useState(null)
    const [aprendizado, setAprendizado] = useState(null)

    const [mlRodando, setMlRodando] = useState(false)
    const [previsoes, setPrevisoes] = useState([])
    const [loading, setLoading] = useState(false)
    const [erro, setErro] = useState("")
    const [msg, setMsg] = useState({ texto: "", tipo: "" })

    async function buscarPrevisoes() {
        setLoading(true);
        setErro("");

        try {
            const [resAp, resHeu] = await Promise.all([
                apiFetch(`/api/listas/previsao_aprendizado/`),
                apiFetch(`/api/listas/previsao/`)
            ]);

            if (!resAp.ok || !resHeu.ok) {
                throw new Error("Erro ao buscar previsões");
            }

            const dataAp = await resAp.json();
            const dataHeu = await resHeu.json();

            setAprendizado(dataAp);
            setHeuristica(dataHeu);

            setMsg({ texto: "Previsão atualizada!", tipo: "success" });
        }

        catch (err) {
            setErro("Erro ao carregar previsões");
            console.error(err)
        }
        finally {
            setLoading(false)
        }
    }

    async function gerarPrevisao() {
        try {
            setLoading(true)
            const res = await apiFetch(`/api/listas/gerar_previsao/`, {
                method: "POST"
            });

            const data = await res.json()

            if (data.status === "ok") {
                setMsg({ texto: "Salvo com sucesso!", tipo: "success" });
            } else if (data.status === "duplicado_recente") {
                setMsg({ texto: "Previsão já gerada recentemente", tipo: "erro" });
            } else {
                setMsg({ texto: "Erro inesperado", tipo: "erro" });
            }
            await buscarPrevisoes();

        } catch (err) {
            setErro("Erro ao gerar previsao")
            console.error(err)
        } finally {
            setLoading(false)
        }
    }

    async function iniciarML() {
        try {
            setMlRodando(true);
            setErro("");
            setMsg({ texto: "Enfileirando IA (ML)...", tipo: "success" });

            const res = await apiFetch(`/api/listas/previsao_ml/`);

            if (!res.ok) {
                const detalhe = await readApiError(res);
                setErro(detalhe);
                setMsg({ texto: detalhe, tipo: "erro" });
                setMlRodando(false);
                return;
            }

            const data = await res.json().catch(() => ({}));

            if (data.status === "processando" && data.task_id) {
                setMsg({ texto: "IA em processamento (Celery)...", tipo: "success" });
                await aguardarTaskMl(data.task_id);
                return;
            }

            const extra = JSON.stringify(data).slice(0, 200);
            setErro(`Resposta inesperada: ${extra}`);
            setMsg({ texto: "Resposta inesperada da API", tipo: "erro" });
            setMlRodando(false);
        } catch (err) {
            console.error(err);
            const texto =
                err instanceof TypeError && err.message === "Failed to fetch"
                    ? "Não foi possível conectar ao backend (URL/CORS/rede). Confira VITE_API_BASE_URL e se o Django está rodando."
                    : err?.message || "Erro ao iniciar ML";
            setErro(texto);
            setMsg({ texto, tipo: "erro" });
            setMlRodando(false);
        }
    }

    async function aguardarTaskMl(taskId) {
        const maxTentativas = 60;
        const intervaloMs = 3000;

        for (let i = 0; i < maxTentativas; i++) {
            const res = await apiFetch(
                `/api/listas/previsao_ml_status/?task_id=${encodeURIComponent(taskId)}`
            );

            if (!res.ok) {
                const detalhe = await readApiError(res);
                setErro(detalhe);
                setMsg({ texto: detalhe, tipo: "erro" });
                setMlRodando(false);
                return;
            }

            const data = await res.json().catch(() => ({}));

            if (data.status === "SUCCESS") {
                setMsg({ texto: "IA finalizou com sucesso!", tipo: "success" });
                setMlRodando(false);
                const prev =
                    data.result?.data?.previsao ||
                    data.ultima_previsao_salva?.numeros;
                const id = data.ultima_previsao_salva?.id;
                if (prev) {
                    setPrevisoes([{ id, tipo: "ml", numeros: prev }]);
                }
                await buscarPrevisoes();
                return;
            }

            if (data.status === "FAILURE") {
                const falha = data.error != null ? String(data.error) : "IA falhou";
                setErro(falha);
                setMsg({ texto: falha, tipo: "erro" });
                setMlRodando(false);
                return;
            }

            await new Promise((r) => setTimeout(r, intervaloMs));
        }

        const limite = "Tempo limite aguardando a IA (worker parado ou fila lenta). Verifique o Celery.";
        setErro(limite);
        setMsg({ texto: limite, tipo: "erro" });
        setMlRodando(false);
    }

    useEffect(() => {
        if (!msg.texto) return;

        const ms = msg.tipo === "erro" ? 12000 : 3000;
        const timer = setTimeout(() => {
            setMsg({ texto: "", tipo: "" });
        }, ms);

        return () => clearTimeout(timer);
    }, [msg]);

    useEffect(() => {
        buscarPrevisoes();
    }, []);

    return (
        <div>
            <h1 className="page-title">Previsões</h1>
            <p className="page-subtitle">
                Heurística, aprendizado e fila ML (Celery). Use os botões abaixo.
            </p>

            <div className="btn-row">
                <button type="button" className="btn" onClick={buscarPrevisoes} disabled={loading}>
                    Atualizar
                </button>
                <button type="button" className="btn" onClick={gerarPrevisao} disabled={loading}>
                    Gerar heurística
                </button>
                <button type="button" className="btn btn-primary" onClick={iniciarML} disabled={mlRodando}>
                    Rodar IA (ML)
                </button>
            </div>

            <BlocoPrevisao
                titulo="Previsão com Aprendizado"
                dados={aprendizado}
            />

            <BlocoPrevisao
                titulo="Previsão com Heurística"
                dados={heuristica}
            />

            {loading && <p className="loading-block">Carregando…</p>}
            {erro && <div className="alert alert-error" role="alert">{erro}</div>}

            {msg.texto && (
                <div
                    className={msg.tipo === "erro" ? "alert alert-error" : "alert alert-success"}
                    role="status"
                >
                    {msg.texto}
                </div>
            )}

            <h2 className="page-title" style={{ fontSize: "1.35rem", marginTop: "1.5rem" }}>
                Última previsão ML
            </h2>

            {mlRodando && <p className="loading-block">IA em processamento…</p>}
            {previsoes
                .filter(p => p.tipo === "ml")
                .map(p => (
                    <div key={p.id ?? "ml"} className="preview-card">
                        <p style={{ fontVariantNumeric: "tabular-nums", fontWeight: 600 }}>
                            {Array.isArray(p.numeros) ? p.numeros.join(", ") : String(p.numeros)}
                        </p>
                    </div>
                ))}
        </div>
    )
}
