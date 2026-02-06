import { create } from 'zustand';
import { authApi } from '../services/api';
import toast from 'react-hot-toast';

interface User {
  id: string;
  email: string;
  name: string;
  onboarding_completed: boolean;
}

interface AuthState {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  login: (email: string, password: string) => Promise<void>;
  register: (email: string, name: string, password: string) => Promise<void>;
  logout: () => Promise<void>;
  checkAuth: () => void;
}

export const useAuthStore = create<AuthState>((set) => ({
  user: null,
  isAuthenticated: false,
  isLoading: false,

  login: async (email: string, password: string) => {
    set({ isLoading: true });
    try {
      const response = await authApi.login(email, password);
      set({
        user: response.user,
        isAuthenticated: true,
        isLoading: false,
      });
      toast.success('Logged in successfully!');
    } catch (error: any) {
      set({ isLoading: false });
      const message = error.response?.data?.detail || 'Login failed';
      toast.error(message);
      throw error;
    }
  },

  register: async (email: string, name: string, password: string) => {
    set({ isLoading: false });
    try {
      const response = await authApi.register({ email, name, password });
      set({
        user: response.user,
        isAuthenticated: true,
        isLoading: false,
      });
      toast.success('Account created successfully!');
    } catch (error: any) {
      set({ isLoading: false });
      const message = error.response?.data?.detail || 'Registration failed';
      toast.error(message);
      throw error;
    }
  },

  logout: async () => {
    try {
      await authApi.logout();
    } catch (error) {
      console.error('Logout error:', error);
    } finally {
      set({
        user: null,
        isAuthenticated: false,
      });
      toast.success('Logged out successfully');
    }
  },

  checkAuth: () => {
    const token = localStorage.getItem('access_token');
    const userStr = localStorage.getItem('user');
    
    if (token && userStr) {
      try {
        const user = JSON.parse(userStr);
        set({
          user,
          isAuthenticated: true,
        });
      } catch (error) {
        localStorage.removeItem('access_token');
        localStorage.removeItem('user');
      }
    }
  },
}));
