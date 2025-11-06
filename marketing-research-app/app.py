"""
Marketing Research AI App
Built for MachinePoem.agency
"""
import streamlit as st
from datetime import datetime
import sys
from pathlib import Path

# Add utils to path
sys.path.append(str(Path(__file__).parent))

from utils.config import Config
from utils.competitor_detector import CompetitorDetector
from utils.ad_scraper import AdScraper
from utils.trends_analyzer import TrendsAnalyzer
from utils.claude_analyzer import ClaudeAnalyzer
from utils.report_generator import ReportGenerator

# Page config
st.set_page_config(
    page_title="Marketing Research AI | MachinePoem",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

def main():
    """Main application."""

    # Header
    st.title("🎯 Marketing Research AI")
    st.markdown("**Research competitors, analyze ads, detect trends, and generate creative ideas with Claude AI**")
    st.markdown("*Built for MachinePoem.agency*")
    st.divider()

    # Validate config
    config_errors = Config.validate()
    if config_errors:
        st.error("⚠️ Configuration Error")
        for error in config_errors:
            st.warning(error)
        st.info("Please create a `.env` file with your API keys. See `.env.example` for reference.")
        return

    # Sidebar for settings
    with st.sidebar:
        st.header("⚙️ Settings")

        # API Status
        st.subheader("API Status")
        if Config.ANTHROPIC_API_KEY:
            st.success("✅ Claude API Connected")
        else:
            st.error("❌ Claude API Missing")

        if Config.META_ACCESS_TOKEN:
            st.success("✅ Meta API Connected")
        else:
            st.info("ℹ️ Meta API Optional (will use scraping)")

        st.divider()

        # Advanced options
        st.subheader("Advanced Options")
        use_cache = st.checkbox("Use cached data", value=True)
        verbose_logging = st.checkbox("Verbose logging", value=False)

    # Main form
    st.header("📋 Company Research Input")

    with st.form("research_form"):
        col1, col2 = st.columns(2)

        with col1:
            company_name = st.text_input(
                "Company Name *",
                placeholder="e.g., Nike, Apple, Coca-Cola",
                help="The company you want to research"
            )

            company_url = st.text_input(
                "Company Website URL *",
                placeholder="https://www.example.com",
                help="The main website of the company"
            )

        with col2:
            num_competitors = st.selectbox(
                "Number of Competitors to Analyze *",
                options=Config.COMPETITORS_OPTIONS,
                index=0,
                help="How many competitors should we analyze?"
            )

            auto_detect = st.checkbox(
                "Auto-detect competitors",
                value=True,
                help="Automatically find competitors if not provided"
            )

        competitors_input = st.text_area(
            "Competitor Websites (Optional)",
            placeholder="https://competitor1.com\nhttps://competitor2.com\nhttps://competitor3.com",
            help="Enter competitor URLs, one per line. Leave empty to auto-detect.",
            height=150
        )

        # Data sources
        st.subheader("📊 Data Sources to Include")
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            include_meta = st.checkbox("Meta Ad Library", value=True)
        with col2:
            include_linkedin = st.checkbox("LinkedIn Posts", value=True)
        with col3:
            include_google_trends = st.checkbox("Google Trends", value=True)
        with col4:
            include_twitter = st.checkbox("Twitter Trends", value=False)

        # Submit button
        submitted = st.form_submit_button("🚀 Start Research", use_container_width=True)

    # Process form submission
    if submitted:
        # Validation
        if not company_name or not company_url:
            st.error("❌ Please fill in all required fields (Company Name and Website URL)")
            return

        # Parse competitors
        competitor_urls = []
        if competitors_input.strip():
            competitor_urls = [url.strip() for url in competitors_input.split('\n') if url.strip()]

        # Run research
        run_research(
            company_name=company_name,
            company_url=company_url,
            competitor_urls=competitor_urls,
            num_competitors=num_competitors,
            auto_detect=auto_detect,
            include_meta=include_meta,
            include_linkedin=include_linkedin,
            include_google_trends=include_google_trends,
            include_twitter=include_twitter,
            use_cache=use_cache,
            verbose=verbose_logging
        )


def run_research(
    company_name: str,
    company_url: str,
    competitor_urls: list,
    num_competitors: int,
    auto_detect: bool,
    include_meta: bool,
    include_linkedin: bool,
    include_google_trends: bool,
    include_twitter: bool,
    use_cache: bool,
    verbose: bool
):
    """Run the full research pipeline."""

    st.divider()
    st.header("🔍 Research in Progress")

    # Progress tracking
    progress_bar = st.progress(0)
    status_text = st.empty()

    try:
        # Store results in session state
        if 'research_data' not in st.session_state:
            st.session_state.research_data = {}

        # Step 1: Detect competitors
        status_text.text("Step 1/5: Detecting competitors...")
        progress_bar.progress(10)

        if auto_detect and len(competitor_urls) < num_competitors:
            with st.spinner(f"🔍 Auto-detecting competitors for {company_name}..."):
                detector = CompetitorDetector()
                detected_competitors = detector.detect_competitors(
                    company_name=company_name,
                    company_url=company_url,
                    num_competitors=num_competitors - len(competitor_urls)
                )
                competitor_urls.extend(detected_competitors)

        # Limit to requested number
        competitor_urls = competitor_urls[:num_competitors]

        st.success(f"✅ Found {len(competitor_urls)} competitors")
        with st.expander("View Competitors"):
            for i, url in enumerate(competitor_urls, 1):
                st.write(f"{i}. {url}")

        progress_bar.progress(20)

        # Step 2: Scrape ad data
        status_text.text("Step 2/5: Scraping ad data from public sources...")
        progress_bar.progress(30)

        ad_data = {}

        if include_meta:
            with st.spinner("📱 Scraping Meta Ad Library..."):
                scraper = AdScraper()
                ad_data['meta'] = scraper.scrape_meta_ads(company_name, competitor_urls)
                st.success(f"✅ Collected {len(ad_data.get('meta', {}))} Meta ads")

        progress_bar.progress(40)

        if include_linkedin:
            with st.spinner("💼 Scraping LinkedIn posts..."):
                scraper = AdScraper()
                ad_data['linkedin'] = scraper.scrape_linkedin_posts(company_name, competitor_urls)
                st.success(f"✅ Collected {len(ad_data.get('linkedin', {}))} LinkedIn posts")

        progress_bar.progress(50)

        # Step 3: Get trends data
        status_text.text("Step 3/5: Analyzing this week's trends...")
        progress_bar.progress(60)

        trends_data = {}

        if include_google_trends:
            with st.spinner("📈 Analyzing Google Trends (last 7 days)..."):
                analyzer = TrendsAnalyzer()
                trends_data['google'] = analyzer.get_google_trends(company_name)
                st.success("✅ Google Trends analyzed")

        if include_twitter:
            with st.spinner("🐦 Fetching Twitter trending topics..."):
                analyzer = TrendsAnalyzer()
                trends_data['twitter'] = analyzer.get_twitter_trends()
                st.success("✅ Twitter trends collected")

        progress_bar.progress(70)

        # Step 4: Claude analysis
        status_text.text("Step 4/5: Generating AI insights with Claude...")
        progress_bar.progress(80)

        with st.spinner("🤖 Claude AI is analyzing all data and generating creative ideas..."):
            claude = ClaudeAnalyzer()
            analysis_result = claude.analyze(
                company_name=company_name,
                company_url=company_url,
                competitor_urls=competitor_urls,
                ad_data=ad_data,
                trends_data=trends_data
            )

        st.success("✅ AI analysis complete!")
        progress_bar.progress(90)

        # Step 5: Generate report
        status_text.text("Step 5/5: Generating downloadable report...")
        progress_bar.progress(95)

        with st.spinner("📄 Creating Markdown report..."):
            generator = ReportGenerator()
            markdown_report = generator.generate_markdown(
                company_name=company_name,
                analysis_result=analysis_result,
                timestamp=datetime.now()
            )

        progress_bar.progress(100)
        status_text.text("✅ Research complete!")

        # Store in session state
        st.session_state.research_data = {
            'company_name': company_name,
            'company_url': company_url,
            'competitors': competitor_urls,
            'ad_data': ad_data,
            'trends_data': trends_data,
            'analysis': analysis_result,
            'report': markdown_report,
            'timestamp': datetime.now().isoformat()
        }

        # Display results
        display_results(markdown_report, company_name)

    except Exception as e:
        st.error(f"❌ An error occurred: {str(e)}")
        if verbose:
            st.exception(e)


def display_results(markdown_report: str, company_name: str):
    """Display the research results."""

    st.divider()
    st.header("📊 Research Results")

    # Download buttons
    col1, col2 = st.columns(2)

    with col1:
        st.download_button(
            label="📥 Download Markdown Report",
            data=markdown_report,
            file_name=f"{company_name.lower().replace(' ', '_')}_research_{datetime.now().strftime('%Y%m%d')}.md",
            mime="text/markdown",
            use_container_width=True
        )

    with col2:
        st.download_button(
            label="📥 Download as Text",
            data=markdown_report,
            file_name=f"{company_name.lower().replace(' ', '_')}_research_{datetime.now().strftime('%Y%m%d')}.txt",
            mime="text/plain",
            use_container_width=True
        )

    # Display preview
    st.subheader("📄 Report Preview")

    with st.container():
        st.markdown(markdown_report)


if __name__ == "__main__":
    main()
