import { motion } from 'framer-motion';
import { Image } from 'lucide-react';

const ImageSuggestion = ({ suggestion }) => {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="glass-card rounded-3xl p-8"
    >
      <div className="flex items-start gap-4">
        <div className="p-3 bg-purple-100 rounded-2xl">
          <Image className="w-6 h-6 text-purple-600" />
        </div>
        <div className="flex-1">
          <h3 className="text-lg font-bold text-slate-800 mb-2">
            🎨 Image Suggestion
          </h3>
          <p className="text-slate-600 leading-relaxed">
            {suggestion}
          </p>
        </div>
      </div>
    </motion.div>
  );
};

export default ImageSuggestion;