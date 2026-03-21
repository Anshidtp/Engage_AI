export const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export const STYLE_OPTIONS = [
  { value: 'professional', label: 'Professional', icon: '👔', description: 'Formal business tone' },
  { value: 'casual', label: 'Casual', icon: '😊', description: 'Friendly & conversational' },
  { value: 'thought-leadership', label: 'Thought Leadership', icon: '💡', description: 'Expert insights' },
];

export const ENDPOINT_OPTIONS = [
  { 
    value: 'standard', 
    label: 'Standard', 
    icon: '⚡', 
    description: '~15s response',
    quality: '7.2/10 avg'
  },
  { 
    value: 'enhanced', 
    label: 'Enhanced (LangGraph)', 
    icon: '🚀', 
    description: '~30s response',
    quality: '8.5/10 avg'
  },
];

export const LOADING_MESSAGES = [
  '🔍 Searching for latest news...',
  '📊 Analyzing industry trends...',
  '✍️ Crafting your content...',
  '🎯 Optimizing for engagement...',
  '✨ Adding finishing touches...',
];