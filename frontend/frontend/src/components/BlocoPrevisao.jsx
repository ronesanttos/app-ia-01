import React from 'react'

export default function BlocoPrevisao({ titulo, dados }) {
    if (!dados) return null;

    return (
        <div className="preview-card">
            <h3>{titulo}</h3>

            <h4>Números</h4>
            <p style={{ fontWeight: 600, fontVariantNumeric: "tabular-nums" }}>
                {dados.previsao?.join(", ") ?? "—"}
            </p>

            <h4>Top score</h4>
            <ul>
                {Object.entries(dados.score || {}).sort((a,b) => b[1] - a[1]).slice(0, 10).map(([num, val]) => (
                    <li key={num}>
                        {num}: {typeof val === "number" ? val.toFixed(3) : val}
                    </li>
                ))}
            </ul>
        </div>
    )
}
