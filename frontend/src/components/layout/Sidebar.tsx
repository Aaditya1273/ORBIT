import React from 'react';
import {
  Drawer,
  List,
  ListItem,
  ListItemButton,
  ListItemIcon,
  ListItemText,
  Box,
  Typography,
  Divider,
  Chip,
  useTheme,
  useMediaQuery
} from '@mui/material';
import {
  Dashboard,
  TrackChanges,
  Analytics,
  Settings,
  Psychology,
  TrendingUp,
  FitnessCenter,
  AttachMoney,
  Work,
  School,
  People,
  Integration,
  Help,
  Feedback
} from '@mui/icons-material';
import { useLocation, useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';

const DRAWER_WIDTH = 280;

interface NavigationItem {
  id: string;
  label: string;
  icon: React.ReactNode;
  path: string;
  badge?: string | number;
  color?: string;
}

const navigationItems: NavigationItem[] = [
  {
    id: 'dashboard',
    label: 'Dashboard',
    icon: <Dashboard />,
    path: '/dashboard',
  },
  {
    id: 'goals',
    label: 'Goals',
    icon: <TrackChanges />,
    path: '/goals',
    badge: 3, // Active goals count
  },
  {
    id: 'analytics',
    label: 'Analytics',
    icon: <Analytics />,
    path: '/analytics',
  },
];

const domainItems: NavigationItem[] = [
  {
    id: 'health',
    label: 'Health & Fitness',
    icon: <FitnessCenter />,
    path: '/goals?domain=health',
    color: '#4CAF50',
  },
  {
    id: 'finance',
    label: 'Finance',
    icon: <AttachMoney />,
    path: '/goals?domain=finance',
    color: '#2196F3',
  },
  {
    id: 'productivity',
    label: 'Productivity',
    icon: <Work />,
    path: '/goals?domain=productivity',
    color: '#FF9800',
  },
  {
    id: 'learning',
    label: 'Learning',
    icon: <School />,
    path: '/goals?domain=learning',
    color: '#9C27B0',
  },
  {
    id: 'social',
    label: 'Social',
    icon: <People />,
    path: '/goals?domain=social',
    color: '#E91E63',
  },
];

const aiItems: NavigationItem[] = [
  {
    id: 'ai-insights',
    label: 'AI Insights',
    icon: <Psychology />,
    path: '/ai-insights',
    badge: 'New',
  },
  {
    id: 'patterns',
    label: 'Behavioral Patterns',
    icon: <TrendingUp />,
    path: '/patterns',
  },
];

const bottomItems: NavigationItem[] = [
  {
    id: 'integrations',
    label: 'Integrations',
    icon: <Integration />,
    path: '/integrations',
  },
  {
    id: 'settings',
    label: 'Settings',
    icon: <Settings />,
    path: '/settings',
  },
  {
    id: 'help',
    label: 'Help & Support',
    icon: <Help />,
    path: '/help',
  },
];

const Sidebar: React.FC = () => {
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('md'));
  const location = useLocation();
  const navigate = useNavigate();

  const isActive = (path: string) => {
    if (path === '/dashboard') {
      return location.pathname === '/' || location.pathname === '/dashboard';
    }
    return location.pathname.startsWith(path);
  };

  const handleNavigation = (path: string) => {
    navigate(path);
  };

  const renderNavigationItem = (item: NavigationItem, index: number) => (
    <motion.div
      key={item.id}
      initial={{ opacity: 0, x: -20 }}
      animate={{ opacity: 1, x: 0 }}
      transition={{ duration: 0.3, delay: index * 0.05 }}
    >
      <ListItem disablePadding sx={{ mb: 0.5 }}>
        <ListItemButton
          onClick={() => handleNavigation(item.path)}
          selected={isActive(item.path)}
          sx={{
            borderRadius: 2,
            mx: 1,
            '&.Mui-selected': {
              bgcolor: 'primary.main',
              color: 'primary.contrastText',
              '&:hover': {
                bgcolor: 'primary.dark',
              },
              '& .MuiListItemIcon-root': {
                color: 'primary.contrastText',
              },
            },
            '&:hover': {
              bgcolor: 'action.hover',
            },
          }}
        >
          <ListItemIcon
            sx={{
              color: item.color || 'inherit',
              minWidth: 40,
            }}
          >
            {item.icon}
          </ListItemIcon>
          <ListItemText
            primary={item.label}
            primaryTypographyProps={{
              fontSize: '0.875rem',
              fontWeight: isActive(item.path) ? 600 : 400,
            }}
          />
          {item.badge && (
            <Chip
              label={item.badge}
              size="small"
              color={typeof item.badge === 'string' ? 'secondary' : 'primary'}
              sx={{
                height: 20,
                fontSize: '0.75rem',
                '& .MuiChip-label': {
                  px: 1,
                },
              }}
            />
          )}
        </ListItemButton>
      </ListItem>
    </motion.div>
  );

  const sidebarContent = (
    <Box sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
      {/* Header */}
      <Box sx={{ p: 3, pb: 2 }}>
        <Typography
          variant="h5"
          sx={{
            fontWeight: 'bold',
            background: 'linear-gradient(45deg, #6366f1, #8b5cf6)',
            backgroundClip: 'text',
            WebkitBackgroundClip: 'text',
            WebkitTextFillColor: 'transparent',
            textAlign: 'center',
          }}
        >
          ORBIT
        </Typography>
        <Typography
          variant="caption"
          color="text.secondary"
          sx={{ display: 'block', textAlign: 'center', mt: 0.5 }}
        >
          Autonomous Life Optimization
        </Typography>
      </Box>

      {/* Main Navigation */}
      <Box sx={{ flexGrow: 1, overflowY: 'auto' }}>
        <List sx={{ px: 1 }}>
          {navigationItems.map((item, index) => renderNavigationItem(item, index))}
        </List>

        {/* Goal Domains */}
        <Box sx={{ px: 2, mt: 3, mb: 1 }}>
          <Typography
            variant="overline"
            color="text.secondary"
            sx={{ fontWeight: 600, fontSize: '0.75rem' }}
          >
            Goal Domains
          </Typography>
        </Box>
        <List sx={{ px: 1 }}>
          {domainItems.map((item, index) => renderNavigationItem(item, index + navigationItems.length))}
        </List>

        {/* AI Features */}
        <Box sx={{ px: 2, mt: 3, mb: 1 }}>
          <Typography
            variant="overline"
            color="text.secondary"
            sx={{ fontWeight: 600, fontSize: '0.75rem' }}
          >
            AI Features
          </Typography>
        </Box>
        <List sx={{ px: 1 }}>
          {aiItems.map((item, index) => renderNavigationItem(item, index + navigationItems.length + domainItems.length))}
        </List>
      </Box>

      {/* Bottom Navigation */}
      <Box>
        <Divider sx={{ mx: 2, mb: 1 }} />
        <List sx={{ px: 1, pb: 2 }}>
          {bottomItems.map((item, index) => renderNavigationItem(item, index))}
        </List>

        {/* AI Reliability Status */}
        <Box sx={{ px: 3, pb: 3 }}>
          <Box
            sx={{
              p: 2,
              bgcolor: 'success.main',
              color: 'success.contrastText',
              borderRadius: 2,
              textAlign: 'center',
            }}
          >
            <Typography variant="caption" sx={{ fontWeight: 600 }}>
              AI Status: Operational
            </Typography>
            <Typography variant="caption" sx={{ display: 'block', opacity: 0.9 }}>
              97% Safety Score
            </Typography>
          </Box>
        </Box>
      </Box>
    </Box>
  );

  if (isMobile) {
    // Mobile drawer (would be controlled by parent component)
    return null; // For now, we'll implement mobile navigation later
  }

  return (
    <Drawer
      variant="permanent"
      sx={{
        width: DRAWER_WIDTH,
        flexShrink: 0,
        '& .MuiDrawer-paper': {
          width: DRAWER_WIDTH,
          boxSizing: 'border-box',
          borderRight: 1,
          borderColor: 'divider',
          bgcolor: 'background.paper',
        },
      }}
    >
      {sidebarContent}
    </Drawer>
  );
};

export default Sidebar;