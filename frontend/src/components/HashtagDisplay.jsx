import { motion } from 'framer-motion';
import { Hash } from 'lucide-react';

const HashtagDisplay = ({ hashtags }) => {
  return (
    <div className="mb-6">
      <div className="flex items-center gap-2 mb-3">
        <Hash className="w-5 h-5 text-slate-600" />
        <span className="font-semibold text-slate-700">Suggested Hashtags</span>
      </div>
      <div className="flex flex-wrap gap-2">
        {hashtags.map((tag, index) => (
          <motion.span
            key={index}
            initial={{ opacity: 0, scale: 0 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: index * 0.1 }}
            className="px-3 py-1.5 bg-gradient-to-r from-primary-100 to-accent-100 text-primary-700 rounded-full text-sm font-medium hover:shadow-md transition-shadow cursor-pointer"
          >
            {tag}
          </motion.span>
        ))}
      </div>
    </div>
  );
};

export default HashtagDisplay;