'use client';

import React, { useState, useEffect } from 'react';
import { useRouter, useSearchParams } from 'next/navigation';
import { motion, AnimatePresence } from 'framer-motion';
import { Psychology, ArrowForward, MailOutline, LockOutlined, PersonOutline } from '@mui/icons-material';
import { useAuthStore } from '../stores/authStore';
import toast from 'react-hot-toast';

function Login() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const { login: loginUser } = useAuthStore();

  // Check URL param for mode (login or signup)
  const urlMode = searchParams.get('mode');
  const [isRegister, setIsRegister] = useState(urlMode === 'signup');

  const [formData, setFormData] = useState({
    email: '',
    password: '',
    name: ''
  });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  // Update isRegister when URL changes
  useEffect(() => {
    setIsRegister(urlMode === 'signup');
  }, [urlMode]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      if (isRegister) {
        // Register new user
        const registerResponse = await fetch('/api/auth/register', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            email: formData.email,
            password: formData.password,
            name: formData.name
          })
        });

        if (!registerResponse.ok) {
          const data = await registerResponse.json();
          throw new Error(data.detail || 'Registration failed');
        }

        toast.success('Account created! Logging you in...');
      }

      // Login (for both new users and existing users)
      const loginResponse = await fetch('/api/auth/login-json', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          email: formData.email,
          password: formData.password
        })
      });

      if (!loginResponse.ok) {
        const data = await loginResponse.json();
        throw new Error(data.detail || 'Login failed');
      }

      const data = await loginResponse.json();
      loginUser(data.access_token, data.user);

      toast.success('Welcome to ORBIT!');

      // Redirect based on onboarding status
      if (data.user.onboarding_completed) {
        router.push('/dashboard');
      } else {
        router.push('/onboarding');
      }
    } catch (err: any) {
      setError(err.message);
      toast.error(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-950 flex relative overflow-hidden font-inter">
      {/* Background Decorative Elements */}
      <div className="absolute top-0 left-0 w-full h-full pointer-events-none">
        <div className="absolute top-[-10%] left-[-10%] w-[40%] h-[40%] bg-white/5 rounded-full blur-[120px]" />
        <div className="absolute bottom-[-10%] right-[-10%] w-[40%] h-[40%] bg-white/5 rounded-full blur-[120px]" />
      </div>

      {/* Left side: Branding/Visual */}
      <div className="hidden lg:flex lg:w-1/2 p-24 flex-col justify-between relative z-10 border-r border-white/5">
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="flex items-center gap-3"
        >
          <div className="w-12 h-12 rounded-2xl bg-white flex items-center justify-center text-slate-950 shadow-[0_0_40px_rgba(255,255,255,0.2)]">
            <Psychology className="text-3xl" />
          </div>
          <span className="text-2xl font-bold tracking-tight text-white font-outfit uppercase">ORBIT</span>
        </motion.div>

        <div className="space-y-6">
          <motion.h1
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2 }}
            className="text-7xl font-bold text-white font-outfit leading-tight tracking-tighter"
          >
            Optimize Your <br />
            <span className="text-transparent bg-clip-text bg-gradient-to-r from-white to-white/40 italic">Human Potential</span>
          </motion.h1>
          <motion.p
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.3 }}
            className="text-xl text-gray-400 max-w-md font-light leading-relaxed"
          >
            Orbit is a sophisticated intelligence layer designed to refine behavioral patterns and maximize cognitive output through AI-driven interventions.
          </motion.p>
        </div>

        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 0.5 }}
          className="flex items-center gap-8"
        >
          <div className="flex flex-col">
            <span className="text-2xl font-bold text-white font-outfit">18.4k</span>
            <span className="text-xs text-gray-500 uppercase tracking-widest font-semibold">Active Nodes</span>
          </div>
          <div className="h-8 w-[1px] bg-white/10" />
          <div className="flex flex-col">
            <span className="text-2xl font-bold text-white font-outfit">99.9%</span>
            <span className="text-xs text-gray-500 uppercase tracking-widest font-semibold">Uptime</span>
          </div>
        </motion.div>
      </div>

      {/* Right side: Auth Form */}
      <div className="w-full lg:w-1/2 flex items-center justify-center p-8 relative z-10">
        <motion.div
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          className="w-full max-w-md bg-white/[0.03] backdrop-blur-3xl border border-white/10 rounded-[48px] p-12 shadow-2xl"
        >
          <div className="mb-10">
            <h2 className="text-3xl font-bold text-white font-outfit mb-3">
              {isRegister ? 'Initialize Account' : 'Satellite Uplink'}
            </h2>
            <p className="text-gray-500 text-sm">
              {isRegister ? 'Join the next generation of life optimization.' : 'Welcome back, Commander. Enter your credentials.'}
            </p>
          </div>

          <form onSubmit={handleSubmit} className="space-y-6">
            <AnimatePresence mode="wait">
              {isRegister && (
                <motion.div
                  initial={{ opacity: 0, height: 0 }}
                  animate={{ opacity: 1, height: 'auto' }}
                  exit={{ opacity: 0, height: 0 }}
                  className="space-y-2"
                >
                  <label className="text-[10px] font-bold text-gray-500 uppercase tracking-[0.2em] ml-1">Identity Name</label>
                  <div className="relative group">
                    <PersonOutline className="absolute left-4 top-1/2 -translate-y-1/2 text-gray-500 group-focus-within:text-white transition-colors" />
                    <input
                      type="text"
                      placeholder="e.g. John Doe"
                      className="w-full bg-white/5 border border-white/10 rounded-2xl py-4 pl-12 pr-4 text-white placeholder:text-gray-600 focus:outline-none focus:border-white/30 focus:bg-white/10 transition-all font-inter text-sm"
                      value={formData.name}
                      onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                      required={isRegister}
                    />
                  </div>
                </motion.div>
              )}
            </AnimatePresence>

            <div className="space-y-2">
              <label className="text-[10px] font-bold text-gray-500 uppercase tracking-[0.2em] ml-1">Network UID</label>
              <div className="relative group">
                <MailOutline className="absolute left-4 top-1/2 -translate-y-1/2 text-gray-500 group-focus-within:text-white transition-colors" />
                <input
                  type="email"
                  placeholder="name@company.com"
                  className="w-full bg-white/5 border border-white/10 rounded-2xl py-4 pl-12 pr-4 text-white placeholder:text-gray-600 focus:outline-none focus:border-white/30 focus:bg-white/10 transition-all font-inter text-sm"
                  value={formData.email}
                  onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                  required
                />
              </div>
            </div>

            <div className="space-y-2">
              <label className="text-[10px] font-bold text-gray-500 uppercase tracking-[0.2em] ml-1">Security Key</label>
              <div className="relative group">
                <LockOutlined className="absolute left-4 top-1/2 -translate-y-1/2 text-gray-500 group-focus-within:text-white transition-colors" />
                <input
                  type="password"
                  placeholder="••••••••"
                  className="w-full bg-white/5 border border-white/10 rounded-2xl py-4 pl-12 pr-4 text-white placeholder:text-gray-600 focus:outline-none focus:border-white/30 focus:bg-white/10 transition-all font-inter text-sm"
                  value={formData.password}
                  onChange={(e) => setFormData({ ...formData, password: e.target.value })}
                  required
                  minLength={8}
                />
              </div>
            </div>

            {error && (
              <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                className="p-4 bg-red-500/10 border border-red-500/20 text-red-500 text-xs rounded-2xl line-clamp-2"
              >
                {error}
              </motion.div>
            )}

            <button
              type="submit"
              disabled={loading}
              className="w-full bg-white text-slate-950 py-4 rounded-2xl font-bold hover:bg-white/90 transition-all shadow-[0_0_30px_rgba(255,255,255,0.2)] flex items-center justify-center gap-2 group disabled:opacity-50"
            >
              <span>{loading ? 'Processing...' : isRegister ? 'Initialize Connection' : 'Establish Link'}</span>
              {!loading && <ArrowForward className="group-hover:translate-x-1 transition-transform" />}
            </button>
          </form>

          <p className="mt-8 text-center text-sm text-gray-500">
            {isRegister ? 'Already registered?' : "Need an identity?"}{' '}
            <button
              onClick={() => setIsRegister(!isRegister)}
              className="text-white font-semibold hover:underline"
            >
              {isRegister ? 'Establish Link' : 'Initialize Account'}
            </button>
          </p>
        </motion.div>
      </div>
    </div>
  );
}

export default Login;
