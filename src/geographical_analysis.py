import plotly.express as px


def prepare_country_data(df):
    """
    Prepare geographical analysis data
    """

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
    """
    Calculate geographical KPIs
    """

    total_countries = country_data["Country"].nunique()

    top_country = (
        country_data
        .sort_values(
            "Revenue",
            ascending=False
        )
        .iloc[0]["Country"]
    )

    total_revenue = country_data["Revenue"].sum()

    return {
        "countries": total_countries,
        "top_country": top_country,
        "revenue": total_revenue
    }



def revenue_map(country_data):

    fig = px.choropleth(
        country_data,
        locations="Country",
        locationmode="country names",
        color="Revenue",
        hover_name="Country",
        hover_data={
            "Revenue": ":,.2f",
            "Orders": True,
            "Customers": True
        },
        title="Revenue Distribution by Country"
    )

    fig.update_layout(
        height=550,
        margin=dict(
            l=0,
            r=0,
            t=50,
            b=0
        )
    )

    return fig



def top_countries_chart(country_data):

    top10 = (
        country_data
        .sort_values(
            "Revenue",
            ascending=False
        )
        .head(10)
    )

    fig = px.bar(
        top10,
        x="Revenue",
        y="Country",
        orientation="h",
        title="Top 10 Countries by Revenue"
    )

    fig.update_layout(
        height=400,
        yaxis={
            "categoryorder": "total ascending"
        }
    )

    return fig



def customers_country_chart(country_data):

    top10 = (
        country_data
        .sort_values(
            "Customers",
            ascending=False
        )
        .head(10)
    )

    fig = px.bar(
        top10,
        x="Customers",
        y="Country",
        orientation="h",
        title="Customers by Country"
    )

    fig.update_layout(
        height=400,
        yaxis={
            "categoryorder": "total ascending"
        }
    )

    return fig