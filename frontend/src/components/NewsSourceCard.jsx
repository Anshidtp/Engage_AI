import { motion } from 'framer-motion';
import { ExternalLink, Calendar, Building2 } from 'lucide-react';

const NewsSourceCard = ({ source, index }) => {
  return (
    <motion.a
      href={source.url}
      target="_blank"
      rel="noopener noreferrer"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: index * 0.1 }}
      whileHover={{ scale: 1.02, y: -4 }}
      className="block bg-white/50 rounded-2xl p-5 border-2 border-slate-100 hover:border-primary-300 hover:shadow-lg transition-all group"
    >
      <div className="flex items-start justify-between mb-3">
        <h4 className="font-semibold text-slate-800 group-hover:text-primary-600 transition-colors flex-1 pr-2">
          {source.title}
        </h4>
        <ExternalLink className="w-4 h-4 text-slate-400 group-hover:text-primary-600 flex-shrink-0" />
      </div>

      {source.snippet && (
        <p className="text-sm text-slate-600 mb-3 line-clamp-2">
          {source.snippet}
        </p>
      )}

      <div className="flex flex-wrap gap-3 text-xs text-slate-500">
        {source.source_name && (
          <div className="flex items-center gap-1">
            <Building2 className="w-3 h-3" />
            <span>{source.source_name}</span>
          </div>
        )}
        {source.published_date && (
          <div className="flex items-center gap-1">
            <Calendar className="w-3 h-3" />
            <span>{new Date(source.published_date).toLocaleDateString()}</span>
          </div>
        )}
      </div>
    </motion.a>
  );
};

export default NewsSourceCard;