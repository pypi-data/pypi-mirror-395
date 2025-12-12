"""About section and footer for Streamlit apps.

This module provides beautiful UI components to showcase the generator
and encourage community support through donations and sharing.

Generated with Streamlit App Generator by Leandro Meyer Dal Cortivo
"""
import streamlit as st


@st.dialog("ℹ️ About This App", width="large")
def show_about_modal():
    """Display beautiful About modal with donation info."""
    # Custom CSS for beautiful styling
    st.markdown("""
        <style>
        .about-header {
            background: linear-gradient(135deg, #FF4B4B 0%, #FF6B6B 100%);
            padding: 2rem;
            border-radius: 15px;
            text-align: center;
            color: white;
            margin-bottom: 1.5rem;
            box-shadow: 0 4px 12px rgba(255, 75, 75, 0.3);
        }
        .about-title {
            font-size: 2rem;
            font-weight: 700;
            margin: 0;
            text-shadow: 0 2px 4px rgba(0,0,0,0.2);
        }
        .about-subtitle {
            font-size: 1.1rem;
            opacity: 1;
            margin-top: 0.5rem;
            text-shadow: 0 1px 2px rgba(0,0,0,0.1);
        }
        .donation-box {
            background: linear-gradient(135deg, #FFF5F5 0%, #FFE5E5 100%);
            padding: 2rem;
            border-radius: 15px;
            margin: 1.5rem 0;
            border: 2px solid #FFD0D0;
        }
        .donation-title {
            font-size: 1.5rem;
            font-weight: 700;
            text-align: center;
            color: #D32F2F;
            margin-bottom: 1rem;
        }
        .donation-item {
            background: white;
            padding: 1.2rem;
            border-radius: 10px;
            margin: 0.8rem 0;
            border-left: 5px solid #FF4B4B;
            box-shadow: 0 2px 6px rgba(0,0,0,0.15);
        }
        .donation-label {
            font-weight: 700;
            color: #D32F2F;
            font-size: 1.05rem;
            margin-bottom: 0.5rem;
        }
        .donation-value {
            font-family: 'Courier New', monospace;
            font-size: 0.95rem;
            color: #000;
            font-weight: 600;
            word-break: break-all;
            background: #F5F5F5;
            padding: 0.8rem;
            border-radius: 6px;
            margin-top: 0.5rem;
            border: 1px solid #E0E0E0;
        }
        .share-btn {
            padding: 0.8rem 1.5rem;
            border-radius: 25px;
            text-decoration: none;
            color: white;
            font-weight: 600;
            text-align: center;
            transition: transform 0.2s, box-shadow 0.2s;
            display: inline-block;
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        }
        .share-btn:hover {
            transform: translateY(-3px);
            box-shadow: 0 6px 16px rgba(0,0,0,0.25);
        }
        .btn-github {
            background: linear-gradient(135deg, #24292e 0%, #000 100%);
        }
        .btn-community {
            background: linear-gradient(135deg, #FF4B4B 0%, #FF6B6B 100%);
        }
        </style>
    """, unsafe_allow_html=True)

    # Header
    st.markdown("""
        <div class="about-header">
            <p class="about-title">🚀 Streamlit App Generator</p>
            <p class="about-subtitle">Production-ready apps in seconds!</p>
        </div>
    """, unsafe_allow_html=True)

    # Description
    st.markdown("""
        This application was **generated automatically** using
        [Streamlit App Generator](https://github.com/leandrodalcortivo/streamlit-app-generator).

        **Features:**
        - 🔐 Secure authentication with bcrypt
        - 👥 Admin panel with user management
        - 🗄️ Multiple database support (PostgreSQL, MySQL, SQLite, MongoDB, Redis, Oracle)
        - 🎨 Beautiful themes (Light/Dark)
        - ☁️ Cloud-ready deployment
        - 🌍 Multilingual support (EN, PT-BR)
    """)

    # Donation section
    st.markdown("""
        <div class="donation-box">
            <p class="donation-title">💖 Support the Project</p>
            <p style="text-align: center; color: #666; margin-bottom: 1.5rem; font-size: 1.1rem;">
                Help keep this tool free and open-source!
            </p>
    """, unsafe_allow_html=True)

    # PIX for Brazil
    st.markdown("""
        <div class="donation-item">
            <div class="donation-label">🇧🇷 PIX (Brazil)</div>
            <div class="donation-value">lmdcorti@gmail.com</div>
        </div>
    """, unsafe_allow_html=True)

    # Crypto for International
    st.markdown("""
        <div class="donation-item">
            <div class="donation-label">💰 Bitcoin (BTC)</div>
            <div class="donation-value">bc1qqkhzmz0fmlgt8m0sn2d3hf9qpz56mpsrmkz4k9</div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("""
        <div class="donation-item">
            <div class="donation-label">💎 Ethereum (ETH)</div>
            <div class="donation-value">0x4533957C8a21043ce3843bD3ACB2e09ca59541F8</div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("""
        <div class="donation-item">
            <div class="donation-label">🔶 Binance (BNB)</div>
            <div class="donation-value">0x4533957C8a21043ce3843bD3ACB2e09ca59541F8</div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("""
        <div class="donation-item">
            <div class="donation-label">💵 USDT (ERC20)</div>
            <div class="donation-value">0x4533957C8a21043ce3843bD3ACB2e09ca59541F8</div>
        </div>
        </div>
    """, unsafe_allow_html=True)

    # Share section
    st.markdown("---")
    st.markdown("""
        <p style="text-align: center; font-weight: 600; color: #333; margin-bottom: 1rem; font-size: 1.2rem;">
            📢 Help spread the word!
        </p>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
            <a href="https://github.com/leandrodalcortivo/streamlit-app-generator"
               target="_blank"
               class="share-btn btn-github"
               style="display: block; text-align: center;">
                ⭐ Star on GitHub
            </a>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
            <a href="https://discuss.streamlit.io/"
               target="_blank"
               class="share-btn btn-community"
               style="display: block; text-align: center;">
                💬 Join Community
            </a>
        """, unsafe_allow_html=True)

    # Credits
    st.markdown("---")
    st.markdown("""
        <p style="text-align: center; font-size: 1rem; color: #666; margin-top: 1.5rem;">
            Created with ❤️ by<br>
            <strong style="font-size: 1.1rem;">Leandro Meyer Dal Cortivo</strong><br>
            <a href="https://github.com/leandrodalcortivo"
               target="_blank"
               style="color: #667eea; text-decoration: none; font-weight: 500;">
                github.com/leandrodalcortivo
            </a>
        </p>
    """, unsafe_allow_html=True)


def show_about_sidebar():
    """Display About button in sidebar that opens the modal."""
    with st.sidebar:
        st.markdown("---")
        if st.button("ℹ️ About This App", use_container_width=True, type="secondary"):
            show_about_modal()


def show_footer():
    """Display discrete footer with credits in all pages."""
    st.markdown("---")
    st.markdown("""
        <style>
        .footer {
            text-align: center;
            padding: 1rem;
            color: #888;
            font-size: 0.85rem;
        }
        .footer a {
            color: #667eea;
            text-decoration: none;
            font-weight: 500;
        }
        .footer a:hover {
            text-decoration: underline;
        }
        </style>
        <div class="footer">
            Generated with
            <a href="https://github.com/leandrodalcortivo/streamlit-app-generator" target="_blank">
                Streamlit App Generator
            </a>
            by <strong>Leandro Meyer DC</strong>
        </div>
    """, unsafe_allow_html=True)


def show_help_button():
    """Display help button with documentation links."""
    with st.sidebar:
        if st.button("❓ Help & Documentation", use_container_width=True):
            st.markdown("""
                ### 📚 Documentation

                - [Generator GitHub](https://github.com/leandrodalcortivo/streamlit-app-generator)
                - [Streamlit Docs](https://docs.streamlit.io)
                - [Report Issues](https://github.com/leandrodalcortivo/streamlit-app-generator/issues)

                ### 🆘 Need Help?

                1. Check the [README.md](./README.md) in your project
                2. Visit the [Issues page](https://github.com/leandrodalcortivo/streamlit-app-generator/issues)
                3. Join [Streamlit Community](https://discuss.streamlit.io)
            """)
