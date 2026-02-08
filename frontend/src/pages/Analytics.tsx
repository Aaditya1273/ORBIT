import React, { useState } from 'react';
import {
  TrendingUp,
  TrendingDown,
  Timeline,
  Speed,
  EmojiEvents,
  AutoAwesome,
  FlashOn,
  Psychology,
  ArrowForward,
  InfoOutlined
} from '@mui/icons-material';
import {
  LineChart,
  Line,
  PieChart,
  Pie,
  Cell,
  XAxis,
  YAxis,
  Tooltip as RechartsTooltip,
  ResponsiveContainer,
  RadarChart,
  PolarGrid,
  PolarAngleAxis,
  Radar
} from 'recharts';
import { motion } from 'framer-motion';
import MainLayout from '../components/layout/MainLayout';

function Analytics() {
  const [timeframe, setTimeframe] = useState('week');

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
    { domain: 'Health', value: 85, color: '#000000' },
    { domain: 'Finance', value: 80, color: '#333333' },
    { domain: 'Productivity', value: 87, color: '#666666' },
    { domain: 'Learning', value: 75, color: '#999999' },
    { domain: 'Social', value: 83, color: '#CCCCCC' },
  ];

  const radarData = [
    { subject: 'Consistency', A: 85 },
    { subject: 'Progress', A: 90 },
    { subject: 'Engagement', A: 78 },
    { subject: 'AI Helpfulness', A: 92 },
    { subject: 'Goal Clarity', A: 88 },
  ];

  const stats = [
    { label: 'Weekly Velocity', value: '+12.4%', icon: <TrendingUp className="text-green-500" /> },
    { label: 'Completion Rate', value: '88.2%', icon: <EmojiEvents className="text-orange-500" /> },
    { label: 'Avg. Cognitive Score', value: '91/100', icon: <Psychology className="text-purple-500" /> },
    { label: 'Momentum Streak', value: '14 Days', icon: <FlashOn className="text-blue-500" /> },
  ];

  return (
    <MainLayout>
      <div className="max-w-7xl mx-auto px-8 py-10">
        {/* Header */}
        <div className="flex flex-col md:flex-row md:items-end justify-between gap-6 mb-12">
          <div>
            <div className="flex items-center gap-2 mb-2 text-gray-400">
              <AutoAwesome className="text-sm" />
              <span className="text-[10px] font-bold uppercase tracking-widest text-purple-600">Advanced Intelligence Layer</span>
            </div>
            <h1 className="text-5xl font-bold text-gray-900 font-outfit tracking-tight">System Analytics <span className="text-gray-300">/</span></h1>
            <p className="text-lg text-gray-500 mt-2 font-inter max-w-xl">
              Orbit's deep-core analysis of your behavioral trajectories and success coefficients.
            </p>
          </div>
          <div className="flex bg-gray-50 p-1 rounded-2xl border border-gray-100 h-fit">
            {['week', 'month', 'year'].map((t) => (
              <button
                key={t}
                onClick={() => setTimeframe(t)}
                className={`px-6 py-2 rounded-xl text-xs font-bold uppercase tracking-widest transition-all ${timeframe === t ? 'bg-white text-gray-900 shadow-sm border border-gray-100' : 'text-gray-400 hover:text-gray-600'
                  }`}
              >
                {t}
              </button>
            ))}
          </div>
        </div>

        {/* Stats Grid */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-12">
          {stats.map((stat, idx) => (
            <motion.div
              key={stat.label}
              initial={{ opacity: 0, scale: 0.95 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ delay: idx * 0.1 }}
              className="glass-card p-6 rounded-3xl"
            >
              <div className="flex items-center justify-between mb-4">
                <span className="text-[10px] font-bold text-gray-400 uppercase tracking-widest">{stat.label}</span>
                {stat.icon}
              </div>
              <h3 className="text-3xl font-bold text-gray-900 font-outfit">{stat.value}</h3>
            </motion.div>
          ))}
        </div>

        {/* Charts Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 mb-12">
          {/* Velocity Chart */}
          <div className="lg:col-span-2 glass-card p-8 rounded-[40px]">
            <div className="flex items-center justify-between mb-8">
              <h3 className="text-xl font-bold text-gray-900 font-outfit">Velocity Trajectories</h3>
              <InfoOutlined className="text-gray-300 cursor-help" />
            </div>
            <div className="h-[400px] w-full">
              <ResponsiveContainer width="100%" height="100%">
                <LineChart data={progressData}>
                  <XAxis dataKey="date" axisLine={false} tickLine={false} tick={{ fontSize: 12, fill: '#94a3b8' }} />
                  <YAxis hide />
                  <RechartsTooltip
                    contentStyle={{ backgroundColor: 'rgba(255,255,255,0.9)', borderRadius: '16px', border: 'none', boxShadow: '0 10px 30px rgba(0,0,0,0.05)' }}
                  />
                  <Line type="monotone" dataKey="productivity" stroke="#000" strokeWidth={3} dot={false} />
                  <Line type="monotone" dataKey="health" stroke="#ccc" strokeWidth={2} strokeDasharray="5 5" dot={false} />
                </LineChart>
              </ResponsiveContainer>
            </div>
          </div>

          {/* Distribution */}
          <div className="glass-card p-8 rounded-[40px] flex flex-col items-center">
            <h3 className="text-xl font-bold text-gray-900 font-outfit self-start mb-8">Asset Distribution</h3>
            <div className="h-[300px] w-full relative">
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie
                    data={domainData}
                    innerRadius={80}
                    outerRadius={100}
                    paddingAngle={8}
                    dataKey="value"
                  >
                    {domainData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={entry.color} />
                    ))}
                  </Pie>
                </PieChart>
              </ResponsiveContainer>
              <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 text-center">
                <span className="text-3xl font-bold text-gray-900 font-outfit">84%</span>
                <p className="text-[10px] text-gray-400 uppercase font-bold">Overall</p>
              </div>
            </div>
            <div className="grid grid-cols-2 gap-4 w-full mt-4">
              {domainData.slice(0, 4).map(d => (
                <div key={d.domain} className="flex items-center gap-2">
                  <div className="w-2 h-2 rounded-full" style={{ background: d.color }} />
                  <span className="text-xs text-gray-500 font-medium">{d.domain}</span>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Intelligence Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Performance Radar */}
          <div className="glass-card p-8 rounded-[40px]">
            <h3 className="text-xl font-bold text-gray-900 font-outfit mb-8">Performance Spectrum</h3>
            <div className="h-[350px] w-full">
              <ResponsiveContainer width="100%" height="100%">
                <RadarChart data={radarData}>
                  <PolarGrid stroke="#f1f5f9" />
                  <PolarAngleAxis dataKey="subject" tick={{ fontSize: 10, fill: '#64748b' }} />
                  <Radar
                    name="Performance"
                    dataKey="A"
                    stroke="#000"
                    fill="#000"
                    fillOpacity={0.05}
                  />
                </RadarChart>
              </ResponsiveContainer>
            </div>
          </div>

          {/* AI Strategy Insights */}
          <div className="space-y-6 flex flex-col justify-between">
            <div className="bg-gray-950 p-8 rounded-[40px] text-white relative overflow-hidden">
              <div className="relative z-10">
                <div className="flex items-center gap-2 mb-6">
                  <div className="w-2 h-2 rounded-full bg-green-500 animate-pulse" />
                  <span className="text-[10px] font-bold uppercase tracking-widest text-gray-400">Strategic Signal Detected</span>
                </div>
                <h3 className="text-2xl font-bold mb-4 font-outfit leading-tight">Your deep-work efficiency is correlating with early morning cycles.</h3>
                <p className="text-gray-400 text-sm mb-8 leading-relaxed">Orbit recommends shifting "Cognitive Expansion" tasks to the 06:00 - 09:00 window to capitalize on neural peak.</p>
                <button className="flex items-center gap-2 text-sm font-bold group">
                  Apply Strategy <ArrowForward className="text-sm group-hover:translate-x-1 transition-transform" />
                </button>
              </div>
              <div className="absolute top-[-50%] right-[-20%] w-80 h-80 bg-white/5 rounded-full blur-3xl text-white" />
            </div>

            <div className="glass-card p-8 rounded-[32px] border border-gray-100">
              <div className="flex items-center gap-4 mb-4 text-orange-500">
                <InfoOutlined />
                <span className="text-sm font-bold">Maintenance Required</span>
              </div>
              <p className="text-gray-500 text-sm leading-relaxed mb-4">Your "Social Network" vector has dropped below optimal threshold. Schedule a connection event to restore balance.</p>
              <div className="w-full h-1 bg-gray-100 rounded-full overflow-hidden">
                <div className="w-[45%] h-full bg-orange-500 rounded-full" />
              </div>
            </div>
          </div>
        </div>
      </div>
    </MainLayout>
  );
}

export default Analytics;
