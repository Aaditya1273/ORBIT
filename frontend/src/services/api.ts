import axios, { AxiosInstance, AxiosError } from 'axios';

// API Configuration
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api/v1';

// Create axios instance
const apiClient: AxiosInstance = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor - Add auth token
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor - Handle errors
apiClient.interceptors.response.use(
  (response) => response,
  async (error: AxiosError) => {
    if (error.response?.status === 401) {
      // Unauthorized - clear token and redirect to login
      localStorage.removeItem('access_token');
      localStorage.removeItem('user');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// Auth API
export const authApi = {
  register: async (data: { email: string; name: string; password: string }) => {
    const response = await apiClient.post('/auth/register', data);
    if (response.data.access_token) {
      localStorage.setItem('access_token', response.data.access_token);
      localStorage.setItem('user', JSON.stringify(response.data.user));
    }
    return response.data;
  },

  login: async (email: string, password: string) => {
    const formData = new FormData();
    formData.append('username', email); // OAuth2 uses 'username' field
    formData.append('password', password);
    
    const response = await apiClient.post('/auth/login', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    
    if (response.data.access_token) {
      localStorage.setItem('access_token', response.data.access_token);
      localStorage.setItem('user', JSON.stringify(response.data.user));
    }
    return response.data;
  },

  logout: async () => {
    try {
      await apiClient.post('/auth/logout');
    } finally {
      localStorage.removeItem('access_token');
      localStorage.removeItem('user');
    }
  },

  getCurrentUser: async () => {
    const response = await apiClient.get('/auth/me');
    return response.data;
  },

  refreshToken: async () => {
    const response = await apiClient.post('/auth/refresh');
    if (response.data.access_token) {
      localStorage.setItem('access_token', response.data.access_token);
    }
    return response.data;
  },
};

// Dashboard API
export const dashboardApi = {
  getDashboardData: async () => {
    // Mock data for now - will be replaced with real API call
    return {
      user: {
        id: '1',
        name: 'Demo User',
        streak_days: 7,
        total_goals: 5,
        active_goals: 3,
      },
      today_focus: 'Complete workout and finish project milestone',
      energy_level: 'High',
      ai_reliability: {
        interventions_this_week: 12,
        helpful_percentage: 85,
        safety_score: 0.92,
        relevance_score: 0.88,
        accuracy_score: 0.90,
      },
      goals: [
        {
          id: '1',
          title: 'Exercise 3x per week',
          domain: 'health',
          progress: 67,
          next_action: 'Schedule tomorrow\'s workout',
          ai_insight: 'You\'re most consistent on Monday mornings',
        },
        {
          id: '2',
          title: 'Save $500 monthly',
          domain: 'finance',
          progress: 80,
          next_action: 'Review this week\'s spending',
          ai_insight: 'On track to exceed your goal this month',
        },
      ],
      todays_plan: [
        { time: '9:00', action: 'Morning workout' },
        { time: '11:00', action: 'Project work session' },
        { time: '14:00', action: 'Team meeting' },
        { time: '16:00', action: 'Learning time' },
      ],
    };
  },
};

// Goals API
export const goalsApi = {
  getGoals: async (status?: string) => {
    const response = await apiClient.get('/goals', {
      params: { status },
    });
    return response.data;
  },

  getGoal: async (goalId: string) => {
    const response = await apiClient.get(`/goals/${goalId}`);
    return response.data;
  },

  createGoal: async (goalData: any) => {
    const response = await apiClient.post('/goals', goalData);
    return response.data;
  },

  updateGoal: async (goalId: string, goalData: any) => {
    const response = await apiClient.put(`/goals/${goalId}`, goalData);
    return response.data;
  },

  deleteGoal: async (goalId: string) => {
    const response = await apiClient.delete(`/goals/${goalId}`);
    return response.data;
  },

  logProgress: async (goalId: string, progressData: any) => {
    const response = await apiClient.post(`/goals/${goalId}/progress`, progressData);
    return response.data;
  },
};

// Interventions API
export const interventionsApi = {
  generateIntervention: async (data: any) => {
    const response = await apiClient.post('/interventions/generate', data);
    return response.data;
  },

  getIntervention: async (interventionId: string) => {
    const response = await apiClient.get(`/interventions/${interventionId}`);
    return response.data;
  },

  getInterventions: async (userId: string) => {
    const response = await apiClient.get('/interventions', {
      params: { user_id: userId },
    });
    return response.data;
  },

  provideFeedback: async (interventionId: string, feedback: any) => {
    const response = await apiClient.post(`/interventions/${interventionId}/feedback`, feedback);
    return response.data;
  },
};

// Users API
export const usersApi = {
  getUser: async (userId: string) => {
    const response = await apiClient.get(`/users/${userId}`);
    return response.data;
  },

  updateUser: async (userId: string, userData: any) => {
    const response = await apiClient.put(`/users/${userId}`, userData);
    return response.data;
  },

  updatePreferences: async (userId: string, preferences: any) => {
    const response = await apiClient.put(`/users/${userId}/preferences`, preferences);
    return response.data;
  },
};

// Health Check
export const healthApi = {
  check: async () => {
    const response = await apiClient.get('/health');
    return response.data;
  },
};

export default apiClient;
