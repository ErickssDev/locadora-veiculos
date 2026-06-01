import { BrowserRouter, Routes, Route, Link } from "react-router-dom";
import Home from "./pages/Home";
import Account from "./pages/Account";
import Login from "./pages/Login";
import Register from "./pages/Register";

export default function App() {
  return (
    <BrowserRouter>
      <div className="min-h-screen bg-slate-950 text-slate-100 antialiased font-sans flex flex-col">
        
        {/* Barra de Navegação */}
        <nav className="border-b border-slate-900 bg-slate-950/80 backdrop-blur-md sticky top-0 z-50">
          <div className="max-w-6xl mx-auto px-6 py-4 flex justify-between items-center">
            <Link to="/" className="text-2xl font-black tracking-tight text-white hover:opacity-85 transition">
              Locadora<span className="text-blue-500">X</span>
            </Link>
            
            <div className="flex gap-6 items-center">
              <Link to="/" className="text-sm font-semibold text-slate-300 hover:text-white transition">
                Catálogo
              </Link>
              <Link to="/login" className="text-sm font-semibold text-slate-300 hover:text-white transition">
                Entrar
              </Link>
              <Link to="/cadastro" className="text-sm font-semibold text-slate-300 hover:text-white transition">
                Criar Conta
              </Link>
              <Link to="/conta" className="text-sm font-semibold text-slate-300 hover:text-white transition">
                Minha Conta
              </Link>
              <div className="w-8 h-8 rounded-lg bg-blue-600 flex items-center justify-center text-xs font-black text-white shadow-md">
                R
              </div>
            </div>
          </div>
        </nav>

        {/* Conteúdo Principal do App */}
        <main className="flex-1 p-6 sm:p-12">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/login" element={<Login />} />
            <Route path="/cadastro" element={<Register />} />
            <Route path="/conta" element={<Account />} />
          </Routes>
        </main>
        
      </div>
    </BrowserRouter>
  );
}