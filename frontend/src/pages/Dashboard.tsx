import React from 'react';
import { useRouter } from 'next/navigation';
import { motion } from 'framer-motion';
import {
  Psychology,
  TrendingUp,
  EmojiEvents,
  FlashOn,
  Add,
  ArrowForward,
  InfoOutlined
} from '@mui/icons-material';
import { useAuthStore } from '../stores/authStore';
import MainLayout from '../components/layout/MainLayout';

const StatCard = ({ title, value, icon, color, delay }: { title: string, value: string, icon: React.ReactNode, color: string, delay: number }) => (
  <motion.div
    initial={{ opacity: 0, y: 20 }}
    animate={{ opacity: 1, y: 0 }}
    transition={{ duration: 0.5, delay }}
    className="glass-card p-6 rounded-3xl hover:scale-[1.02] transition-all cursor-pointer group"
  >
    <div className="flex items-center justify-between mb-4">
      <div className={`w-12 h-12 rounded-2xl flex items-center justify-center ${color} bg-opacity-10 shadow-inner`}>
        {icon}
      </div>
      <div className="text-gray-300 group-hover:text-gray-900 transition-colors">
        <ArrowForward className="text-sm" />
      </div>
    </div>
    <p className="text-sm font-semibold text-gray-400 uppercase tracking-widest mb-1">{title}</p>
    <h3 className="text-3xl font-bold text-gray-900 font-outfit">{value}</h3>
  </motion.div>
);

function Dashboard() {
  const navigate = useRouter();
  const { user } = useAuthStore();

  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        staggerChildren: 0.1
      }
    }
  };

  const itemVariants = {
    hidden: { opacity: 0, y: 20 },
    visible: { opacity: 1, y: 0 }
  };

  return (
    <MainLayout>
      <div className="max-w-7xl mx-auto px-8 py-10">
        {/* Welcome Section */}
        <motion.div
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          className="mb-12 flex items-center justify-between"
        >
          <div>
            <div className="flex items-center gap-2 mb-2">
              <span className="px-2.5 py-1 rounded-full bg-gray-950 text-white text-[10px] font-bold uppercase tracking-tighter">System Status: Active</span>
              <span className="text-gray-300">•</span>
              <span className="text-xs text-gray-500 font-medium">{new Date().toLocaleDateString('en-US', { month: 'long', day: 'numeric', year: 'numeric' })}</span>
            </div>
            <h2 className="text-5xl font-bold text-gray-900 font-outfit tracking-tight">
              Hello, {user?.name || 'Commander'} <span className="text-gray-300">/</span>
            </h2>
            <p className="text-lg text-gray-500 mt-2 font-inter max-w-xl">
              Orbit has analyzed your current trajectories. You are <span className="text-gray-950 font-semibold italic">12% ahead</span> of your weekly goals.
            </p>
          </div>
          <button
            onClick={() => router.push('/goals')}
            className="btn-premium gap-2 group shadow-xl shadow-gray-200"
          >
            <Add className="text-lg" />
            <span>Create New Objective</span>
          </button>
        </motion.div>

        {/* Intelligence Grid */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-12">
          <StatCard
            title="Active Vectors"
            value="8"
            icon={<EmojiEvents className="text-orange-500" />}
            color="bg-orange-500"
            delay={0.1}
          />
          <StatCard
            title="AI Interventions"
            value="142"
            icon={<Psychology className="text-purple-500" />}
            color="bg-purple-500"
            delay={0.2}
          />
          <StatCard
            title="Success Coefficient"
            value="94.2%"
            icon={<TrendingUp className="text-green-500" />}
            color="bg-green-500"
            delay={0.3}
          />
          <StatCard
            title="Productivity Streak"
            value="18"
            icon={<FlashOn className="text-blue-500" />}
            color="bg-blue-500"
            delay={0.4}
          />
        </div>

        {/* Main Interface Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Recent Strategy Insights */}
          <motion.div
            variants={containerVariants}
            initial="hidden"
            animate="visible"
            className="lg:col-span-2 space-y-6"
          >
            <div className="flex items-center justify-between">
              <h3 className="text-xl font-bold text-gray-900 font-outfit">Priority Insights</h3>
              <button className="text-sm font-semibold text-gray-400 hover:text-gray-900 transition-colors">See all intelligence</button>
            </div>

            {[1, 2, 3].map((i) => (
              <motion.div
                key={i}
                variants={itemVariants}
                className="glass-card p-6 rounded-3xl flex items-start gap-5 hover:bg-white transition-all cursor-pointer border border-gray-50 group"
              >
                <div className="w-14 h-14 rounded-2xl bg-gray-50 flex items-center justify-center text-gray-400 group-hover:bg-gray-950 group-hover:text-white transition-all duration-300">
                  <FlashOn />
                </div>
                <div className="flex-1">
                  <div className="flex items-center gap-2 mb-1">
                    <span className="text-[10px] font-bold text-purple-600 uppercase tracking-widest">Habit Strategy</span>
                    <span className="text-gray-200">|</span>
                    <span className="text-xs text-gray-400">24m ago</span>
                  </div>
                  <h4 className="text-lg font-bold text-gray-900 mb-1 group-hover:translate-x-1 transition-transform">Optimization of Deep Work Cycles</h4>
                  <p className="text-sm text-gray-500 leading-relaxed line-clamp-2">Orbit detected a drop in cognitive maintenance. Switching to Pomodoro-90 technique is recommended for current focus level.</p>
                </div>
              </motion.div>
            ))}
          </motion.div>

          {/* Quick Stats / Feedback */}
          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.5 }}
            className="space-y-6"
          >
            <div className="glass-card p-8 rounded-[40px] bg-gray-950 text-white relative overflow-hidden">
              <div className="relative z-10">
                <div className="w-10 h-10 rounded-full bg-white/10 flex items-center justify-center mb-6">
                  <InfoOutlined />
                </div>
                <h3 className="text-2xl font-bold mb-3 font-outfit">System Optimization Ready</h3>
                <p className="text-gray-400 text-sm mb-6 leading-relaxed">Your behavioral patterns suggest a high probability of success for <span className="text-white font-semibold">Project Aurora</span> today.</p>
                <button className="w-full py-4 bg-white text-gray-950 rounded-2xl font-bold hover:scale-[0.98] transition-transform flex items-center justify-center gap-2">
                  Initialize Push <ArrowForward className="text-sm" />
                </button>
              </div>
              <div className="absolute top-0 right-0 w-64 h-64 bg-white/5 rounded-full -mr-32 -mt-32 blur-3xl" />
            </div>

            <div className="glass-card p-6 rounded-3xl">
              <h4 className="font-bold text-gray-900 mb-4 font-outfit">AI Confidence Graph</h4>
              <div className="h-32 flex items-end gap-2 px-2">
                {[40, 70, 45, 90, 65, 80, 55, 95].map((h, i) => (
                  <div
                    key={i}
                    style={{ height: `${h}%` }}
                    className="flex-1 bg-gray-100 rounded-t-lg hover:bg-gray-950 transition-colors cursor-help group relative"
                  >
                    <div className="absolute -top-8 left-1/2 -translate-x-1/2 bg-gray-900 text-white text-[10px] px-2 py-1 rounded opacity-0 group-hover:opacity-100 transition-opacity">
                      {h}%
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </motion.div>
        </div>
      </div>
    </MainLayout>
  );
}

export default Dashboard;
