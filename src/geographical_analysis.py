import pandas as pd
import plotly.express as px


def prepare_country_data(df):
    """
    Prepare data for geographical analysis
    """

    country_data = (
        df.groupby("Country")
        .agg(
            Revenue=("TotalPrice", "sum"),
            Orders=("InvoiceNo", "nunique"),
            Customers=("CustomerID", "nunique")
        )
        .reset_index()
    )

    return country_data



def revenue_by_country_map(country_data):
    """
    World map - Revenue by Country
    """

    fig = px.choropleth(
        country_data,
        locations="Country",
        locationmode="country names",
        color="Revenue",
        hover_name="Country",
        hover_data=[
            "Revenue",
            "Orders",
            "Customers"
        ],
        title="Revenue by Country"
    )

    fig.update_layout(
        height=500
    )

    return fig



def top_countries_revenue(country_data):
    """
    Top 10 countries by revenue
    """

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



def customers_by_country(country_data):
    """
    Customers by Country
    """

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
        x="Country",
        y="Customers",
        title="Customers by Country"
    )

    fig.update_layout(
        height=400
    )

    return fig