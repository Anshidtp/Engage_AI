import { motion } from 'framer-motion';
import { Award } from 'lucide-react';

const QualityScore = ({ score }) => {
  const getColor = (score) => {
    if (score >= 8.5) return 'text-green-600 bg-green-100';
    if (score >= 7.5) return 'text-blue-600 bg-blue-100';
    if (score >= 6.5) return 'text-yellow-600 bg-yellow-100';
    return 'text-orange-600 bg-orange-100';
  };

  const getLabel = (score) => {
    if (score >= 8.5) return 'Excellent';
    if (score >= 7.5) return 'Good';
    if (score >= 6.5) return 'Fair';
    return 'Needs Work';
  };

  return (
    <motion.div
      initial={{ scale: 0 }}
      animate={{ scale: 1 }}
      transition={{ type: "spring", stiffness: 200 }}
      className={`flex items-center gap-2 px-4 py-2 rounded-full ${getColor(score)}`}
    >
      <Award className="w-5 h-5" />
      <div className="font-bold">
        {score.toFixed(1)}/10
      </div>
      <div className="text-sm font-medium">
        {getLabel(score)}
      </div>
    </motion.div>
  );
};

export default QualityScore;