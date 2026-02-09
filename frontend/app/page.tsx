'use client';

import { motion } from 'framer-motion';
import { useRouter } from 'next/navigation';
import {
    AutoAwesome,
    Psychology,
    TrendingUp,
    DataObject,
    ArrowForward,
    CheckCircle
} from '@mui/icons-material';

export default function HomePage() {
    const router = useRouter();

    const features = [
        {
            icon: <Psychology className="text-3xl" />,
            title: 'Neural Intelligence',
            description: 'Advanced AI that learns your patterns and adapts interventions in real-time'
        },
        {
            icon: <TrendingUp className="text-3xl" />,
            title: 'Behavioral Science',
            description: 'Evidence-based strategies grounded in cutting-edge cognitive research'
        },
        {
            icon: <DataObject className="text-3xl" />,
            title: 'Complete Transparency',
            description: 'Full visibility into AI decision-making with explainable interventions'
        }
    ];

    const stats = [
        { value: '18.4k', label: 'Active Nodes' },
        { value: '99.9%', label: 'Uptime' },
        { value: '2.4M', label: 'Interventions' }
    ];

    return (
        <div className="min-h-screen cinematic-grid text-white overflow-hidden">
            {/* Header/Nav */}
            <motion.nav
                initial={{ y: -100, opacity: 0 }}
                animate={{ y: 0, opacity: 1 }}
                className="fixed top-0 left-0 right-0 z-50 border-b border-white/10 bg-slate-950/80 backdrop-blur-2xl"
            >
                <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
                    <div className="flex items-center gap-3">
                        <div className="w-10 h-10 rounded-xl bg-white flex items-center justify-center text-slate-950 font-bold shadow-2xl">
                            O
                        </div>
                        <span className="text-2xl font-outfit font-bold tracking-tight">ORBIT</span>
                    </div>

                    <div className="flex items-center gap-3">
                        <button
                            onClick={() => router.push('/login?mode=login')}
                            className="px-6 py-2.5 rounded-xl text-sm font-bold text-white/80 hover:text-white transition-all"
                        >
                            Sign In
                        </button>
                        <button
                            onClick={() => router.push('/login?mode=signup')}
                            className="px-6 py-2.5 bg-white text-slate-950 rounded-xl text-sm font-bold hover:bg-white/90 transition-all shadow-[0_0_30px_rgba(255,255,255,0.2)] flex items-center gap-2"
                        >
                            Get Started <ArrowForward className="text-sm" />
                        </button>
                    </div>
                </div>
            </motion.nav>

            {/* Hero Section */}
            <section className="relative pt-32 pb-20 px-6">
                <div className="max-w-7xl mx-auto">
                    <div className="grid grid-cols-1 lg:grid-cols-2 gap-16 items-center">
                        {/* Left: Hero Content */}
                        <motion.div
                            initial={{ opacity: 0, x: -50 }}
                            animate={{ opacity: 1, x: 0 }}
                            transition={{ delay: 0.2 }}
                        >
                            <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-white/5 border border-white/10 mb-8">
                                <AutoAwesome className="text-sm text-white" />
                                <span className="text-xs font-bold uppercase tracking-widest text-gray-400">
                                    World's Most Advanced AI Platform
                                </span>
                            </div>

                            <h1 className="text-7xl font-outfit font-bold mb-6 leading-[1.1] tracking-tight">
                                Optimize Your
                                <br />
                                <span className="bg-gradient-to-r from-white to-gray-400 bg-clip-text text-transparent">
                                    Human Potential
                                </span>
                            </h1>

                            <p className="text-xl text-gray-400 font-inter mb-10 leading-relaxed max-w-xl">
                                ORBIT is a sophisticated intelligence layer designed to refine behavioral patterns and maximize cognitive output through AI-driven interventions.
                            </p>

                            <div className="flex items-center gap-4 mb-12">
                                <button
                                    onClick={() => router.push('/login?mode=signup')}
                                    className="px-8 py-4 bg-white text-slate-950 rounded-2xl font-bold text-lg hover:bg-white/90 transition-all shadow-[0_0_40px_rgba(255,255,255,0.3)] flex items-center gap-2"
                                >
                                    Initialize Account <ArrowForward />
                                </button>
                                <button
                                    onClick={() => router.push('/login?mode=login')}
                                    className="px-8 py-4 bg-white/5 border border-white/10 rounded-2xl font-bold text-lg hover:bg-white/10 transition-all"
                                >
                                    Establish Link
                                </button>
                            </div>

                            {/* Stats */}
                            <div className="flex items-center gap-8 pt-8 border-t border-white/10">
                                {stats.map((stat, idx) => (
                                    <div key={idx}>
                                        <div className="text-3xl font-bold font-outfit">{stat.value}</div>
                                        <div className="text-xs text-gray-500 uppercase tracking-widest">{stat.label}</div>
                                    </div>
                                ))}
                            </div>
                        </motion.div>

                        {/* Right: Floating Card */}
                        <motion.div
                            initial={{ opacity: 0, scale: 0.9 }}
                            animate={{ opacity: 1, scale: 1 }}
                            transition={{ delay: 0.4 }}
                            className="relative"
                        >
                            <div className="glass-card p-10 rounded-[48px] border border-white/10 bg-white/5 backdrop-blur-3xl">
                                <div className="absolute -top-4 -right-4 w-20 h-20 bg-white/10 rounded-full blur-2xl"></div>
                                <div className="absolute -bottom-6 -left-6 w-32 h-32 bg-white/5 rounded-full blur-3xl"></div>

                                <div className="relative">
                                    <div className="flex items-center gap-3 mb-6">
                                        <div className="w-12 h-12 rounded-2xl bg-white/10 flex items-center justify-center">
                                            <Psychology className="text-2xl" />
                                        </div>
                                        <div>
                                            <div className="text-sm text-gray-400 uppercase tracking-widest">System Status</div>
                                            <div className="text-xl font-bold font-outfit">Operational</div>
                                        </div>
                                    </div>

                                    <div className="space-y-4 mb-6">
                                        {[
                                            'Neural Pattern Recognition',
                                            'Behavioral Optimization Engine',
                                            'Cognitive Enhancement Protocol',
                                            'Transparent Decision Framework'
                                        ].map((item, idx) => (
                                            <div key={idx} className="flex items-center gap-3">
                                                <CheckCircle className="text-lg text-green-400" />
                                                <span className="text-sm text-gray-300">{item}</span>
                                            </div>
                                        ))}
                                    </div>

                                    <div className="grid grid-cols-2 gap-4">
                                        <div className="p-4 rounded-2xl bg-white/5 border border-white/10">
                                            <div className="text-2xl font-bold font-outfit">247ms</div>
                                            <div className="text-xs text-gray-500 uppercase tracking-widest">Avg Response</div>
                                        </div>
                                        <div className="p-4 rounded-2xl bg-white/5 border border-white/10">
                                            <div className="text-2xl font-bold font-outfit">98.7%</div>
                                            <div className="text-xs text-gray-500 uppercase tracking-widest">Accuracy</div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </motion.div>
                    </div>
                </div>
            </section>

            {/* Features Section */}
            <section className="py-20 px-6">
                <div className="max-w-7xl mx-auto">
                    <motion.div
                        initial={{ opacity: 0, y: 30 }}
                        whileInView={{ opacity: 1, y: 0 }}
                        viewport={{ once: true }}
                        className="text-center mb-16"
                    >
                        <h2 className="text-5xl font-bold font-outfit mb-4">Intelligence Architecture</h2>
                        <p className="text-gray-400 text-lg max-w-2xl mx-auto">
                            Three pillars of autonomous optimization working in perfect harmony
                        </p>
                    </motion.div>

                    <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                        {features.map((feature, idx) => (
                            <motion.div
                                key={idx}
                                initial={{ opacity: 0, y: 30 }}
                                whileInView={{ opacity: 1, y: 0 }}
                                viewport={{ once: true }}
                                transition={{ delay: idx * 0.1 }}
                                className="p-8 rounded-[40px] bg-white/5 border border-white/10 hover:bg-white/10 transition-all group"
                            >
                                <div className="w-16 h-16 rounded-2xl bg-white/10 flex items-center justify-center mb-6 group-hover:bg-white/20 transition-all">
                                    {feature.icon}
                                </div>
                                <h3 className="text-2xl font-bold font-outfit mb-3">{feature.title}</h3>
                                <p className="text-gray-400 leading-relaxed">{feature.description}</p>
                            </motion.div>
                        ))}
                    </div>
                </div>
            </section>

            {/* CTA Section */}
            <section className="py-20 px-6">
                <div className="max-w-4xl mx-auto">
                    <motion.div
                        initial={{ opacity: 0, scale: 0.95 }}
                        whileInView={{ opacity: 1, scale: 1 }}
                        viewport={{ once: true }}
                        className="glass-card p-16 rounded-[48px] border border-white/10 bg-white/5 backdrop-blur-3xl text-center"
                    >
                        <h2 className="text-5xl font-bold font-outfit mb-6">Ready to Expand Your Orbit?</h2>
                        <p className="text-xl text-gray-400 mb-10 max-w-2xl mx-auto">
                            Join thousands of users optimizing their lives with AI-powered insights and interventions.
                        </p>
                        <button
                            onClick={() => router.push('/login?mode=signup')}
                            className="px-10 py-5 bg-white text-slate-950 rounded-2xl font-bold text-lg hover:bg-white/90 transition-all shadow-[0_0_50px_rgba(255,255,255,0.3)] inline-flex items-center gap-3"
                        >
                            Start Your Journey <ArrowForward className="text-xl" />
                        </button>
                    </motion.div>
                </div>
            </section>

            {/* Footer */}
            <footer className="py-10 px-6 border-t border-white/10">
                <div className="max-w-7xl mx-auto text-center">
                    <p className="text-xs text-gray-600 font-bold uppercase tracking-[0.4em]">
                        ORBIT Core OS v2.0.4-premium
                    </p>
                </div>
            </footer>
        </div>
    );
}
