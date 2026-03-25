export const shareToLinkedIn = (post, hashtags = [], imageSuggestion = '') => {
  // Combine post with hashtags
  const fullText = `${post}\n\n${hashtags.join(' ')}`;
  
  // LinkedIn share URL with text
  const linkedInUrl = `https://www.linkedin.com/sharing/share-offsite/?url=${encodeURIComponent(window.location.href)}`;
  
  // Open LinkedIn in new window
  const width = 600;
  const height = 600;
  const left = (window.screen.width - width) / 2;
  const top = (window.screen.height - height) / 2;
  
  window.open(
    linkedInUrl,
    'linkedin-share',
    `width=${width},height=${height},left=${left},top=${top}`
  );
  
  // Copy to clipboard for easy pasting
  navigator.clipboard.writeText(fullText).then(() => {
    console.log('Post copied to clipboard for easy pasting on LinkedIn');
  });
};

export const copyToClipboard = async (text) => {
  try {
    await navigator.clipboard.writeText(text);
    return true;
  } catch (err) {
    console.error('Failed to copy:', err);
    return false;
  }
};