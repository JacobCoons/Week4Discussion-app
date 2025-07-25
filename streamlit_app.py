import streamlit as st
import altair as alt
import pandas as pd

url = "https://cdn.jsdelivr.net/npm/vega-datasets@1/data/burtin.json"
df = pd.read_json(url)

# Keep only species (last token)
df['Bacteria_short'] = df['Bacteria'].apply(lambda x: x.split()[-1])

# Rename column for convenience
df = df.rename(columns={"Gram_Staining": "Gram"})



# Always linear scale
y_scale = alt.Scale(type="linear")

def make_bar(y_col, nice_name):
    return (
        alt.Chart(df)
        .mark_bar()
        .encode(
            x=alt.X(
                "Bacteria_short:N",
                axis=alt.Axis(title="Bacteria (species only)", labelAngle=-45)
            ),
            y=alt.Y(
                f"{y_col}:Q",
                title="Minimum Inhibitory Concentration (MIC, µg/mL)",
                scale=y_scale
            ),
            color=alt.Color("Gram:N", scale=alt.Scale(scheme='redblue'), title="Gram Staining"),
            tooltip=[
                alt.Tooltip("Bacteria:N", title="Bacteria (full)"),
                alt.Tooltip("Bacteria_short:N", title="Species"),
                alt.Tooltip(f"{y_col}:Q", title=f"{nice_name} MIC"),
                alt.Tooltip("Gram:N", title="Gram")
            ]
        )
        .properties(
            title=f"MIC of {nice_name}",
            width=700,
            height=300
        )
    )

bar1 = make_bar("Penicillin", "Penicillin")
bar2 = make_bar("Streptomycin", "Streptomycin")
bar3 = make_bar("Neomycin", "Neomycin")

annotation1 = (
    alt.Chart(pd.DataFrame({"text": ["Penicillin fails against most Gram-negative bacteria"]}))
    .mark_text(align="left", fontSize=12, dx=90, dy=-10)
    .encode(x=alt.value(5), y=alt.value(15), text="text:N")
)

annotation3 = (
    alt.Chart(pd.DataFrame({"text": ["Neomycin remains consistently effective"]}))
    .mark_text(align="left", fontSize=12, dx=100, dy=100)
    .encode(x=alt.value(5), y=alt.value(15), text="text:N")
)

bar1 = bar1 + annotation1
bar3 = bar3 + annotation3

# Stack charts
chart = alt.vconcat(bar1, bar2, bar3).resolve_scale(y='shared')
st.title('Antibiotics behave differently depending on whether bacteria are Gram-positive or Gram-negative.')
st.subheader('Penicillin dominates Gram-positive infections, but Streptomycin is the more universal option.')
st.write("This app visualizes the Minimum Inhibitory Concentration (MIC) of various bacteria against different antibiotics. It is important to note that the lower MIC the more effective the antibiotic is. The data is sourced from Burtin.")
st.altair_chart(chart, use_container_width=True)
