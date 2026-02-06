import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import toast from 'react-hot-toast';

interface User {
  id: string;
  email: string;
  name: string;
  onboarding_completed: boolean;
  created_at: string;
}

interface AuthState {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  error: string | null;
  
  // Actions
  login: (email: string, password: string) => Promise<void>;
  register: (email: string, password: string, name: string) => Promise<void>;
  logout: () => void;
  updateUser: (user: Partial<User>) => void;
  clearError: () => void;
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
        set({ isLoading: true, error: null });
        
        try {
          // Demo login - replace with actual API call
          if (email === 'demo@orbit.ai' && password === 'demo123') {
            const mockUser: User = {
              id: 'demo-user-123',
              email: 'demo@orbit.ai',
              name: 'Demo User',
              onboarding_completed: true,
              created_at: new Date().toISOString(),
            };
            
            const mockToken = 'demo-jwt-token-' + Date.now();
            
            set({
              user: mockUser,
              token: mockToken,
              isAuthenticated: true,
              isLoading: false,
              error: null,
            });
            
            toast.success('Welcome back to ORBIT!');
          } else {
            // Simulate API call
            await new Promise(resolve => setTimeout(resolve, 1000));
            
            // For demo purposes, accept any credentials
            const mockUser: User = {
              id: 'user-' + Date.now(),
              email: email,
              name: email.split('@')[0],
              onboarding_completed: true,
              created_at: new Date().toISOString(),
            };
            
            const mockToken = 'jwt-token-' + Date.now();
            
            set({
              user: mockUser,
              token: mockToken,
              isAuthenticated: true,
              isLoading: false,
              error: null,
            });
            
            toast.success('Welcome to ORBIT!');
          }
        } catch (error: any) {
          set({
            isLoading: false,
            error: error.message || 'Login failed',
          });
          toast.error('Login failed. Please try again.');
          throw error;
        }
      },

      register: async (email: string, password: string, name: string) => {
        set({ isLoading: true, error: null });
        
        try {
          // Simulate API call
          await new Promise(resolve => setTimeout(resolve, 1500));
          
          const mockUser: User = {
            id: 'user-' + Date.now(),
            email: email,
            name: name,
            onboarding_completed: false, // New users need onboarding
            created_at: new Date().toISOString(),
          };
          
          const mockToken = 'jwt-token-' + Date.now();
          
          set({
            user: mockUser,
            token: mockToken,
            isAuthenticated: true,
            isLoading: false,
            error: null,
          });
          
          toast.success('Account created successfully!');
        } catch (error: any) {
          set({
            isLoading: false,
            error: error.message || 'Registration failed',
          });
          toast.error('Registration failed. Please try again.');
          throw error;
        }
      },

      logout: () => {
        set({
          user: null,
          token: null,
          isAuthenticated: false,
          error: null,
        });
        toast.success('Logged out successfully');
      },

      updateUser: (userData: Partial<User>) => {
        const currentUser = get().user;
        if (currentUser) {
          set({
            user: { ...currentUser, ...userData },
          });
        }
      },

      clearError: () => {
        set({ error: null });
      },
    }),
    {
      name: 'orbit-auth-storage',
      partialize: (state) => ({
        user: state.user,
        token: state.token,
        isAuthenticated: state.isAuthenticated,
      }),
    }
  )
);