
# import pandas as pd
# import streamlit as st 
# import plotly.express as px
# import matplotlib.pyplot as plt
# import sqlite3 as sql
# st.title("Supply Chain Management")
# st.divider()
# st.sidebar.header("Choose your option")
# x=st.sidebar.file_uploader("Upload your data here",type="csv")
# Data=pd.read_csv(x)

# Data['Date']=pd.to_datetime(Data['Date']).dt.date


# database=sql.connect("supply_chain.db")
# database.execute('DROP TABLE IF EXISTS "Data"')
# database.commit()
# Data.to_sql('Data',database,if_exists="replace",index=False)
# supplychain=pd.read_sql('select * from Data',database)
# supplychain

# tab1,tab2,tab3,tab4=st.tabs(["Overview","Distance Analysis","Supply Analysis","Inventory Management"])

# with tab1:
    
#     selected_columns=st.sidebar.multiselect("Select the columns you want to see",Data["Product_Category"].unique())
#     selected_date = st.sidebar.date_input(
#         "Select Date",
#         Data["Date"].min(),
#         Data["Date"].min(),
#         Data["Date"].max()
#     )
#     p=pd.read_sql('select Product_Category,count(*) as Total_products ' 
#     'from Data '   
#     'group by Product_Category',database)
#     st.write("Total products in each category")
#     st.bar_chart(p,x='Product_Category',y='Total_products',color='Product_Category')
#     o=Data.groupby('Product_Category')['Weight_MT'].sum().reset_index()
    
#     i=st.area_chart(o,x='Product_Category',y='Weight_MT',color='green')
    

# with tab2:
 
#     i=pd.read_sql('select Transport_Mode, sum(Distance_km) as Total_Distance_km ' 
#     'from Data '   
#     'group by Transport_Mode',database)
#     st.write("Total distance covered by each transport mode")
#     st.bar_chart(i,x="Transport_Mode",y="Total_Distance_km",color="Transport_Mode",horizontal=True)
#     plt.boxplot(Data['Fuel_Price_Index'])
#     plt.title("Fuel Price Index Distribution")
#     st.pyplot(plt)



#     with tab3:
#         r=pd.read_sql('select Origin_Port,count(Shipment_ID) as Total_Shipments '
#                     'from Data '
#                     'Group by Origin_Port',database)
        
#         st.bar_chart(r,x="Origin_Port",y="Total_Shipments",color="Origin_Port")
#         d=Data.groupby('Destination_Port')['Shipment_ID'].count().reset_index()
       
       
#         st.bar_chart(d, x='Destination_Port', y='Shipment_ID',horizontal=True,color='Destination_Port')
#         plt.boxplot(Data['Geopolitical_Risk_Score'])
#         plt.title('Geopolitical_Risk_Score')
#         st.pyplot(plt)

#     with tab4:
#              g=Data['Weather_Condition'].value_counts()
#              g
#              plt.boxplot(Data['Lead_Time_Days'])
#              plt.title('Time_Traking')
#              st.pyplot(plt)

            




####################
import pandas as pd
import streamlit as st
import plotly.express as px
import matplotlib.pyplot as plt
import sqlite3 as sql

st.set_page_config(page_title="Supply Chain Management", page_icon="🚚", layout="wide")

# ------------------------------------------------------------------ #
#  STYLE: colors + animations
# ------------------------------------------------------------------ #
PALETTE = ["#00E5FF", "#7C4DFF", "#FF4081", "#FFC400", "#00E676", "#FF6E40", "#40C4FF", "#E040FB"]

st.markdown("""
<style>
@keyframes bgShift {0%{background-position:0% 50%} 50%{background-position:100% 50%} 100%{background-position:0% 50%}}
@keyframes fadeUp {from{opacity:0; transform:translateY(24px)} to{opacity:1; transform:translateY(0)}}
@keyframes floaty {0%,100%{transform:translateY(0)} 50%{transform:translateY(-6px)}}
@keyframes glow {0%,100%{box-shadow:0 0 0 rgba(0,229,255,0)} 50%{box-shadow:0 0 22px rgba(0,229,255,.35)}}
@keyframes titleShine {0%{background-position:0% 50%} 100%{background-position:200% 50%}}

.stApp{
  background: linear-gradient(135deg,#0B1020,#12193a,#0B1020,#16123a);
  background-size: 400% 400%;
  animation: bgShift 22s ease infinite;
  color:#E6EDF7;
}
h1{
  background: linear-gradient(90deg,#00E5FF,#7C4DFF,#FF4081,#00E5FF);
  background-size:200% auto;
  -webkit-background-clip:text; -webkit-text-fill-color:transparent;
  animation: titleShine 6s linear infinite, fadeUp .8s ease both;
  font-weight:800 !important;
}
[data-testid="stSidebar"]{
  background: linear-gradient(180deg,#0E1630,#0A0F22);
  border-right:1px solid rgba(0,229,255,.2);
}
.stTabs [data-baseweb="tab-list"]{gap:8px}
.stTabs [data-baseweb="tab"]{
  background:rgba(255,255,255,.05); border-radius:12px 12px 0 0;
  padding:10px 18px; transition:all .3s ease;
}
.stTabs [data-baseweb="tab"]:hover{background:rgba(0,229,255,.15); transform:translateY(-2px)}
.stTabs [aria-selected="true"]{
  background:linear-gradient(90deg,#00E5FF33,#7C4DFF33) !important;
  border-bottom:3px solid #00E5FF !important;
}
.kpi-card{
  --c:#00E5FF;
  background:linear-gradient(145deg,rgba(255,255,255,.08),rgba(255,255,255,.02));
  border:1px solid rgba(255,255,255,.1); border-top:4px solid var(--c);
  border-radius:16px; padding:16px 18px; margin-bottom:12px;
  animation: fadeUp .7s ease both;
  transition: transform .3s ease, box-shadow .3s ease;
}
.kpi-card:hover{transform:translateY(-6px) scale(1.02); box-shadow:0 10px 30px color-mix(in srgb,var(--c) 45%,transparent)}
.kpi-icon{font-size:30px; display:inline-block; animation: floaty 3s ease-in-out infinite}
.kpi-label{font-size:13px; letter-spacing:.8px; text-transform:uppercase; color:#9FB3D1; margin-top:4px}
.kpi-value{font-size:30px; font-weight:800; color:var(--c)}
[data-testid="stPlotlyChart"], [data-testid="stImage"], [data-testid="stDataFrame"]{
  animation: fadeUp .9s ease both;
  background:rgba(255,255,255,.03); border:1px solid rgba(255,255,255,.07);
  border-radius:16px; padding:8px;
}
[data-testid="stPlotlyChart"]:hover{animation: glow 2s ease infinite}
hr{border-color:rgba(0,229,255,.25) !important}
</style>
""", unsafe_allow_html=True)


# ------------------------------------------------------------------ #
#  HELPERS
# ------------------------------------------------------------------ #
def kpi_row(items):
    """items = [(icon, label, value, color), ...]"""
    cols = st.columns(len(items))
    for i, (col, (icon, label, value, color)) in enumerate(zip(cols, items)):
        col.markdown(
            f'<div class="kpi-card" style="--c:{color}; animation-delay:{i*0.12}s">'
            f'<div class="kpi-icon">{icon}</div>'
            f'<div class="kpi-label">{label}</div>'
            f'<div class="kpi-value">{value}</div></div>',
            unsafe_allow_html=True,
        )


def style_fig(fig):
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#E6EDF7"),
        legend_title_text="",
        margin=dict(t=40, b=20, l=10, r=10),
        transition_duration=600,
    )
    return fig


def label_bars(fig):
    fig.update_traces(textposition="outside", cliponaxis=False, textfont_size=13,
                      marker_line_width=0)
    return style_fig(fig)


def styled_box(series, title, color):
    """Matplotlib boxplot (same as before) + data labels for the key stats."""
    s = series.dropna()
    fig, ax = plt.subplots(figsize=(8, 4))
    fig.patch.set_facecolor("#111A2E")
    ax.set_facecolor("#111A2E")
    ax.boxplot(
        s, patch_artist=True,
        boxprops=dict(facecolor=color + "55", edgecolor=color, linewidth=2),
        medianprops=dict(color="#FFC400", linewidth=2.5),
        whiskerprops=dict(color=color), capprops=dict(color=color),
        flierprops=dict(markerfacecolor="#FF4081", markeredgecolor="#FF4081", alpha=.7),
    )
    ax.set_title(title, color="white", fontsize=14, fontweight="bold")
    ax.tick_params(colors="#9FB3D1")
    for sp in ax.spines.values():
        sp.set_color("#2B3A5C")
    stats = {"Min": s.min(), "Q1": s.quantile(.25), "Median": s.median(),
             "Q3": s.quantile(.75), "Max": s.max()}
    for name, val in stats.items():
        ax.annotate(f"{name}: {val:,.2f}", xy=(1.08, val), color="white", fontsize=9,
                    va="center", bbox=dict(boxstyle="round,pad=0.2", fc="#1B2A4A", ec=color, lw=.8))
    ax.set_xlim(0.6, 1.5)
    st.pyplot(fig)
    plt.close(fig)


def range_filter(label, series, key):
    lo, hi = float(series.min()), float(series.max())
    if lo == hi:
        return lo, hi
    return st.slider(label, lo, hi, (lo, hi), key=key)


# ------------------------------------------------------------------ #
#  APP (original structure)
# ------------------------------------------------------------------ #
st.title("🚚 Supply Chain Management")
st.divider()
st.sidebar.header("🎛️ Choose your option")
x = st.sidebar.file_uploader("Upload your data here", type="csv")

if x is None:
    st.info("⬅️ Upload your CSV file from the sidebar to load the dashboard.")
    st.stop()

Data = pd.read_csv(x)

Data['Date'] = pd.to_datetime(Data['Date']).dt.date


database = sql.connect("supply_chain.db")
database.execute('DROP TABLE IF EXISTS "Data"')
database.commit()
Data.to_sql('Data', database, if_exists="replace", index=False)
supplychain = pd.read_sql('select * from Data', database)
# supplychain

tab1, tab2, tab3, tab4 = st.tabs(["📊 Overview", "📏 Distance Analysis", "🌍 Supply Analysis", "📦 Inventory Management"])

# ------------------------------- TAB 1 ------------------------------- #
with tab1:

    selected_columns = st.sidebar.multiselect("📂 Select the columns you want to see", Data["Product_Category"].unique())
    selected_date = st.sidebar.date_input(
        "📅 Select Date",
        (Data["Date"].min(), Data["Date"].max()),
        Data["Date"].min(),
        Data["Date"].max()
    )

    # dynamic filtering (sidebar filters drive this tab)
    f1 = Data.copy()
    if selected_columns:
        f1 = f1[f1["Product_Category"].isin(selected_columns)]
    if isinstance(selected_date, (tuple, list)) and len(selected_date) == 2:
        f1 = f1[(f1["Date"] >= selected_date[0]) & (f1["Date"] <= selected_date[1])]

    if f1.empty:
        st.warning("No data for the selected filters.")
    else:
        f1.to_sql('Filtered', database, if_exists="replace", index=False)

        kpi_row([
            ("📦", "Total Shipments", f"{f1['Shipment_ID'].count():,}", "#00E5FF"),
            ("⚖️", "Total Weight (MT)", f"{f1['Weight_MT'].sum():,.0f}", "#7C4DFF"),
            ("🗂️", "Product Categories", f"{f1['Product_Category'].nunique()}", "#FF4081"),
            ("⏱️", "Avg Lead Time (Days)", f"{f1['Lead_Time_Days'].mean():.1f}", "#FFC400"),
        ])

        p = pd.read_sql('select Product_Category,count(*) as Total_products '
                        'from Filtered '
                        'group by Product_Category', database)
        o = f1.groupby('Product_Category')['Weight_MT'].sum().reset_index()

        st.write("Total products in each category")
        fig = px.bar(p, x='Product_Category', y='Total_products', color='Product_Category',
                     text='Total_products', color_discrete_sequence=PALETTE)
        st.plotly_chart(label_bars(fig), use_container_width=True)

        i = px.area(o, x='Product_Category', y='Weight_MT',title='Product_Category by Weight' ,color_discrete_sequence=["green"],
                    text='Weight_MT', markers=True)
            
        i.update_traces(mode="lines+markers+text", texttemplate="%{y:,.0f}", textposition="top center",
                        fillcolor="rgba(0,230,118,.25)", line_color="#00E676")
        st.plotly_chart(style_fig(i), use_container_width=True)


# ------------------------------- TAB 2 ------------------------------- #
with tab2:

    c1, c2 = st.columns(2)
    with c1:
        sel_mode = st.multiselect("🚛 Transport Mode", sorted(Data["Transport_Mode"].unique()), key="t2_mode")
    with c2:
        dist_lo, dist_hi = range_filter("📏 Distance (km)", Data["Distance_km"], "t2_dist")

    f2 = Data.copy()
    if sel_mode:
        f2 = f2[f2["Transport_Mode"].isin(sel_mode)]
    f2 = f2[(f2["Distance_km"] >= dist_lo) & (f2["Distance_km"] <= dist_hi)]

    if f2.empty:
        st.warning("No data for the selected filters.")
    else:
        f2.to_sql('Filtered', database, if_exists="replace", index=False)

        kpi_row([
            ("🛣️", "Total Distance (km)", f"{f2['Distance_km'].sum():,.0f}", "#00E676"),
            ("📐", "Avg Distance (km)", f"{f2['Distance_km'].mean():,.1f}", "#00E5FF"),
            ("🚢", "Transport Modes", f"{f2['Transport_Mode'].nunique()}", "#FF6E40"),
            ("⛽", "Avg Fuel Price Index", f"{f2['Fuel_Price_Index'].mean():.2f}", "#FFC400"),
        ])

        i = pd.read_sql('select Transport_Mode, sum(Distance_km) as Total_Distance_km '
                        'from Filtered '
                        'group by Transport_Mode', database)
        st.write("Total distance covered by each transport mode")
        fig = px.bar(i, x="Total_Distance_km", y="Transport_Mode", color="Transport_Mode",
                     orientation="h", text="Total_Distance_km", color_discrete_sequence=PALETTE)
        fig.update_traces(texttemplate="%{x:,.0f}")
        st.plotly_chart(label_bars(fig), use_container_width=True)

        styled_box(f2['Fuel_Price_Index'], "Fuel Price Index Distribution", "#00E5FF")


# ------------------------------- TAB 3 ------------------------------- #
with tab3:

    c1, c2, c3 = st.columns(3)
    with c1:
        sel_origin = st.multiselect("🛫 Origin Port", sorted(Data["Origin_Port"].unique()), key="t3_o")
    with c2:
        sel_dest = st.multiselect("🛬 Destination Port", sorted(Data["Destination_Port"].unique()), key="t3_d")
    with c3:
        risk_lo, risk_hi = range_filter("⚠️ Geopolitical Risk", Data["Geopolitical_Risk_Score"], "t3_risk")

    f3 = Data.copy()
    if sel_origin:
        f3 = f3[f3["Origin_Port"].isin(sel_origin)]
    if sel_dest:
        f3 = f3[f3["Destination_Port"].isin(sel_dest)]
    f3 = f3[(f3["Geopolitical_Risk_Score"] >= risk_lo) & (f3["Geopolitical_Risk_Score"] <= risk_hi)]

    if f3.empty:
        st.warning("No data for the selected filters.")
    else:
        f3.to_sql('Filtered', database, if_exists="replace", index=False)

        kpi_row([
            ("🚚", "Total Shipments", f"{f3['Shipment_ID'].count():,}", "#7C4DFF"),
            ("🛫", "Origin Ports", f"{f3['Origin_Port'].nunique()}", "#00E5FF"),
            ("🛬", "Destination Ports", f"{f3['Destination_Port'].nunique()}", "#00E676"),
            ("⚠️", "Avg Risk Score", f"{f3['Geopolitical_Risk_Score'].mean():.2f}", "#FF4081"),
        ])

        r = pd.read_sql('select Origin_Port,count(Shipment_ID) as Total_Shipments '
                        'from Filtered '
                        'Group by Origin_Port', database)

        d = f3.groupby('Destination_Port')['Shipment_ID'].count().reset_index()

        st.write("Shipments by origin port")
        fig = px.bar(r, x="Origin_Port", y="Total_Shipments", color="Origin_Port",
                     text="Total_Shipments", color_discrete_sequence=PALETTE)
        st.plotly_chart(label_bars(fig), use_container_width=True)

        st.write("Shipments by destination port")
        fig = px.bar(d, x='Shipment_ID', y='Destination_Port', color='Destination_Port',
                     orientation="h", text='Shipment_ID', color_discrete_sequence=PALETTE[::-1])
        st.plotly_chart(label_bars(fig), use_container_width=True)

        styled_box(f3['Geopolitical_Risk_Score'], 'Geopolitical_Risk_Score', "#FF4081")


# ------------------------------- TAB 4 ------------------------------- #
with tab4:

    c1, c2 = st.columns(2)
    with c1:
        sel_weather = st.multiselect("🌦️ Weather Condition", sorted(Data["Weather_Condition"].unique()), key="t4_w")
    with c2:
        lt_lo, lt_hi = range_filter("⏳ Lead Time (Days)", Data["Lead_Time_Days"], "t4_lt")

    f4 = Data.copy()
    if sel_weather:
        f4 = f4[f4["Weather_Condition"].isin(sel_weather)]
    f4 = f4[(f4["Lead_Time_Days"] >= lt_lo) & (f4["Lead_Time_Days"] <= lt_hi)]

    if f4.empty:
        st.warning("No data for the selected filters.")
    else:
        kpi_row([
            ("⏱️", "Avg Lead Time (Days)", f"{f4['Lead_Time_Days'].mean():.1f}", "#FFC400"),
            ("🐢", "Max Lead Time (Days)", f"{f4['Lead_Time_Days'].max():,.0f}", "#FF4081"),
            ("🌦️", "Most Common Weather", f"{f4['Weather_Condition'].mode()[0]}", "#00E5FF"),
            ("🌍", "Weather Types", f"{f4['Weather_Condition'].nunique()}", "#00E676"),
        ])

        g = f4['Weather_Condition'].value_counts()
        gdf = g.reset_index()
        gdf.columns = ["Weather_Condition", "Count"]

        g
        fig = px.bar(gdf, x="Weather_Condition", y="Count", color="Weather_Condition",
                     text="Count", color_discrete_sequence=PALETTE)
        st.plotly_chart(label_bars(fig), use_container_width=True)

        styled_box(f4['Lead_Time_Days'], 'Time_Traking', "#FFC400")