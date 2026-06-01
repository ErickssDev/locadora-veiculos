import { useEffect, useState } from 'react';
import { usersApi, reservationsApi } from '../services/api';
import type { User, Reservation } from '../services/api';

export default function Account() {
  const [usuario, setUsuario] = useState<User | null>(null);
  const [reservas, setReservas] = useState<Reservation[]>([]);
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    // Faz a chamada paralela usando os novos objetos modulares da API
    Promise.all([
      usersApi.getPerfilMe(),
      reservationsApi.listarTodas()
    ])
      .then(([dadosUsuario, dadosReservas]) => {
        setUsuario(dadosUsuario);
        setReservas(Array.isArray(dadosReservas) ? dadosReservas : []);
        setLoading(false);
      })
      .catch((err) => {
        console.error("Erro ao carregar dados do perfil:", err);
        setLoading(false);
      });
  }, []);

  if (loading) {
    return (
      <div className="min-h-screen bg-slate-950 flex items-center justify-center text-slate-400 font-medium animate-pulse">
        Carregando painel do usuário...
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-slate-950 text-white py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-3xl mx-auto space-y-8">
        
        {/* Card de Perfil */}
        {usuario && (
          <section className="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-xl">
            <h2 className="text-xl font-bold border-b border-slate-800 pb-3 mb-4 text-blue-400">
              Minha Conta
            </h2>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 text-sm text-slate-300">
              <div>
                <span className="block text-xs font-semibold text-slate-500 uppercase">Nome Completo</span>
                <span className="text-slate-200 text-base">{usuario.name}</span>
              </div>
              <div>
                <span className="block text-xs font-semibold text-slate-500 uppercase">E-mail</span>
                <span className="text-slate-200 text-base">{usuario.email}</span>
              </div>
              <div>
                <span className="block text-xs font-semibold text-slate-500 uppercase">Telefone</span>
                <span className="text-slate-200 text-base">{usuario.phone || 'Não cadastrado'}</span>
              </div>
              <div>
                <span className="block text-xs font-semibold text-slate-500 uppercase">Nível de Acesso</span>
                <span className="inline-block mt-1 px-2.5 py-0.5 rounded-full text-xs font-semibold bg-blue-950 text-blue-400 border border-blue-900 uppercase">
                  {usuario.user_type}
                </span>
              </div>
            </div>
          </section>
        )}

        {/* Histórico de Reservas */}
        <section className="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-xl">
          <h2 className="text-xl font-bold border-b border-slate-800 pb-3 mb-4 text-green-400">
            Minhas Reservas
          </h2>
          
          {reservas.length === 0 ? (
            <p className="text-slate-500 text-sm py-4">Nenhuma reserva encontrada no histórico.</p>
          ) : (
            <div className="divide-y divide-slate-800/60">
              {reservas.map((reserva) => (
                <div key={reserva.id} className="py-4 flex justify-between items-center text-sm">
                  <div>
                    <p className="font-semibold text-slate-200">Código de Reserva #{reserva.id}</p>
                    <p className="text-xs text-slate-400 mt-0.5">
                      Período: {reserva.start_date} até {reserva.end_date} ({reserva.total_days} dias)
                    </p>
                  </div>
                  <div className="text-right">
                    <span className={`text-[10px] font-bold px-2 py-0.5 rounded uppercase ${
                      reserva.status === 'confirmed' || reserva.status === 'completed'
                        ? 'bg-green-950 text-green-400 border border-green-900'
                        : 'bg-amber-950 text-amber-400 border border-amber-900'
                    }`}>
                      {reserva.status}
                    </span>
                    <p className="font-bold mt-1 text-slate-200">R$ {reserva.total_amount}</p>
                  </div>
                </div>
              ))}
            </div>
          )}
        </section>

      </div>
    </div>
  );
}