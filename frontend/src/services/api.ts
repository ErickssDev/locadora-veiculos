import axios from 'axios';

// ==========================================
// 1. ENUMS E INTERFACES (TIPAGEM)
// ==========================================

export type VehicleCategory = 'hatch' | 'sedan' | 'suv' | 'pickup' | 'van' | 'moto' | 'outro';

export interface User {
  id: number;
  name: string;
  email: string;
  phone: string;
  user_type: 'owner' | 'client' | string;
  avatar_url: string | null;
  is_active: boolean;
  is_verified: boolean;
  created_at: string;
  updated_at: string;
}

export interface Carro {
  id: number;
  brand: string;
  model: string;
  year: number;
  color: string;
  plate: string;
  category: string;
  description: string;
  daily_rate: number;
  city: string;
  state: string;
  is_available: boolean;
  owner_id: number;
  status: string;
}

export interface Reservation {
  id: number;
  vehicle_id: number;
  client_id: number;
  owner_id: number;
  start_date: string;
  end_date: string;
  total_days: number;
  daily_rate_snapshot: number;
  total_amount: number;
  status: 'pending' | 'confirmed' | 'completed' | 'cancelled' | string;
  cancellation_reason: string | null;
  created_at: string;
  updated_at: string;
}

export interface Notification {
  id: number;
  user_id: number;
  title: string;
  message: string;
  is_read: boolean;
  created_at: string;
}

// ==========================================
// 2. CONFIGURAÇÃO BASE DO AXIOS
// ==========================================

export const api = axios.create({
  // URL corrigida de acordo com o túnel ativo do Ngrok do Erick
  baseURL: 'https://vengeful-savior-apricot.ngrok-free.dev/api/v1', 
});

// Interceptor para injetar o Token JWT automaticamente em rotas protegidas
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('@DriveX:token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// ==========================================
// 3. FUNÇÕES DA API
// ==========================================

/**
 * 🔑 AUTENTICAÇÃO (AUTH)
 */
export const authApi = {
  register: async (dados: any) => {
    const response = await api.post('/auth/register', dados);
    return response.data;
  },
  login: async (credenciais: any) => {
    const response = await api.post('/auth/login', credenciais);
    return response.data; // ex: { access_token: "...", token_type: "bearer" }
  },
  token: async (dados: any) => {
    const response = await api.post('/auth/token', dados);
    return response.data;
  },
  refresh: async () => {
    const response = await api.post('/auth/refresh');
    return response.data;
  },
  forgotPassword: async (email: string) => {
    const response = await api.post('/auth/forgot-password', { email });
    return response.data;
  },
  resetPassword: async (dados: any) => {
    const response = await api.post('/auth/reset-password', dados);
    return response.data;
  },
  logout: async () => {
    const response = await api.post('/auth/logout');
    return response.data;
  }
};

/**
 * 👤 USUÁRIOS (USERS)
 */
export const usersApi = {
  getPerfilMe: async () => {
    const response = await api.get<User>('/users/me');
    return response.data;
  },
  updatePerfilMe: async (dados: Partial<User>) => {
    const response = await api.put<User>('/users/me', dados);
    return response.data;
  },
  uploadDocumento: async (formData: FormData) => {
    const response = await api.post('/users/me/documents', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    });
    return response.data;
  },
  listarDocumentos: async () => {
    const response = await api.get('/users/me/documents');
    return response.data;
  },
  deletarDocumento: async (documentId: number) => {
    const response = await api.delete(`/users/me/documents/${documentId}`);
    return response.data;
  }
};

/**
 * 🚗 VEÍCULOS (VEHICLES) - Atenção à barra '/' no final exigida pelo FastAPI
 */
export const vehiclesApi = {
  listarTodos: async () => {
    const response = await api.get<Carro[]>('/vehicles/');
    return response.data;
  },
  criar: async (dados: Omit<Carro, 'id' | 'owner_id' | 'status' | 'created_at' | 'updated_at'>) => {
    const response = await api.post<Carro>('/vehicles/', dados);
    return response.data;
  },
  listarMeusVeiculos: async () => {
    const response = await api.get<Carro[]>('/vehicles/me');
    return response.data;
  },
  buscarPorId: async (vehicleId: number) => {
    const response = await api.get<Carro>(`/vehicles/${vehicleId}`);
    return response.data;
  },
  atualizar: async (vehicleId: number, dados: Partial<Carro>) => {
    const response = await api.put<Carro>(`/vehicles/${vehicleId}`, dados);
    return response.data;
  },
  deletar: async (vehicleId: number) => {
    const response = await api.delete(`/vehicles/${vehicleId}`);
    return response.data;
  }
};

/**
 * 📅 RESERVAS (RESERVATIONS)
 */
export const reservationsApi = {
  listarTodas: async () => {
    const response = await api.get<Reservation[]>('/reservations/');
    return response.data;
  },
  criar: async (dados: { vehicle_id: number; start_date: string; end_date: string }) => {
    const response = await api.post<Reservation>('/reservations/', dados);
    return response.data;
  },
  buscarPorId: async (reservationId: number) => {
    const response = await api.get<Reservation>(`/reservations/${reservationId}`);
    return response.data;
  },
  cancelar: async (reservationId: number, reason: string) => {
    const response = await api.put<Reservation>(`/reservations/${reservationId}/cancel`, { cancellation_reason: reason });
    return response.data;
  },
  confirmar: async (reservationId: number) => {
    const response = await api.put<Reservation>(`/reservations/${reservationId}/confirm`);
    return response.data;
  },
  concluir: async (reservationId: number) => {
    const response = await api.put<Reservation>(`/reservations/${reservationId}/complete`);
    return response.data;
  }
};

/**
 * 🔔 NOTIFICAÇÕES (NOTIFICATIONS)
 */
export const notificationsApi = {
  listar: async () => {
    const response = await api.get<Notification[]>('/notifications/');
    return response.data;
  },
  marcarComoLida: async (notificationId: number) => {
    const response = await api.put(`/notifications/${notificationId}/read`);
    return response.data;
  },
  marcarTodasComoLidas: async () => {
    const response = await api.put('/notifications/read-all');
    return response.data;
  }
};

/**
 * 👑 PAINEL ADMINISTRATIVO (ADMIN)
 */
export const adminApi = {
  getDashboard: async () => {
    const response = await api.get('/admin/dashboard');
    return response.data;
  },
  listarUsuarios: async () => {
    const response = await api.get<User[]>('/admin/users');
    return response.data;
  },
  listarVeiculos: async () => {
    const response = await api.get<Carro[]>('/admin/vehicles');
    return response.data;
  },
  listarReservas: async () => {
    const response = await api.get<Reservation[]>('/admin/reservations');
    return response.data;
  }
};