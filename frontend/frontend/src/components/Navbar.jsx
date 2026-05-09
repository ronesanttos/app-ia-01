import { Link } from "react-router-dom";

export default function Navbar() {
  return (
    <nav className="nav-app">
      <h2 className="logo">IA — Painel</h2>

      <div className="links">
        <Link to="/">Dashboard</Link>
        <Link to="/adicionar">Adicionar</Link>
        <Link to="/historico">Histórico</Link>
        <Link to="/previsao">Previsão</Link>
        <Link to="/validar">Validar</Link>
        <Link to="/metricas">Métricas</Link>
      </div>
    </nav>
  );
}