import React, { useState } from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  Button,
  Stepper,
  Step,
  StepLabel,
  TextField,
  Chip,
  Grid,
  Avatar,
  Container
} from '@mui/material';
import {
  FitnessCenter,
  AttachMoney,
  Work,
  School,
  People,
  ArrowForward,
  ArrowBack,
  CheckCircle
} from '@mui/icons-material';
import { motion } from 'framer-motion';
import { useNavigate } from 'react-router-dom';
import toast from 'react-hot-toast';

import { useAuthStore } from '../stores/authStore';

const domains = [
  { id: 'health', name: 'Health & Fitness', icon: <FitnessCenter />, color: '#4CAF50' },
  { id: 'finance', name: 'Finance & Money', icon: <AttachMoney />, color: '#2196F3' },
  { id: 'productivity', name: 'Work & Productivity', icon: <Work />, color: '#FF9800' },
  { id: 'learning', name: 'Learning & Growth', icon: <School />, color: '#9C27B0' },
  { id: 'social', name: 'Social & Relationships', icon: <People />, color: '#E91E63' },
];

const Onboarding: React.FC = () => {
  const navigate = useNavigate();
  const { updateUser } = useAuthStore();
  const [activeStep, setActiveStep] = useState(0);
  const [selectedDomains, setSelectedDomains] = useState<string[]>([]);
  const [goals, setGoals] = useState<{ [key: string]: string }>({});

  const steps = ['Welcome', 'Choose Domains', 'Set Goals', 'Complete'];

  const handleNext = () => {
    if (activeStep === 1 && selectedDomains.length === 0) {
      toast.error('Please select at least one domain');
      return;
    }
    setActiveStep((prev) => prev + 1);
  };

  const handleBack = () => {
    setActiveStep((prev) => prev - 1);
  };

  const handleComplete = () => {
    updateUser({ onboarding_completed: true });
    toast.success('Welcome to ORBIT! Let\'s achieve your goals together.');
    navigate('/dashboard');
  };

  const toggleDomain = (domainId: string) => {
    setSelectedDomains((prev) =>
      prev.includes(domainId)
        ? prev.filter((id) => id !== domainId)
        : [...prev, domainId]
    );
  };

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
      <Container maxWidth="md">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
        >
          <Card sx={{ p: 4 }}>
            <CardContent>
              <Stepper activeStep={activeStep} sx={{ mb: 4 }}>
                {steps.map((label) => (
                  <Step key={label}>
                    <StepLabel>{label}</StepLabel>
                  </Step>
                ))}
              </Stepper>

              {/* Step 0: Welcome */}
              {activeStep === 0 && (
                <Box sx={{ textAlign: 'center', py: 4 }}>
                  <Typography variant="h3" gutterBottom fontWeight="bold">
                    Welcome to ORBIT! 🚀
                  </Typography>
                  <Typography variant="h6" color="text.secondary" sx={{ mb: 4 }}>
                    Your AI-powered life optimization platform
                  </Typography>
                  <Typography variant="body1" sx={{ mb: 4, maxWidth: 600, mx: 'auto' }}>
                    ORBIT uses advanced AI and behavioral science to help you achieve your goals.
                    Let's get started by understanding what matters most to you.
                  </Typography>
                  <Box sx={{ display: 'flex', gap: 2, justifyContent: 'center', flexWrap: 'wrap' }}>
                    <Chip icon={<CheckCircle />} label="AI-Powered Coaching" color="primary" />
                    <Chip icon={<CheckCircle />} label="Transparent Decisions" color="primary" />
                    <Chip icon={<CheckCircle />} label="24/7 Support" color="primary" />
                  </Box>
                </Box>
              )}

              {/* Step 1: Choose Domains */}
              {activeStep === 1 && (
                <Box sx={{ py: 2 }}>
                  <Typography variant="h5" gutterBottom textAlign="center">
                    Which areas do you want to focus on?
                  </Typography>
                  <Typography variant="body2" color="text.secondary" textAlign="center" sx={{ mb: 4 }}>
                    Select one or more domains (you can always change this later)
                  </Typography>

                  <Grid container spacing={2}>
                    {domains.map((domain) => (
                      <Grid item xs={12} sm={6} key={domain.id}>
                        <Card
                          sx={{
                            cursor: 'pointer',
                            border: '2px solid',
                            borderColor: selectedDomains.includes(domain.id)
                              ? domain.color
                              : 'transparent',
                            bgcolor: selectedDomains.includes(domain.id)
                              ? `${domain.color}10`
                              : 'background.paper',
                            '&:hover': {
                              borderColor: domain.color,
                              transform: 'translateY(-4px)',
                              transition: 'all 0.3s ease',
                            },
                          }}
                          onClick={() => toggleDomain(domain.id)}
                        >
                          <CardContent>
                            <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                              <Avatar sx={{ bgcolor: domain.color }}>
                                {domain.icon}
                              </Avatar>
                              <Typography variant="h6">{domain.name}</Typography>
                            </Box>
                          </CardContent>
                        </Card>
                      </Grid>
                    ))}
                  </Grid>
                </Box>
              )}

              {/* Step 2: Set Goals */}
              {activeStep === 2 && (
                <Box sx={{ py: 2 }}>
                  <Typography variant="h5" gutterBottom textAlign="center">
                    What are your main goals?
                  </Typography>
                  <Typography variant="body2" color="text.secondary" textAlign="center" sx={{ mb: 4 }}>
                    Tell us what you want to achieve in each domain
                  </Typography>

                  <Box sx={{ display: 'flex', flexDirection: 'column', gap: 3 }}>
                    {selectedDomains.map((domainId) => {
                      const domain = domains.find((d) => d.id === domainId);
                      return (
                        <Box key={domainId}>
                          <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 1 }}>
                            <Avatar sx={{ bgcolor: domain?.color, width: 32, height: 32 }}>
                              {React.cloneElement(domain?.icon as React.ReactElement, {
                                sx: { fontSize: 18 },
                              })}
                            </Avatar>
                            <Typography variant="subtitle1" fontWeight="bold">
                              {domain?.name}
                            </Typography>
                          </Box>
                          <TextField
                            fullWidth
                            multiline
                            rows={2}
                            placeholder={`e.g., ${
                              domainId === 'health'
                                ? 'Exercise 3 times per week'
                                : domainId === 'finance'
                                ? 'Save $500 per month'
                                : domainId === 'productivity'
                                ? 'Complete project by end of month'
                                : domainId === 'learning'
                                ? 'Finish online course'
                                : 'Meet friends weekly'
                            }`}
                            value={goals[domainId] || ''}
                            onChange={(e) =>
                              setGoals({ ...goals, [domainId]: e.target.value })
                            }
                          />
                        </Box>
                      );
                    })}
                  </Box>
                </Box>
              )}

              {/* Step 3: Complete */}
              {activeStep === 3 && (
                <Box sx={{ textAlign: 'center', py: 4 }}>
                  <CheckCircle sx={{ fontSize: 80, color: 'success.main', mb: 2 }} />
                  <Typography variant="h4" gutterBottom fontWeight="bold">
                    You're All Set! 🎉
                  </Typography>
                  <Typography variant="body1" color="text.secondary" sx={{ mb: 4 }}>
                    ORBIT is now ready to help you achieve your goals with AI-powered insights
                    and personalized interventions.
                  </Typography>
                  <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2, maxWidth: 400, mx: 'auto' }}>
                    <Typography variant="subtitle2" textAlign="left">
                      What happens next:
                    </Typography>
                    <Box sx={{ textAlign: 'left' }}>
                      <Typography variant="body2" gutterBottom>
                        ✓ AI will analyze your goals and create a personalized plan
                      </Typography>
                      <Typography variant="body2" gutterBottom>
                        ✓ You'll receive daily insights and interventions
                      </Typography>
                      <Typography variant="body2" gutterBottom>
                        ✓ Track your progress with detailed analytics
                      </Typography>
                      <Typography variant="body2">
                        ✓ Get 24/7 support from our AI agents
                      </Typography>
                    </Box>
                  </Box>
                </Box>
              )}

              {/* Navigation Buttons */}
              <Box sx={{ display: 'flex', justifyContent: 'space-between', mt: 4 }}>
                <Button
                  disabled={activeStep === 0}
                  onClick={handleBack}
                  startIcon={<ArrowBack />}
                >
                  Back
                </Button>
                {activeStep === steps.length - 1 ? (
                  <Button
                    variant="contained"
                    onClick={handleComplete}
                    endIcon={<CheckCircle />}
                  >
                    Get Started
                  </Button>
                ) : (
                  <Button
                    variant="contained"
                    onClick={handleNext}
                    endIcon={<ArrowForward />}
                  >
                    Next
                  </Button>
                )}
              </Box>
            </CardContent>
          </Card>
        </motion.div>
      </Container>
    </Box>
  );
};

export default Onboarding;