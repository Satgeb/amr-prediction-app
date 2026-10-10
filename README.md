# 🧬 Salmonella AMR Prediction App

### Machine Learning for Antimicrobial Resistance Research

An interactive machine-learning application that predicts **antimicrobial resistance (AMR) gene-burden categories** in *Salmonella enterica* using genomic and epidemiological features. Built with XGBoost and Streamlit, the app provides an accessible interface for exploring AMR-related patterns.

## 🚀 Live Demo
**Try the application:** [Open AMR Prediction App](https://amr-prediction-app.streamlit.app/)

## 📊 Dataset
The project uses the [Pathogen Detection – Salmonella enterica dataset on Kaggle](https://www.kaggle.com/datasets/imtkaggleteam/pathogen-detection-salmonella-enterica).

During data preparation, samples were categorised according to the number of AMR genes recorded:

| Predicted category | Number of AMR genes |
|---|---:|
| Low | 0–1 |
| Moderate | 2–5 |
| High | >5 |

These categories represent AMR gene burden, not clinical infection severity or confirmed resistance to a specific antibiotic.

## 🔬 Features Used
The model uses five features to predict the AMR category:

- **Serovar:** Bacterial serovar classification.
- **Isolation source:** Recorded source of the bacterial isolate.
- **SNP cluster:** Grouping of genomically related isolates.
- **Min-same:** Minimum SNP distance to an isolate of the same isolation type within the relevant cluster.
- **Min-diff:** Minimum SNP distance to an isolate of a different isolation type within the relevant cluster.

## ⚙️ Model and Methodology
- **Algorithm:** XGBoost classifier.
- **Target:** Low, Moderate, or High AMR gene-burden category.
- **Preprocessing:** Target encoding of categorical features.
- **Deployment:** Streamlit Community Cloud.

The model learns associations between the five input features and the categories derived from AMR gene counts. At prediction time, users enter feature values and receive a predicted category.

## 📈 Model Performance

The reported classification results across 111,764 evaluated samples were:

| Metric | Score |
|---|---:|
| Accuracy | 94% |
| Macro F1-score | 0.87 |
| Weighted F1-score | 0.94 |

The model achieved its strongest class-level performance for Class 2 (F1-score: 0.97), while Class 1 had an F1-score of 0.80. The class distribution was imbalanced, so class-specific results are important alongside overall accuracy.

## 💡 Research Significance
This project explores whether bacterial classification, isolation-source information, and genomic clustering features can help predict AMR gene-burden categories. It demonstrates the application of machine learning to pathogen-related data and the deployment of a research model as an interactive web application.

## ⚠️ Limitations
Predictions reflect patterns learned from the training data. The model does not directly count AMR genes in a new sample or confirm resistance to an individual antibiotic. Its performance on independent datasets requires appropriate validation.

This application is intended for research and educational purposes and does not replace laboratory antimicrobial susceptibility testing or clinical decision-making.

## 🛠️ Technologies
Python · XGBoost · Scikit-learn · Category Encoders · Pandas · Joblib · Streamlit

## 👤 Author
**Saimon Ahmad Talukdar**

GitHub repository: [https://github.com/Satgeb/amr-prediction-app.git]
