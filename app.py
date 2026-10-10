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


serovar = st.text_input(
    "Serovar"
)


source = st.text_input(
    "Isolation source"
)


snp = st.text_input(
    "SNP cluster"
)


min_same = st.number_input(
    "Min-same"
)


min_diff = st.number_input(
    "Min-diff"
)



if st.button("Predict"):


    result = predict_amr(

        serovar,

        source,

        snp,

        min_same,

        min_diff

    )


    st.success(
        f"Predicted AMR class: {result}"
    )

