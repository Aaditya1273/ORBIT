import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import { authApi, User } from '../services/api';
import toast from 'react-hot-toast';

interface AuthState {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  error: string | null;
  
  // Actions
  login: (email: string, password: string) => Promise<void>;
  register: (userData: { name: string; email: string; password: string }) => Promise<void>;
  logout: () => Promise<void>;
  refreshToken: () => Promise<void>;
  getCurrentUser: () => Promise<void>;
  clearError: () => void;
  setLoading: (loading: boolean) => void;
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set, get) => ({
      user: null,
      token: null,
      isAuthenticated: false,
      isLoading: false,
      error: null,

      login: async (email: string, password: string) => {
        try {
          set({ isLoading: true, error: null });
          
          const response = await authApi.login(email, password);
          
          // Store token in localStorage
          localStorage.setItem('orbit_token', response.token);
          
          set({
            user: response.user,
            token: response.token,
            isAuthenticated: true,
            isLoading: false,
            error: null,
          });
          
          toast.success(`Welcome back, ${response.user.name}!`);
        } catch (error: any) {
          const errorMessage = error.response?.data?.message || 'Login failed';
          set({
            user: null,
            token: null,
            isAuthenticated: false,
            isLoading: false,
            error: errorMessage,
          });
          toast.error(errorMessage);
          throw error;
        }
      },

      register: async (userData: { name: string; email: string; password: string }) => {
        try {
          set({ isLoading: true, error: null });
          
          const response = await authApi.register(userData);
          
          // Store token in localStorage
          localStorage.setItem('orbit_token', response.token);
          
          set({
            user: response.user,
            token: response.token,
            isAuthenticated: true,
            isLoading: false,
            error: null,
          });
          
          toast.success(`Welcome to ORBIT, ${response.user.name}!`);
        } catch (error: any) {
          const errorMessage = error.response?.data?.message || 'Registration failed';
          set({
            user: null,
            token: null,
            isAuthenticated: false,
            isLoading: false,
            error: errorMessage,
          });
          toast.error(errorMessage);
          throw error;
        }
      },

      logout: async () => {
        try {
          set({ isLoading: true });
          
          // Call logout API to invalidate token on server
          await authApi.logout();
          
          // Clear local storage
          localStorage.removeItem('orbit_token');
          
          set({
            user: null,
            token: null,
            isAuthenticated: false,
            isLoading: false,
            error: null,
          });
          
          toast.success('Logged out successfully');
        } catch (error: any) {
          // Even if API call fails, clear local state
          localStorage.removeItem('orbit_token');
          set({
            user: null,
            token: null,
            isAuthenticated: false,
            isLoading: false,
            error: null,
          });
          
          console.error('Logout error:', error);
        }
      },

      refreshToken: async () => {
        try {
          const response = await authApi.refreshToken();
          
          // Update token in localStorage
          localStorage.setItem('orbit_token', response.token);
          
          set({
            token: response.token,
            error: null,
          });
        } catch (error: any) {
          // If refresh fails, logout user
          localStorage.removeItem('orbit_token');
          set({
            user: null,
            token: null,
            isAuthenticated: false,
            error: 'Session expired',
          });
          
          toast.error('Session expired. Please log in again.');
          throw error;
        }
      },

      getCurrentUser: async () => {
        try {
          set({ isLoading: true, error: null });
          
          const user = await authApi.getCurrentUser();
          
          set({
            user,
            isLoading: false,
            error: null,
          });
        } catch (error: any) {
          const errorMessage = error.response?.data?.message || 'Failed to get user data';
          set({
            isLoading: false,
            error: errorMessage,
          });
          
          // If unauthorized, clear auth state
          if (error.response?.status === 401) {
            localStorage.removeItem('orbit_token');
            set({
              user: null,
              token: null,
              isAuthenticated: false,
            });
          }
          
          throw error;
        }
      },

      clearError: () => {
        set({ error: null });
      },

      setLoading: (loading: boolean) => {
        set({ isLoading: loading });
      },
    }),
    {
      name: 'orbit-auth-storage',
      partialize: (state) => ({
        user: state.user,
        token: state.token,
        isAuthenticated: state.isAuthenticated,
      }),
      onRehydrateStorage: () => (state) => {
        // Check if we have a token in localStorage
        const token = localStorage.getItem('orbit_token');
        if (token && state) {
          state.token = token;
          state.isAuthenticated = true;
          
          // Optionally refresh user data on app load
          state.getCurrentUser().catch(() => {
            // If getting user fails, clear auth state
            localStorage.removeItem('orbit_token');
            state.user = null;
            state.token = null;
            state.isAuthenticated = false;
          });
        }
      },
    }
  )
);

// Helper hooks for common auth operations
export const useAuth = () => {
  const {
    user,
    isAuthenticated,
    isLoading,
    error,
    login,
    register,
    logout,
    clearError,
  } = useAuthStore();

  return {
    user,
    isAuthenticated,
    isLoading,
    error,
    login,
    register,
    logout,
    clearError,
  };
};

export const useUser = () => {
  const user = useAuthStore((state) => state.user);
  return user;
};

export const useIsAuthenticated = () => {
  const isAuthenticated = useAuthStore((state) => state.isAuthenticated);
  return isAuthenticated;
};