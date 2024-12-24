from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import numpy as np
import pandas as pd

def get_performance_metrics(pred_y, selected_features_to_scale, testing_data_cleaned, testing_data_raw, yeo_transformer, model_name):
    testing_data_pred = testing_data_cleaned[selected_features_to_scale].copy()

    # Drop 'annual_consume' column if it exists
    testing_data_pred.drop(columns=['annual_consume'], inplace=True, errors='ignore')

    # Add the predicted values
    testing_data_pred['annual_consume'] = pred_y

    # Use the transformer with a DataFrame to retain feature names
    test_data_pred_original_scale = yeo_transformer.inverse_transform(
        testing_data_pred[selected_features_to_scale]
    )
    # Convert the result back to a DataFrame
    test_data_pred_original_scale = pd.DataFrame(
        test_data_pred_original_scale, columns=selected_features_to_scale
    )

    # Extract the true values
    test_y = testing_data_raw['annual_consume']
    pred_y_scaled = test_data_pred_original_scale['annual_consume']

    # Calculate evaluation metrics using the original scale of predictions
    rmse = np.sqrt(mean_squared_error(test_y, pred_y_scaled))
    mae = mean_absolute_error(test_y, pred_y_scaled)
    r2 = r2_score(test_y, pred_y_scaled)

    # Print metrics
    print(f'{model_name}:')
    print(f"  RMSE: {rmse}")
    print(f"  MAE: {mae}")
    print(f"  R2: {r2}")
    # return (pred_y_scaled, test_y)