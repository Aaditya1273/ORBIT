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
  Avatar
} from '@mui/material';
import {
  Dashboard,
  EmojiEvents,
  Timeline,
  Settings,
  FitnessCenter,
  AttachMoney,
  Work,
  School,
  People,
  Psychology
} from '@mui/icons-material';
import { useNavigate, useLocation } from 'react-router-dom';

const drawerWidth = 260;

const Sidebar: React.FC = () => {
  const navigate = useNavigate();
  const location = useLocation();

  const mainMenuItems = [
    { text: 'Dashboard', icon: <Dashboard />, path: '/dashboard' },
    { text: 'Goals', icon: <EmojiEvents />, path: '/goals' },
    { text: 'Analytics', icon: <Timeline />, path: '/analytics' },
    { text: 'Settings', icon: <Settings />, path: '/settings' },
  ];

  const domainItems = [
    { text: 'Health', icon: <FitnessCenter />, color: '#4CAF50', count: 3 },
    { text: 'Finance', icon: <AttachMoney />, color: '#2196F3', count: 2 },
    { text: 'Productivity', icon: <Work />, color: '#FF9800', count: 4 },
    { text: 'Learning', icon: <School />, color: '#9C27B0', count: 1 },
    { text: 'Social', icon: <People />, color: '#E91E63', count: 2 },
  ];

  const isActive = (path: string) => location.pathname === path;

  return (
    <Drawer
      variant="permanent"
      sx={{
        width: drawerWidth,
        flexShrink: 0,
        '& .MuiDrawer-paper': {
          width: drawerWidth,
          boxSizing: 'border-box',
          borderRight: '1px solid',
          borderColor: 'divider',
          bgcolor: 'background.paper',
        },
      }}
    >
      <Box sx={{ overflow: 'auto', height: '100%', display: 'flex', flexDirection: 'column' }}>
        {/* Logo Section */}
        <Box sx={{ p: 3, display: 'flex', alignItems: 'center', gap: 1 }}>
          <Avatar sx={{ bgcolor: 'primary.main', width: 40, height: 40 }}>
            <Psychology />
          </Avatar>
          <Box>
            <Typography variant="h6" sx={{ fontWeight: 'bold', lineHeight: 1.2 }}>
              ORBIT
            </Typography>
            <Typography variant="caption" color="text.secondary">
              Life Optimizer
            </Typography>
          </Box>
        </Box>

        <Divider />

        {/* Main Navigation */}
        <List sx={{ px: 2, py: 1 }}>
          {mainMenuItems.map((item) => (
            <ListItem key={item.text} disablePadding sx={{ mb: 0.5 }}>
              <ListItemButton
                onClick={() => navigate(item.path)}
                selected={isActive(item.path)}
                sx={{
                  borderRadius: 2,
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
                }}
              >
                <ListItemIcon
                  sx={{
                    minWidth: 40,
                    color: isActive(item.path) ? 'inherit' : 'text.secondary',
                  }}
                >
                  {item.icon}
                </ListItemIcon>
                <ListItemText 
                  primary={item.text}
                  primaryTypographyProps={{
                    fontWeight: isActive(item.path) ? 600 : 400,
                  }}
                />
              </ListItemButton>
            </ListItem>
          ))}
        </List>

        <Divider sx={{ mx: 2 }} />

        {/* Domains Section */}
        <Box sx={{ px: 2, py: 2 }}>
          <Typography
            variant="caption"
            sx={{
              px: 2,
              py: 1,
              display: 'block',
              color: 'text.secondary',
              fontWeight: 600,
              textTransform: 'uppercase',
              letterSpacing: 1,
            }}
          >
            Goal Domains
          </Typography>
          <List sx={{ py: 0 }}>
            {domainItems.map((item) => (
              <ListItem key={item.text} disablePadding sx={{ mb: 0.5 }}>
                <ListItemButton
                  sx={{
                    borderRadius: 2,
                    '&:hover': {
                      bgcolor: 'action.hover',
                    },
                  }}
                >
                  <ListItemIcon sx={{ minWidth: 40 }}>
                    <Avatar
                      sx={{
                        bgcolor: item.color,
                        width: 32,
                        height: 32,
                      }}
                    >
                      {React.cloneElement(item.icon, { sx: { fontSize: 18 } })}
                    </Avatar>
                  </ListItemIcon>
                  <ListItemText 
                    primary={item.text}
                    primaryTypographyProps={{
                      fontSize: '0.875rem',
                    }}
                  />
                  <Chip
                    label={item.count}
                    size="small"
                    sx={{
                      height: 20,
                      fontSize: '0.75rem',
                      bgcolor: `${item.color}20`,
                      color: item.color,
                      fontWeight: 600,
                    }}
                  />
                </ListItemButton>
              </ListItem>
            ))}
          </List>
        </Box>

        {/* Bottom Section - AI Status */}
        <Box sx={{ mt: 'auto', p: 2 }}>
          <Box
            sx={{
              p: 2,
              borderRadius: 2,
              bgcolor: 'primary.main',
              color: 'primary.contrastText',
            }}
          >
            <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
              <Psychology sx={{ mr: 1, fontSize: 20 }} />
              <Typography variant="subtitle2" fontWeight="bold">
                AI Status
              </Typography>
            </Box>
            <Typography variant="caption" sx={{ display: 'block', mb: 1, opacity: 0.9 }}>
              All systems operational
            </Typography>
            <Box sx={{ display: 'flex', gap: 1 }}>
              <Chip
                label="Safety: 98%"
                size="small"
                sx={{
                  bgcolor: 'rgba(255, 255, 255, 0.2)',
                  color: 'inherit',
                  fontSize: '0.7rem',
                  height: 20,
                }}
              />
              <Chip
                label="Active"
                size="small"
                sx={{
                  bgcolor: 'rgba(76, 175, 80, 0.3)',
                  color: 'inherit',
                  fontSize: '0.7rem',
                  height: 20,
                }}
              />
            </Box>
          </Box>
        </Box>
      </Box>
    </Drawer>
  );
};

export default Sidebar;