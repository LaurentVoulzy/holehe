# 🚀 Quick Start Guide

Get started with Marketing Research AI in 5 minutes!

## Prerequisites
- Python 3.10+
- Claude API key from Anthropic

## Step 1: Get Your API Key

1. Go to [Anthropic Console](https://console.anthropic.com/)
2. Sign up or log in
3. Create a new API key
4. Copy your API key

## Step 2: Install & Setup

### Option A: Using the Startup Script (Recommended)

**On Linux/Mac:**
```bash
./run.sh
```

**On Windows:**
```bash
run.bat
```

The script will:
- Create a virtual environment
- Install all dependencies
- Create a `.env` file
- Prompt you to add your API key
- Launch the app

### Option B: Manual Setup

```bash
# 1. Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Create .env file
cp .env.example .env

# 4. Edit .env and add your API key
nano .env  # or use any text editor

# 5. Run the app
streamlit run app.py
```

## Step 3: Add Your API Key

Open the `.env` file and add your Claude API key:

```env
ANTHROPIC_API_KEY=sk-ant-your-key-here
```

Save and close the file.

## Step 4: Run the App

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## Step 5: Test with an Example

Try this example:

1. **Company Name**: `Nike`
2. **Company Website**: `https://www.nike.com`
3. **Number of Competitors**: `3`
4. **Auto-detect competitors**: ✓ (checked)
5. Click **"Start Research"**

The app will:
- Find 3 competitors automatically
- Collect ad data and trends
- Generate a full marketing research report with Claude AI
- Provide downloadable Markdown report

## Expected Results

You'll get a comprehensive report with:

- ✅ Company analysis
- ✅ 3 competitor analyses
- ✅ This week's viral trends
- ✅ 10+ ad concepts with full scripts
- ✅ 10+ social content ideas with full scripts

## Troubleshooting

### "ANTHROPIC_API_KEY is required"
- Make sure `.env` file exists
- Check that your API key is correct
- Restart the app

### Dependencies not installing
```bash
# Upgrade pip first
pip install --upgrade pip
pip install -r requirements.txt
```

### App won't start
```bash
# Check Python version (needs 3.10+)
python --version

# Try with python3 explicitly
python3 -m streamlit run app.py
```

## Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Customize settings in `utils/config.py`
- Add optional API keys for enhanced features

## Need Help?

1. Check [README.md](README.md) for full documentation
2. Review code comments in the source files
3. Contact MachinePoem.agency for support

---

**Ready to generate amazing marketing ideas! 🎯**
