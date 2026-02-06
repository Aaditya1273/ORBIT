import React, { useState } from 'react';
import {
  Box,
  Grid,
  Card,
  CardContent,
  Typography,
  Button,
  Chip,
  LinearProgress,
  IconButton,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  MenuItem,
  Fab,
  Avatar,
  Paper,
  Tabs,
  Tab
} from '@mui/material';
import {
  Add,
  Edit,
  Delete,
  TrendingUp,
  CheckCircle,
  FitnessCenter,
  AttachMoney,
  Work,
  School,
  People
} from '@mui/icons-material';
import { motion } from 'framer-motion';
import toast from 'react-hot-toast';

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

const Goals: React.FC = () => {
  const [selectedTab, setSelectedTab] = useState(0);
  const [openDialog, setOpenDialog] = useState(false);
  const [newGoal, setNewGoal] = useState({
    title: '',
    description: '',
    domain: 'health',
    target_value: '',
    deadline: '',
  });

  // Mock goals data
  const mockGoals = [
    {
      id: '1',
      title: 'Exercise 3x per week',
      description: 'Maintain consistent workout routine',
      domain: 'health',
      progress: 67,
      target_value: '12 workouts',
      current_value: '8 workouts',
      deadline: '2026-03-01',
      status: 'active',
    },
    {
      id: '2',
      title: 'Save $500 monthly',
      description: 'Build emergency fund',
      domain: 'finance',
      progress: 80,
      target_value: '$500',
      current_value: '$400',
      deadline: '2026-02-28',
      status: 'active',
    },
    {
      id: '3',
      title: 'Complete online course',
      description: 'Finish React Advanced course',
      domain: 'learning',
      progress: 45,
      target_value: '100%',
      current_value: '45%',
      deadline: '2026-04-15',
      status: 'active',
    },
  ];

  const handleCreateGoal = () => {
    toast.success('Goal created successfully!');
    setOpenDialog(false);
    setNewGoal({
      title: '',
      description: '',
      domain: 'health',
      target_value: '',
      deadline: '',
    });
  };

  const filteredGoals = selectedTab === 0 
    ? mockGoals 
    : mockGoals.filter(g => g.domain === ['health', 'finance', 'productivity', 'learning', 'social'][selectedTab - 1]);

  return (
    <Box>
      {/* Header */}
      <Box sx={{ mb: 4, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <Box>
          <Typography variant="h4" gutterBottom>
            🎯 My Goals
          </Typography>
          <Typography variant="body1" color="text.secondary">
            Track and achieve your life goals with AI-powered insights
          </Typography>
        </Box>
        <Button
          variant="contained"
          startIcon={<Add />}
          onClick={() => setOpenDialog(true)}
          sx={{ height: 'fit-content' }}
        >
          New Goal
        </Button>
      </Box>

      {/* Tabs */}
      <Paper sx={{ mb: 3 }}>
        <Tabs
          value={selectedTab}
          onChange={(e, newValue) => setSelectedTab(newValue)}
          variant="scrollable"
          scrollButtons="auto"
        >
          <Tab label="All Goals" />
          <Tab icon={<FitnessCenter />} label="Health" />
          <Tab icon={<AttachMoney />} label="Finance" />
          <Tab icon={<Work />} label="Productivity" />
          <Tab icon={<School />} label="Learning" />
          <Tab icon={<People />} label="Social" />
        </Tabs>
      </Paper>

      {/* Goals Grid */}
      <Grid container spacing={3}>
        {filteredGoals.map((goal, index) => (
          <Grid item xs={12} md={6} lg={4} key={goal.id}>
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

      {/* Create Goal Dialog */}
      <Dialog open={openDialog} onClose={() => setOpenDialog(false)} maxWidth="sm" fullWidth>
        <DialogTitle>Create New Goal</DialogTitle>
        <DialogContent>
          <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2, mt: 2 }}>
            <TextField
              label="Goal Title"
              fullWidth
              value={newGoal.title}
              onChange={(e) => setNewGoal({ ...newGoal, title: e.target.value })}
            />
            <TextField
              label="Description"
              fullWidth
              multiline
              rows={3}
              value={newGoal.description}
              onChange={(e) => setNewGoal({ ...newGoal, description: e.target.value })}
            />
            <TextField
              select
              label="Domain"
              fullWidth
              value={newGoal.domain}
              onChange={(e) => setNewGoal({ ...newGoal, domain: e.target.value })}
            >
              <MenuItem value="health">Health</MenuItem>
              <MenuItem value="finance">Finance</MenuItem>
              <MenuItem value="productivity">Productivity</MenuItem>
              <MenuItem value="learning">Learning</MenuItem>
              <MenuItem value="social">Social</MenuItem>
            </TextField>
            <TextField
              label="Target Value"
              fullWidth
              value={newGoal.target_value}
              onChange={(e) => setNewGoal({ ...newGoal, target_value: e.target.value })}
              placeholder="e.g., 10 workouts, $1000, 100%"
            />
            <TextField
              label="Deadline"
              type="date"
              fullWidth
              value={newGoal.deadline}
              onChange={(e) => setNewGoal({ ...newGoal, deadline: e.target.value })}
              InputLabelProps={{ shrink: true }}
            />
          </Box>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setOpenDialog(false)}>Cancel</Button>
          <Button variant="contained" onClick={handleCreateGoal}>
            Create Goal
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

const GoalCard: React.FC<{ goal: any }> = ({ goal }) => {
  const DomainIcon = domainIcons[goal.domain as keyof typeof domainIcons];
  const domainColor = domainColors[goal.domain as keyof typeof domainColors];

  return (
    <Card
      sx={{
        height: '100%',
        borderLeft: `4px solid ${domainColor}`,
        '&:hover': {
          boxShadow: 6,
          transform: 'translateY(-4px)',
          transition: 'all 0.3s ease',
        },
      }}
    >
      <CardContent>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 2 }}>
          <Avatar sx={{ bgcolor: domainColor }}>
            <DomainIcon />
          </Avatar>
          <Box>
            <IconButton size="small">
              <Edit fontSize="small" />
            </IconButton>
            <IconButton size="small" color="error">
              <Delete fontSize="small" />
            </IconButton>
          </Box>
        </Box>

        <Typography variant="h6" gutterBottom>
          {goal.title}
        </Typography>
        <Typography variant="body2" color="text.secondary" gutterBottom>
          {goal.description}
        </Typography>

        <Box sx={{ my: 2 }}>
          <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
            <Typography variant="body2" color="text.secondary">
              Progress
            </Typography>
            <Typography variant="body2" fontWeight="bold" color={domainColor}>
              {goal.progress}%
            </Typography>
          </Box>
          <LinearProgress
            variant="determinate"
            value={goal.progress}
            sx={{
              height: 8,
              borderRadius: 4,
              '& .MuiLinearProgress-bar': {
                backgroundColor: domainColor,
              },
            }}
          />
        </Box>

        <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 2 }}>
          <Typography variant="caption" color="text.secondary">
            Current: {goal.current_value}
          </Typography>
          <Typography variant="caption" color="text.secondary">
            Target: {goal.target_value}
          </Typography>
        </Box>

        <Box sx={{ display: 'flex', gap: 1, flexWrap: 'wrap' }}>
          <Chip
            label={goal.domain}
            size="small"
            sx={{ bgcolor: `${domainColor}20`, color: domainColor }}
          />
          <Chip
            label={`Due: ${new Date(goal.deadline).toLocaleDateString()}`}
            size="small"
            variant="outlined"
          />
        </Box>

        <Button
          fullWidth
          variant="outlined"
          startIcon={<CheckCircle />}
          sx={{ mt: 2 }}
          onClick={() => toast.success('Progress logged!')}
        >
          Log Progress
        </Button>
      </CardContent>
    </Card>
  );
};

export default Goals;