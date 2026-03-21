import { useState } from 'react';
import { motion } from 'framer-motion';
import { Send, Settings } from 'lucide-react';
import { STYLE_OPTIONS, ENDPOINT_OPTIONS } from '../utils/constants';

const PostForm = ({ onSubmit, loading }) => {
  const [formData, setFormData] = useState({
    topic: '',
    style: 'professional',
    endpoint: 'enhanced',
    includeHashtags: true,
    maxLength: 2000,
  });

  const [showAdvanced, setShowAdvanced] = useState(false);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (formData.topic.trim()) {
      onSubmit(formData);
    }
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
      className="glass-card rounded-3xl p-8 mb-8"
    >
      <form onSubmit={handleSubmit} className="space-y-6">
        {/* Topic Input */}
        <div>
          <label className="block text-sm font-semibold text-slate-700 mb-2">
            What's your topic? 🎯
          </label>
          <input
            type="text"
            value={formData.topic}
            onChange={(e) => setFormData({ ...formData, topic: e.target.value })}
            placeholder="e.g., Artificial Intelligence, Remote Work, Sustainability..."
            className="input-field text-lg"
            disabled={loading}
            required
          />
          <p className="text-xs text-slate-500 mt-2">
            Enter any topic you want to create a LinkedIn post about
          </p>
        </div>

        {/* Style Selection */}
        <div>
          <label className="block text-sm font-semibold text-slate-700 mb-3">
            Choose your style ✨
          </label>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
            {STYLE_OPTIONS.map((option) => (
              <motion.button
                key={option.value}
                type="button"
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
                onClick={() => setFormData({ ...formData, style: option.value })}
                className={`p-4 rounded-xl border-2 transition-all duration-300 text-left ${
                  formData.style === option.value
                    ? 'border-primary-500 bg-primary-50 shadow-lg'
                    : 'border-slate-200 bg-white hover:border-primary-300'
                }`}
                disabled={loading}
              >
                <div className="text-2xl mb-2">{option.icon}</div>
                <div className="font-semibold text-slate-800">{option.label}</div>
                <div className="text-xs text-slate-500 mt-1">{option.description}</div>
              </motion.button>
            ))}
          </div>
        </div>

        {/* Endpoint Selection */}
        <div>
          <label className="block text-sm font-semibold text-slate-700 mb-3">
            Generation mode 🚀
          </label>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
            {ENDPOINT_OPTIONS.map((option) => (
              <motion.button
                key={option.value}
                type="button"
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
                onClick={() => setFormData({ ...formData, endpoint: option.value })}
                className={`p-4 rounded-xl border-2 transition-all duration-300 text-left ${
                  formData.endpoint === option.value
                    ? 'border-accent-500 bg-accent-50 shadow-lg'
                    : 'border-slate-200 bg-white hover:border-accent-300'
                }`}
                disabled={loading}
              >
                <div className="flex items-start justify-between">
                  <div>
                    <div className="text-2xl mb-2">{option.icon}</div>
                    <div className="font-semibold text-slate-800">{option.label}</div>
                    <div className="text-xs text-slate-500 mt-1">{option.description}</div>
                  </div>
                  <div className="text-xs bg-green-100 text-green-700 px-2 py-1 rounded-full font-medium">
                    {option.quality}
                  </div>
                </div>
              </motion.button>
            ))}
          </div>
        </div>

        {/* Advanced Options */}
        <div>
          <button
            type="button"
            onClick={() => setShowAdvanced(!showAdvanced)}
            className="flex items-center gap-2 text-sm text-slate-600 hover:text-primary-600 transition-colors"
          >
            <Settings className="w-4 h-4" />
            <span>{showAdvanced ? 'Hide' : 'Show'} Advanced Options</span>
          </button>

          {showAdvanced && (
            <motion.div
              initial={{ opacity: 0, height: 0 }}
              animate={{ opacity: 1, height: 'auto' }}
              exit={{ opacity: 0, height: 0 }}
              className="mt-4 space-y-4"
            >
              <div className="flex items-center gap-3">
                <input
                  type="checkbox"
                  id="hashtags"
                  checked={formData.includeHashtags}
                  onChange={(e) => setFormData({ ...formData, includeHashtags: e.target.checked })}
                  className="w-5 h-5 text-primary-600 rounded focus:ring-2 focus:ring-primary-500"
                  disabled={loading}
                />
                <label htmlFor="hashtags" className="text-sm text-slate-700 font-medium">
                  Include hashtags
                </label>
              </div>

              <div>
                <label className="block text-sm font-medium text-slate-700 mb-2">
                  Max length: {formData.maxLength} characters
                </label>
                <input
                  type="range"
                  min="500"
                  max="3000"
                  step="100"
                  value={formData.maxLength}
                  onChange={(e) => setFormData({ ...formData, maxLength: parseInt(e.target.value) })}
                  className="w-full h-2 bg-slate-200 rounded-lg appearance-none cursor-pointer accent-primary-600"
                  disabled={loading}
                />
              </div>
            </motion.div>
          )}
        </div>

        {/* Submit Button */}
        <motion.button
          type="submit"
          whileHover={{ scale: 1.02 }}
          whileTap={{ scale: 0.98 }}
          disabled={loading || !formData.topic.trim()}
          className="btn-primary w-full flex items-center justify-center gap-2 text-lg"
        >
          {loading ? (
            <>
              <motion.div
                animate={{ rotate: 360 }}
                transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
              >
                <Sparkles className="w-5 h-5" />
              </motion.div>
              <span>Generating...</span>
            </>
          ) : (
            <>
              <Send className="w-5 h-5" />
              <span>Generate Post</span>
            </>
          )}
        </motion.button>
      </form>
    </motion.div>
  );
};

export default PostForm;