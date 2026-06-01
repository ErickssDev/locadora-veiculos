import type { Carro } from '../services/api';

interface CarCardProps {
  carro: Carro;
}

export default function CarCard({ carro }: CarCardProps) {
  return (
    <div className="bg-slate-900 border border-slate-800 rounded-2xl overflow-hidden shadow-lg hover:border-slate-700 transition duration-300 flex flex-col">
      <div className="p-6 flex-1">
        <div className="flex justify-between items-start mb-2">
          <h3 className="text-xl font-bold text-white">
            {carro.brand} <span className="text-blue-400">{carro.model}</span>
          </h3>
          <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-950 text-blue-400 border border-blue-900 capitalize">
            {carro.category}
          </span>
        </div>
        
        <p className="text-sm text-slate-400 line-clamp-2 mt-2">
          {carro.description || 'Nenhuma descrição fornecida para este veículo.'}
        </p>

        <div className="grid grid-cols-2 gap-4 mt-6 pt-4 border-t border-slate-800/60 text-sm text-slate-400">
          <div>
            <span className="block text-xs text-slate-500">Ano</span>
            <span className="font-medium text-slate-300">{carro.year}</span>
          </div>
          <div>
            <span className="block text-xs text-slate-500">Cor</span>
            <span className="font-medium text-slate-300">{carro.color}</span>
          </div>
        </div>
      </div>

      <div className="p-6 bg-slate-900/50 border-t border-slate-800/40 flex items-center justify-between">
        <div>
          <span className="text-xs text-slate-500 block">Diária</span>
          <span className="text-xl font-black text-green-400">
            R$ {Number(carro.daily_rate).toFixed(2)}
          </span>
        </div>
        <button 
          disabled={!carro.is_available}
          className={`px-4 py-2.5 rounded-xl font-semibold text-sm transition ${
            carro.is_available 
              ? 'bg-blue-600 text-white hover:bg-blue-500' 
              : 'bg-slate-800 text-slate-500 cursor-not-allowed'
          }`}
        >
          {carro.is_available ? 'Reservar' : 'Esgotado'}
        </button>
      </div>
    </div>
  );
}