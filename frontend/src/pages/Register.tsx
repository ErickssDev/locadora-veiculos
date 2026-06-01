import { useState } from 'react';
import { authApi } from '../services/api';

export default function Register() {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [phone, setPhone] = useState('');
  const [password, setPassword] = useState('');
  const [userType, setUserType] = useState('client');
  const [loading, setLoading] = useState(false);
  const [mensagem, setMensagem] = useState<{ tipo: 'sucesso' | 'erro'; texto: string } | null>(null);

  const handleRegister = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setMensagem(null);

    try {
      await authApi.register({
        name,
        email,
        phone,
        password,
        user_type: userType,
      });

      setMensagem({ tipo: 'sucesso', texto: 'Conta criada com sucesso! Faça o login.' });
      // Limpa o formulário
      setName('');
      setEmail('');
      setPhone('');
      setPassword('');
    } catch (err: any) {
      console.error(err);
      setMensagem({ 
        tipo: 'erro', 
        texto: err.response?.data?.detail || 'Erro ao criar conta. Verifique os dados.' 
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-950 flex items-center justify-center p-4">
      <div className="bg-slate-900 border border-slate-800 rounded-2xl p-8 w-full max-w-md shadow-2xl">
        <h2 className="text-2xl font-black text-white text-center mb-1">Criar Conta</h2>
        <p className="text-slate-400 text-sm text-center mb-6">Cadastre-se na LocadoraX</p>

        {mensagem && (
          <div className={`p-3 rounded-xl text-sm mb-4 text-center border ${
            mensagem.tipo === 'sucesso' 
              ? 'bg-green-950/40 text-green-400 border-green-900' 
              : 'bg-red-950/40 text-red-400 border-red-900'
          }`}>
            {mensagem.texto}
          </div>
        )}

        <form onSubmit={handleRegister} className="space-y-4">
          <div>
            <label className="block text-xs font-semibold text-slate-400 uppercase mb-1">Nome Completo</label>
            <input 
              type="text" required value={name} onChange={e => setName(e.target.value)}
              className="w-full bg-slate-950 border border-slate-800 rounded-xl px-4 py-2.5 text-white focus:outline-none focus:border-blue-500 text-sm"
            />
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-400 uppercase mb-1">E-mail</label>
            <input 
              type="email" required value={email} onChange={e => setEmail(e.target.value)}
              className="w-full bg-slate-950 border border-slate-800 rounded-xl px-4 py-2.5 text-white focus:outline-none focus:border-blue-500 text-sm"
            />
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-400 uppercase mb-1">Telefone</label>
            <input 
              type="tel" required value={phone} onChange={e => setPhone(e.target.value)}
              className="w-full bg-slate-950 border border-slate-800 rounded-xl px-4 py-2.5 text-white focus:outline-none focus:border-blue-500 text-sm"
            />
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-400 uppercase mb-1">Senha</label>
            <input 
              type="password" required value={password} onChange={e => setPassword(e.target.value)}
              className="w-full bg-slate-950 border border-slate-800 rounded-xl px-4 py-2.5 text-white focus:outline-none focus:border-blue-500 text-sm"
            />
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-400 uppercase mb-1">Tipo de Perfil</label>
            <select 
              value={userType} onChange={e => setUserType(e.target.value)}
              className="w-full bg-slate-950 border border-slate-800 rounded-xl px-4 py-2.5 text-white focus:outline-none focus:border-blue-500 text-sm"
            >
              <option value="client">Quero Alugar (Cliente)</option>
              <option value="owner">Quero Anunciar (Proprietário)</option>
            </select>
          </div>

          <button 
            type="submit" disabled={loading}
            className="w-full bg-blue-600 hover:bg-blue-500 text-white font-bold py-3 rounded-xl transition duration-200 text-sm mt-2 disabled:opacity-50"
          >
            {loading ? 'Cadastrando...' : 'Concluir Cadastro'}
          </button>
        </form>
      </div>
    </div>
  );
}