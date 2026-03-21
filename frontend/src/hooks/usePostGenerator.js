import { useState } from 'react';
import { generatePost } from '../services/api';
import toast from 'react-hot-toast';

export const usePostGenerator = () => {
  const [loading, setLoading] = useState(false);
  const [generatedPost, setGeneratedPost] = useState(null);
  const [error, setError] = useState(null);

  const generate = async (formData) => {
    setLoading(true);
    setError(null);
    setGeneratedPost(null);

    try {
      const data = await generatePost({
        topic: formData.topic,
        style: formData.style,
        include_hashtags: formData.includeHashtags,
        max_length: formData.maxLength,
      }, formData.endpoint);

      setGeneratedPost(data);
      toast.success('Post generated successfully! 🎉');
    } catch (err) {
      const errorMessage = err.response?.data?.error || err.message || 'Failed to generate post';
      setError(errorMessage);
      toast.error(errorMessage);
      console.error('Generation error:', err);
    } finally {
      setLoading(false);
    }
  };

  const reset = () => {
    setGeneratedPost(null);
    setError(null);
  };

  return { loading, generatedPost, error, generate, reset };
};