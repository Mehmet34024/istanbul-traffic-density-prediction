import streamlit as st

def init_v0_styles():
    """
    💻 UI/UX DESIGN & TAILWIND CSS LAYER (Mehmet Açıkgöz)
    TR: v0.app üzerindeki kurumsal ve modern arayüz taslağının Streamlit mimarisine
        giydirildiği global CSS ve font yapılandırma katmanıdır (Separation of Concerns).
    EN: Global CSS and typography layer that adapts the v0.app UI design into Streamlit.
    """
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Geist:wght=300;400;500;600;700&display=swap');
        
        * { font-family: 'Geist', sans-serif !important; }
        .stApp { background-color: #f8fafc !important; }
        [data-testid="stMainBlockContainer"] { max-width: 95% !important; padding: 2rem !important; }
        [data-testid="stSidebar"] { background-color: #ffffff !important; border-right: 1px solid #e2e8f0 !important; }
        
        .v0-card {
            background-color: #ffffff;
            padding: 24px;
            border-radius: 0.625rem;
            box-shadow: 0 1px 3px 0 rgb(0 0 0 / 0.05), 0 1px 2px -1px rgb(0 0 0 / 0.05);
            border: 1px solid #e2e8f0;
            margin-bottom: 24px;
            width: 100% !important;
        }
        
        .team-card { height: 230px !important; margin-bottom: 24px !important; }
        
        .stButton>button {
            background-color: #0f172a !important; color: #f8fafc !important;
            border-radius: 0.625rem !important; padding: 12px 24px !important;
            font-weight: 600 !important; border: 1px solid #0f172a !important;
            width: 100%; transition: all 0.2s ease;
        }
        .stButton>button:hover { background-color: #1e293b !important; border-color: #1e293b !important; transform: translateY(-1px); }
        h1, h2, h3, h4, h5, h6 { color: #0f172a !important; font-weight: 700 !important; }
        p { color: #64748b !important; }
        
        .badge { display: inline-flex; align-items: center; border-radius: 9999px; padding: 6px 14px; font-size: 14px; font-weight: 600; }
        .badge-red { background-color: #fee2e2; color: #991b1b; }
        .badge-yellow { background-color: #fef9c3; color: #854d0e; }
        .badge-green { background-color: #dcfce7; color: #166534; }
        </style>
    """, unsafe_allow_html=True)