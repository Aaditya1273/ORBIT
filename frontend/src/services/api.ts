import axios, { AxiosInstance } from 'axios';
import toast from 'react-hot-toast';

// Create axios instance with base configuration
const api: AxiosInstance = axios.create({
  baseURL: process.env.REACT_APP_API_URL || 'http://localhost:8000/api/v1',
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add auth token
api.interceptors.request.use(
  (config) => {
    const authStorage = localStorage.getItem('orbit-auth-storage');
    if (authStorage) {
      try {
        const { state } = JSON.parse(authStorage);
        if (state?.token) {
          config.headers.Authorization = `Bearer ${state.token}`;
        }
      } catch (error) {
        console.error('Error parsing auth storage:', error);
      }
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response) {
      // Server responded with error status
      const status = error.response.status;
      const message = error.response.data?.message || error.message;

      switch (status) {
        case 401:
          toast.error('Session expired. Please login again.');
          // Clear auth and redirect to login
          localStorage.removeItem('orbit-auth-storage');
          window.location.href = '/login';
          break;
        case 403:
          toast.error('Access denied');
          break;
        case 404:
          toast.error('Resource not found');
          break;
        case 500:
          toast.error('Server error. Please try again later.');
          break;
        default:
          toast.error(message || 'An error occurred');
      }
    } else if (error.request) {
      // Request made but no response
      toast.error('Network error. Please check your connection.');
    } else {
      // Something else happened
      toast.error('An unexpected error occurred');
    }

    return Promise.reject(error);
  }
);

// API endpoints
export const authApi = {
  login: async (email: string, password: string) => {
    const response = await api.post('/auth/login', { email, password });
    return response.data;
  },

  register: async (email: string, password: string, name: string) => {
    const response = await api.post('/auth/register', { email, password, name });
    return response.data;
  },

  logout: async () => {
    const response = await api.post('/auth/logout');
    return response.data;
  },

  refreshToken: async () => {
    const response = await api.post('/auth/refresh');
    return response.data;
  },
};

export const dashboardApi = {
  getDashboardData: async () => {
    // Mock data for demo - replace with actual API call
    return {
      user: {
        id: 'demo-user-123',
        name: 'Demo User',
        streak_days: 7,
        total_goals: 12,
        active_goals: 8,
      },
      today_focus: 'Complete morning workout and finish project proposal',
      energy_level: 'High',
      ai_reliability: {
        interventions_this_week: 24,
        helpful_percentage: 92,
        safety_score: 0.98,
        relevance_score: 0.94,
        accuracy_score: 0.96,
      },
      goals: [
        {
          id: '1',
          title: 'Exercise 3x per week',
          domain: 'health',
          progress: 67,
          next_action: 'Morning run at 7 AM',
          ai_insight: 'Your consistency has improved 40% this month!',
        },
        {
          id: '2',
          title: 'Save $500 monthly',
          domain: 'finance',
          progress: 80,
          next_action: 'Review spending categories',
          ai_insight: 'You\'re on track to exceed your goal by 15%',
        },
        {
          id: '3',
          title: 'Complete online course',
          domain: 'learning',
          progress: 45,
          next_action: 'Watch Module 5 videos',
          ai_insight: 'Schedule 30min daily for consistent progress',
        },
        {
          id: '4',
          title: 'Finish project proposal',
          domain: 'productivity',
          progress: 90,
          next_action: 'Final review and submit',
          ai_insight: 'Great momentum! You\'re almost there',
        },
      ],
      todays_plan: [
        { time: '07:00', action: 'Morning workout (30 min)' },
        { time: '09:00', action: 'Work on project proposal' },
        { time: '12:00', action: 'Lunch break & meditation' },
        { time: '14:00', action: 'Online course - Module 5' },
        { time: '17:00', action: 'Review daily progress' },
        { time: '19:00', action: 'Social time with friends' },
      ],
    };
  },
};

export const goalsApi = {
  getGoals: async () => {
    const response = await api.get('/goals');
    return response.data;
  },

  getGoal: async (id: string) => {
    const response = await api.get(`/goals/${id}`);
    return response.data;
  },

  createGoal: async (goalData: any) => {
    const response = await api.post('/goals', goalData);
    return response.data;
  },

  updateGoal: async (id: string, goalData: any) => {
    const response = await api.put(`/goals/${id}`, goalData);
    return response.data;
  },

  deleteGoal: async (id: string) => {
    const response = await api.delete(`/goals/${id}`);
    return response.data;
  },

  logProgress: async (id: string, progressData: any) => {
    const response = await api.post(`/goals/${id}/progress`, progressData);
    return response.data;
  },
};

export const interventionsApi = {
  getInterventions: async () => {
    const response = await api.get('/interventions');
    return response.data;
  },

  generateIntervention: async (data: any) => {
    const response = await api.post('/interventions/generate', data);
    return response.data;
  },

  rateIntervention: async (id: string, rating: number, feedback?: string) => {
    const response = await api.post(`/interventions/${id}/rate`, { rating, feedback });
    return response.data;
  },
};

export const analyticsApi = {
  getAnalytics: async (timeframe: string = 'week') => {
    const response = await api.get(`/analytics?timeframe=${timeframe}`);
    return response.data;
  },

  getGoalAnalytics: async (goalId: string) => {
    const response = await api.get(`/analytics/goals/${goalId}`);
    return response.data;
  },

  getDomainAnalytics: async (domain: string) => {
    const response = await api.get(`/analytics/domains/${domain}`);
    return response.data;
  },
};

export const userApi = {
  getProfile: async () => {
    const response = await api.get('/users/me');
    return response.data;
  },

  updateProfile: async (userData: any) => {
    const response = await api.put('/users/me', userData);
    return response.data;
  },

  updatePreferences: async (preferences: any) => {
    const response = await api.put('/users/me/preferences', preferences);
    return response.data;
  },

  completeOnboarding: async (onboardingData: any) => {
    const response = await api.post('/users/me/onboarding', onboardingData);
    return response.data;
  },
};

export default api;