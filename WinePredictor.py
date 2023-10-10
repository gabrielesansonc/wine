import pandas as pd
import streamlit as st
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_curve, auc
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix


# Load the data into data variable
data = pd.read_excel(r"WineSampleFile.xlsx")

# Calculate the correlation matrix
correlation_matrix = data[['Price', 'Europe', 'VivinoRating', 'ABV', 'Bold', 'Tannic', 'Sweet', 'Acidic']].corr()

# Define the Streamlit app
def main():
    st.title("Wine Likelihood Prediction App")

    # Get user inputs for predictor variables
    price = st.number_input("Price", min_value=0.0, step=0.01)
    europe = st.selectbox("Europe (1 for Europe, 0 for non-Europe)", [1, 0])
    vivino_rating = st.number_input("Vivino Rating", min_value=0.0, max_value=5.0, step=0.1)
    abv = st.number_input("ABV (Alcohol by Volume)", min_value=0.0, step=0.1)
    bold = st.number_input("Bold", min_value=0.0, max_value=10.0, step=0.5)
    tannic = st.number_input("Tannic", min_value=0.0, max_value=10.0, step=0.5)
    sweet = st.number_input("Sweet", min_value=0.0, max_value=10.0, step=0.5)
    acidic = st.number_input("Acidic", min_value=0.0, max_value=10.0, step=0.5)

    # Define the predictor variables
    xvar = data[['Price', 'Europe', 'VivinoRating', 'ABV', 'Bold', 'Tannic', 'Sweet', 'Acidic']]

    # Create a binary rating based on the threshold
    BinaryRating = []
    for i in data['MyRating']:
        if i > 8.5:
            BinaryRating.append(1)
        else:
            BinaryRating.append(0)
    data['MyRatBin'] = BinaryRating

    # Define the target variable
    yvar = data['MyRatBin']

    # Train the Logistic Regression Model
    model = LogisticRegression(max_iter=1000)  # Increase max_iter from the default value
    model.fit(xvar, yvar)

    # Create a new DataFrame with user input
    user_input = pd.DataFrame({'Price': [price], 'Europe': [europe],
                                'VivinoRating': [vivino_rating], 'ABV': [abv], 'Bold': [bold],
                                'Tannic': [tannic], 'Sweet': [sweet], 'Acidic': [acidic]})

    # Predict the probability of liking the wine
    prob_liking = model.predict_proba(user_input)[:, 1]  # Probabilities of the positive class

    # Display the result
    st.subheader("Prediction Result")
    st.write(f"Probability of liking the wine: {prob_liking[0]:.2f}")

    # Calculate and display the confusion matrix
    st.subheader("Confusion Matrix")
    y_pred = model.predict(xvar)
    cm = confusion_matrix(yvar, y_pred)
    plt.figure(figsize=(6, 4))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', linewidths=.5, annot_kws={"size": 16})
    plt.xlabel('Predicted')
    plt.ylabel('Actual')
    st.pyplot(plt)

    # Calculate ROC curve
    fpr, tpr, _ = roc_curve(yvar, model.predict_proba(xvar)[:, 1])
    roc_auc = auc(fpr, tpr)

    # Display ROC curve
    st.subheader("Receiver Operating Characteristic (ROC) Curve")
    fig, ax = plt.subplots()
    plt.plot(fpr, tpr, color='darkorange', lw=2, label='ROC curve (area = {:.2f})'.format(roc_auc))

    # Customize the plot (add labels, legend, etc.)
    plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('ROC Curve')
    plt.legend(loc="lower right")

    # Display the plot in Streamlit
    st.pyplot(fig)

if __name__ == "__main__":
    main()