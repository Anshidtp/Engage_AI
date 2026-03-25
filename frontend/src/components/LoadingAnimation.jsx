import { motion, AnimatePresence } from 'framer-motion';
import { useState, useEffect } from 'react';
import { LOADING_MESSAGES } from '../utils/constants';
import { Sparkles, Zap, TrendingUp, Search, FileText, Target, CheckCircle } from 'lucide-react';

const LoadingAnimation = ({ plan = 'standard' }) => {
  const messages = LOADING_MESSAGES[plan] || LOADING_MESSAGES.standard;
  const [messageIndex, setMessageIndex] = useState(0);
  const [progress, setProgress] = useState(0);

  useEffect(() => {
    const messageInterval = setInterval(() => {
      setMessageIndex((prev) => (prev + 1) % messages.length);
    }, plan === 'pro' ? 4000 : 3000);

    const progressInterval = setInterval(() => {
      setProgress((prev) => {
        if (prev >= 95) return prev;
        return prev + Math.random() * (plan === 'pro' ? 5 : 8);
      });
    }, 500);

    return () => {
      clearInterval(messageInterval);
      clearInterval(progressInterval);
    };
  }, [plan, messages.length]);

  const icons = plan === 'pro' 
    ? [Search, FileText, Target, Sparkles, CheckCircle, Zap, TrendingUp]
    : [Search, Sparkles, Zap, TrendingUp];
  const Icon = icons[messageIndex % icons.length];

  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.95 }}
      animate={{ opacity: 1, scale: 1 }}
      exit={{ opacity: 0, scale: 0.95 }}
      className="glass-card rounded-3xl p-12 text-center"
    >
      <div className="max-w-md mx-auto space-y-8">
        {/* Plan Badge */}
        <div className="inline-block px-4 py-2 bg-gradient-to-r from-primary-500 to-accent-500 text-white rounded-full text-sm font-semibold">
          {plan === 'pro' ? '🚀 Pro Plan' : '⚡ Standard Plan'}
        </div>

        {/* Animated Icon */}
        <motion.div
          animate={{ 
            rotate: [0, 360],
            scale: [1, 1.2, 1],
          }}
          transition={{ 
            duration: 3, 
            repeat: Infinity,
            ease: "easeInOut"
          }}
          className="inline-block"
        >
          <div className="relative">
            <motion.div
              animate={{ scale: [1, 1.5, 1] }}
              transition={{ duration: 2, repeat: Infinity }}
              className="absolute inset-0 bg-primary-400 rounded-full blur-xl opacity-30"
            />
            <Icon className="w-20 h-20 text-primary-600 relative" />
          </div>
        </motion.div>

        {/* Loading Messages */}
        <div className="h-20">
          <AnimatePresence mode="wait">
            <motion.div
              key={messageIndex}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              transition={{ duration: 0.5 }}
              className="text-xl font-semibold text-slate-700"
            >
              {messages[messageIndex]}
            </motion.div>
          </AnimatePresence>
        </div>

        {/* Progress Bar */}
        <div className="space-y-2">
          <div className="w-full h-3 bg-slate-200 rounded-full overflow-hidden">
            <motion.div
              initial={{ width: 0 }}
              animate={{ width: `${progress}%` }}
              transition={{ duration: 0.5 }}
              className={`h-full rounded-full ${
                plan === 'pro'
                  ? 'bg-gradient-to-r from-amber-500 via-orange-500 to-primary-500'
                  : 'bg-gradient-to-r from-primary-500 to-accent-500'
              }`}
            />
          </div>
          <p className="text-sm text-slate-500">
            {Math.round(progress)}% complete
          </p>
        </div>

        {/* Workflow Steps */}
        <div className={`grid gap-2 ${plan === 'pro' ? 'grid-cols-7' : 'grid-cols-4'}`}>
          {[...Array(plan === 'pro' ? 7 : 4)].map((_, i) => (
            <motion.div
              key={i}
              initial={{ scale: 0 }}
              animate={{ 
                scale: i <= messageIndex ? 1 : 0.7,
                backgroundColor: i <= messageIndex ? '#0ea5e9' : '#e2e8f0'
              }}
              transition={{ delay: i * 0.1 }}
              className="h-2 rounded-full"
            />
          ))}
        </div>

        <p className="text-xs text-slate-500">
          {plan === 'pro' ? 'Using advanced LangGraph workflow...' : 'Generating your content...'}
        </p>
      </div>
    </motion.div>
  );
};

export default LoadingAnimation;