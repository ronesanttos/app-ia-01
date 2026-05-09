/**
 * `items`: lista do backend [{ numero, frequencia }, ...] (0–99)
 */
export default function Heatmap({ items = [] }) {
  const map = new Map();
  for (const it of items) {
    if (it && typeof it.numero === "number") {
      map.set(it.numero, Number(it.frequencia) || 0);
    }
  }

  const freqs = [];
  for (let n = 0; n < 100; n++) {
    freqs.push(map.get(n) ?? 0);
  }
  const max = Math.max(...freqs, 1);

  return (
    <div className="heatmap-wrap" aria-label="Mapa de calor de frequência por número">
      <div className="heatmap-grid">
        {freqs.map((freq, num) => {
          const t = freq / max;
          const hue = 265;
          const sat = 35 + t * 55;
          const light = 88 - t * 52;
          const bg = `hsl(${hue} ${sat}% ${light}%)`;
          const fg = light < 52 ? "#f9fafb" : "#111827";

          return (
            <div
              key={num}
              className="heatmap-cell"
              style={{ background: bg, color: fg }}
              title={`${num}: ${freq} ocorrências`}
            >
              {num}
            </div>
          );
        })}
      </div>
      <p className="heatmap-legend">
        Mais escuro = maior frequência nas listas recentes (0–99).
      </p>
    </div>
  );
}
