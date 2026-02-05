import axios, { AxiosInstance, AxiosResponse } from 'axios';
import toast from 'react-hot-toast';

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

// Request interceptor for auth
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('orbit_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor for error handling
apiClient.interceptors.response.use(
  (response: AxiosResponse) => {
    return response;
  },
  (error) => {
    if (error.response?.status === 401) {
      // Unauthorized - clear token and redirect to login
      localStorage.removeItem('orbit_token');
      window.location.href = '/login';
    } else if (error.response?.status >= 500) {
      toast.error('Server error. Please try again later.');
    } else if (error.response?.data?.message) {
      toast.error(error.response.data.message);
    } else if (error.message) {
      toast.error(error.message);
    }
    
    return Promise.reject(error);
  }
);

// Types
export interface User {
  id: string;
  name: string;
  email: string;
  timezone: string;
  subscription_tier: string;
  onboarding_completed: boolean;
  created_at: string;
  last_active: string;
}

export interface Goal {
  id: string;
  title: string;
  description?: string;
  domain: 'health' | 'finance' | 'productivity' | 'learning' | 'social';
  status: 'active' | 'paused' | 'completed' | 'abandoned';
  progress: number;
  created_date: string;
  target_date?: string;
  last_updated: string;
  priority: number;
  target_value?: string | number;
  current_value?: string | number;
  unit?: string;
  ai_insights: string[];
  next_actions: string[];
}

export interface Intervention {
  intervention_id: string;
  content: string;
  reasoning?: string;
  confidence: number;
  supervisor_evaluation?: any;
  metadata?: any;
  execution_time_ms: number;
}

export interface InterventionRequest {
  user_input: string;
  session_id: string;
  trigger_type: 'scheduled' | 'reactive' | 'predictive' | 'general';
  domain: 'health' | 'finance' | 'productivity' | 'learning' | 'social';
  urgency: 'low' | 'medium' | 'high' | 'critical';
  current_goals: any[];
  user_state: any;
  recent_history: any[];
  external_context?: any;
}

export interface InterventionFeedback {
  complied: boolean;
  rating: number;
  feedback_text?: string;
  completion_time_minutes?: number;
  difficulty_rating?: number;
}

export interface DashboardData {
  user: {
    id: string;
    name: string;
    streak_days: number;
    total_goals: number;
    active_goals: number;
  };
  today_focus: string;
  energy_level: string;
  ai_reliability: {
    interventions_this_week: number;
    helpful_percentage: number;
    safety_score: number;
    relevance_score: number;
    accuracy_score: number;
  };
  goals: Array<{
    id: string;
    title: string;
    domain: string;
    progress: number;
    next_action: string;
    ai_insight: string;
  }>;
  todays_plan: Array<{
    time: string;
    action: string;
  }>;
}

export interface UserPatterns {
  user_id: string;
  analysis_timestamp: string;
  confidence: number;
  insights: Array<{
    type: string;
    insight: string;
    confidence: number;
    actionable: boolean;
  }>;
  recommendations: string[];
  temporal_patterns: any;
  compliance_patterns: any;
  energy_patterns: any;
}

export interface AnalyticsData {
  period: {
    start_date: string;
    end_date: string;
  };
  metrics: {
    goal_completion_rate: number;
    intervention_compliance: number;
    average_daily_progress: number;
  };
  trends: {
    goal_completion: string;
    engagement: string;
  };
  insights: string[];
}

// API Services
export const authApi = {
  login: async (email: string, password: string): Promise<{ token: string; user: User }> => {
    const response = await apiClient.post('/auth/login', { email, password });
    return response.data;
  },

  register: async (userData: {
    name: string;
    email: string;
    password: string;
  }): Promise<{ token: string; user: User }> => {
    const response = await apiClient.post('/auth/register', userData);
    return response.data;
  },

  logout: async (): Promise<void> => {
    await apiClient.post('/auth/logout');
    localStorage.removeItem('orbit_token');
  },

  refreshToken: async (): Promise<{ token: string }> => {
    const response = await apiClient.post('/auth/refresh');
    return response.data;
  },

  getCurrentUser: async (): Promise<User> => {
    const response = await apiClient.get('/auth/me');
    return response.data;
  },
};

export const dashboardApi = {
  getDashboardData: async (): Promise<DashboardData> => {
    const response = await apiClient.get('/dashboard');
    return response.data;
  },
};

export const goalsApi = {
  getGoals: async (status?: string): Promise<Goal[]> => {
    const params = status ? { status } : {};
    const response = await apiClient.get('/goals', { params });
    return response.data;
  },

  getGoal: async (goalId: string): Promise<Goal> => {
    const response = await apiClient.get(`/goals/${goalId}`);
    return response.data;
  },

  createGoal: async (goalData: {
    title: string;
    description?: string;
    domain: string;
    target_date?: string;
    priority?: number;
    target_value?: string | number;
    current_value?: string | number;
    unit?: string;
  }): Promise<Goal> => {
    const response = await apiClient.post('/goals', goalData);
    return response.data;
  },

  updateGoal: async (goalId: string, updates: Partial<Goal>): Promise<Goal> => {
    const response = await apiClient.patch(`/goals/${goalId}`, updates);
    return response.data;
  },

  deleteGoal: async (goalId: string): Promise<void> => {
    await apiClient.delete(`/goals/${goalId}`);
  },

  updateProgress: async (goalId: string, progress: number, notes?: string): Promise<Goal> => {
    const response = await apiClient.post(`/goals/${goalId}/progress`, {
      progress,
      notes,
    });
    return response.data;
  },
};

export const interventionsApi = {
  generateIntervention: async (request: InterventionRequest): Promise<Intervention> => {
    const response = await apiClient.post('/interventions/generate', request);
    return response.data;
  },

  submitFeedback: async (
    interventionId: string,
    feedback: InterventionFeedback
  ): Promise<{ status: string; message: string }> => {
    const response = await apiClient.post(`/interventions/${interventionId}/feedback`, feedback);
    return response.data;
  },

  getInterventionHistory: async (limit?: number): Promise<Intervention[]> => {
    const params = limit ? { limit } : {};
    const response = await apiClient.get('/interventions/history', { params });
    return response.data;
  },
};

export const analyticsApi = {
  getUserPatterns: async (): Promise<UserPatterns> => {
    const response = await apiClient.get('/users/me/patterns');
    return response.data;
  },

  getAnalytics: async (
    startDate: string,
    endDate: string,
    metrics?: string[],
    granularity?: string
  ): Promise<AnalyticsData> => {
    const response = await apiClient.post('/analytics', {
      start_date: startDate,
      end_date: endDate,
      metrics: metrics || [],
      granularity: granularity || 'daily',
    });
    return response.data;
  },

  getGoalAnalytics: async (goalId: string): Promise<any> => {
    const response = await apiClient.get(`/analytics/goals/${goalId}`);
    return response.data;
  },
};

export const integrationsApi = {
  getIntegrations: async (): Promise<any[]> => {
    const response = await apiClient.get('/integrations');
    return response.data;
  },

  connectIntegration: async (integrationType: string, credentials: any): Promise<any> => {
    const response = await apiClient.post('/integrations/connect', {
      integration_type: integrationType,
      credentials,
    });
    return response.data;
  },

  disconnectIntegration: async (integrationId: string): Promise<void> => {
    await apiClient.delete(`/integrations/${integrationId}`);
  },

  syncIntegration: async (integrationId: string): Promise<any> => {
    const response = await apiClient.post(`/integrations/${integrationId}/sync`);
    return response.data;
  },
};

export const settingsApi = {
  updateProfile: async (updates: Partial<User>): Promise<User> => {
    const response = await apiClient.patch('/users/me', updates);
    return response.data;
  },

  updatePreferences: async (preferences: any): Promise<any> => {
    const response = await apiClient.patch('/users/me/preferences', preferences);
    return response.data;
  },

  updateNotificationSettings: async (settings: any): Promise<any> => {
    const response = await apiClient.patch('/users/me/notifications', settings);
    return response.data;
  },

  changePassword: async (currentPassword: string, newPassword: string): Promise<void> => {
    await apiClient.post('/users/me/change-password', {
      current_password: currentPassword,
      new_password: newPassword,
    });
  },

  deleteAccount: async (password: string): Promise<void> => {
    await apiClient.delete('/users/me', {
      data: { password },
    });
  },

  exportData: async (): Promise<any> => {
    const response = await apiClient.get('/users/me/export');
    return response.data;
  },
};

// Health check
export const healthApi = {
  check: async (): Promise<any> => {
    const response = await apiClient.get('/health');
    return response.data;
  },
};

// Utility functions
export const handleApiError = (error: any): string => {
  if (error.response?.data?.message) {
    return error.response.data.message;
  } else if (error.message) {
    return error.message;
  } else {
    return 'An unexpected error occurred';
  }
};

export const isApiError = (error: any): boolean => {
  return error.response !== undefined;
};

// Export the configured axios instance for custom requests
export { apiClient };

export default {
  auth: authApi,
  dashboard: dashboardApi,
  goals: goalsApi,
  interventions: interventionsApi,
  analytics: analyticsApi,
  integrations: integrationsApi,
  settings: settingsApi,
  health: healthApi,
};