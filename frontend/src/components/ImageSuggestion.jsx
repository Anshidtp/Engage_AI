import { motion } from 'framer-motion';
import { Image } from 'lucide-react';

const ImageSuggestion = ({ suggestion }) => {
  const isUrl = suggestion?.startsWith("http");

  // fallback image if not URL
  const fallbackImage = suggestion
    ? `https://source.unsplash.com/800x400/?${encodeURIComponent(suggestion)}`
    : null;

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
          <h3 className="text-lg font-bold text-slate-800 mb-3">
            🎨 Image Suggestion
          </h3>

          {(isUrl || fallbackImage) ? (
            <img
              src={isUrl ? suggestion : fallbackImage}
              alt="Suggested"
              className="rounded-xl w-full max-h-80 object-cover border"
            />
          ) : (
            <p className="text-slate-600">{suggestion}</p>
          )}
        </div>
      </div>
    </motion.div>
  );
};

export default ImageSuggestion;