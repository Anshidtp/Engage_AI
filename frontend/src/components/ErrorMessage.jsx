import { motion } from 'framer-motion';
import { AlertCircle, RefreshCw } from 'lucide-react';

const ErrorMessage = ({ message, onRetry }) => {
  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.9 }}
      animate={{ opacity: 1, scale: 1 }}
      className="glass-card rounded-3xl p-8 border-2 border-red-200"
    >
      <div className="text-center max-w-md mx-auto">
        <motion.div
          animate={{ rotate: [0, 10, -10, 0] }}
          transition={{ duration: 0.5, repeat: 3 }}
          className="inline-block mb-4"
        >
          <AlertCircle className="w-16 h-16 text-red-500" />
        </motion.div>

        <h3 className="text-xl font-bold text-slate-800 mb-2">
          Oops! Something went wrong
        </h3>

        <p className="text-slate-600 mb-6">
          {message}
        </p>

        <motion.button
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
          onClick={onRetry}
          className="btn-primary inline-flex items-center gap-2"
        >
          <RefreshCw className="w-5 h-5" />
          <span>Try Again</span>
        </motion.button>
      </div>
    </motion.div>
  );
};

export default ErrorMessage;