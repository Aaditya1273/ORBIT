import React, { useState } from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  TextField,
  Button,
  Switch,
  FormControlLabel,
  Divider,
  Grid,
  Avatar,
  IconButton,
  Chip,
  List,
  ListItem,
  ListItemText,
  ListItemSecondaryAction
} from '@mui/material';
import {
  Edit,
  Notifications,
  Security,
  Psychology,
  Language,
  Palette
} from '@mui/icons-material';
import toast from 'react-hot-toast';

import { useAuthStore } from '../stores/authStore';
import { useThemeStore } from '../stores/themeStore';

const Settings: React.FC = () => {
  const { user, updateUser } = useAuthStore();
  const { isDarkMode, toggleTheme } = useThemeStore();
  
  const [profile, setProfile] = useState({
    name: user?.name || '',
    email: user?.email || '',
    timezone: 'UTC-5',
  });

  const [notifications, setNotifications] = useState({
    email: true,
    push: true,
    daily_summary: true,
    goal_reminders: true,
    ai_insights: true,
  });

  const [aiSettings, setAiSettings] = useState({
    intervention_frequency: 'medium',
    transparency_level: 'high',
    auto_optimize: true,
  });

  const handleSaveProfile = () => {
    updateUser({ name: profile.name });
    toast.success('Profile updated successfully!');
  };

  const handleSaveNotifications = () => {
    toast.success('Notification preferences saved!');
  };

  const handleSaveAI = () => {
    toast.success('AI settings updated!');
  };

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        ⚙️ Settings
      </Typography>
      <Typography variant="body1" color="text.secondary" sx={{ mb: 4 }}>
        Manage your account and preferences
      </Typography>

      <Grid container spacing={3}>
        {/* Profile Settings */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 3 }}>
                <Edit sx={{ mr: 1 }} />
                <Typography variant="h6">Profile</Typography>
              </Box>

              <Box sx={{ display: 'flex', alignItems: 'center', mb: 3 }}>
                <Avatar
                  sx={{
                    width: 80,
                    height: 80,
                    bgcolor: 'primary.main',
                    fontSize: '2rem',
                  }}
                >
                  {user?.name?.charAt(0).toUpperCase()}
                </Avatar>
                <Box sx={{ ml: 2 }}>
                  <Button variant="outlined" size="small">
                    Change Photo
                  </Button>
                </Box>
              </Box>

              <TextField
                fullWidth
                label="Name"
                value={profile.name}
                onChange={(e) => setProfile({ ...profile, name: e.target.value })}
                sx={{ mb: 2 }}
              />

              <TextField
                fullWidth
                label="Email"
                value={profile.email}
                disabled
                sx={{ mb: 2 }}
              />

              <TextField
                fullWidth
                select
                label="Timezone"
                value={profile.timezone}
                onChange={(e) => setProfile({ ...profile, timezone: e.target.value })}
                sx={{ mb: 2 }}
                SelectProps={{ native: true }}
              >
                <option value="UTC-5">Eastern Time (UTC-5)</option>
                <option value="UTC-6">Central Time (UTC-6)</option>
                <option value="UTC-7">Mountain Time (UTC-7)</option>
                <option value="UTC-8">Pacific Time (UTC-8)</option>
              </TextField>

              <Button variant="contained" fullWidth onClick={handleSaveProfile}>
                Save Profile
              </Button>
            </CardContent>
          </Card>
        </Grid>

        {/* Notification Settings */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 3 }}>
                <Notifications sx={{ mr: 1 }} />
                <Typography variant="h6">Notifications</Typography>
              </Box>

              <List>
                <ListItem>
                  <ListItemText
                    primary="Email Notifications"
                    secondary="Receive updates via email"
                  />
                  <ListItemSecondaryAction>
                    <Switch
                      checked={notifications.email}
                      onChange={(e) =>
                        setNotifications({ ...notifications, email: e.target.checked })
                      }
                    />
                  </ListItemSecondaryAction>
                </ListItem>

                <ListItem>
                  <ListItemText
                    primary="Push Notifications"
                    secondary="Browser push notifications"
                  />
                  <ListItemSecondaryAction>
                    <Switch
                      checked={notifications.push}
                      onChange={(e) =>
                        setNotifications({ ...notifications, push: e.target.checked })
                      }
                    />
                  </ListItemSecondaryAction>
                </ListItem>

                <ListItem>
                  <ListItemText
                    primary="Daily Summary"
                    secondary="Morning briefing at 7 AM"
                  />
                  <ListItemSecondaryAction>
                    <Switch
                      checked={notifications.daily_summary}
                      onChange={(e) =>
                        setNotifications({ ...notifications, daily_summary: e.target.checked })
                      }
                    />
                  </ListItemSecondaryAction>
                </ListItem>

                <ListItem>
                  <ListItemText
                    primary="Goal Reminders"
                    secondary="Timely reminders for your goals"
                  />
                  <ListItemSecondaryAction>
                    <Switch
                      checked={notifications.goal_reminders}
                      onChange={(e) =>
                        setNotifications({ ...notifications, goal_reminders: e.target.checked })
                      }
                    />
                  </ListItemSecondaryAction>
                </ListItem>

                <ListItem>
                  <ListItemText
                    primary="AI Insights"
                    secondary="Behavioral pattern notifications"
                  />
                  <ListItemSecondaryAction>
                    <Switch
                      checked={notifications.ai_insights}
                      onChange={(e) =>
                        setNotifications({ ...notifications, ai_insights: e.target.checked })
                      }
                    />
                  </ListItemSecondaryAction>
                </ListItem>
              </List>

              <Button variant="contained" fullWidth onClick={handleSaveNotifications}>
                Save Preferences
              </Button>
            </CardContent>
          </Card>
        </Grid>

        {/* AI Settings */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 3 }}>
                <Psychology sx={{ mr: 1 }} />
                <Typography variant="h6">AI Configuration</Typography>
              </Box>

              <Typography variant="body2" color="text.secondary" gutterBottom>
                Intervention Frequency
              </Typography>
              <Box sx={{ display: 'flex', gap: 1, mb: 3 }}>
                {['low', 'medium', 'high'].map((freq) => (
                  <Chip
                    key={freq}
                    label={freq.charAt(0).toUpperCase() + freq.slice(1)}
                    onClick={() => setAiSettings({ ...aiSettings, intervention_frequency: freq })}
                    color={aiSettings.intervention_frequency === freq ? 'primary' : 'default'}
                    variant={aiSettings.intervention_frequency === freq ? 'filled' : 'outlined'}
                  />
                ))}
              </Box>

              <Typography variant="body2" color="text.secondary" gutterBottom>
                Transparency Level
              </Typography>
              <Box sx={{ display: 'flex', gap: 1, mb: 3 }}>
                {['low', 'medium', 'high'].map((level) => (
                  <Chip
                    key={level}
                    label={level.charAt(0).toUpperCase() + level.slice(1)}
                    onClick={() => setAiSettings({ ...aiSettings, transparency_level: level })}
                    color={aiSettings.transparency_level === level ? 'primary' : 'default'}
                    variant={aiSettings.transparency_level === level ? 'filled' : 'outlined'}
                  />
                ))}
              </Box>

              <FormControlLabel
                control={
                  <Switch
                    checked={aiSettings.auto_optimize}
                    onChange={(e) =>
                      setAiSettings({ ...aiSettings, auto_optimize: e.target.checked })
                    }
                  />
                }
                label="Auto-optimize interventions based on feedback"
              />

              <Button variant="contained" fullWidth onClick={handleSaveAI} sx={{ mt: 2 }}>
                Save AI Settings
              </Button>
            </CardContent>
          </Card>
        </Grid>

        {/* Appearance */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 3 }}>
                <Palette sx={{ mr: 1 }} />
                <Typography variant="h6">Appearance</Typography>
              </Box>

              <FormControlLabel
                control={<Switch checked={isDarkMode} onChange={toggleTheme} />}
                label="Dark Mode"
              />

              <Divider sx={{ my: 2 }} />

              <Typography variant="body2" color="text.secondary" gutterBottom>
                Theme Preview
              </Typography>
              <Box
                sx={{
                  p: 2,
                  borderRadius: 2,
                  bgcolor: 'background.default',
                  border: '1px solid',
                  borderColor: 'divider',
                }}
              >
                <Typography variant="body2">
                  Current theme: {isDarkMode ? 'Dark' : 'Light'}
                </Typography>
              </Box>
            </CardContent>
          </Card>
        </Grid>

        {/* Security */}
        <Grid item xs={12}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 3 }}>
                <Security sx={{ mr: 1 }} />
                <Typography variant="h6">Security & Privacy</Typography>
              </Box>

              <Grid container spacing={2}>
                <Grid item xs={12} md={4}>
                  <Button variant="outlined" fullWidth>
                    Change Password
                  </Button>
                </Grid>
                <Grid item xs={12} md={4}>
                  <Button variant="outlined" fullWidth>
                    Export Data
                  </Button>
                </Grid>
                <Grid item xs={12} md={4}>
                  <Button variant="outlined" color="error" fullWidth>
                    Delete Account
                  </Button>
                </Grid>
              </Grid>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  );
};

export default Settings;