import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.set_page_config(
    page_title="Shaping STEM Futures – Event Dashboard",
    page_icon="🌱",
    layout="wide"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;600&family=DM+Serif+Display&display=swap');
    html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
    h1, h2, h3 { font-family: 'DM Serif Display', serif; }
    .metric-card {
        background: #f0f7f4;
        border-left: 4px solid #2d7a5f;
        border-radius: 8px;
        padding: 1.2rem 1.5rem;
    }
    .metric-card .label { font-size: 0.8rem; color: #6b7280; text-transform: uppercase; letter-spacing: 0.08em; }
    .metric-card .value { font-size: 2.2rem; font-weight: 600; color: #1a1a2e; line-height: 1.1; }
</style>
""", unsafe_allow_html=True)

# ─── Load from Excel ──────────────────────────────────────────────────────────
EXCEL_FILE = "events_data.xlsx"

if not os.path.exists(EXCEL_FILE):
    st.error(f"❌ Could not find '{EXCEL_FILE}'. Make sure it's in the same folder as dashboard.py")
    st.stop()

df = pd.read_excel(EXCEL_FILE, sheet_name="Events")
df = df.dropna(subset=["Registrations"])           # skip empty rows / TOTAL row
df = df[pd.to_numeric(df["Registrations"], errors="coerce").notna()]
df["Registrations"] = df["Registrations"].astype(int)
df["Date"] = pd.to_datetime(df["Date"])
df = df.sort_values("Date")

# ─── Header ───────────────────────────────────────────────────────────────────
st.title("Shaping STEM Futures")
st.markdown("#### Event Registration Dashboard · Design for Change 2025")
st.markdown("---")

# ─── Metric cards ─────────────────────────────────────────────────────────────
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(f'<div class="metric-card"><div class="label">Total Registrations</div><div class="value">{df["Registrations"].sum()}</div></div>', unsafe_allow_html=True)
with col2:
    st.markdown(f'<div class="metric-card"><div class="label">Events Run</div><div class="value">{len(df)}</div></div>', unsafe_allow_html=True)
with col3:
    st.markdown(f'<div class="metric-card"><div class="label">Avg per Event</div><div class="value">{df["Registrations"].mean():.1f}</div></div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ─── Charts ───────────────────────────────────────────────────────────────────
col_left, col_right = st.columns([3, 2])

with col_left:
    fig_bar = px.bar(df, x="Event", y="Registrations", text="Registrations",
                     color="Registrations", color_continuous_scale=["#a8d5c2", "#2d7a5f"],
                     title="Registrations per Event")
    fig_bar.update_traces(textposition="outside")
    fig_bar.update_layout(showlegend=False, coloraxis_showscale=False,
                          plot_bgcolor="white", paper_bgcolor="white",
                          font_family="DM Sans", title_font_size=18,
                          margin=dict(t=50, b=20), xaxis=dict(tickangle=-20))
    st.plotly_chart(fig_bar, use_container_width=True)

with col_right:
    fig_line = px.line(df, x="Date", y="Registrations", markers=True, title="Trend Over Time")
    fig_line.update_traces(line_color="#2d7a5f", marker=dict(size=10, color="#2d7a5f"))
    fig_line.update_layout(plot_bgcolor="white", paper_bgcolor="white",
                           font_family="DM Sans", title_font_size=18, margin=dict(t=50, b=20))
    st.plotly_chart(fig_line, use_container_width=True)

# ─── Table ────────────────────────────────────────────────────────────────────
st.markdown("#### Event Breakdown")
display_df = df.copy()
display_df["Date"] = display_df["Date"].dt.strftime("%-d %b %Y")
st.dataframe(display_df[["Date", "Event", "Registrations"]], use_container_width=True, hide_index=True)

st.markdown("---")
st.caption("Data: Shaping STEM Futures · Swinburne University of Technology")
