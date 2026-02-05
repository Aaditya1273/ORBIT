import { create } from 'zustand';
import { persist } from 'zustand/middleware';

interface ThemeState {
  isDarkMode: boolean;
  primaryColor: string;
  fontSize: 'small' | 'medium' | 'large';
  compactMode: boolean;
  
  // Actions
  toggleDarkMode: () => void;
  setPrimaryColor: (color: string) => void;
  setFontSize: (size: 'small' | 'medium' | 'large') => void;
  setCompactMode: (compact: boolean) => void;
  resetTheme: () => void;
}

const defaultTheme = {
  isDarkMode: false,
  primaryColor: '#6366f1', // Indigo
  fontSize: 'medium' as const,
  compactMode: false,
};

export const useThemeStore = create<ThemeState>()(
  persist(
    (set, get) => ({
      ...defaultTheme,

      toggleDarkMode: () => {
        set((state) => ({ isDarkMode: !state.isDarkMode }));
      },

      setPrimaryColor: (color: string) => {
        set({ primaryColor: color });
      },

      setFontSize: (size: 'small' | 'medium' | 'large') => {
        set({ fontSize: size });
      },

      setCompactMode: (compact: boolean) => {
        set({ compactMode: compact });
      },

      resetTheme: () => {
        set(defaultTheme);
      },
    }),
    {
      name: 'orbit-theme-storage',
    }
  )
);

// Predefined color options
export const colorOptions = [
  { name: 'Indigo', value: '#6366f1' },
  { name: 'Blue', value: '#2196F3' },
  { name: 'Purple', value: '#9C27B0' },
  { name: 'Green', value: '#4CAF50' },
  { name: 'Orange', value: '#FF9800' },
  { name: 'Red', value: '#F44336' },
  { name: 'Teal', value: '#009688' },
  { name: 'Pink', value: '#E91E63' },
];

// Helper hook for theme values
export const useTheme = () => {
  const {
    isDarkMode,
    primaryColor,
    fontSize,
    compactMode,
    toggleDarkMode,
    setPrimaryColor,
    setFontSize,
    setCompactMode,
    resetTheme,
  } = useThemeStore();

  return {
    isDarkMode,
    primaryColor,
    fontSize,
    compactMode,
    toggleDarkMode,
    setPrimaryColor,
    setFontSize,
    setCompactMode,
    resetTheme,
  };
};