import React, { useState } from 'react';
import {
  Box,
  Grid,
  Card,
  CardContent,
  Typography,
  LinearProgress,
  Chip,
  Button,
  Avatar,
  IconButton,
  Divider,
  List,
  ListItem,
  ListItemText,
  ListItemIcon,
  Paper,
  Alert,
} from '@mui/material';
import {
  TrendingUp,
  Psychology,
  Schedule,
  Notifications,
  CheckCircle,
  Warning,
  Info,
  FitnessCenter,
  AttachMoney,
  Work,
  School,
  People,
  Lightbulb,
  Timeline,
} from '@mui/icons-material';
import { motion } from 'framer-motion';
import { useQuery } from 'react-query';

// Components
import InterventionCard from '../components/dashboard/InterventionCard';
import GoalProgressCard from '../components/dashboard/GoalProgressCard';
import AIReliabilityCard from '../components/dashboard/AIReliabilityCard';
import TodaysPlanCard from '../components/dashboard/TodaysPlanCard';
import QuickActionsCard from '../components/dashboard/QuickActionsCard';

// Services
import { dashboardService } from '../services/dashboardService';
import { interventionService } from '../services/interventionService';

// Types
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

const Dashboard: React.FC = () => {
  const [selectedGoal, setSelectedGoal] = useState<string | null>(null);

  // Fetch dashboard data
  const { data: dashboardData, isLoading, error } = useQuery<DashboardData>(
    'dashboard',
    dashboardService.getDashboardData,
    {
      refetchInterval: 5 * 60 * 1000, // Refetch every 5 minutes
    }
  );

  // Fetch recent interventions
  const { data: recentInterventions } = useQuery(
    'recent-interventions',
    () => interventionService.getRecentInterventions(5),
    {
      refetchInterval: 2 * 60 * 1000, // Refetch every 2 minutes
    }
  );

  if (isLoading) {
    return (
      <Box sx={{ p: 3 }}>
        <Typography variant="h4" gutterBottom>
          Loading your dashboard...
        </Typography>
        <LinearProgress />
      </Box>
    );
  }

  if (error) {
    return (
      <Box sx={{ p: 3 }}>
        <Alert severity="error">
          Failed to load dashboard data. Please try refreshing the page.
        </Alert>
      </Box>
    );
  }

  const getDomainIcon = (domain: string) => {
    switch (domain) {
      case 'health': return <FitnessCenter />;
      case 'finance': return <AttachMoney />;
      case 'productivity': return <Work />;
      case 'learning': return <School />;
      case 'social': return <People />;
      default: return <TrendingUp />;
    }
  };

  const getDomainColor = (domain: string) => {
    switch (domain) {
      case 'health': return '#10b981';
      case 'finance': return '#f59e0b';
      case 'productivity': return '#6366f1';
      case 'learning': return '#8b5cf6';
      case 'social': return '#ec4899';
      default: return '#6b7280';
    }
  };

  return (
    <Box sx={{ maxWidth: 1400, mx: 'auto' }}>
      {/* Header Section */}
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
      >
        <Box sx={{ mb: 4 }}>
          <Typography variant="h3" component="h1" gutterBottom sx={{ fontWeight: 700 }}>
            Good morning, {dashboardData?.user.name}! 🌅
          </Typography>
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 3, mb: 2 }}>
            <Chip
              icon={<TrendingUp />}
              label={`${dashboardData?.user.streak_days} day streak`}
              color="success"
              variant="outlined"
            />
            <Chip
              icon={<Psychology />}
              label={`Today's focus: ${dashboardData?.today_focus}`}
              color="primary"
              variant="outlined"
            />
            <Chip
              label={`Energy: ${dashboardData?.energy_level}`}
              color="info"
              variant="outlined"
            />
          </Box>
        </Box>
      </motion.div>

      <Grid container spacing={3}>
        {/* Left Column */}
        <Grid item xs={12} lg={8}>
          {/* AI Reliability Card */}
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.5, delay: 0.1 }}
          >
            <AIReliabilityCard data={dashboardData?.ai_reliability} />
          </motion.div>

          {/* Goals Overview */}
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.5, delay: 0.2 }}
          >
            <Card sx={{ mt: 3 }}>
              <CardContent>
                <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', mb: 3 }}>
                  <Typography variant="h5" component="h2" sx={{ fontWeight: 600 }}>
                    📊 Active Goals
                  </Typography>
                  <Button variant="outlined" size="small">
                    View All
                  </Button>
                </Box>
                
                <Grid container spacing={2}>
                  {dashboardData?.goals.map((goal, index) => (
                    <Grid item xs={12} md={6} key={goal.id}>
                      <motion.div
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ duration: 0.3, delay: index * 0.1 }}
                      >
                        <GoalProgressCard
                          goal={goal}
                          onSelect={() => setSelectedGoal(goal.id)}
                          isSelected={selectedGoal === goal.id}
                        />
                      </motion.div>
                    </Grid>
                  ))}
                </Grid>
              </CardContent>
            </Card>
          </motion.div>

          {/* Recent Interventions */}
          {recentInterventions && recentInterventions.length > 0 && (
            <motion.div
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.5, delay: 0.3 }}
            >
              <Card sx={{ mt: 3 }}>
                <CardContent>
                  <Typography variant="h5" component="h2" sx={{ fontWeight: 600, mb: 3 }}>
                    🤖 Recent AI Interventions
                  </Typography>
                  
                  <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
                    {recentInterventions.slice(0, 3).map((intervention: any, index: number) => (
                      <motion.div
                        key={intervention.id}
                        initial={{ opacity: 0, x: 20 }}
                        animate={{ opacity: 1, x: 0 }}
                        transition={{ duration: 0.3, delay: index * 0.1 }}
                      >
                        <InterventionCard intervention={intervention} />
                      </motion.div>
                    ))}
                  </Box>
                </CardContent>
              </Card>
            </motion.div>
          )}
        </Grid>

        {/* Right Column */}
        <Grid item xs={12} lg={4}>
          {/* Today's Plan */}
          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.5, delay: 0.1 }}
          >
            <TodaysPlanCard plan={dashboardData?.todays_plan || []} />
          </motion.div>

          {/* Quick Actions */}
          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.5, delay: 0.2 }}
          >
            <QuickActionsCard />
          </motion.div>

          {/* Insights & Tips */}
          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.5, delay: 0.3 }}
          >
            <Card sx={{ mt: 3 }}>
              <CardContent>
                <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                  <Lightbulb sx={{ mr: 1, color: 'warning.main' }} />
                  <Typography variant="h6" component="h3" sx={{ fontWeight: 600 }}>
                    AI Insights
                  </Typography>
                </Box>
                
                <List dense>
                  <ListItem>
                    <ListItemIcon>
                      <Info color="info" />
                    </ListItemIcon>
                    <ListItemText
                      primary="Peak Productivity"
                      secondary="You're most productive between 9-11 AM. Schedule important tasks then."
                    />
                  </ListItem>
                  
                  <ListItem>
                    <ListItemIcon>
                      <CheckCircle color="success" />
                    </ListItemIcon>
                    <ListItemText
                      primary="Great Progress"
                      secondary="Your consistency has improved 23% this week!"
                    />
                  </ListItem>
                  
                  <ListItem>
                    <ListItemIcon>
                      <Warning color="warning" />
                    </ListItemIcon>
                    <ListItemText
                      primary="Attention Needed"
                      secondary="Consider meal prep to support your health goals."
                    />
                  </ListItem>
                </List>
              </CardContent>
            </Card>
          </motion.div>

          {/* Weekly Stats */}
          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.5, delay: 0.4 }}
          >
            <Card sx={{ mt: 3 }}>
              <CardContent>
                <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                  <Timeline sx={{ mr: 1, color: 'primary.main' }} />
                  <Typography variant="h6" component="h3" sx={{ fontWeight: 600 }}>
                    This Week
                  </Typography>
                </Box>
                
                <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 2 }}>
                  <Typography variant="body2" color="text.secondary">
                    Goal Completion
                  </Typography>
                  <Typography variant="body2" sx={{ fontWeight: 600 }}>
                    78%
                  </Typography>
                </Box>
                <LinearProgress 
                  variant="determinate" 
                  value={78} 
                  sx={{ mb: 2, height: 6, borderRadius: 3 }}
                />
                
                <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 2 }}>
                  <Typography variant="body2" color="text.secondary">
                    AI Helpfulness
                  </Typography>
                  <Typography variant="body2" sx={{ fontWeight: 600 }}>
                    89%
                  </Typography>
                </Box>
                <LinearProgress 
                  variant="determinate" 
                  value={89} 
                  color="success"
                  sx={{ mb: 2, height: 6, borderRadius: 3 }}
                />
                
                <Box sx={{ display: 'flex', justifyContent: 'space-between' }}>
                  <Typography variant="body2" color="text.secondary">
                    Streak Maintenance
                  </Typography>
                  <Typography variant="body2" sx={{ fontWeight: 600 }}>
                    100%
                  </Typography>
                </Box>
                <LinearProgress 
                  variant="determinate" 
                  value={100} 
                  color="info"
                  sx={{ height: 6, borderRadius: 3 }}
                />
              </CardContent>
            </Card>
          </motion.div>
        </Grid>
      </Grid>
    </Box>
  );
};

export default Dashboard;