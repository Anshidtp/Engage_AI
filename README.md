# Engage_AI
A production-ready AI-powered service that generates engaging LinkedIn posts based on recent news using Google Gemini and LangChain.

- You can watch the Demo Here: [ENGAGE_aI](https://github.com/Anshidtp/Engage_AI/blob/main/sample/Engage_ai.mp4)
- For Live Demo: [Engage_ai](https://engage-ai-wrzr.onrender.com)

![Demo](https://github.com/Anshidtp/Engage_AI/blob/main/sample/engage%20aigif.gif)

## 🚀 Features

- **AI-Powered Content Generation**: Uses Google Gemini for intelligent, contextual post creation
- **Real-time News Integration**: Fetches recent news articles to keep content current and relevant
- **Smart Hashtag Generation**: Automatically suggests relevant industry hashtags
- **Image Recommendations**: Provides suggestions for accompanying visuals
- **Comprehensive Documentation**: Auto-generated Swagger/OpenAPI docs
- **Production Ready**: Proper error handling, logging, and monitoring

## 🛠️ Tech Stack

- **Backend**: FastAPI (Python)
- **AI/ML**: Google Gemini API, LangChain
- **News & Image Search**: SerpAPI (with fallback options)
- **Deployment**: Render
- **Documentation**: Swagger

## 📋 Prerequisites

1. **Google Gemini API Key**: Get your free API key from [Google AI Studio](https://makersuite.google.com/)
2. **SerpAPI Key** (Optional): For enhanced news search capabilities from [SerpAPI](https://serpapi.com/)

## 🚀 Quick Start

### 1. Clone and Setup

```bash
git clone https://github.com/Anshidtp/Engage_AI.git
cd Engage_AI
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Environment Configuration

Create a `.env` file:

```env
# Required
GOOGLE_API_KEY=your_gemini_api_key_here

# Optional (for better news search)
SERPAPI_API_KEY=your_serpapi_key_here

```

### 4. Run Locally

```bash
# Development mode
uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000

# Production mode
python app/main.py
```

### 5. Test the API

Visit `http://localhost:8000/docs` for interactive API documentation.

Or test with curl:

```bash
curl -X POST "http://localhost:8000/api/v1/generate-post" \
     -H "Content-Type: application/json" \
     -d '{"topic": "Artificial Intelligence"}'
```

### Deployment on Render
1. Connect to Render:
```bash
  - Go to render.com
  - Create new Web Service
  - Connect your GitHub repository
```
2. Configure Service:
```bash
  - Build Command: pip install -r requirements.txt
  - Start Command: uvicorn app.main:app --host 0.0.0.0 --port $PORT

```
3. Set Environment Variables in Render dashboard:

```bash
  GOOGLE_API_KEY: Your Gemini API key
  SERPAPI_API_KEY: Your SerpAPI key
```
- Production URL
```bash
Your app will be available at: https://your-app-name.onrender.com

```

## 📊 API Reference

### Generate Post

**POST** `/posts/generate-post`

Generate a LinkedIn post based on recent news about a topic.

#### Request Body
```json
{
  "topic": "Gold Price Hike"
}
```

#### Parameters

- `topic` (required): The main topic to search news for (3-100 characters)

#### Response

```json
{
  "topic": "Gold price hike",
  "news_sources": [
    {
      "title": "What Was the Highest Gold Price Ever? Updates on Gold's Record-Breaking Performance",
      "url": "https://investingnews.com/daily/resource-investing/precious-metals-investing/gold-investing/highest-price-for-gold/",
      "published_date": null,
      "source_name": "Investing News Network",
      "snippet": "The gold price set a new all-time high in September 2025 of over US$3700. Find out what factors are affecting the gold market and what the new gold ATH is."
    },
    {
      "title": "Gold Price Today: September 18, 2025",
      "url": "https://www.forbes.com/advisor/investing/gold-price/",
      "published_date": null,
      "source_name": "Forbes",
      "snippet": "The price of gold today, as of 9:19 a.m. ET, was $3665.42 per ounce. That's up 0.03% over the past 24 hours. Compared to last week, the price of gold is up..."
    },
    {
      "title": "Gold price rally hits pause after Fed rate cut, opens lower by Rs 500. Should you sell now?",
      "url": "https://m.economictimes.com/markets/commodities/news/gold-price-rally-hits-pause-after-fed-rate-cut-opens-lower-by-rs-500-should-you-sell-now/articleshow/123963372.cms",
      "published_date": null,
      "source_name": "The Economic Times",
      "snippet": "Gold prices dipped Rs 500 as the Fed's rate cut and dollar rebound triggered volatility. Experts expect choppy trade in gold and silver, with key support..."
    },
    {
      "title": "Gold price hikes by Rs 1,100 per tola – The Rising Nepal",
      "url": "https://berawangnews.com/gold-price-hikes-by-rs-1100-per-tola-the-rising-nepal/",
      "published_date": null,
      "source_name": "Berawang News",
      "snippet": "Understanding the Recent Surge in Gold Prices: A Closer Look at the Rs 1100 Hike."
    },
    {
      "title": "Gold Price Breaks US$3,700, Then Falls as Fed Cuts Rates",
      "url": "https://investingnews.com/federal-reserve-gold-price/",
      "published_date": null,
      "source_name": "Investing News Network",
      "snippet": "The Fed made a 25 basis point cut to its benchmark interest rate amid rising inflation, slowing jobs growth and tariff impacts."
    }
  ],
  "linkedin_post": "Is gold the ultimate safe haven, or are we witnessing peak volatility in the precious metals market?\nGold has once again captured global attention, shattering records with a new all-time high of over US$3700 earlier this month. As of September 18, 2025, the precious metal stands strong at $3665.42 per ounce, reflecting a consistent upward trend over the past week.\nThis remarkable performance has been fueled by various macroeconomic factors, solidifying gold's role as a key asset in uncertain times. However, the market isn't without its immediate shifts. We've just seen a pause in the rally, with prices dipping following the Federal Reserve's recent rate cut and a subsequent rebound in the dollar. This move has introduced a period of choppy trade, leaving many investors to ponder the immediate future.\nFor portfolio managers, strategic investors, and financial analysts, understanding these dynamics is crucial. Is this a temporary correction before another surge, or a signal to re-evaluate positions? The interplay between central bank policies, currency movements, and investor sentiment continues to shape gold's trajectory.\nWhat are your predictions for gold's performance in the coming months, especially given the current market volatility and macroeconomic landscape? Share your insights below.",
  "image_suggestion": "https://media.cnn.com/api/v1/images/stellar/prod/ap25245201005561.jpg?c=original"
}
```

### Health Check

**GET** `/posts/health`

Check service health and API key configuration.


## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

### Common Issues

1. **"Service configuration error"**: Check your `GOOGLE_API_KEY` environment variable
2. **"Failed to search news"**: Verify your `SERPAPI_API_KEY` or check network connectivity

