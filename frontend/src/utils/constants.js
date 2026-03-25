export const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export const STYLE_OPTIONS = [
  { value: 'professional', label: 'Professional', icon: '👔', description: 'Formal business tone' },
  { value: 'casual', label: 'Casual', icon: '😊', description: 'Friendly & conversational' },
  { value: 'thought-leadership', label: 'Thought Leadership', icon: '💡', description: 'Expert insights' },
];

export const PLAN_OPTIONS = [
  { 
    value: 'standard', 
    label: 'Standard', 
    icon: '⚡', 
    badge: 'Fast',
    description: '~15-20s response',
    quality: '7-8/10',
    features: ['Quick generation', 'Good quality', 'Perfect for volume']
  },
  { 
    value: 'pro', 
    label: 'Pro', 
    icon: '🚀', 
    badge: 'Premium',
    description: '~30-40s response',
    quality: '8.5-9.5/10',
    features: ['Advanced workflow', 'Quality refinement', 'Best quality']
  },
];

export const LOADING_MESSAGES = {
  standard: [
    '⚡ Searching latest news...',
    '✍️ Generating your post...',
    '🎯 Optimizing content...',
    '✨ Finalizing...',
  ],
  pro: [
    '🔍 Searching news sources...',
    '📊 Analyzing trends & insights...',
    '📝 Creating content outline...',
    '✍️ Crafting your post...',
    '🎯 Checking quality...',
    '🔄 Refining content...',
    '✨ Adding final touches...',
  ]
};