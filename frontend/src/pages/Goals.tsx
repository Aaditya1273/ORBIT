import React, { useState } from 'react';
import {
  FitnessCenter,
  AttachMoney,
  Work,
  School,
  People,
  Add,
  MoreVert,
  TrendingUp,
  History,
  InfoOutlined,
  CheckCircle,
  DeleteOutline,
  EditOutlined
} from '@mui/icons-material';
import { motion, AnimatePresence } from 'framer-motion';
import MainLayout from '../components/layout/MainLayout';

const domainIcons: Record<string, any> = {
  health: FitnessCenter,
  finance: AttachMoney,
  productivity: Work,
  learning: School,
  social: People
};

const domainLabels: Record<string, string> = {
  health: 'Physical Integrity',
  finance: 'Capital Flow',
  productivity: 'Output Optimization',
  learning: 'Cognitive Expansion',
  social: 'Social Network'
};

const GoalCard = ({ goal, delay }: { goal: any, delay: number }) => {
  const Icon = domainIcons[goal.domain];
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay }}
      className="glass-card p-6 rounded-[32px] group hover:bg-white transition-all border border-gray-50 flex flex-col"
    >
      <div className="flex items-start justify-between mb-6">
        <div className="w-12 h-12 rounded-2xl bg-gray-50 flex items-center justify-center text-gray-400 group-hover:bg-gray-950 group-hover:text-white transition-all duration-300">
          <Icon className="text-xl" />
        </div>
        <button className="text-gray-300 hover:text-gray-900 transition-colors">
          <MoreVert />
        </button>
      </div>

      <div className="flex-1">
        <span className="text-[10px] font-bold text-gray-400 uppercase tracking-widest mb-2 block">{domainLabels[goal.domain]}</span>
        <h3 className="text-xl font-bold text-gray-900 font-outfit mb-2 group-hover:translate-x-1 transition-transform">{goal.title}</h3>
        <p className="text-sm text-gray-500 leading-relaxed mb-6 line-clamp-2">{goal.description}</p>
      </div>

      <div className="space-y-4 pt-4 border-t border-gray-50/50">
        <div className="flex justify-between items-end">
          <div className="flex flex-col">
            <span className="text-[10px] text-gray-400 uppercase font-bold tracking-tighter">Current Velocity</span>
            <span className="text-base font-bold text-gray-900">{goal.current_value}</span>
          </div>
          <div className="flex flex-col items-end">
            <span className="text-xs font-bold text-gray-950">{goal.progress}%</span>
          </div>
        </div>
        <div className="w-full h-1.5 bg-gray-100 rounded-full overflow-hidden">
          <div
            className="h-full bg-gray-950 transition-all duration-1000 ease-out"
            style={{ width: `${goal.progress}%` }}
          />
        </div>
        <div className="flex items-center justify-between text-[11px] text-gray-400">
          <div className="flex items-center gap-1">
            <History className="text-[14px]" />
            <span>Target: {goal.target_value}</span>
          </div>
          <span className="font-medium">Due {new Date(goal.deadline).toLocaleDateString()}</span>
        </div>
      </div>

      <button className="mt-6 w-full py-3 bg-gray-950 text-white rounded-xl text-sm font-bold opacity-0 group-hover:opacity-100 transition-all hover:scale-[0.98]">
        Update Metrics
      </button>
    </motion.div>
  );
};

function Goals() {
  const [selectedTab, setSelectedTab] = useState(0);
  const domains = ['All Objectives', 'Health', 'Finance', 'Productivity', 'Learning', 'Social'];

  const mockGoals = [
    {
      id: '1',
      title: 'Aerobic Maintenance',
      description: 'System-wide cardiovascular optimization through 150min hebdomadal effort.',
      domain: 'health',
      progress: 67,
      target_value: '12 sessions',
      current_value: '8 sessions',
      deadline: '2026-03-01',
    },
    {
      id: '2',
      title: 'Capital Reserve Expansion',
      description: 'Stabilizing fiscal foundations for future-proof scalability.',
      domain: 'finance',
      progress: 80,
      target_value: '$5,000',
      current_value: '$4,000',
      deadline: '2026-02-28',
    },
    {
      id: '3',
      title: 'Neural Architecture Expansion',
      description: 'Advanced mastery of full-stack AI orchestration dynamics.',
      domain: 'learning',
      progress: 45,
      target_value: '100% Mastery',
      current_value: '45% Progress',
      deadline: '2026-04-15',
    },
  ];

  const filteredGoals = selectedTab === 0
    ? mockGoals
    : mockGoals.filter(g => g.domain === ['health', 'finance', 'productivity', 'learning', 'social'][selectedTab - 1]);

  return (
    <MainLayout>
      <div className="max-w-7xl mx-auto px-8 py-10">
        {/* Header Section */}
        <div className="flex flex-col md:flex-row md:items-end justify-between gap-6 mb-12">
          <div>
            <div className="flex items-center gap-2 mb-2 text-gray-400">
              <TrendingUp className="text-sm" />
              <span className="text-[10px] font-bold uppercase tracking-widest text-orange-500">Peak Performance Detected</span>
            </div>
            <h1 className="text-5xl font-bold text-gray-900 font-outfit tracking-tight">Active Objectives <span className="text-gray-300">/</span></h1>
            <p className="text-lg text-gray-500 mt-2 font-inter max-w-xl">
              Orbit is tracking <span className="text-gray-950 font-semibold">{mockGoals.length} primary vectors</span>. Your current execution rate is optimal.
            </p>
          </div>
          <button className="btn-premium gap-2 shadow-xl shadow-gray-200 h-fit">
            <Add className="text-lg" />
            <span>New Objective</span>
          </button>
        </div>

        {/* Tab Selection */}
        <div className="flex items-center gap-2 mb-10 overflow-x-auto pb-2 scrollbar-hide">
          {domains.map((domain, idx) => (
            <button
              key={domain}
              onClick={() => setSelectedTab(idx)}
              className={`px-6 py-2.5 rounded-full text-sm font-semibold whitespace-nowrap transition-all border ${selectedTab === idx
                  ? 'bg-gray-950 text-white border-gray-950 shadow-lg shadow-gray-200'
                  : 'bg-white text-gray-500 border-gray-100 hover:border-gray-300 hover:text-gray-900'
                }`}
            >
              {domain}
            </button>
          ))}
        </div>

        {/* Content Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          <AnimatePresence mode="popLayout">
            {filteredGoals.map((goal, idx) => (
              <GoalCard key={goal.id} goal={goal} delay={idx * 0.1} />
            ))}
          </AnimatePresence>

          {/* New Goal Placeholder */}
          <motion.button
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="border-2 border-dashed border-gray-100 rounded-[32px] p-8 flex flex-col items-center justify-center text-gray-300 hover:border-gray-300 hover:text-gray-500 transition-all group min-h-[300px]"
          >
            <div className="w-16 h-16 rounded-3xl border-2 border-dashed border-gray-200 flex items-center justify-center mb-4 group-hover:scale-110 transition-transform">
              <Add className="text-3xl" />
            </div>
            <span className="font-bold font-outfit">Initialize Next Vector</span>
            <p className="text-xs text-center mt-2 px-4">Ready to optimize a new area of your life footprint?</p>
          </motion.button>
        </div>
      </div>
    </MainLayout>
  );
}

export default Goals;
