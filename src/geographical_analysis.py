import plotly.express as px

def prepare_country_data(df):
    country_data = (
        df.groupby("Country")
        .agg(
            Revenue=("TotalPrice", "sum"),
            Orders=("Invoice", "nunique"),
            Customers=("Customer ID", "nunique")
        )
        .reset_index()
    )
    return country_data

def get_geographical_kpis(country_data):
    total_countries = country_data["Country"].nunique()
    # Rregullimi i iloc[0] për të parandaluar gabimet e indeksimit në Python
    top_country = country_data.sort_values("Revenue", ascending=False).iloc[0]["Country"]
    total_revenue = country_data["Revenue"].sum()
    return {
        "countries": total_countries,
        "top_country": top_country,
        "revenue": total_revenue
    }

def revenue_map(country_data):
    """Krijon hartën që mbush komplet katrorin dhe fokusohet te shtetet"""
    fig = px.choropleth(
        country_data,
        locations="Country",
        locationmode="country names",
        color="Revenue",
        hover_name="Country",
        hover_data={"Revenue": ":,.2f", "Orders": True, "Customers": True},
        color_continuous_scale=px.colors.sequential.Tealgrn
    )
    
    fig.update_geos(
        # 1. Ky rresht e detyron hartën të bëjë ZOOM AUTOMATIK vetëm te shtetet që kanë të dhëna
        fitbounds="locations", 
        
        showframe=False,
        showcoastlines=True,
        coastlinecolor="#CBD5E1",
        showland=True,
        landcolor="#F8FAFC",
        
        # Heqim oqeanin global në mënyrë që harta të shtrihet plotësisht në katror
        showocean=False, 
        
        # Përdorim projeksionin e sheshtë që lejon shtrirjen maksimale në katrorin e Streamlit
        projection_type="equirectangular" 
    )
    
    fig.update_layout(
        height=500,  # Mund ta rritësh në 550 ose 600 nëse dëshiron katror më të lartë
        margin=dict(l=0, r=0, t=10, b=0),  # Heqim çdo hapësirë boshe anësore (Margins)
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        coloraxis_colorbar=dict(
            title="Revenue", 
            thickness=15, 
            len=250,
            yanchor="middle",
            y=0.5
        )
    )
    return fig