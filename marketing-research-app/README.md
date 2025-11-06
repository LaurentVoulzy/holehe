# 🎯 Marketing Research AI

A powerful Streamlit web application that researches companies and competitors, analyzes their ads and content from public sources, detects viral trends, and uses Claude AI to generate creative marketing ideas.

**Built for MachinePoem.agency**

---

## 🚀 Features

### Core Functionality
- **Auto-detect Competitors**: Automatically find 3-7 competitors using web search
- **Ad Data Scraping**: Collect ads from:
  - Meta Ad Library (official API)
  - LinkedIn company pages
  - Google Ads Transparency Center
- **Trend Detection**: Analyze trends from:
  - Google Trends (last 7 days)
  - Twitter/X trending topics
  - TikTok Creative Center
- **AI Analysis**: Claude AI generates:
  - Company analysis
  - Competitor analysis
  - Trend adaptation strategies
  - 10+ ad concepts with full scripts
  - 10+ social content ideas with full scripts
- **Report Generation**: Download reports in Markdown format

### MVP Capabilities
The current MVP includes:
- ✅ Input form with company details
- ✅ Competitor auto-detection via web search
- ✅ Basic ad data collection framework
- ✅ Google Trends integration
- ✅ Claude API integration for full analysis
- ✅ Markdown report generation with download

---

## 📋 Requirements

- Python 3.10 or higher
- Anthropic API key (Claude)
- Optional: Meta API access token, Twitter API key

---

## 🛠️ Installation

### 1. Clone the Repository
```bash
cd marketing-research-app
```

### 2. Create Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables
Create a `.env` file in the project root:

```bash
cp .env.example .env
```

Edit `.env` and add your API keys:

```env
# Required
ANTHROPIC_API_KEY=your_claude_api_key_here

# Optional
META_ACCESS_TOKEN=your_meta_access_token
TWITTER_BEARER_TOKEN=your_twitter_bearer_token
GOOGLE_API_KEY=your_google_api_key
```

**Get API Keys:**
- **Anthropic Claude**: https://console.anthropic.com/
- **Meta Graph API**: https://developers.facebook.com/
- **Twitter API**: https://developer.twitter.com/

---

## 🎮 Usage

### Start the Application

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

### Using the App

1. **Enter Company Details**:
   - Company name (required)
   - Company website URL (required)
   - Number of competitors to analyze (3, 5, or 7)

2. **Add Competitors** (Optional):
   - Enter competitor URLs manually, or
   - Enable "Auto-detect competitors" to find them automatically

3. **Select Data Sources**:
   - Meta Ad Library
   - LinkedIn Posts
   - Google Trends
   - Twitter Trends

4. **Click "Start Research"**:
   - Watch the progress as the app collects data
   - Claude AI analyzes everything and generates ideas
   - Download your report when complete

### Example Input

```
Company Name: Nike
Company Website: https://www.nike.com
Number of Competitors: 3
Auto-detect: ✓
```

---

## 📊 Output Structure

The generated report includes:

### 1. Company Analysis
- Current advertising and social content strategy
- Active platforms
- Creative strengths and weaknesses
- Visual style, tone, messaging

### 2. Competitor Analysis
- 3-7 competitors with analysis
- Winning creative patterns
- What's working (hooks, visuals, CTAs)
- Category gaps and opportunities

### 3. This Week's Viral Trends
- Platform-specific trends
- Why they're trending
- Target audiences

### 4. Trend Adaptation
- How to apply trends to your brand
- Ad ideas inspired by trends
- Organic content ideas

### 5. Ad Concepts (10+ Ideas)
Each includes:
- Target group
- Duration
- Creative concept
- Success prediction
- Full script with visual direction

### 6. Social Content Ideas (10+ Ideas)
Each includes:
- Target group
- Duration
- Platform-specific concept
- Success prediction
- Full script with VO/captions

---

## 🏗️ Project Structure

```
marketing-research-app/
├── app.py                          # Main Streamlit application
├── requirements.txt                # Python dependencies
├── .env.example                    # Environment variables template
├── .env                           # Your API keys (not in git)
├── README.md                      # This file
│
├── utils/                         # Utility modules
│   ├── __init__.py
│   ├── config.py                  # Configuration and settings
│   ├── competitor_detector.py     # Auto-detect competitors
│   ├── ad_scraper.py              # Scrape ads from platforms
│   ├── trends_analyzer.py         # Analyze trends
│   ├── claude_analyzer.py         # Claude AI integration
│   └── report_generator.py        # Generate reports
│
└── data/                          # Data storage (optional)
```

---

## 🔧 Configuration

Edit `utils/config.py` to customize:

- Claude model and parameters
- Request timeouts and retries
- Default competitor count
- User agent strings

---

## 📝 Notes

### Current MVP Limitations

1. **Meta Ad Library**: Currently uses placeholder structure. For production:
   - Use Meta Graph API with access token
   - Or implement Playwright for JavaScript rendering

2. **LinkedIn**: Requires authentication. For production:
   - Use LinkedIn API
   - Or implement authenticated browser session

3. **Twitter/X**: Requires API v2 authentication
   - Currently uses sample data
   - Add Twitter bearer token for real data

4. **TikTok**: Requires Creative Center access
   - Currently uses sample data

### Future Enhancements

- [ ] Full Meta Graph API integration
- [ ] LinkedIn API integration
- [ ] Twitter API v2 integration
- [ ] TikTok Creative Center API
- [ ] PDF report generation
- [ ] Caching for faster repeated searches
- [ ] Batch processing for multiple companies
- [ ] Historical trend analysis
- [ ] Competitive benchmarking dashboard

---

## 🔒 Security

- Never commit `.env` file to version control
- Keep API keys secure
- Rate limit API calls to avoid bans
- Review Terms of Service for each platform

---

## 🐛 Troubleshooting

### "ANTHROPIC_API_KEY is required"
- Make sure you created a `.env` file
- Add your Claude API key to `.env`
- Restart the Streamlit app

### "Module not found" errors
- Activate your virtual environment
- Run `pip install -r requirements.txt`

### Competitor detection not working
- Check your internet connection
- Some searches may be rate-limited
- Try using manual competitor entry

### Claude API timeout
- Increase `CLAUDE_MAX_TOKENS` in `config.py`
- Check your Anthropic account quota
- Simplify the request if needed

---

## 📞 Support

For issues or questions:
1. Check this README
2. Review the code comments
3. Contact MachinePoem.agency

---

## 📄 License

For internal use at MachinePoem.agency only.

---

## 🙏 Credits

- **AI Model**: Claude Sonnet 4.5 by Anthropic
- **Framework**: Streamlit
- **Built for**: MachinePoem.agency

---

## 🚀 Quick Start Guide

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Set up API key
echo "ANTHROPIC_API_KEY=your_key_here" > .env

# 3. Run the app
streamlit run app.py

# 4. Open browser to http://localhost:8501

# 5. Enter company details and start research!
```

---

**Happy researching! 🎯**
