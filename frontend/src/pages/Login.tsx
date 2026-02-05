import React, { useState } from 'react';
import {
  Box,
  Card,
  CardContent,
  TextField,
  Button,
  Typography,
  Link,
  Alert,
  InputAdornment,
  IconButton,
  Divider,
  Chip,
  Paper,
  Container
} from '@mui/material';
import {
  Visibility,
  VisibilityOff,
  Email,
  Lock,
  Psychology,
  TrendingUp,
  Security,
  Speed
} from '@mui/icons-material';
import { useForm, Controller } from 'react-hook-form';
import { yupResolver } from '@hookform/resolvers/yup';
import * as yup from 'yup';
import { motion } from 'framer-motion';
import { useNavigate } from 'react-router-dom';

import { useAuthStore } from '../stores/authStore';

// Validation schema
const loginSchema = yup.object({
  email: yup
    .string()
    .email('Please enter a valid email')
    .required('Email is required'),
  password: yup
    .string()
    .min(6, 'Password must be at least 6 characters')
    .required('Password is required'),
});

interface LoginFormData {
  email: string;
  password: string;
}

const Login: React.FC = () => {
  const navigate = useNavigate();
  const { login, isLoading, error } = useAuthStore();
  const [showPassword, setShowPassword] = useState(false);
  const [isRegisterMode, setIsRegisterMode] = useState(false);

  const {
    control,
    handleSubmit,
    formState: { errors },
    reset,
  } = useForm<LoginFormData>({
    resolver: yupResolver(loginSchema),
    defaultValues: {
      email: '',
      password: '',
    },
  });

  const onSubmit = async (data: LoginFormData) => {
    try {
      await login(data.email, data.password);
      navigate('/dashboard');
    } catch (error) {
      // Error is handled by the store and displayed via toast
      console.error('Login error:', error);
    }
  };

  const handleToggleMode = () => {
    setIsRegisterMode(!isRegisterMode);
    reset();
  };

  const features = [
    {
      icon: <Psychology />,
      title: 'AI-Powered Coaching',
      description: 'Get personalized interventions based on behavioral science'
    },
    {
      icon: <TrendingUp />,
      title: 'Pattern Recognition',
      description: 'Discover your behavioral patterns and optimize for success'
    },
    {
      icon: <Security />,
      title: 'Transparent AI',
      description: 'See exactly how our AI makes decisions with full transparency'
    },
    {
      icon: <Speed />,
      title: 'Real-time Adaptation',
      description: '24/7 monitoring and adaptive intervention strategies'
    }
  ];

  return (
    <Box
      sx={{
        minHeight: '100vh',
        background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        p: 2,
      }}
    >
      <Container maxWidth="lg">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
        >
          <Box
            sx={{
              display: 'flex',
              gap: 4,
              alignItems: 'center',
              justifyContent: 'center',
              flexWrap: 'wrap',
            }}
          >
            {/* Left Side - Features */}
            <Box sx={{ flex: 1, minWidth: 300, maxWidth: 500 }}>
              <motion.div
                initial={{ opacity: 0, x: -50 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ duration: 0.6, delay: 0.2 }}
              >
                <Typography
                  variant="h2"
                  sx={{
                    color: 'white',
                    fontWeight: 'bold',
                    mb: 2,
                    textAlign: { xs: 'center', md: 'left' }
                  }}
                >
                  ORBIT
                </Typography>
                <Typography
                  variant="h5"
                  sx={{
                    color: 'rgba(255, 255, 255, 0.9)',
                    mb: 4,
                    textAlign: { xs: 'center', md: 'left' }
                  }}
                >
                  Your Autonomous Life Optimization Platform
                </Typography>

                <Box sx={{ display: 'flex', flexDirection: 'column', gap: 3 }}>
                  {features.map((feature, index) => (
                    <motion.div
                      key={feature.title}
                      initial={{ opacity: 0, x: -30 }}
                      animate={{ opacity: 1, x: 0 }}
                      transition={{ duration: 0.5, delay: 0.3 + index * 0.1 }}
                    >
                      <Paper
                        elevation={3}
                        sx={{
                          p: 3,
                          bgcolor: 'rgba(255, 255, 255, 0.1)',
                          backdropFilter: 'blur(10px)',
                          border: '1px solid rgba(255, 255, 255, 0.2)',
                          color: 'white',
                        }}
                      >
                        <Box sx={{ display: 'flex', alignItems: 'flex-start', gap: 2 }}>
                          <Box
                            sx={{
                              p: 1,
                              borderRadius: 2,
                              bgcolor: 'rgba(255, 255, 255, 0.2)',
                            }}
                          >
                            {feature.icon}
                          </Box>
                          <Box>
                            <Typography variant="h6" gutterBottom>
                              {feature.title}
                            </Typography>
                            <Typography variant="body2" sx={{ opacity: 0.9 }}>
                              {feature.description}
                            </Typography>
                          </Box>
                        </Box>
                      </Paper>
                    </motion.div>
                  ))}
                </Box>
              </motion.div>
            </Box>

            {/* Right Side - Login Form */}
            <Box sx={{ flex: 1, minWidth: 300, maxWidth: 400 }}>
              <motion.div
                initial={{ opacity: 0, x: 50 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ duration: 0.6, delay: 0.4 }}
              >
                <Card
                  elevation={10}
                  sx={{
                    bgcolor: 'rgba(255, 255, 255, 0.95)',
                    backdropFilter: 'blur(20px)',
                    border: '1px solid rgba(255, 255, 255, 0.3)',
                  }}
                >
                  <CardContent sx={{ p: 4 }}>
                    <Box sx={{ textAlign: 'center', mb: 4 }}>
                      <Typography variant="h4" gutterBottom sx={{ fontWeight: 'bold' }}>
                        {isRegisterMode ? 'Join ORBIT' : 'Welcome Back'}
                      </Typography>
                      <Typography variant="body1" color="text.secondary">
                        {isRegisterMode
                          ? 'Start your journey to goal achievement'
                          : 'Sign in to continue your progress'
                        }
                      </Typography>
                    </Box>

                    {error && (
                      <Alert severity="error" sx={{ mb: 3 }}>
                        {error}
                      </Alert>
                    )}

                    <form onSubmit={handleSubmit(onSubmit)}>
                      <Controller
                        name="email"
                        control={control}
                        render={({ field }) => (
                          <TextField
                            {...field}
                            fullWidth
                            label="Email Address"
                            type="email"
                            error={!!errors.email}
                            helperText={errors.email?.message}
                            sx={{ mb: 3 }}
                            InputProps={{
                              startAdornment: (
                                <InputAdornment position="start">
                                  <Email color="action" />
                                </InputAdornment>
                              ),
                            }}
                          />
                        )}
                      />

                      <Controller
                        name="password"
                        control={control}
                        render={({ field }) => (
                          <TextField
                            {...field}
                            fullWidth
                            label="Password"
                            type={showPassword ? 'text' : 'password'}
                            error={!!errors.password}
                            helperText={errors.password?.message}
                            sx={{ mb: 3 }}
                            InputProps={{
                              startAdornment: (
                                <InputAdornment position="start">
                                  <Lock color="action" />
                                </InputAdornment>
                              ),
                              endAdornment: (
                                <InputAdornment position="end">
                                  <IconButton
                                    onClick={() => setShowPassword(!showPassword)}
                                    edge="end"
                                  >
                                    {showPassword ? <VisibilityOff /> : <Visibility />}
                                  </IconButton>
                                </InputAdornment>
                              ),
                            }}
                          />
                        )}
                      />

                      <Button
                        type="submit"
                        fullWidth
                        variant="contained"
                        size="large"
                        disabled={isLoading}
                        sx={{
                          mb: 3,
                          py: 1.5,
                          background: 'linear-gradient(45deg, #6366f1, #8b5cf6)',
                          '&:hover': {
                            background: 'linear-gradient(45deg, #4f46e5, #7c3aed)',
                          },
                        }}
                      >
                        {isLoading
                          ? 'Signing In...'
                          : isRegisterMode
                          ? 'Create Account'
                          : 'Sign In'
                        }
                      </Button>

                      <Divider sx={{ mb: 3 }}>
                        <Chip label="or" size="small" />
                      </Divider>

                      <Box sx={{ textAlign: 'center' }}>
                        <Typography variant="body2" color="text.secondary">
                          {isRegisterMode
                            ? 'Already have an account?'
                            : "Don't have an account?"
                          }{' '}
                          <Link
                            component="button"
                            type="button"
                            onClick={handleToggleMode}
                            sx={{ fontWeight: 'bold' }}
                          >
                            {isRegisterMode ? 'Sign In' : 'Sign Up'}
                          </Link>
                        </Typography>
                      </Box>
                    </form>

                    {/* Demo Credentials */}
                    <Box sx={{ mt: 4, p: 2, bgcolor: 'grey.50', borderRadius: 2 }}>
                      <Typography variant="caption" color="text.secondary" gutterBottom>
                        Demo Credentials:
                      </Typography>
                      <Typography variant="body2" sx={{ fontFamily: 'monospace' }}>
                        Email: demo@orbit.ai
                        <br />
                        Password: demo123
                      </Typography>
                    </Box>
                  </CardContent>
                </Card>
              </motion.div>
            </Box>
          </Box>
        </motion.div>
      </Container>
    </Box>
  );
};

export default Login;