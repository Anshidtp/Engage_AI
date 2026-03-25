import { motion } from 'framer-motion';
import { Copy, Check, RefreshCw, Download, Linkedin } from 'lucide-react';
import { useState } from 'react';
import toast from 'react-hot-toast';
import { shareToLinkedIn, copyToClipboard } from '../utils/linkedinShare';
import NewsSourceCard from './NewsSourceCard';
import HashtagDisplay from './HashtagDisplay';
import ImageSuggestion from './ImageSuggestion';

const GeneratedPost = ({ data, onReset, plan }) => {
  const [copied, setCopied] = useState(false);
  const uniqueHashtags = [...new Set(data?.hashtags || [])];
  const [showSources, setShowSources] = useState(false);

  const handleCopy = async () => {
    const fullPost = `${data.linkedin_post}\n\n${uniqueHashtags?.join(' ') || ''}`;
    const success = await copyToClipboard(fullPost);
    
    if (success) {
      setCopied(true);
      toast.success('Copied to clipboard!');
      setTimeout(() => setCopied(false), 2000);
    }
  };

  const handleLinkedInShare = () => {
    shareToLinkedIn(data.linkedin_post, uniqueHashtags, data.image_suggestion);
    toast.success('Post copied! Opening LinkedIn...', {
      icon: '🔗',
      style: {
        background: '#0A66C2',
        color: '#fff',
      },
    });
  };

  const handleDownload = () => {
    const content = `${data.linkedin_post}\n\n${uniqueHashtags?.join(' ') || ''}\n\nImage Suggestion: ${data.image_suggestion || 'N/A'}\n\nGenerated with ${plan === 'pro' ? 'Pro' : 'Standard'} Plan`;
    const blob = new Blob([content], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `linkedin-post-${data.topic.replace(/\s+/g, '-').toLowerCase()}.txt`;
    a.click();
    toast.success('Downloaded!');
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
      className="space-y-6"
    >
      {/* Main Post Card */}
      <div className="glass-card rounded-3xl p-8">
        <div className="flex items-start justify-between mb-6">
          <div>
            <div className="flex items-center gap-2 mb-2">
              <h2 className="text-2xl font-bold text-slate-800">
                Your LinkedIn Post ✨
              </h2>
              <span className={`text-xs font-bold px-3 py-1 rounded-full ${
                plan === 'pro'
                  ? 'bg-gradient-to-r from-amber-400 to-orange-500 text-white'
                  : 'bg-blue-100 text-blue-700'
              }`}>
                {plan === 'pro' ? '🚀 Pro' : '⚡ Standard'}
              </span>
            </div>
            <p className="text-sm text-slate-500">
              Topic: <span className="font-semibold text-slate-700">{data.topic?.toUpperCase()}</span>
            </p>
          </div>
          
          <div className="flex items-center gap-2">
            {data.quality_score && plan === 'pro' && (
              <div className="flex items-center gap-2 px-4 py-2 bg-green-100 text-green-700 rounded-full text-sm font-semibold">
                ⭐ {data.quality_score.toFixed(1)}/10
              </div>
            )}

            {data.news_sources?.length > 0 && (
              <button
                onClick={() => setShowSources(true)}
                className="text-xs px-3 py-1 bg-slate-100 hover:bg-slate-200 rounded-full font-medium"
              >
                📰 Sources ({data.news_sources.length})
              </button>
            )}
          </div>
        </div>

        {/* Post Content */}
        <div className="bg-gradient-to-br from-white to-slate-50 rounded-2xl p-6 mb-6 border-2 border-slate-100 shadow-inner">
          <div className="prose prose-slate max-w-none">
            <pre className="whitespace-pre-wrap font-sans text-slate-700 leading-relaxed text-[15px]">
              {data.linkedin_post}
            </pre>
          </div>
        </div>

        {/* Hashtags */}
        {data.hashtags && data.hashtags.length > 0 && (
          <HashtagDisplay hashtags={uniqueHashtags} />
        )}

        {/* Stats */}
        <div className="flex flex-wrap gap-3 mb-6 text-sm">
          <div className="flex items-center gap-2 px-4 py-2 bg-blue-50 rounded-lg">
            <span className="text-blue-600 font-semibold">Words:</span>
            <span className="text-slate-700 font-bold">{data.word_count}</span>
          </div>
          <div className="flex items-center gap-2 px-4 py-2 bg-purple-50 rounded-lg">
            <span className="text-purple-600 font-semibold">Characters:</span>
            <span className="text-slate-700 font-bold">{data.character_count}</span>
          </div>
          {data.news_sources && (
            <div className="flex items-center gap-2 px-4 py-2 bg-green-50 rounded-lg">
              <span className="text-green-600 font-semibold">Sources:</span>
              <span className="text-slate-700 font-bold">{data.news_sources.length}</span>
            </div>
          )}
        </div>

        {/* Action Buttons */}
        <div className="flex flex-wrap gap-3">
          {/* LinkedIn Share Button - Primary */}
          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={handleLinkedInShare}
            className="flex items-center gap-2 px-8 py-3 bg-[#0A66C2] hover:bg-[#004182] text-white rounded-xl font-semibold shadow-lg hover:shadow-xl transition-all"
          >
            <Linkedin className="w-5 h-5" />
            <span>Post to LinkedIn</span>
          </motion.button>

          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={handleCopy}
            className="flex items-center gap-2 px-6 py-3 bg-slate-600 text-white rounded-xl font-semibold shadow-lg hover:shadow-xl transition-all"
          >
            {copied ? <Check className="w-5 h-5" /> : <Copy className="w-5 h-5" />}
            <span>{copied ? 'Copied!' : 'Copy'}</span>
          </motion.button>

          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={handleDownload}
            className="flex items-center gap-2 px-6 py-3 bg-white border-2 border-slate-300 text-slate-700 rounded-xl font-semibold hover:bg-slate-50 transition-all"
          >
            <Download className="w-5 h-5" />
            <span>Download</span>
          </motion.button>

          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={onReset}
            className="flex items-center gap-2 px-6 py-3 bg-white border-2 border-primary-300 text-primary-600 rounded-xl font-semibold hover:bg-primary-50 transition-all"
          >
            <RefreshCw className="w-5 h-5" />
            <span>New Post</span>
          </motion.button>
        </div>
      </div>

      {/* Image Suggestion */}
      {data.image_suggestion && (
        <ImageSuggestion suggestion={data.image_suggestion} />
      )}

      {/* News Sources */}
      {showSources && (
        <div className="fixed inset-0 bg-black/40 flex items-center justify-center z-50">
          <div className="bg-white rounded-2xl p-6 w-[90%] max-w-2xl max-h-[80vh] overflow-y-auto shadow-xl">
            
            <div className="flex justify-between items-center mb-4">
              <h3 className="font-bold text-lg">📰 Sources</h3>
              <button onClick={() => setShowSources(false)}>✖</button>
            </div>

            <div className="space-y-3">
              {data.news_sources?.map((source, index) => (
                <NewsSourceCard key={index} source={source} index={index} />
              ))}
            </div>

          </div>
        </div>
      )}
    </motion.div>
  );
};

export default GeneratedPost;