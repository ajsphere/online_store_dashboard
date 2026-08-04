import streamlit as st
import pandas as pd
import plotly.express as px


def prepare_country_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Prepare country-level metrics for geographical analysis.
    """

    country_data = (
        df.groupby("Country", as_index=False)
        .agg(
            Revenue=("TotalPrice", "sum"),
            Orders=("Invoice", "nunique"),
            Customers=("Customer ID", "nunique"),
        )
        .sort_values(
            by="Revenue",
            ascending=False,
        )
    )

    return country_data
def revenue_by_country_map(country_data: pd.DataFrame):

    fig = px.choropleth(
        country_data,
        locations="Country",
        locationmode="country names",
        color="Revenue",
        hover_name="Country",
        hover_data={
            "Revenue": ":,.2f",
            "Orders": True,
            "Customers": True,
        },
        color_continuous_scale="Blues",
        projection="natural earth",
    )

    fig.update_layout(
        height=550,
        margin=dict(l=0, r=0, t=10, b=0),
        coloraxis_colorbar_title="Revenue"
    )

    fig.update_geos(
        showframe=False,
        showcoastlines=True,
        coastlinecolor="lightgray",
        showcountries=True,
        countrycolor="white",
    )

    return fig

def render_geographical_dashboard(df: pd.DataFrame):

    st.markdown("---")
st.subheader("Geographical Analysis")

country_data = prepare_country_data(df)

st.plotly_chart(
    revenue_by_country_map(country_data),
    use_container_width=True,
)

left, right = st.columns(2)

with left:
    st.plotly_chart(
        top_revenue_markets(country_data),
        use_container_width=True,
    )

with right:
    st.plotly_chart(
        customer_distribution(country_data),
        use_container_width=True,
    )
def top_revenue_markets(country_data: pd.DataFrame):

    top10 = (
        country_data
        .nlargest(10, "Revenue")
        .sort_values("Revenue")
    )

    fig = px.bar(
        top10,
        x="Revenue",
        y="Country",
        orientation="h",
        text="Revenue",
        color="Revenue",
        color_continuous_scale="Blues",
    )

    fig.update_traces(
        texttemplate="£%{x:,.0f}",
        textposition="outside",
    )

    fig.update_layout(
        title="Top Revenue Markets",
        height=420,
        coloraxis_showscale=False,
        xaxis_title="Revenue",
        yaxis_title="",
        margin=dict(l=0, r=10, t=45, b=0),
    )

    return fig
def customer_distribution(country_data: pd.DataFrame):

    top10 = (
        country_data
        .nlargest(10, "Customers")
        .sort_values("Customers")
    )

    fig = px.bar(
        top10,
        x="Customers",
        y="Country",
        orientation="h",
        text="Customers",
        color="Customers",
        color_continuous_scale="Greens",
    )

    fig.update_traces(
        textposition="outside",
    )

    fig.update_layout(
        title="Customer Distribution",
        height=420,
        coloraxis_showscale=False,
        xaxis_title="Customers",
        yaxis_title="",
        margin=dict(l=0, r=10, t=45, b=0),
    )

    return fig