import React, { useState } from 'react';
import {
  Box,
  Grid,
  Card,
  CardContent,
  Typography,
  ToggleButtonGroup,
  ToggleButton,
  Paper,
  Chip
} from '@mui/material';
import {
  TrendingUp,
  TrendingDown,
  Timeline,
  Speed,
  EmojiEvents
} from '@mui/icons-material';
import {
  LineChart,
  Line,
  BarChart,
  Bar,
  PieChart,
  Pie,
  Cell,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  RadarChart,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  Radar
} from 'recharts';

const Analytics: React.FC = () => {
  const [timeframe, setTimeframe] = useState('week');

  // Mock data
  const progressData = [
    { date: 'Mon', health: 80, finance: 70, productivity: 90, learning: 60, social: 75 },
    { date: 'Tue', health: 85, finance: 75, productivity: 85, learning: 65, social: 80 },
    { date: 'Wed', health: 75, finance: 80, productivity: 95, learning: 70, social: 70 },
    { date: 'Thu', health: 90, finance: 85, productivity: 88, learning: 75, social: 85 },
    { date: 'Fri', health: 88, finance: 90, productivity: 92, learning: 80, social: 90 },
    { date: 'Sat', health: 95, finance: 88, productivity: 70, learning: 85, social: 95 },
    { date: 'Sun', health: 92, finance: 92, productivity: 75, learning: 90, social: 88 },
  ];

  const domainData = [
    { domain: 'Health', value: 85, color: '#4CAF50' },
    { domain: 'Finance', value: 80, color: '#2196F3' },
    { domain: 'Productivity', value: 87, color: '#FF9800' },
    { domain: 'Learning', value: 75, color: '#9C27B0' },
    { domain: 'Social', value: 83, color: '#E91E63' },
  ];

  const radarData = [
    { subject: 'Consistency', A: 85, fullMark: 100 },
    { subject: 'Progress', A: 90, fullMark: 100 },
    { subject: 'Engagement', A: 78, fullMark: 100 },
    { subject: 'AI Helpfulness', A: 92, fullMark: 100 },
    { subject: 'Goal Clarity', A: 88, fullMark: 100 },
  ];

  const stats = [
    { label: 'Weekly Progress', value: '+12%', trend: 'up', icon: <TrendingUp /> },
    { label: 'Goals Completed', value: '8/12', trend: 'up', icon: <EmojiEvents /> },
    { label: 'Avg. Daily Score', value: '85%', trend: 'up', icon: <Speed /> },
    { label: 'Streak Days', value: '14', trend: 'up', icon: <Timeline /> },
  ];

  return (
    <Box>
      {/* Header */}
      <Box sx={{ mb: 4, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <Box>
          <Typography variant="h4" gutterBottom>
            📊 Analytics
          </Typography>
          <Typography variant="body1" color="text.secondary">
            Track your progress and insights across all domains
          </Typography>
        </Box>
        <ToggleButtonGroup
          value={timeframe}
          exclusive
          onChange={(e, newValue) => newValue && setTimeframe(newValue)}
          size="small"
        >
          <ToggleButton value="week">Week</ToggleButton>
          <ToggleButton value="month">Month</ToggleButton>
          <ToggleButton value="year">Year</ToggleButton>
        </ToggleButtonGroup>
      </Box>

      {/* Stats Cards */}
      <Grid container spacing={3} sx={{ mb: 3 }}>
        {stats.map((stat, index) => (
          <Grid item xs={12} sm={6} md={3} key={index}>
            <Card>
              <CardContent>
                <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                  <Box>
                    <Typography variant="body2" color="text.secondary" gutterBottom>
                      {stat.label}
                    </Typography>
                    <Typography variant="h4" fontWeight="bold">
                      {stat.value}
                    </Typography>
                  </Box>
                  <Box
                    sx={{
                      p: 1.5,
                      borderRadius: 2,
                      bgcolor: stat.trend === 'up' ? 'success.light' : 'error.light',
                      color: stat.trend === 'up' ? 'success.dark' : 'error.dark',
                    }}
                  >
                    {stat.icon}
                  </Box>
                </Box>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>

      {/* Charts */}
      <Grid container spacing={3}>
        {/* Progress Over Time */}
        <Grid item xs={12} lg={8}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Progress Over Time
              </Typography>
              <ResponsiveContainer width="100%" height={300}>
                <LineChart data={progressData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="date" />
                  <YAxis />
                  <Tooltip />
                  <Legend />
                  <Line type="monotone" dataKey="health" stroke="#4CAF50" strokeWidth={2} />
                  <Line type="monotone" dataKey="finance" stroke="#2196F3" strokeWidth={2} />
                  <Line type="monotone" dataKey="productivity" stroke="#FF9800" strokeWidth={2} />
                  <Line type="monotone" dataKey="learning" stroke="#9C27B0" strokeWidth={2} />
                  <Line type="monotone" dataKey="social" stroke="#E91E63" strokeWidth={2} />
                </LineChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>
        </Grid>

        {/* Domain Distribution */}
        <Grid item xs={12} lg={4}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Domain Distribution
              </Typography>
              <ResponsiveContainer width="100%" height={300}>
                <PieChart>
                  <Pie
                    data={domainData}
                    cx="50%"
                    cy="50%"
                    labelLine={false}
                    label={(entry) => `${entry.domain}: ${entry.value}%`}
                    outerRadius={80}
                    fill="#8884d8"
                    dataKey="value"
                  >
                    {domainData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={entry.color} />
                    ))}
                  </Pie>
                  <Tooltip />
                </PieChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>
        </Grid>

        {/* Performance Radar */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Performance Metrics
              </Typography>
              <ResponsiveContainer width="100%" height={300}>
                <RadarChart data={radarData}>
                  <PolarGrid />
                  <PolarAngleAxis dataKey="subject" />
                  <PolarRadiusAxis angle={90} domain={[0, 100]} />
                  <Radar
                    name="Your Score"
                    dataKey="A"
                    stroke="#6366f1"
                    fill="#6366f1"
                    fillOpacity={0.6}
                  />
                  <Tooltip />
                </RadarChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>
        </Grid>

        {/* AI Insights */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                🤖 AI Insights
              </Typography>
              <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
                <Paper sx={{ p: 2, bgcolor: 'success.light' }}>
                  <Typography variant="subtitle2" gutterBottom>
                    💪 Strength Detected
                  </Typography>
                  <Typography variant="body2">
                    Your productivity has increased 25% this week. Keep up the momentum!
                  </Typography>
                </Paper>
                <Paper sx={{ p: 2, bgcolor: 'warning.light' }}>
                  <Typography variant="subtitle2" gutterBottom>
                    ⚠️ Area for Improvement
                  </Typography>
                  <Typography variant="body2">
                    Learning goals need more attention. Consider scheduling dedicated time.
                  </Typography>
                </Paper>
                <Paper sx={{ p: 2, bgcolor: 'info.light' }}>
                  <Typography variant="subtitle2" gutterBottom>
                    💡 Recommendation
                  </Typography>
                  <Typography variant="body2">
                    Your best performance time is 9-11 AM. Schedule important tasks then.
                  </Typography>
                </Paper>
              </Box>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  );
};

export default Analytics;