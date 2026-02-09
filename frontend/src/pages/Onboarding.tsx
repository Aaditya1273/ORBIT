import React, { useState } from 'react';
import {
  FitnessCenter,
  AttachMoney,
  Work,
  School,
  People,
  ArrowForward,
  ArrowBack,
  CheckCircle,
  AutoAwesome,
  RocketLaunch
} from '@mui/icons-material';
import { motion, AnimatePresence } from 'framer-motion';
import { useRouter } from 'next/navigation';
import toast from 'react-hot-toast';
import { useAuthStore } from '../stores/authStore';

const domains = [
  { id: 'health', name: 'Physical Integrity', icon: <FitnessCenter />, description: 'Optimize your biological foundation' },
  { id: 'finance', name: 'Capital Flow', icon: <AttachMoney />, description: 'Stabilize and scale your fiscal footprint' },
  { id: 'productivity', name: 'Output Optimization', icon: <Work />, description: 'Maximize your daily execution coefficients' },
  { id: 'learning', name: 'Cognitive Expansion', icon: <School />, description: 'Broaden your neural and skill architecture' },
  { id: 'social', name: 'Social Network', icon: <People />, description: 'Enhance your human connection vectors' },
];

const Onboarding: React.FC = () => {
  const navigate = useRouter();
  const { updateUser } = useAuthStore();
  const [activeStep, setActiveStep] = useState(0);
  const [selectedDomains, setSelectedDomains] = useState<string[]>([]);
  const [goals, setGoals] = useState<{ [key: string]: string }>({});

  const steps = ['Initialization', 'Vectors', 'Objectives', 'Link Established'];

  const handleNext = () => {
    if (activeStep === 1 && selectedDomains.length === 0) {
      toast.error('Initialization requires at least one primary vector.');
      return;
    }
    setActiveStep((prev) => prev + 1);
  };

  const handleBack = () => {
    setActiveStep((prev) => prev - 1);
  };

  const handleComplete = () => {
    updateUser({ onboarding_completed: true });
    toast.success('System link established. Welcome to ORBIT.');
    router.push('/dashboard');
  };

  const toggleDomain = (domainId: string) => {
    setSelectedDomains((prev) =>
      prev.includes(domainId)
        ? prev.filter((id) => id !== domainId)
        : [...prev, domainId]
    );
  };

  return (
    <div className="min-h-screen cinematic-grid flex items-center justify-center p-6 relative">
      <div className="absolute top-10 left-10 flex items-center gap-2">
        <div className="w-8 h-8 rounded-lg bg-white flex items-center justify-center text-slate-950 font-bold shadow-2xl">
          O
        </div>
        <span className="text-white font-outfit font-bold tracking-widest text-xs uppercase">Orbit v2.0 Initializer</span>
      </div>

      <div className="max-w-4xl w-full">
        <motion.div
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          className="glass-card p-12 rounded-[48px] border border-white/10 bg-slate-900/40 backdrop-blur-3xl"
        >
          {/* Custom Stepper */}
          <div className="flex justify-between items-center mb-16 px-4">
            {steps.map((step, idx) => (
              <div key={step} className="flex flex-col items-center gap-2 group">
                <div className={`w-8 h-1 rounded-full transition-all duration-500 ${idx <= activeStep ? 'bg-white w-12' : 'bg-white/10'}`} />
                <span className={`text-[10px] font-bold uppercase tracking-widest transition-colors ${idx <= activeStep ? 'text-white' : 'text-gray-500'}`}>
                  {step}
                </span>
              </div>
            ))}
          </div>

          <AnimatePresence mode="wait">
            {/* Step 0: Welcome */}
            {activeStep === 0 && (
              <motion.div
                key="step0"
                initial={{ opacity: 0, x: 20 }}
                animate={{ opacity: 1, x: 0 }}
                exit={{ opacity: 0, x: -20 }}
                className="text-center"
              >
                <div className="w-20 h-20 bg-white/5 rounded-3xl flex items-center justify-center mx-auto mb-8 text-white shadow-2xl border border-white/10">
                  <AutoAwesome className="text-4xl" />
                </div>
                <h1 className="text-5xl font-bold text-white font-outfit mb-6 tracking-tight">Expand Your Orbit <span className="text-white/30">/</span></h1>
                <p className="text-gray-400 text-lg font-inter max-w-xl mx-auto leading-relaxed mb-10">
                  Welcome to the next generation of life optimization. Orbit uses predictive intelligence to synchronize your daily actions with your ultimate potential.
                </p>
                <div className="flex justify-center gap-4 flex-wrap">
                  {['AI Orchestration', 'Neural Feedback', 'Vector Integration'].map(tag => (
                    <div key={tag} className="px-4 py-2 rounded-full border border-white/10 text-[10px] uppercase font-bold text-gray-400 tracking-widest">
                      {tag}
                    </div>
                  ))}
                </div>
              </motion.div>
            )}

            {/* Step 1: Choose Domains */}
            {activeStep === 1 && (
              <motion.div
                key="step1"
                initial={{ opacity: 0, x: 20 }}
                animate={{ opacity: 1, x: 0 }}
                exit={{ opacity: 0, x: -20 }}
              >
                <h2 className="text-3xl font-bold text-white font-outfit mb-2">Select Primary Vectors</h2>
                <p className="text-gray-400 text-sm mb-10 font-inter">Identify the core dimensions of your life that require system optimization.</p>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  {domains.map((domain) => (
                    <button
                      key={domain.id}
                      onClick={() => toggleDomain(domain.id)}
                      className={`p-6 rounded-3xl border transition-all text-left flex items-start gap-4 group ${selectedDomains.includes(domain.id)
                        ? 'bg-white border-white'
                        : 'bg-white/5 border-white/10 hover:border-white/30'
                        }`}
                    >
                      <div className={`p-3 rounded-2xl transition-colors ${selectedDomains.includes(domain.id) ? 'bg-slate-900 text-white' : 'bg-white/5 text-gray-400 group-hover:text-white'
                        }`}>
                        {domain.icon}
                      </div>
                      <div>
                        <h4 className={`font-bold font-outfit mb-1 ${selectedDomains.includes(domain.id) ? 'text-slate-900' : 'text-white'
                          }`}>{domain.name}</h4>
                        <p className={`text-xs ${selectedDomains.includes(domain.id) ? 'text-slate-600' : 'text-gray-500'
                          }`}>{domain.description}</p>
                      </div>
                    </button>
                  ))}
                </div>
              </motion.div>
            )}

            {/* Step 2: Set Goals */}
            {activeStep === 2 && (
              <motion.div
                key="step2"
                initial={{ opacity: 0, x: 20 }}
                animate={{ opacity: 1, x: 0 }}
                exit={{ opacity: 0, x: -20 }}
              >
                <h2 className="text-3xl font-bold text-white font-outfit mb-2">Configure Objectives</h2>
                <p className="text-gray-400 text-sm mb-10 font-inter">Define the specific targets for each selected vector.</p>

                <div className="space-y-6 max-h-[400px] overflow-y-auto pr-4 custom-scrollbar">
                  {selectedDomains.map((domainId) => {
                    const domain = domains.find((d) => d.id === domainId);
                    return (
                      <div key={domainId} className="space-y-3">
                        <div className="flex items-center gap-2 text-white">
                          {domain?.icon}
                          <span className="text-[10px] font-bold uppercase tracking-widest">{domain?.name} Target</span>
                        </div>
                        <textarea
                          rows={2}
                          placeholder={`Enter objective for ${domain?.name}...`}
                          className="w-full bg-white/5 border border-white/10 rounded-2xl p-4 text-white text-sm placeholder:text-gray-600 focus:outline-none focus:border-white/30 transition-all resize-none"
                          value={goals[domainId] || ''}
                          onChange={(e) => setGoals({ ...goals, [domainId]: e.target.value })}
                        />
                      </div>
                    );
                  })}
                </div>
              </motion.div>
            )}

            {/* Step 3: Complete */}
            {activeStep === 3 && (
              <motion.div
                key="step3"
                initial={{ opacity: 0, scale: 0.95 }}
                animate={{ opacity: 1, scale: 1 }}
                className="text-center"
              >
                <div className="w-24 h-24 bg-white rounded-full flex items-center justify-center mx-auto mb-8 text-slate-950 shadow-[0_0_50px_rgba(255,255,255,0.3)]">
                  <CheckCircle className="text-5xl" />
                </div>
                <h2 className="text-4xl font-bold text-white font-outfit mb-4">Link Established</h2>
                <p className="text-gray-400 text-lg font-inter max-w-md mx-auto leading-relaxed mb-10">
                  Your life footprint is now synced with Orbit Core. AI orchestration is active and ready for your first command.
                </p>
              </motion.div>
            )}
          </AnimatePresence>

          {/* Navigation Buttons */}
          <div className="flex justify-between items-center mt-16 pt-8 border-t border-white/5">
            <button
              onClick={handleBack}
              disabled={activeStep === 0}
              className={`flex items-center gap-2 text-sm font-bold transition-all ${activeStep === 0 ? 'opacity-0 cursor-default' : 'text-gray-500 hover:text-white'
                }`}
            >
              <ArrowBack className="text-sm" /> Previous Strategy
            </button>

            {activeStep === steps.length - 1 ? (
              <button
                onClick={handleComplete}
                className="bg-white text-slate-950 px-10 py-4 rounded-2xl font-bold hover:bg-white/90 transition-all flex items-center gap-2 shadow-[0_0_30px_rgba(255,255,255,0.2)]"
              >
                Enter ORBIT <RocketLaunch className="text-sm" />
              </button>
            ) : (
              <button
                onClick={handleNext}
                className="bg-white/10 text-white border border-white/10 px-10 py-4 rounded-2xl font-bold hover:bg-white hover:text-slate-950 transition-all flex items-center gap-2"
              >
                Proceed <ArrowForward className="text-sm" />
              </button>
            )}
          </div>
        </motion.div>
      </div>
    </div>
  );
};

export default Onboarding;
