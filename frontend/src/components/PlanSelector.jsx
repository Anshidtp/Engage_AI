import { motion } from 'framer-motion';
import { Check } from 'lucide-react';
import { PLAN_OPTIONS } from '../utils/constants';

const PlanSelector = ({ selectedPlan, onSelectPlan, disabled }) => {
  return (
    <div>
      <label className="block text-sm font-semibold text-slate-700 mb-3">
        Choose your plan 🚀
      </label>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {PLAN_OPTIONS.map((plan) => (
          <motion.button
            key={plan.value}
            type="button"
            whileHover={{ scale: disabled ? 1 : 1.02 }}
            whileTap={{ scale: disabled ? 1 : 0.98 }}
            onClick={() => onSelectPlan(plan.value)}
            disabled={disabled}
            className={`relative p-5 rounded-2xl border-2 transition-all duration-300 text-left ${
              selectedPlan === plan.value
                ? 'border-primary-500 bg-gradient-to-br from-primary-50 to-accent-50 shadow-lg ring-2 ring-primary-200'
                : 'border-slate-200 bg-white hover:border-primary-300 hover:shadow-md'
            } ${disabled ? 'opacity-50 cursor-not-allowed' : ''}`}
          >
            {/* Badge */}
            <div className="absolute top-3 right-3">
              <span className={`text-xs font-bold px-2 py-1 rounded-full ${
                plan.value === 'pro' 
                  ? 'bg-gradient-to-r from-amber-400 to-orange-500 text-white'
                  : 'bg-blue-100 text-blue-700'
              }`}>
                {plan.badge}
              </span>
            </div>

            {/* Selected Check */}
            {selectedPlan === plan.value && (
              <motion.div
                initial={{ scale: 0 }}
                animate={{ scale: 1 }}
                className="absolute top-3 left-3 w-6 h-6 bg-primary-600 rounded-full flex items-center justify-center"
              >
                <Check className="w-4 h-4 text-white" />
              </motion.div>
            )}

            {/* Content */}
            <div className="mt-2">
              <div className="flex items-center gap-2 mb-2">
                <span className="text-3xl">{plan.icon}</span>
                <div>
                  <h3 className="font-bold text-lg text-slate-800">{plan.label}</h3>
                  <p className="text-xs text-slate-500">{plan.description}</p>
                </div>
              </div>

              {/* Quality Badge */}
              <div className="inline-block px-3 py-1 bg-green-100 text-green-700 rounded-full text-xs font-semibold mb-3">
                ⭐ {plan.quality} Quality
              </div>

              {/* Features */}
              <ul className="space-y-1.5">
                {plan.features.map((feature, idx) => (
                  <li key={idx} className="flex items-center gap-2 text-xs text-slate-600">
                    <div className="w-1.5 h-1.5 bg-primary-500 rounded-full" />
                    {feature}
                  </li>
                ))}
              </ul>
            </div>
          </motion.button>
        ))}
      </div>
    </div>
  );
};

export default PlanSelector;