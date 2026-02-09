import React, { useState } from 'react';
import { useRouter } from 'next/navigation';
import {
  Notifications,
  Search,
  Menu as MenuIcon,
  Psychology,
  AccountCircle,
  Settings,
  Logout
} from '@mui/icons-material';
import {
  Badge,
  Avatar,
  Tooltip,
  IconButton
} from '@mui/material';
import { useAuthStore } from '../../stores/authStore';

const Navbar: React.FC = () => {
  const navigate = useRouter();
  const { user, logout } = useAuthStore();
  const [showProfileMenu, setShowProfileMenu] = useState(false);

  const handleLogout = () => {
    logout();
    router.push('/login');
  };

  return (
    <nav className="nav-blur px-6 py-3 flex items-center justify-between">
      {/* Left Section: Logo & Search */}
      <div className="flex items-center gap-8">
        <div
          className="flex items-center gap-2 cursor-pointer group"
          onClick={() => router.push('/dashboard')}
        >
          <div className="w-10 h-10 rounded-xl bg-gray-950 flex items-center justify-center text-white shadow-lg group-hover:scale-110 transition-transform duration-300">
            <Psychology className="text-2xl" />
          </div>
          <span className="text-xl font-bold tracking-tight text-gray-900 font-outfit">
            ORBIT
          </span>
        </div>

        <div className="hidden md:flex items-center relative">
          <Search className="absolute left-3 text-gray-400 text-sm" />
          <input
            type="text"
            placeholder="Search goals or insights..."
            className="pl-10 pr-4 py-2 bg-gray-50 border border-gray-100 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-gray-900/10 focus:bg-white transition-all w-64 font-inter"
          />
        </div>
      </div>

      {/* Right Section: Actions */}
      <div className="flex items-center gap-4">
        <Tooltip title="Notifications">
          <IconButton className="text-gray-600 hover:bg-gray-100/50">
            <Badge badgeContent={3} color="primary" variant="dot">
              <Notifications className="text-[22px]" />
            </Badge>
          </IconButton>
        </Tooltip>

        <div className="h-6 w-[1px] bg-gray-200 mx-2" />

        <div className="relative">
          <button
            onClick={() => setShowProfileMenu(!showProfileMenu)}
            className="flex items-center gap-3 p-1 rounded-full hover:bg-gray-100 transition-colors"
          >
            <div className="flex flex-col items-end hidden sm:flex">
              <span className="text-xs font-semibold text-gray-900">{user?.name || 'User'}</span>
              <span className="text-[10px] text-gray-500 font-medium">Pro Plan</span>
            </div>
            <Avatar
              className="w-9 h-9 border border-gray-200 shadow-sm"
              sx={{ bgcolor: 'white', color: 'black' }}
            >
              {user?.name?.charAt(0) || 'U'}
            </Avatar>
          </button>

          {showProfileMenu && (
            <div className="absolute right-0 mt-3 w-56 glass-card rounded-2xl py-2 z-[100] animate-in fade-in zoom-in duration-200 origin-top-right">
              <div className="px-4 py-2 mb-2">
                <p className="text-xs text-gray-400 font-semibold uppercase tracking-wider">Account</p>
              </div>
              <button
                onClick={() => router.push('/settings')}
                className="w-full px-4 py-2.5 flex items-center gap-3 text-sm text-gray-700 hover:bg-gray-50 transition-colors"
              >
                <Settings className="text-lg text-gray-400" />
                <span>Settings</span>
              </button>
              <button
                onClick={() => router.push('/settings')}
                className="w-full px-4 py-2.5 flex items-center gap-3 text-sm text-gray-700 hover:bg-gray-50 transition-colors"
              >
                <AccountCircle className="text-lg text-gray-400" />
                <span>My Profile</span>
              </button>
              <div className="h-[1px] bg-gray-100 my-2 mx-2" />
              <button
                onClick={handleLogout}
                className="w-full px-4 py-2.5 flex items-center gap-3 text-sm text-red-600 hover:bg-red-50 transition-colors"
              >
                <Logout className="text-lg" />
                <span>Logout</span>
              </button>
            </div>
          )}
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
