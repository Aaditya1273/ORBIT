import React from 'react';
import {
  Dashboard,
  EmojiEvents,
  Timeline,
  Settings,
  Psychology,
  AutoAwesome,
  ChevronLeft,
  ChevronRight,
  FiberManualRecord
} from '@mui/icons-material';
import { useNavigate, useLocation } from 'react-router-dom';
import { Tooltip } from '@mui/material';

const Sidebar: React.FC = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const [isCollapsed, setIsCollapsed] = React.useState(false);

  const mainMenuItems = [
    { text: 'Dashboard', icon: <Dashboard />, path: '/dashboard' },
    { text: 'Goals', icon: <EmojiEvents />, path: '/goals' },
    { text: 'Analytics', icon: <Timeline />, path: '/analytics' },
    { text: 'Settings', icon: <Settings />, path: '/settings' },
  ];

  const isActive = (path: string) => location.pathname === path;

  return (
    <aside
      className={`h-screen border-r border-gray-100 bg-white transition-all duration-300 ease-in-out flex flex-col z-40 ${isCollapsed ? 'w-20' : 'w-64'
        }`}
    >
      {/* Header Section */}
      <div className="p-4 flex items-center justify-between border-b border-gray-50 mb-4">
        {!isCollapsed && (
          <div className="flex items-center gap-3">
            <div className="w-8 h-8 rounded-lg bg-gray-900 border border-gray-800 flex items-center justify-center text-white">
              <Psychology className="text-xl" />
            </div>
            <div className="flex flex-col">
              <span className="text-sm font-bold text-gray-900 font-outfit uppercase tracking-wider">ORBIT</span>
              <span className="text-[10px] text-gray-400 font-medium">Life OS</span>
            </div>
          </div>
        )}
        {isCollapsed && (
          <div className="w-8 h-8 rounded-lg bg-gray-900 border border-gray-800 flex items-center justify-center text-white mx-auto">
            <Psychology className="text-xl" />
          </div>
        )}
      </div>

      {/* Main Menu */}
      <div className="flex-1 px-3 space-y-1">
        {mainMenuItems.map((item) => (
          <button
            key={item.text}
            onClick={() => navigate(item.path)}
            className={`w-full flex items-center gap-3 px-3 py-2.5 rounded-xl transition-all group relative ${isActive(item.path)
              ? 'bg-gray-950 text-white shadow-lg shadow-gray-200'
              : 'text-gray-500 hover:bg-gray-50 hover:text-gray-900'
              }`}
          >
            <div className={`${isActive(item.path) ? 'text-white' : 'text-gray-400 group-hover:text-gray-900 transition-colors'
              }`}>
              {item.icon}
            </div>
            {!isCollapsed && (
              <span className={`text-sm font-medium ${isActive(item.path) ? 'font-semibold' : ''}`}>
                {item.text}
              </span>
            )}
            {isActive(item.path) && !isCollapsed && (
              <div className="absolute right-3 w-1.5 h-1.5 rounded-full bg-white animate-pulse" />
            )}

            {isCollapsed && (
              <div className="absolute left-full ml-2 px-2 py-1 bg-gray-900 text-white text-xs rounded opacity-0 group-hover:opacity-100 transition-opacity z-50 pointer-events-none whitespace-nowrap">
                {item.text}
              </div>
            )}
          </button>
        ))}
      </div>

      {/* AI Intelligence Status */}
      <div className="p-4 mt-auto">
        <div className={`rounded-2xl border border-gray-100 p-4 transition-all ${isCollapsed ? 'opacity-0 scale-75' : 'bg-gray-50'
          }`}>
          {!isCollapsed && (
            <>
              <div className="flex items-center justify-between mb-3">
                <div className="flex items-center gap-2">
                  <div className="w-2 h-2 rounded-full bg-green-500 animate-pulse" />
                  <span className="text-[10px] font-bold text-gray-400 uppercase tracking-widest">AI Agent Online</span>
                </div>
                <AutoAwesome className="text-gray-400 text-sm" />
              </div>
              <div className="space-y-2">
                <div className="flex justify-between items-center text-[11px]">
                  <span className="text-gray-500">Core Intelligence</span>
                  <span className="font-semibold text-gray-900">98.4%</span>
                </div>
                <div className="w-full h-1 bg-gray-200 rounded-full overflow-hidden">
                  <div className="w-[98%] h-full bg-gray-900 rounded-full" />
                </div>
              </div>
            </>
          )}
        </div>
      </div>

      {/* Collapse Toggle */}
      <button
        onClick={() => setIsCollapsed(!isCollapsed)}
        className="w-full p-4 border-t border-gray-50 flex items-center justify-center text-gray-400 hover:text-gray-900 transition-colors hover:bg-gray-50"
      >
        {isCollapsed ? <ChevronRight /> : <ChevronLeft />}
      </button>
    </aside>
  );
};

export default Sidebar;