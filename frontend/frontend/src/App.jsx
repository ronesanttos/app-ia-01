import { Route, Routes } from "react-router-dom";

import Navbar from "./components/Navbar";

import Dashboard from "./pages/Dashboard";
import Historico from "./pages/Historico";
import Previsao from "./pages/Previsao"
import AdicionarDados from "./pages/AdiconarDados";
import Metricas from "./pages/Metricas";
import ValidarPrevisao from "./pages/validarPrevisao";

function App() {
  
  return (
    <>
      <Navbar/>
      <main className="app-main">
        <Routes>
          <Route path="/" element={<Dashboard/>} />
          <Route path="/historico" element={<Historico/>} />
          <Route path="/adicionar" element={<AdicionarDados/>} />
          <Route path="/previsao" element={<Previsao />} />
          <Route path="/validar" element={<ValidarPrevisao/>} />
          <Route path="/metricas" element={<Metricas/>} />
        </Routes>
      </main>
    </>
  );
}

export default App;