import { motion } from 'framer-motion';
import { Sparkles, Zap, TrendingUp } from 'lucide-react';

const Hero = () => {
  return (
    <motion.div
      initial={{ opacity: 0, y: -20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.6 }}
      className="text-center mb-12"
    >
      <div className="inline-block mb-4">
        <motion.div
          animate={{ rotate: 360 }}
          transition={{ duration: 20, repeat: Infinity, ease: "linear" }}
          className="inline-block"
        >
          <Sparkles className="w-16 h-16 text-primary-600" />
        </motion.div>
      </div>
      
      <h1 className="text-5xl md:text-6xl font-bold mb-4">
        <span className="gradient-text">Engage AI</span>
        <br />
      </h1>
      
      <p className="text-xl text-slate-600 mb-6 max-w-2xl mx-auto">
        Transform your ideas into engaging LinkedIn content in seconds with our 
        advanced AI powered workflow
      </p>
      
      <div className="flex flex-wrap justify-center gap-6 text-sm">
        <motion.div
          whileHover={{ scale: 1.05 }}
          className="flex items-center gap-2 px-4 py-2 bg-white/60 backdrop-blur rounded-full shadow-md"
        >
          <Zap className="w-5 h-5 text-yellow-500" />
          <span className="font-semibold">95% Success Rate</span>
        </motion.div>
        
        <motion.div
          whileHover={{ scale: 1.05 }}
          className="flex items-center gap-2 px-4 py-2 bg-white/60 backdrop-blur rounded-full shadow-md"
        >
          <TrendingUp className="w-5 h-5 text-green-500" />
          <span className="font-semibold">8.5/10 Quality Score</span>
        </motion.div>
        
        <motion.div
          whileHover={{ scale: 1.05 }}
          className="flex items-center gap-2 px-4 py-2 bg-white/60 backdrop-blur rounded-full shadow-md"
        >
          <Sparkles className="w-5 h-5 text-purple-500" />
          <span className="font-semibold">1000+ Posts Generated</span>
        </motion.div>
      </div>
    </motion.div>
  );
};

export default Hero;