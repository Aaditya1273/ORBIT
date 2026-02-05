import React, { useState, useEffect } from 'react';
import {
  Box,
  Grid,
  Card,
  CardContent,
  Typography,
  LinearProgress,
  Chip,
  Avatar,
  IconButton,
  Button,
  Alert,
  Skeleton,
  Divider,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  Paper
} from '@mui/material';
import {
  TrendingUp,
  Psychology,
  Schedule,
  Notifications,
  CheckCircle,
  Warning,
  Info,
  Star,
  Timeline,
  Speed,
  Security,
  Accuracy,
  EmojiEvents,
  FitnessCenter,
  AttachMoney,
  Work,
  School,
  People
} from '@mui/icons-material';
import { useQuery } from 'react-query';
import { motion } from 'framer-motion';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';
import toast from 'react-hot-toast';

import { dashboardApi } from '../services/api';
import { useAuthStore } from '../stores/authStore';

interface DashboardData {
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

const domainIcons = {
  health: FitnessCenter,
  finance: AttachMoney,
  productivity: Work,
  learning: School,
  social: People
};

const domainColors = {
  health: '#4CAF50',
  finance: '#2196F3',
  productivity: '#FF9800',
  learning: '#9C27B0',
  social: '#E91E63'
};

const Dashboard: React.FC = () => {
  const { user } = useAuthStore();
  const [selectedTimeframe, setSelectedTimeframe] = useState('week');

  const { data: dashboardData, isLoading, error } = useQuery<DashboardData>(
    'dashboard',
    dashboardApi.getDashboardData,
    {
      refetchInterval: 30000, // Refresh every 30 seconds
      onError: (error) => {
        toast.error('Failed to load dashboard data');
        console.error('Dashboard error:', error);
      }
    }
  );

  if (isLoading) {
    return <DashboardSkeleton />;
  }

  if (error) {
    return (
      <Box sx={{ p: 3 }}>
        <Alert severity="error">
          Failed to load dashboard. Please try refreshing the page.
        </Alert>
      </Box>
    );
  }

  if (!dashboardData) {
    return null;
  }

  return (
    <Box sx={{ p: 3 }}>
      {/* Welcome Header */}
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
      >
        <Box sx={{ mb: 4 }}>
          <Typography variant="h4" gutterBottom>
            Good {getTimeOfDay()}, {dashboardData.user.name}! 👋
          </Typography>
          <Typography variant="h6" color="text.secondary" gutterBottom>
            🎯 Today's Focus: {dashboardData.today_focus}
          </Typography>
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, mt: 2 }}>
            <Chip
              icon={<EmojiEvents />}
              label={`${dashboardData.user.streak_days} day streak`}
              color="primary"
              variant="outlined"
            />
            <Chip
              label={`⚡ Energy: ${dashboardData.energy_level}`}
              color="secondary"
              variant="outlined"
            />
            <Chip
              label={`${dashboardData.user.active_goals}/${dashboardData.user.total_goals} active goals`}
              color="info"
              variant="outlined"
            />
          </Box>
        </Box>
      </motion.div>

      <Grid container spacing={3}>
        {/* AI Reliability Dashboard */}
        <Grid item xs={12} lg={4}>
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.5, delay: 0.1 }}
          >
            <Card sx={{ height: '100%' }}>
              <CardContent>
                <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                  <Psychology color="primary" sx={{ mr: 1 }} />
                  <Typography variant="h6">AI Reliability</Typography>
                </Box>
                
                <Typography variant="body2" color="text.secondary" gutterBottom>
                  This week: {dashboardData.ai_reliability.interventions_this_week} interventions | {dashboardData.ai_reliability.helpful_percentage}% helpful
                </Typography>

                <Box sx={{ mt: 3 }}>
                  <ReliabilityMetric
                    icon={<Security />}
                    label="Safety Score"
                    value={dashboardData.ai_reliability.safety_score}
                    color="#4CAF50"
                  />
                  <ReliabilityMetric
                    icon={<TrendingUp />}
                    label="Relevance Score"
                    value={dashboardData.ai_reliability.relevance_score}
                    color="#2196F3"
                  />
                  <ReliabilityMetric
                    icon={<Accuracy />}
                    label="Accuracy Score"
                    value={dashboardData.ai_reliability.accuracy_score}
                    color="#FF9800"
                  />
                </Box>

                <Button
                  variant="outlined"
                  size="small"
                  sx={{ mt: 2 }}
                  onClick={() => toast.info('Detailed traces coming soon!')}
                >
                  View Detailed Traces →
                </Button>
              </CardContent>
            </Card>
          </motion.div>
        </Grid>

        {/* Active Goals */}
        <Grid item xs={12} lg={8}>
          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.5, delay: 0.2 }}
          >
            <Card sx={{ height: '100%' }}>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  📊 Active Goals
                </Typography>
                
                <Grid container spacing={2}>
                  {dashboardData.goals.map((goal, index) => (
                    <Grid item xs={12} md={6} key={goal.id}>
                      <motion.div
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ duration: 0.3, delay: index * 0.1 }}
                      >
                        <GoalCard goal={goal} />
                      </motion.div>
                    </Grid>
                  ))}
                </Grid>
              </CardContent>
            </Card>
          </motion.div>
        </Grid>

        {/* Today's Plan */}
        <Grid item xs={12} md={6}>
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.3 }}
          >
            <Card sx={{ height: '100%' }}>
              <CardContent>
                <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                  <Schedule color="primary" sx={{ mr: 1 }} />
                  <Typography variant="h6">Today's Plan</Typography>
                </Box>
                
                <Typography variant="body2" color="text.secondary" gutterBottom>
                  AI-generated, personalized schedule
                </Typography>

                <List dense>
                  {dashboardData.todays_plan.map((item, index) => (
                    <ListItem key={index} sx={{ px: 0 }}>
                      <ListItemIcon sx={{ minWidth: 40 }}>
                        <Typography variant="body2" color="primary" fontWeight="bold">
                          {item.time}
                        </Typography>
                      </ListItemIcon>
                      <ListItemText
                        primary={item.action}
                        sx={{ ml: 1 }}
                      />
                    </ListItem>
                  ))}
                </List>
              </CardContent>
            </Card>
          </motion.div>
        </Grid>

        {/* Quick Actions */}
        <Grid item xs={12} md={6}>
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.4 }}
          >
            <Card sx={{ height: '100%' }}>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  ⚡ Quick Actions
                </Typography>
                
                <Grid container spacing={2}>
                  <Grid item xs={6}>
                    <Button
                      variant="outlined"
                      fullWidth
                      startIcon={<CheckCircle />}
                      onClick={() => toast.success('Goal progress updated!')}
                    >
                      Log Progress
                    </Button>
                  </Grid>
                  <Grid item xs={6}>
                    <Button
                      variant="outlined"
                      fullWidth
                      startIcon={<Psychology />}
                      onClick={() => toast.info('AI intervention requested')}
                    >
                      Get AI Help
                    </Button>
                  </Grid>
                  <Grid item xs={6}>
                    <Button
                      variant="outlined"
                      fullWidth
                      startIcon={<Timeline />}
                      onClick={() => toast.info('Analytics coming soon!')}
                    >
                      View Analytics
                    </Button>
                  </Grid>
                  <Grid item xs={6}>
                    <Button
                      variant="outlined"
                      fullWidth
                      startIcon={<Star />}
                      onClick={() => toast.info('New goal wizard coming soon!')}
                    >
                      New Goal
                    </Button>
                  </Grid>
                </Grid>

                <Divider sx={{ my: 2 }} />

                <Typography variant="subtitle2" gutterBottom>
                  Recent Self-Corrections:
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  • Prevented overspending alert false alarm
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  • Adjusted workout after detecting fatigue
                </Typography>
              </CardContent>
            </Card>
          </motion.div>
        </Grid>
      </Grid>
    </Box>
  );
};

// Helper Components
const ReliabilityMetric: React.FC<{
  icon: React.ReactNode;
  label: string;
  value: number;
  color: string;
}> = ({ icon, label, value, color }) => (
  <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
    <Box sx={{ color, mr: 1 }}>{icon}</Box>
    <Box sx={{ flexGrow: 1 }}>
      <Typography variant="body2" color="text.secondary">
        {label}
      </Typography>
      <Box sx={{ display: 'flex', alignItems: 'center', mt: 0.5 }}>
        <LinearProgress
          variant="determinate"
          value={value * 100}
          sx={{
            flexGrow: 1,
            mr: 1,
            height: 6,
            borderRadius: 3,
            '& .MuiLinearProgress-bar': {
              backgroundColor: color
            }
          }}
        />
        <Typography variant="body2" fontWeight="bold">
          {(value * 100).toFixed(0)}%
        </Typography>
      </Box>
    </Box>
  </Box>
);

const GoalCard: React.FC<{ goal: any }> = ({ goal }) => {
  const DomainIcon = domainIcons[goal.domain as keyof typeof domainIcons] || Work;
  const domainColor = domainColors[goal.domain as keyof typeof domainColors] || '#666';

  return (
    <Paper
      elevation={1}
      sx={{
        p: 2,
        borderLeft: `4px solid ${domainColor}`,
        '&:hover': {
          elevation: 3,
          transform: 'translateY(-2px)',
          transition: 'all 0.2s ease-in-out'
        }
      }}
    >
      <Box sx={{ display: 'flex', alignItems: 'flex-start', mb: 1 }}>
        <Avatar
          sx={{
            bgcolor: domainColor,
            width: 32,
            height: 32,
            mr: 1.5
          }}
        >
          <DomainIcon sx={{ fontSize: 18 }} />
        </Avatar>
        <Box sx={{ flexGrow: 1 }}>
          <Typography variant="subtitle2" fontWeight="bold">
            {goal.title}
          </Typography>
          <Typography variant="caption" color="text.secondary">
            {goal.domain.toUpperCase()}
          </Typography>
        </Box>
        <Typography variant="h6" color="primary" fontWeight="bold">
          {goal.progress}%
        </Typography>
      </Box>

      <LinearProgress
        variant="determinate"
        value={goal.progress}
        sx={{
          mb: 1,
          height: 6,
          borderRadius: 3,
          '& .MuiLinearProgress-bar': {
            backgroundColor: domainColor
          }
        }}
      />

      <Typography variant="body2" gutterBottom>
        <strong>Next:</strong> {goal.next_action}
      </Typography>

      <Typography variant="body2" color="text.secondary" sx={{ fontStyle: 'italic' }}>
        💡 {goal.ai_insight}
      </Typography>
    </Paper>
  );
};

const DashboardSkeleton: React.FC = () => (
  <Box sx={{ p: 3 }}>
    <Skeleton variant="text" width="60%" height={40} />
    <Skeleton variant="text" width="40%" height={30} sx={{ mb: 3 }} />
    
    <Grid container spacing={3}>
      <Grid item xs={12} md={4}>
        <Skeleton variant="rectangular" height={300} />
      </Grid>
      <Grid item xs={12} md={8}>
        <Skeleton variant="rectangular" height={300} />
      </Grid>
      <Grid item xs={12} md={6}>
        <Skeleton variant="rectangular" height={400} />
      </Grid>
      <Grid item xs={12} md={6}>
        <Skeleton variant="rectangular" height={400} />
      </Grid>
    </Grid>
  </Box>
);

// Helper Functions
const getTimeOfDay = (): string => {
  const hour = new Date().getHours();
  if (hour < 12) return 'morning';
  if (hour < 17) return 'afternoon';
  return 'evening';
};

export default Dashboard;