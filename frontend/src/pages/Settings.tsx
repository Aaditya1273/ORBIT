import React, { useState } from 'react';
import {
  Notifications,
  Shield,
  AutoAwesome,
  Tune,
  PersonOutline,
  ChevronRight
} from '@mui/icons-material';
import { motion } from 'framer-motion';
import toast from 'react-hot-toast';
import { useAuthStore } from '../stores/authStore';
import { useThemeStore } from '../stores/themeStore';
import MainLayout from '../components/layout/MainLayout';

const SettingsSection = ({ icon, title, subtitle, children }: { icon: React.ReactNode, title: string, subtitle: string, children: React.ReactNode }) => (
  <motion.div
    initial={{ opacity: 0, y: 20 }}
    whileInView={{ opacity: 1, y: 0 }}
    viewport={{ once: true }}
    className="glass-card p-10 rounded-[40px] mb-8 border border-gray-50 bg-white"
  >
    <div className="flex items-start justify-between mb-8">
      <div className="flex items-center gap-4">
        <div className="w-12 h-12 rounded-2xl bg-gray-950 flex items-center justify-center text-white">
          {icon}
        </div>
        <div>
          <h3 className="text-xl font-bold text-gray-900 font-outfit">{title}</h3>
          <p className="text-sm text-gray-400 font-inter">{subtitle}</p>
        </div>
      </div>
    </div>
    <div className="space-y-6">
      {children}
    </div>
  </motion.div>
);

const ToggleRow = ({ label, description, checked, onChange }: { label: string, description: string, checked: boolean, onChange: (val: boolean) => void }) => (
  <div className="flex items-center justify-between py-2">
    <div>
      <p className="text-sm font-bold text-gray-900 font-outfit">{label}</p>
      <p className="text-xs text-gray-400 font-inter">{description}</p>
    </div>
    <button
      onClick={() => onChange(!checked)}
      className={`w-12 h-6 rounded-full transition-all duration-300 relative ${checked ? 'bg-gray-950' : 'bg-gray-100'}`}
    >
      <div className={`absolute top-1 w-4 h-4 rounded-full bg-white transition-all duration-300 ${checked ? 'left-7' : 'left-1'}`} />
    </button>
  </div>
);

function Settings() {
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

  const handleSave = (msg: string) => {
    updateUser({ name: profile.name });
    toast.success(msg);
  };

  return (
    <MainLayout>
      <div className="max-w-5xl mx-auto px-8 py-10">
        {/* Header */}
        <div className="mb-12">
          <div className="flex items-center gap-2 mb-2 text-gray-400">
            <Tune className="text-sm" />
            <span className="text-[10px] font-bold uppercase tracking-widest text-gray-950 underline underline-offset-4">System Configuration</span>
          </div>
          <h1 className="text-5xl font-bold text-gray-900 font-outfit tracking-tight">Core Preferences</h1>
          <p className="text-lg text-gray-500 mt-2 font-inter max-w-xl">
            Calibrate Orbit's intelligence layer and customize your user experience.
          </p>
        </div>

        <div className="grid grid-cols-1 gap-4">
          {/* Identity Section */}
          <SettingsSection
            icon={<PersonOutline />}
            title="User Identity"
            subtitle="Manage your primary authentication data."
          >
            <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
              <div className="space-y-2">
                <label className="text-[10px] font-bold text-gray-400 uppercase tracking-widest ml-1">Full Name</label>
                <input
                  type="text"
                  value={profile.name}
                  onChange={(e) => setProfile({ ...profile, name: e.target.value })}
                  className="input-premium py-4"
                />
              </div>
              <div className="space-y-2">
                <label className="text-[10px] font-bold text-gray-400 uppercase tracking-widest ml-1">Network Identifier</label>
                <input
                  type="text"
                  value={profile.email}
                  disabled
                  className="input-premium py-4 bg-gray-50 cursor-not-allowed opacity-60"
                />
              </div>
            </div>
            <button
              onClick={() => handleSave('Identity updated')}
              className="btn-premium w-fit mt-4"
            >
              Commit Changes
            </button>
          </SettingsSection>

          {/* Intelligence Section */}
          <SettingsSection
            icon={<AutoAwesome />}
            title="AI Orchestration"
            subtitle="Fine-tune the intervention frequency and intelligence algorithms."
          >
            <div className="space-y-8">
              <div className="space-y-4">
                <p className="text-[10px] font-bold text-gray-400 uppercase tracking-widest ml-1">Intervention Frequency</p>
                <div className="flex gap-2 bg-gray-50 p-1.5 rounded-2xl w-fit">
                  {['low', 'medium', 'high'].map((freq) => (
                    <button
                      key={freq}
                      onClick={() => setAiSettings({ ...aiSettings, intervention_frequency: freq })}
                      className={`px-6 py-2 rounded-xl text-xs font-bold uppercase transition-all ${aiSettings.intervention_frequency === freq
                        ? 'bg-gray-950 text-white shadow-lg'
                        : 'text-gray-400 hover:text-gray-600'
                        }`}
                    >
                      {freq}
                    </button>
                  ))}
                </div>
              </div>

              <ToggleRow
                label="Autonomous Optimization"
                description="Allow Orbit to adjust intervention timing based on neural feedback."
                checked={aiSettings.auto_optimize}
                onChange={(val) => setAiSettings({ ...aiSettings, auto_optimize: val })}
              />
            </div>
          </SettingsSection>

          {/* Communication Section */}
          <SettingsSection
            icon={<Notifications />}
            title="Signal Management"
            subtitle="Configure how Orbit communicates critical insights."
          >
            <div className="space-y-4 divide-y divide-gray-50">
              <ToggleRow
                label="Daily Tactical Summary"
                description="Comprehensive briefing delivered at 07:00 local time."
                checked={notifications.daily_summary}
                onChange={(val) => setNotifications({ ...notifications, daily_summary: val })}
              />
              <ToggleRow
                label="Strategic Insights"
                description="Real-time behavioral pattern analysis notifications."
                checked={notifications.ai_insights}
                onChange={(val) => setNotifications({ ...notifications, ai_insights: val })}
              />
              <ToggleRow
                label="Vector Reminders"
                description="Timely signals for active life objectives."
                checked={notifications.goal_reminders}
                onChange={(val) => setNotifications({ ...notifications, goal_reminders: val })}
              />
            </div>
          </SettingsSection>

          {/* Security & System */}
          <SettingsSection
            icon={<Shield />}
            title="Security Protocols"
            subtitle="Control your data footprint and account safety."
          >
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <button className="p-4 border border-gray-100 rounded-2xl text-sm font-bold text-gray-900 hover:bg-gray-50 transition-colors flex items-center justify-between group">
                Change Access Key <ChevronRight className="text-gray-300 group-hover:text-gray-950" />
              </button>
              <button className="p-4 border border-gray-100 rounded-2xl text-sm font-bold text-gray-900 hover:bg-gray-50 transition-colors flex items-center justify-between group">
                Satellite Data Export <ChevronRight className="text-gray-300 group-hover:text-gray-950" />
              </button>
              <button className="p-4 border border-red-50 rounded-2xl text-sm font-bold text-red-500 hover:bg-red-50 transition-colors flex items-center justify-between group">
                Decommission Account <ChevronRight className="text-red-200 group-hover:text-red-500" />
              </button>
            </div>
          </SettingsSection>
        </div>

        {/* Footer/System ID */}
        <div className="mt-12 text-center">
          <p className="text-[10px] text-gray-300 font-bold uppercase tracking-[0.4em]">ORBIT Core OS v2.0.4-premium</p>
        </div>
      </div>
    </MainLayout>
  );
}

export default Settings;
