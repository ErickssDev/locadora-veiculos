import { useEffect, useState } from 'react';
import { vehiclesApi } from '../services/api';
import type { Carro } from '../services/api';
import CarCard from '../components/CarCard';

export default function Home() {
  const [carros, setCarros] = useState<Carro[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [erro, setErro] = useState<string | null>(null);

  useEffect(() => {
    // Nova chamada baseada no seu objeto agrupado vehiclesApi
    vehiclesApi.listarTodos()
      .then((dados) => {
        setCarros(dados);
        setLoading(false);
      })
      .catch((err) => {
        console.error("Erro ao carregar o catálogo:", err);
        setErro("Não foi possível carregar o catálogo de veículos. Verifique a API.");
        setLoading(false);
      });
  }, []);

  if (loading) {
    return (
      <div className="min-h-screen bg-slate-950 flex items-center justify-center text-slate-400 font-medium animate-pulse">
        Carregando o catálogo DriveX...
      </div>
    );
  }

  if (erro) {
    return (
      <div className="min-h-screen bg-slate-950 flex items-center justify-center p-4">
        <div className="p-4 bg-red-950/40 border border-red-900 rounded-xl max-w-md text-center text-red-400 text-sm">
          {erro}
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-slate-950 text-white px-4 py-12 sm:px-6 lg:px-8">
      <div className="max-w-7xl mx-auto">
        <header className="mb-10">
          <h1 className="text-3xl font-extrabold tracking-tight sm:text-4xl text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-indigo-500">
            Modelos Disponíveis
          </h1>
        </header>

        {carros.length === 0 ? (
          <div className="text-center py-16 border border-dashed border-slate-800 rounded-2xl bg-slate-900/20">
            <p className="text-slate-500">Nenhum veículo disponível no momento.</p>
          </div>
        ) : (
          <main className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
            {carros.map((carro) => (
              <CarCard key={carro.id} Pattern carro={carro} />
            ))}
          </main>
        )}
      </div>
    </div>
  );
}