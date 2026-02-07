import React from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuthStore } from '../stores/authStore';

function Dashboard() {
  const navigate = useNavigate();
  const { user, logout } = useAuthStore();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow">
        <div className="max-w-7xl mx-auto px-4 py-4 flex justify-between items-center">
          <div className="flex items-center space-x-4">
            <h1 className="text-2xl font-bold text-purple-600">🎯 ORBIT</h1>
            <nav className="hidden md:flex space-x-4">
              <button
                onClick={() => navigate('/dashboard')}
                className="px-3 py-2 rounded-md bg-purple-100 text-purple-700"
              >
                Dashboard
              </button>
              <button
                onClick={() => navigate('/goals')}
                className="px-3 py-2 rounded-md hover:bg-gray-100"
              >
                Goals
              </button>
              <button
                onClick={() => navigate('/analytics')}
                className="px-3 py-2 rounded-md hover:bg-gray-100"
              >
                Analytics
              </button>
              <button
                onClick={() => navigate('/settings')}
                className="px-3 py-2 rounded-md hover:bg-gray-100"
              >
                Settings
              </button>
            </nav>
          </div>
          <div className="flex items-center space-x-4">
            <span className="text-sm text-gray-600">
              {user?.name || user?.email}
            </span>
            <button
              onClick={handleLogout}
              className="px-4 py-2 bg-red-500 text-white rounded-md hover:bg-red-600"
            >
              Logout
            </button>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 py-8">
        {/* Welcome */}
        <div className="mb-8">
          <h2 className="text-3xl font-bold text-gray-900 mb-2">
            Welcome back, {user?.name}! 👋
          </h2>
          <p className="text-gray-600">
            Here's your life optimization dashboard
          </p>
        </div>

        {/* Stats Grid */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <div className="bg-white p-6 rounded-lg shadow">
            <div className="flex items-center justify-between mb-2">
              <span className="text-gray-600">Active Goals</span>
              <span className="text-2xl">🎯</span>
            </div>
            <p className="text-3xl font-bold text-purple-600">0</p>
            <p className="text-sm text-gray-500 mt-1">Start creating goals</p>
          </div>

          <div className="bg-white p-6 rounded-lg shadow">
            <div className="flex items-center justify-between mb-2">
              <span className="text-gray-600">Interventions</span>
              <span className="text-2xl">🤖</span>
            </div>
            <p className="text-3xl font-bold text-blue-600">0</p>
            <p className="text-sm text-gray-500 mt-1">AI suggestions</p>
          </div>

          <div className="bg-white p-6 rounded-lg shadow">
            <div className="flex items-center justify-between mb-2">
              <span className="text-gray-600">Success Rate</span>
              <span className="text-2xl">📈</span>
            </div>
            <p className="text-3xl font-bold text-green-600">0%</p>
            <p className="text-sm text-gray-500 mt-1">Complete goals to track</p>
          </div>

          <div className="bg-white p-6 rounded-lg shadow">
            <div className="flex items-center justify-between mb-2">
              <span className="text-gray-600">Streak</span>
              <span className="text-2xl">🔥</span>
            </div>
            <p className="text-3xl font-bold text-orange-600">0</p>
            <p className="text-sm text-gray-500 mt-1">Days active</p>
          </div>
        </div>

        {/* Quick Actions */}
        <div className="bg-white rounded-lg shadow p-6 mb-8">
          <h3 className="text-xl font-bold mb-4">Quick Actions</h3>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <button
              onClick={() => navigate('/goals')}
              className="p-4 border-2 border-purple-200 rounded-lg hover:border-purple-400 hover:bg-purple-50 transition"
            >
              <div className="text-3xl mb-2">🎯</div>
              <div className="font-semibold">Create Goal</div>
              <div className="text-sm text-gray-600">Set a new objective</div>
            </button>

            <button className="p-4 border-2 border-blue-200 rounded-lg hover:border-blue-400 hover:bg-blue-50 transition">
              <div className="text-3xl mb-2">📊</div>
              <div className="font-semibold">View Analytics</div>
              <div className="text-sm text-gray-600">Track your progress</div>
            </button>

            <button className="p-4 border-2 border-green-200 rounded-lg hover:border-green-400 hover:bg-green-50 transition">
              <div className="text-3xl mb-2">🤖</div>
              <div className="font-semibold">AI Insights</div>
              <div className="text-sm text-gray-600">Get recommendations</div>
            </button>
          </div>
        </div>

        {/* Getting Started */}
        <div className="bg-gradient-to-r from-purple-500 to-blue-500 rounded-lg shadow p-8 text-white">
          <h3 className="text-2xl font-bold mb-4">🚀 Getting Started with ORBIT</h3>
          <div className="space-y-3">
            <div className="flex items-start">
              <span className="mr-3">1️⃣</span>
              <div>
                <div className="font-semibold">Create Your First Goal</div>
                <div className="text-purple-100">Define what you want to achieve</div>
              </div>
            </div>
            <div className="flex items-start">
              <span className="mr-3">2️⃣</span>
              <div>
                <div className="font-semibold">Get AI Interventions</div>
                <div className="text-purple-100">Receive personalized suggestions</div>
              </div>
            </div>
            <div className="flex items-start">
              <span className="mr-3">3️⃣</span>
              <div>
                <div className="font-semibold">Track Your Progress</div>
                <div className="text-purple-100">Monitor your success rate</div>
              </div>
            </div>
          </div>
          <button
            onClick={() => navigate('/goals')}
            className="mt-6 px-6 py-3 bg-white text-purple-600 rounded-lg font-semibold hover:bg-gray-100 transition"
          >
            Create Your First Goal →
          </button>
        </div>
      </main>
    </div>
  );
}

export default Dashboard;
