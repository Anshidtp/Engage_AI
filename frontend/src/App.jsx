import { Toaster } from 'react-hot-toast';
import { AnimatePresence } from 'framer-motion';
import Hero from './components/Hero';
import PostForm from './components/PostForm';
import LoadingAnimation from './components/LoadingAnimation';
import GeneratedPost from './components/GeneratedPost';
import ErrorMessage from './components/ErrorMessage';
import { usePostGenerator } from './hooks/usePostGenerator';

function App() {
  const { loading, generatedPost, error, generate, reset } = usePostGenerator();

  return (
    <div className="min-h-screen py-12 px-4 sm:px-6 lg:px-8">
      <Toaster 
        position="top-right"
        toastOptions={{
          duration: 3000,
          style: {
            background: '#fff',
            color: '#334155',
            boxShadow: '0 10px 15px -3px rgba(0, 0, 0, 0.1)',
          },
        }}
      />

      <div className="max-w-5xl mx-auto">
        <Hero />

        <AnimatePresence mode="wait">
          {!generatedPost && !loading && (
            <PostForm onSubmit={generate} loading={loading} />
          )}

          {loading && (
            <LoadingAnimation key="loading" />
          )}

          {error && !loading && (
            <ErrorMessage key="error" message={error} onRetry={reset} />
          )}

          {generatedPost && !loading && (
            <GeneratedPost key="result" data={generatedPost} onReset={reset} />
          )}
        </AnimatePresence>

        {/* Footer */}
        <footer className="mt-16 text-center text-sm text-slate-500">
          <p>
            Powered by{' '}
            <span className="font-semibold text-primary-600">LangGraph</span>,{' '}
            <span className="font-semibold text-accent-600">Google Gemini</span>, and{' '}
            <span className="font-semibold text-purple-600">LangChain</span>
          </p>
          <p className="mt-2">
            Built with ❤️ for professional content creators
          </p>
        </footer>
      </div>
    </div>
  );
}

export default App;