import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
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
        margin-bottom: 0.5rem;
    }
    .metric-card .label { font-size: 0.8rem; color: #6b7280; text-transform: uppercase; letter-spacing: 0.08em; }
    .metric-card .value { font-size: 2.2rem; font-weight: 600; color: #1a1a2e; line-height: 1.1; }
</style>
""", unsafe_allow_html=True)

EXCEL_FILE = "events_data.xlsx"

if not os.path.exists(EXCEL_FILE):
    st.error(f"❌ Could not find '{EXCEL_FILE}'. Make sure it's in the same folder as dashboard.py")
    st.stop()

# ─── Load data ────────────────────────────────────────────────────────────────
df_events = pd.read_excel(EXCEL_FILE, sheet_name="Events")
df_events = df_events[pd.to_numeric(df_events["Registrations"], errors="coerce").notna()]
df_events["Registrations"] = df_events["Registrations"].astype(int)
df_events["Date"] = pd.to_datetime(df_events["Date"])
df_events = df_events.sort_values("Date")

df_annual = pd.read_excel(EXCEL_FILE, sheet_name="Annual")

# ─── Header ───────────────────────────────────────────────────────────────────
st.title("Shaping STEM Futures")
st.markdown("#### Registration & Satisfaction Dashboard")
st.markdown("---")

# ─── SECTION 1: Annual overview ───────────────────────────────────────────────
st.markdown("### Annual Program Overview")

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown(f'<div class="metric-card"><div class="label">Total Registrations (All Years)</div><div class="value">1,185</div></div>', unsafe_allow_html=True)
with col2:
    st.markdown(f'<div class="metric-card"><div class="label">Start Talking Total</div><div class="value">690</div></div>', unsafe_allow_html=True)
with col3:
    st.markdown(f'<div class="metric-card"><div class="label">Design for Change Total</div><div class="value">495</div></div>', unsafe_allow_html=True)
with col4:
    st.markdown(f'<div class="metric-card"><div class="label">Avg Satisfaction</div><div class="value">85%</div></div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

col_left, col_right = st.columns(2)

with col_left:
    fig_grouped = go.Figure()
    fig_grouped.add_trace(go.Bar(
        x=df_annual["Year"], y=df_annual["Start Talking Registrations"],
        name="Start Talking", marker_color="#2d7a5f"
    ))
    fig_grouped.add_trace(go.Bar(
        x=df_annual["Year"], y=df_annual["Design for Change Registrations"],
        name="Design for Change", marker_color="#a8d5c2"
    ))
    fig_grouped.update_layout(
        barmode="group", title="Registrations by Program per Year",
        plot_bgcolor="white", paper_bgcolor="white",
        font_family="DM Sans", title_font_size=16,
        legend=dict(orientation="h", yanchor="bottom", y=1.02),
        margin=dict(t=60, b=20),
        xaxis=dict(tickmode='linear', dtick=1, tickformat='d')
    )
    st.plotly_chart(fig_grouped, use_container_width=True)

with col_right:
    fig_sat = go.Figure()
    fig_sat.add_trace(go.Scatter(
        x=df_annual["Year"], y=df_annual["Start Talking Satisfaction"],
        mode="lines+markers", name="Start Talking",
        line=dict(color="#2d7a5f", width=2),
        marker=dict(size=8)
    ))
    fig_sat.add_trace(go.Scatter(
        x=df_annual["Year"], y=df_annual["Design for Change Satisfaction"],
        mode="lines+markers", name="Design for Change",
        line=dict(color="#a8d5c2", width=2),
        marker=dict(size=8)
    ))
    fig_sat.update_layout(
        title="Satisfaction Score Over Time (%)",
        plot_bgcolor="white", paper_bgcolor="white",
        font_family="DM Sans", title_font_size=16,
        yaxis=dict(range=[70, 100]),
        legend=dict(orientation="h", yanchor="bottom", y=1.02),
        margin=dict(t=60, b=20),
        xaxis=dict(tickmode='linear', dtick=1, tickformat='d')
    )
    st.plotly_chart(fig_sat, use_container_width=True)

# Combined trend
fig_total = px.line(
    df_annual, x="Year", y="Combined Total",
    markers=True, title="Combined Registration Trend (All Programs)"
)
fig_total.update_traces(line_color="#2d7a5f", marker=dict(size=10, color="#2d7a5f"))
fig_total.update_layout(
    plot_bgcolor="white", paper_bgcolor="white",
    font_family="DM Sans", title_font_size=16, margin=dict(t=50, b=20),
    xaxis=dict(tickmode='linear', dtick=1, tickformat='d')
)
st.plotly_chart(fig_total, use_container_width=True)

st.markdown("---")

# ─── SECTION 2: 2025 Workshop breakdown ───────────────────────────────────────
st.markdown("### 2025 Workshop Breakdown – Design for Change")

col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(f'<div class="metric-card"><div class="label">Total Registrations</div><div class="value">{df_events["Registrations"].sum()}</div></div>', unsafe_allow_html=True)
with col2:
    st.markdown(f'<div class="metric-card"><div class="label">Workshops Run</div><div class="value">{len(df_events)}</div></div>', unsafe_allow_html=True)
with col3:
    st.markdown(f'<div class="metric-card"><div class="label">Avg per Workshop</div><div class="value">{df_events["Registrations"].mean():.1f}</div></div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

col_left, col_right = st.columns([3, 2])

with col_left:
    fig_bar = px.bar(
        df_events, x="Event", y="Registrations", text="Registrations",
        color="Registrations", color_continuous_scale=["#a8d5c2", "#2d7a5f"],
        title="Registrations per Workshop"
    )
    fig_bar.update_traces(textposition="outside")
    fig_bar.update_layout(
        showlegend=False, coloraxis_showscale=False,
        plot_bgcolor="white", paper_bgcolor="white",
        font_family="DM Sans", title_font_size=16,
        margin=dict(t=50, b=20), xaxis=dict(tickangle=-20)
    )
    st.plotly_chart(fig_bar, use_container_width=True)

with col_right:
    fig_line = px.line(
        df_events, x="Date", y="Registrations",
        markers=True, title="Trend Over Time"
    )
    fig_line.update_traces(line_color="#2d7a5f", marker=dict(size=10, color="#2d7a5f"))
    fig_line.update_layout(
        plot_bgcolor="white", paper_bgcolor="white",
        font_family="DM Sans", title_font_size=16, margin=dict(t=50, b=20)
    )
    st.plotly_chart(fig_line, use_container_width=True)

st.markdown("#### Workshop Breakdown")
display_df = df_events.copy()
display_df["Date"] = display_df["Date"].dt.strftime("%-d %b %Y")
st.dataframe(display_df[["Date", "Event", "Registrations"]], use_container_width=True, hide_index=True)

st.markdown("---")
st.caption("Data: Shaping STEM Futures · Swinburne University of Technology")