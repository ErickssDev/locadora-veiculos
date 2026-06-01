import { useState } from 'react';
import { authApi } from '../services/api';

export default function Login() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [erro, setErro] = useState<string | null>(null);

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setErro(null);

    try {
      // Envia os dados no formato esperado pela autenticação do FastAPI
      const dados = await authApi.login({ email, password });
      
      if (dados.access_token) {
        // Salva o token exatamente no formato mapeado pelo seu interceptor do Axios
        localStorage.setItem('@DriveX:token', dados.access_token);
        setErro(null);
        alert('Login efetuado com sucesso! Token armazenado.');
        window.location.reload(); // Recarrega para aplicar o token globalmente
      }
    } catch (err: any) {
      console.error(err);
      setErro(err.response?.data?.detail || 'Falha na autenticação. Verifique e-mail e senha.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-950 flex items-center justify-center p-4">
      <div className="bg-slate-900 border border-slate-800 rounded-2xl p-8 w-full max-w-md shadow-2xl">
        <h2 className="text-2xl font-black text-white text-center mb-1">Acessar Sistema</h2>
        <p className="text-slate-400 text-sm text-center mb-6">Insira suas credenciais DriveX</p>

        {erro && (
          <div className="p-3 bg-red-950/40 border border-red-900 text-red-400 rounded-xl text-sm mb-4 text-center">
            {erro}
          </div>
        )}

        <form onSubmit={handleLogin} className="space-y-4">
          <div>
            <label className="block text-xs font-semibold text-slate-400 uppercase mb-1">E-mail</label>
            <input 
              type="email" required value={email} onChange={e => setEmail(e.target.value)}
              className="w-full bg-slate-950 border border-slate-800 rounded-xl px-4 py-2.5 text-white focus:outline-none focus:border-blue-500 text-sm"
              placeholder="seuemail@exemplo.com"
            />
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-400 uppercase mb-1">Senha</label>
            <input 
              type="password" required value={password} onChange={e => setPassword(e.target.value)}
              className="w-full bg-slate-950 border border-slate-800 rounded-xl px-4 py-2.5 text-white focus:outline-none focus:border-blue-500 text-sm"
              placeholder="••••••••"
            />
          </div>

          <button 
            type="submit" disabled={loading}
            className="w-full bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-500 hover:to-indigo-500 text-white font-bold py-3 rounded-xl transition duration-200 text-sm mt-2 disabled:opacity-50"
          >
            {loading ? 'Verificando...' : 'Entrar no Sistema'}
          </button>
        </form>
      </div>
    </div>
  );
}