import streamlit as st
import pandas as pd
import joblib


model = joblib.load(
    "xgb_amr_model.pkl"
)


amr_label_encoder = joblib.load(
    "amr_label_encoder.pkl"
)


features = joblib.load(
    "feature_columns.pkl"
)


target_encoder = joblib.load(
    "target_encoder.pkl"
)

def predict_amr(
    serovar,
    isolation_source,
    snp_cluster,
    min_same,
    min_diff
):

    # Create input dataframe
    input_data = pd.DataFrame({

        "Serovar": [serovar],

        "Isolation source": [isolation_source],

        "SNP cluster": [snp_cluster],

        "Min-same": [min_same],

        "Min-diff": [min_diff]

    })


    # Fill missing categorical values

    cat_cols = [
        "Serovar",
        "Isolation source",
        "SNP cluster"
    ]


    input_data[cat_cols] = input_data[cat_cols].fillna("Unknown")


    # Target encode only categorical columns

    encoded_cat = target_encoder.transform(
        input_data[cat_cols]
    )


    # Add numerical columns back

    final_input = pd.concat(
        [
            encoded_cat,

            input_data[
                [
                "Min-same",
                "Min-diff"
                ]
            ]
        ],
        axis=1
    )


    # Ensure same order as training

    final_input = final_input[
        [
        "Serovar",
        "Isolation source",
        "SNP cluster",
        "Min-same",
        "Min-diff"
        ]
    ]


    # Predict

    prediction = model.predict(
        final_input
    )


    # Convert back to label

    result = amr_label_encoder.inverse_transform(
        prediction.astype(int)
    )


    return result[0]


st.title("AMR Prediction")

st.write(
    "Enter the details of the Salmonella isolate "
    "to predict its AMR class."
)

serovar = st.text_input("Serovar")
st.caption(
    "The specific type of Salmonella enterica, "
    "such as Enteritidis or Typhimurium."
)

source = st.text_input("Isolation source")
st.caption(
    "Where the bacterial sample was collected, "
    "such as from a human, animal, food, or the environment."
)

snp = st.text_input("SNP cluster")
st.caption(
    "The identifier of the genetic cluster to which "
    "the isolate belongs, based on SNP analysis."
)

min_same = st.number_input(
    "Min-same",
    min_value=0,
    step=1
)
st.caption(
    "Minimum SNP distance to an isolate of the same "
    "isolation type within the relevant cluster."
)

min_diff = st.number_input(
    "Min-diff",
    min_value=0,
    step=1
)
st.caption(
    "Minimum SNP distance to an isolate of a different "
    "isolation type within the relevant cluster."
)


if st.button("Predict"):

    # Check that all required inputs are provided
    if not serovar.strip():
        st.warning("Please enter the Serovar.")

    elif not source.strip():
        st.warning("Please enter the Isolation source.")

    elif not snp.strip():
        st.warning("Please enter the SNP cluster.")

    else:
        # Run prediction only after validation
        result = predict_amr(
            serovar,
            source,
            snp,
            min_same,
            min_diff
        )

        # Display prediction
        st.success(f"Predicted AMR class: {result}")

        # Display interpretation
        st.subheader("Interpretation")

        if str(result).strip().title() == "Low":
            st.info(
                "The model predicts a low AMR gene burden, "
                "corresponding to 0 or 1 antimicrobial "
                "resistance gene."
            )

        elif str(result).strip().title() == "Moderate":
            st.warning(
                "The model predicts a moderate AMR gene burden, "
                "corresponding to 2 to 5 antimicrobial "
                "resistance genes."
            )

        elif str(result).strip().title() == "High":
            st.error(
                "The model predicts a high AMR gene burden, "
                "corresponding to more than 5 antimicrobial "
                "resistance genes."
            )

        else:
            st.info(
                "No interpretation is available for this class."
            )

st.caption(
            "This is a machine-learning prediction and does not "
            "confirm resistance to a specific antibiotic."
        )
