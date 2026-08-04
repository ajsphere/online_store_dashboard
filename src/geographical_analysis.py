import plotly.express as px

def prepare_country_data(df):
    """Përgatit të dhënat gjeografike"""
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
    """Llogarit KPI-të kryesore me rregullim iloc"""
    total_countries = country_data["Country"].nunique()
    # Rregulluar iloc për të marrë saktë vlerën e shtetit të parë pa nxjerrë gabim
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
        # ZOOM AUTOMATIK vetëm te shtetet që kanë të dhëna
        fitbounds="locations", 
        showframe=False,
        showcoastlines=True,
        coastlinecolor="#CBD5E1",
        showland=True,
        landcolor="#F8FAFC",
        showocean=False, 
        projection_type="equirectangular" 
    )
    
    fig.update_layout(
        height=500,  
        margin=dict(l=0, r=0, t=10, b=0),  # Heq çdo hapësirë boshe anësore
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

def top_countries_chart(country_data):
    """Krijon grafikun e shteteve kryesore në fund majtas"""
    top10 = country_data.sort_values("Revenue", ascending=False).head(10)
    fig = px.bar(
        top10, x="Revenue", y="Country", orientation="h",
        color="Revenue", color_continuous_scale=px.colors.sequential.Tealgrn
    )
    fig.update_layout(
        height=320, showlegend=False, coloraxis_showscale=False,
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=10, r=10, t=10, b=10)
    )
    fig.update_xaxes(showgrid=True, gridcolor="#E2E8F0", zeroline=False)
    fig.update_yaxes(showgrid=False, zeroline=False)
    return fig

def customers_country_chart(country_data):
    """Krijon grafikun e klientëve në fund djathtas"""
    top10 = country_data.sort_values("Customers", ascending=False).head(10)
    fig = px.bar(
        top10, x="Customers", y="Country", orientation="h",
        color="Customers", color_continuous_scale=px.colors.sequential.Blues
    )
    fig.update_layout(
        height=320, showlegend=False, coloraxis_showscale=False,
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=10, r=10, t=10, b=10)
    )
    fig.update_xaxes(showgrid=True, gridcolor="#E2E8F0", zeroline=False)
    fig.update_yaxes(showgrid=False, zeroline=False)
    return fig