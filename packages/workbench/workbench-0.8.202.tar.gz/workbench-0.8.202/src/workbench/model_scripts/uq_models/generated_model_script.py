# Model: XGBoost for point predictions + LightGBM with MAPIE for conformalized intervals
from mapie.regression import ConformalizedQuantileRegressor
from lightgbm import LGBMRegressor
from xgboost import XGBRegressor
from sklearn.model_selection import train_test_split

# Model Performance Scores
from sklearn.metrics import mean_absolute_error, median_absolute_error, r2_score, root_mean_squared_error
from scipy.stats import spearmanr

from io import StringIO
import json
import argparse
import joblib
import os
import numpy as np
import pandas as pd
from typing import List, Tuple, Optional, Dict

# Template Placeholders
TEMPLATE_PARAMS = {
    "target": "caco_2_efflux",
    "features": ['chi2v', 'fr_sulfone', 'chi1v', 'bcut2d_logplow', 'fr_piperzine', 'kappa3', 'smr_vsa1', 'slogp_vsa5', 'fr_ketone_topliss', 'fr_sulfonamd', 'fr_imine', 'fr_benzene', 'fr_ester', 'chi2n', 'labuteasa', 'peoe_vsa2', 'smr_vsa6', 'bcut2d_chglo', 'fr_sh', 'peoe_vsa1', 'fr_allylic_oxid', 'chi4n', 'fr_ar_oh', 'fr_nh0', 'fr_term_acetylene', 'slogp_vsa7', 'slogp_vsa4', 'estate_vsa1', 'vsa_estate4', 'numbridgeheadatoms', 'numheterocycles', 'fr_ketone', 'fr_morpholine', 'fr_guanido', 'estate_vsa2', 'numheteroatoms', 'fr_nitro_arom_nonortho', 'fr_piperdine', 'nocount', 'numspiroatoms', 'fr_aniline', 'fr_thiophene', 'slogp_vsa10', 'fr_amide', 'slogp_vsa2', 'fr_epoxide', 'vsa_estate7', 'fr_ar_coo', 'fr_imidazole', 'fr_nitrile', 'fr_oxazole', 'numsaturatedrings', 'fr_pyridine', 'fr_hoccn', 'fr_ndealkylation1', 'numaliphaticheterocycles', 'fr_phenol', 'maxpartialcharge', 'vsa_estate5', 'peoe_vsa13', 'minpartialcharge', 'qed', 'fr_al_oh', 'slogp_vsa11', 'chi0n', 'fr_bicyclic', 'peoe_vsa12', 'fpdensitymorgan1', 'fr_oxime', 'molwt', 'fr_dihydropyridine', 'smr_vsa5', 'peoe_vsa5', 'fr_nitro', 'hallkieralpha', 'heavyatommolwt', 'fr_alkyl_halide', 'peoe_vsa8', 'fr_nhpyrrole', 'fr_isocyan', 'bcut2d_chghi', 'fr_lactam', 'peoe_vsa11', 'smr_vsa9', 'tpsa', 'chi4v', 'slogp_vsa1', 'phi', 'bcut2d_logphi', 'avgipc', 'estate_vsa11', 'fr_coo', 'bcut2d_mwhi', 'numunspecifiedatomstereocenters', 'vsa_estate10', 'estate_vsa8', 'numvalenceelectrons', 'fr_nh2', 'fr_lactone', 'vsa_estate1', 'estate_vsa4', 'numatomstereocenters', 'vsa_estate8', 'fr_para_hydroxylation', 'peoe_vsa3', 'fr_thiazole', 'peoe_vsa10', 'fr_ndealkylation2', 'slogp_vsa12', 'peoe_vsa9', 'maxestateindex', 'fr_quatn', 'smr_vsa7', 'minestateindex', 'numaromaticheterocycles', 'numrotatablebonds', 'fr_ar_nh', 'fr_ether', 'exactmolwt', 'fr_phenol_noorthohbond', 'slogp_vsa3', 'fr_ar_n', 'sps', 'fr_c_o_nocoo', 'bertzct', 'peoe_vsa7', 'slogp_vsa8', 'numradicalelectrons', 'molmr', 'fr_tetrazole', 'numsaturatedcarbocycles', 'bcut2d_mrhi', 'kappa1', 'numamidebonds', 'fpdensitymorgan2', 'smr_vsa8', 'chi1n', 'estate_vsa6', 'fr_barbitur', 'fr_diazo', 'kappa2', 'chi0', 'bcut2d_mrlow', 'balabanj', 'peoe_vsa4', 'numhacceptors', 'fr_sulfide', 'chi3n', 'smr_vsa2', 'fr_al_oh_notert', 'fr_benzodiazepine', 'fr_phos_ester', 'fr_aldehyde', 'fr_coo2', 'estate_vsa5', 'fr_prisulfonamd', 'numaromaticcarbocycles', 'fr_unbrch_alkane', 'fr_urea', 'fr_nitroso', 'smr_vsa10', 'fr_c_s', 'smr_vsa3', 'fr_methoxy', 'maxabspartialcharge', 'slogp_vsa9', 'heavyatomcount', 'fr_azide', 'chi3v', 'smr_vsa4', 'mollogp', 'chi0v', 'fr_aryl_methyl', 'fr_nh1', 'fpdensitymorgan3', 'fr_furan', 'fr_hdrzine', 'fr_arn', 'numaromaticrings', 'vsa_estate3', 'fr_azo', 'fr_halogen', 'estate_vsa9', 'fr_hdrzone', 'numhdonors', 'fr_alkyl_carbamate', 'fr_isothiocyan', 'minabspartialcharge', 'fr_al_coo', 'ringcount', 'chi1', 'estate_vsa7', 'fr_nitro_arom', 'vsa_estate9', 'minabsestateindex', 'maxabsestateindex', 'vsa_estate6', 'estate_vsa10', 'estate_vsa3', 'fr_n_o', 'fr_amidine', 'fr_thiocyan', 'fr_phos_acid', 'fr_c_o', 'fr_imide', 'numaliphaticrings', 'peoe_vsa6', 'vsa_estate2', 'nhohcount', 'numsaturatedheterocycles', 'slogp_vsa6', 'peoe_vsa14', 'fractioncsp3', 'bcut2d_mwlow', 'numaliphaticcarbocycles', 'fr_priamide', 'nacid', 'nbase', 'naromatom', 'narombond', 'sz', 'sm', 'sv', 'sse', 'spe', 'sare', 'sp', 'si', 'mz', 'mm', 'mv', 'mse', 'mpe', 'mare', 'mp', 'mi', 'xch_3d', 'xch_4d', 'xch_5d', 'xch_6d', 'xch_7d', 'xch_3dv', 'xch_4dv', 'xch_5dv', 'xch_6dv', 'xch_7dv', 'xc_3d', 'xc_4d', 'xc_5d', 'xc_6d', 'xc_3dv', 'xc_4dv', 'xc_5dv', 'xc_6dv', 'xpc_4d', 'xpc_5d', 'xpc_6d', 'xpc_4dv', 'xpc_5dv', 'xpc_6dv', 'xp_0d', 'xp_1d', 'xp_2d', 'xp_3d', 'xp_4d', 'xp_5d', 'xp_6d', 'xp_7d', 'axp_0d', 'axp_1d', 'axp_2d', 'axp_3d', 'axp_4d', 'axp_5d', 'axp_6d', 'axp_7d', 'xp_0dv', 'xp_1dv', 'xp_2dv', 'xp_3dv', 'xp_4dv', 'xp_5dv', 'xp_6dv', 'xp_7dv', 'axp_0dv', 'axp_1dv', 'axp_2dv', 'axp_3dv', 'axp_4dv', 'axp_5dv', 'axp_6dv', 'axp_7dv', 'c1sp1', 'c2sp1', 'c1sp2', 'c2sp2', 'c3sp2', 'c1sp3', 'c2sp3', 'c3sp3', 'c4sp3', 'hybratio', 'fcsp3', 'num_stereocenters', 'num_unspecified_stereocenters', 'num_defined_stereocenters', 'num_r_centers', 'num_s_centers', 'num_stereobonds', 'num_e_bonds', 'num_z_bonds', 'stereo_complexity', 'frac_defined_stereo'],
    "compressed_features": [],
    "train_all_data": True,
    "hyperparameters": {'n_estimators': 200, 'max_depth': 6, 'learning_rate': 0.05, 'subsample': 0.7, 'colsample_bytree': 0.6, 'colsample_bylevel': 0.8, 'min_child_weight': 5, 'gamma': 0.2, 'reg_alpha': 0.5, 'reg_lambda': 2.0, 'random_state': 42},
}


def compute_confidence(
        df: pd.DataFrame,
        median_interval_width: float,
        lower_q: str = "q_10",
        upper_q: str = "q_90",
        alpha: float = 1.0,
        beta: float = 1.0,
) -> pd.DataFrame:
    """
    Compute confidence scores (0.0 to 1.0) based on prediction interval width
    and distance from median using exponential decay.

    Args:
        df: DataFrame with 'prediction', 'q_50', and quantile columns
        median_interval_width: Pre-computed median interval width from training data
        lower_q: Lower quantile column name (default: 'q_10')
        upper_q: Upper quantile column name (default: 'q_90')
        alpha: Weight for interval width term (default: 1.0)
        beta: Weight for distance from median term (default: 1.0)

    Returns:
        DataFrame with added 'confidence' column
    """
    # Interval width
    interval_width = (df[upper_q] - df[lower_q]).abs()

    # Distance from median, normalized by interval width
    distance_from_median = (df['prediction'] - df['q_50']).abs()
    normalized_distance = distance_from_median / (interval_width + 1e-6)

    # Cap the distance penalty at 1.0
    normalized_distance = np.minimum(normalized_distance, 1.0)

    # Confidence using exponential decay
    interval_term = interval_width / median_interval_width
    df['confidence'] = np.exp(-(alpha * interval_term + beta * normalized_distance))

    return df


# Function to check if dataframe is empty
def check_dataframe(df: pd.DataFrame, df_name: str) -> None:
    """
    Check if the provided dataframe is empty and raise an exception if it is.

    Args:
        df (pd.DataFrame): DataFrame to check
        df_name (str): Name of the DataFrame
    """
    if df.empty:
        msg = f"*** The training data {df_name} has 0 rows! ***STOPPING***"
        print(msg)
        raise ValueError(msg)


def match_features_case_insensitive(df: pd.DataFrame, model_features: list) -> pd.DataFrame:
    """
    Matches and renames DataFrame columns to match model feature names (case-insensitive).
    Prioritizes exact matches, then case-insensitive matches.

    Raises ValueError if any model features cannot be matched.
    """
    df_columns_lower = {col.lower(): col for col in df.columns}
    rename_dict = {}
    missing = []
    for feature in model_features:
        if feature in df.columns:
            continue  # Exact match
        elif feature.lower() in df_columns_lower:
            rename_dict[df_columns_lower[feature.lower()]] = feature
        else:
            missing.append(feature)

    if missing:
        raise ValueError(f"Features not found: {missing}")

    # Rename the DataFrame columns to match the model features
    return df.rename(columns=rename_dict)


def convert_categorical_types(df: pd.DataFrame, features: list, category_mappings={}) -> tuple:
    """
    Converts appropriate columns to categorical type with consistent mappings.

    Args:
        df (pd.DataFrame): The DataFrame to process.
        features (list): List of feature names to consider for conversion.
        category_mappings (dict, optional): Existing category mappings. If empty dict, we're in
                                            training mode. If populated, we're in inference mode.

    Returns:
        tuple: (processed DataFrame, category mappings dictionary)
    """
    # Training mode
    if category_mappings == {}:
        for col in df.select_dtypes(include=["object", "string"]):
            if col in features and df[col].nunique() < 20:
                print(f"Training mode: Converting {col} to category")
                df[col] = df[col].astype("category")
                category_mappings[col] = df[col].cat.categories.tolist()  # Store category mappings

    # Inference mode
    else:
        for col, categories in category_mappings.items():
            if col in df.columns:
                print(f"Inference mode: Applying categorical mapping for {col}")
                df[col] = pd.Categorical(df[col], categories=categories)  # Apply consistent categorical mapping

    return df, category_mappings


def decompress_features(
        df: pd.DataFrame, features: List[str], compressed_features: List[str]
) -> Tuple[pd.DataFrame, List[str]]:
    """Prepare features for the model by decompressing bitstring features

    Args:
        df (pd.DataFrame): The features DataFrame
        features (List[str]): Full list of feature names
        compressed_features (List[str]): List of feature names to decompress (bitstrings)

    Returns:
        pd.DataFrame: DataFrame with the decompressed features
        List[str]: Updated list of feature names after decompression

    Raises:
        ValueError: If any missing values are found in the specified features
    """

    # Check for any missing values in the required features
    missing_counts = df[features].isna().sum()
    if missing_counts.any():
        missing_features = missing_counts[missing_counts > 0]
        print(
            f"WARNING: Found missing values in features: {missing_features.to_dict()}. "
            "WARNING: You might want to remove/replace all NaN values before processing."
        )

    # Decompress the specified compressed features
    decompressed_features = features.copy()
    for feature in compressed_features:
        if (feature not in df.columns) or (feature not in features):
            print(f"Feature '{feature}' not in the features list, skipping decompression.")
            continue

        # Remove the feature from the list of features to avoid duplication
        decompressed_features.remove(feature)

        # Handle all compressed features as bitstrings
        bit_matrix = np.array([list(bitstring) for bitstring in df[feature]], dtype=np.uint8)
        prefix = feature[:3]

        # Create all new columns at once - avoids fragmentation
        new_col_names = [f"{prefix}_{i}" for i in range(bit_matrix.shape[1])]
        new_df = pd.DataFrame(bit_matrix, columns=new_col_names, index=df.index)

        # Add to features list
        decompressed_features.extend(new_col_names)

        # Drop original column and concatenate new ones
        df = df.drop(columns=[feature])
        df = pd.concat([df, new_df], axis=1)

    return df, decompressed_features


if __name__ == "__main__":
    # Template Parameters
    target = TEMPLATE_PARAMS["target"]
    features = TEMPLATE_PARAMS["features"]
    orig_features = features.copy()
    compressed_features = TEMPLATE_PARAMS["compressed_features"]
    train_all_data = TEMPLATE_PARAMS["train_all_data"]
    hyperparameters = TEMPLATE_PARAMS["hyperparameters"]
    validation_split = 0.2

    # Script arguments for input/output directories
    parser = argparse.ArgumentParser()
    parser.add_argument("--model-dir", type=str, default=os.environ.get("SM_MODEL_DIR", "/opt/ml/model"))
    parser.add_argument("--train", type=str, default=os.environ.get("SM_CHANNEL_TRAIN", "/opt/ml/input/data/train"))
    parser.add_argument(
        "--output-data-dir", type=str, default=os.environ.get("SM_OUTPUT_DATA_DIR", "/opt/ml/output/data")
    )
    args = parser.parse_args()

    # Read the training data into DataFrames
    training_files = [os.path.join(args.train, file) for file in os.listdir(args.train) if file.endswith(".csv")]
    print(f"Training Files: {training_files}")

    # Combine files and read them all into a single pandas dataframe
    all_df = pd.concat([pd.read_csv(file, engine="python") for file in training_files])

    # Check if the dataframe is empty
    check_dataframe(all_df, "training_df")

    # Features/Target output
    print(f"Target: {target}")
    print(f"Features: {str(features)}")

    # Convert any features that might be categorical to 'category' type
    all_df, category_mappings = convert_categorical_types(all_df, features)

    # If we have compressed features, decompress them
    if compressed_features:
        print(f"Decompressing features {compressed_features}...")
        all_df, features = decompress_features(all_df, features, compressed_features)

    # Do we want to train on all the data?
    if train_all_data:
        print("Training on ALL of the data")
        df_train = all_df.copy()
        df_val = all_df.copy()

    # Does the dataframe have a training column?
    elif "training" in all_df.columns:
        print("Found training column, splitting data based on training column")
        df_train = all_df[all_df["training"]]
        df_val = all_df[~all_df["training"]]
    else:
        # Just do a random training Split
        print("WARNING: No training column found, splitting data with random state=42")
        df_train, df_val = train_test_split(all_df, test_size=validation_split, random_state=42)
    print(f"FIT/TRAIN: {df_train.shape}")
    print(f"VALIDATION: {df_val.shape}")

    # Extract sample weights if present
    if 'sample_weight' in df_train.columns:
        sample_weights = df_train['sample_weight']
        print(f"Using sample weights: min={sample_weights.min():.2f}, max={sample_weights.max():.2f}, mean={sample_weights.mean():.2f}")
    else:
        sample_weights = None
        print("No sample weights found, training with equal weights")

    # Prepare features and targets for training
    X_train = df_train[features]
    X_validate = df_val[features]
    y_train = df_train[target]
    y_validate = df_val[target]

    # Train XGBoost for point predictions
    print("\nTraining XGBoost for point predictions...")
    print(f"  Hyperparameters: {hyperparameters}")
    xgb_model = XGBRegressor(enable_categorical=True, **hyperparameters)
    xgb_model.fit(X_train, y_train, sample_weight=sample_weights)

    # Evaluate XGBoost performance
    y_pred_xgb = xgb_model.predict(X_validate)
    xgb_rmse = root_mean_squared_error(y_validate, y_pred_xgb)
    xgb_mae = mean_absolute_error(y_validate, y_pred_xgb)
    xgb_r2 = r2_score(y_validate, y_pred_xgb)

    xgb_medae = median_absolute_error(y_validate, y_pred_xgb)
    xgb_spearman = spearmanr(y_validate, y_pred_xgb).correlation

    print(f"\nXGBoost Point Prediction Performance:")
    print(f"rmse: {xgb_rmse:.3f}")
    print(f"mae: {xgb_mae:.3f}")
    print(f"medae: {xgb_medae:.3f}")
    print(f"r2: {xgb_r2:.3f}")
    print(f"spearmanr: {xgb_spearman:.3f}")

    # Define confidence levels we want to model
    confidence_levels = [0.50, 0.68, 0.80, 0.90, 0.95]  # 50%, 68%, 80%, 90%, 95% confidence intervals

    # Store MAPIE models for each confidence level
    mapie_models = {}

    # Train models for each confidence level
    for confidence_level in confidence_levels:
        alpha = 1 - confidence_level
        lower_q = alpha / 2
        upper_q = 1 - alpha / 2

        print(f"\nTraining quantile models for {confidence_level * 100:.0f}% confidence interval...")
        print(f"  Quantiles: {lower_q:.3f}, {upper_q:.3f}, 0.500")

        # Train three models for this confidence level
        quantile_estimators = []
        for q in [lower_q, upper_q, 0.5]:
            print(f"    Training model for quantile {q:.3f}...")
            est = LGBMRegressor(
                objective="quantile",
                alpha=q,
                n_estimators=1000,
                max_depth=6,
                learning_rate=0.01,
                num_leaves=31,
                min_child_samples=20,
                subsample=0.8,
                colsample_bytree=0.8,
                random_state=42,
                verbose=-1,
                force_col_wise=True,
            )
            est.fit(X_train, y_train)
            quantile_estimators.append(est)

        # Create MAPIE CQR model for this confidence level
        print(f"  Setting up MAPIE CQR for {confidence_level * 100:.0f}% confidence...")
        mapie_model = ConformalizedQuantileRegressor(
            quantile_estimators, confidence_level=confidence_level, prefit=True
        )

        # Conformalize the model
        print(f"  Conformalizing with validation data...")
        mapie_model.conformalize(X_validate, y_validate)

        # Store the model
        mapie_models[f"mapie_{confidence_level:.2f}"] = mapie_model

        # Validate coverage for this confidence level
        y_pred, y_pis = mapie_model.predict_interval(X_validate)
        coverage = np.mean((y_validate >= y_pis[:, 0, 0]) & (y_validate <= y_pis[:, 1, 0]))
        print(f"  Coverage: Target={confidence_level * 100:.0f}%, Empirical={coverage * 100:.1f}%")

    support = len(df_val)
    print(f"\nOverall Model Performance Summary:")
    print(f"rmse: {xgb_rmse:.3f}")
    print(f"mae: {xgb_mae:.3f}")
    print(f"medae: {xgb_medae:.3f}")
    print(f"r2: {xgb_r2:.3f}")
    print(f"spearmanr: {xgb_spearman:.3f}")
    print(f"support: {support}")

    # Analyze interval widths across confidence levels
    print(f"\nInterval Width Analysis:")
    for conf_level in confidence_levels:
        model = mapie_models[f"mapie_{conf_level:.2f}"]
        _, y_pis = model.predict_interval(X_validate)
        widths = y_pis[:, 1, 0] - y_pis[:, 0, 0]
        print(f"  {conf_level * 100:.0f}% CI: Mean width={np.mean(widths):.3f}, Std={np.std(widths):.3f}")

    # Compute normalization statistics for confidence calculation
    print(f"\nComputing normalization statistics for confidence scores...")

    # Add predictions directly to validation dataframe
    df_val["prediction"] = xgb_model.predict(X_validate)

    # Add all quantile predictions
    for conf_level in confidence_levels:
        model_name = f"mapie_{conf_level:.2f}"
        model = mapie_models[model_name]
        y_pred, y_pis = model.predict_interval(X_validate)

        if conf_level == 0.50:
            df_val["q_25"] = y_pis[:, 0, 0]
            df_val["q_75"] = y_pis[:, 1, 0]
            # y_pred is the median prediction
            df_val["q_50"] = y_pred
        elif conf_level == 0.68:
            df_val["q_16"] = y_pis[:, 0, 0]
            df_val["q_84"] = y_pis[:, 1, 0]
        elif conf_level == 0.80:
            df_val["q_10"] = y_pis[:, 0, 0]
            df_val["q_90"] = y_pis[:, 1, 0]
        elif conf_level == 0.90:
            df_val["q_05"] = y_pis[:, 0, 0]
            df_val["q_95"] = y_pis[:, 1, 0]
        elif conf_level == 0.95:
            df_val["q_025"] = y_pis[:, 0, 0]
            df_val["q_975"] = y_pis[:, 1, 0]

    # Compute normalization stats using q_10 and q_90 (default range)
    interval_width = (df_val["q_90"] - df_val["q_10"]).abs()
    median_interval_width = float(interval_width.median())
    print(f"  Median interval width (q_10-q_90): {median_interval_width:.6f}")

    # Save median interval width for confidence calculation
    with open(os.path.join(args.model_dir, "median_interval_width.json"), "w") as fp:
        json.dump(median_interval_width, fp)

    # Save the trained XGBoost model
    joblib.dump(xgb_model, os.path.join(args.model_dir, "xgb_model.joblib"))

    # Save all MAPIE models
    for model_name, model in mapie_models.items():
        joblib.dump(model, os.path.join(args.model_dir, f"{model_name}.joblib"))

    # Save the feature list
    with open(os.path.join(args.model_dir, "feature_columns.json"), "w") as fp:
        json.dump(features, fp)

    # Save category mappings if any
    if category_mappings:
        with open(os.path.join(args.model_dir, "category_mappings.json"), "w") as fp:
            json.dump(category_mappings, fp)

    # Save model configuration
    model_config = {
        "model_type": "XGBoost_MAPIE_CQR_LightGBM",
        "confidence_levels": confidence_levels,
        "n_features": len(features),
        "target": target,
        "validation_metrics": {
            "xgb_rmse": float(xgb_rmse),
            "xgb_mae": float(xgb_mae),
            "xgb_r2": float(xgb_r2),
            "n_validation": len(df_val),
        },
    }
    with open(os.path.join(args.model_dir, "model_config.json"), "w") as fp:
        json.dump(model_config, fp, indent=2)

    print(f"\nModel training complete!")
    print(f"Saved 1 XGBoost model and {len(mapie_models)} MAPIE models to {args.model_dir}")


#
# Inference Section
#
def model_fn(model_dir) -> dict:
    """Load XGBoost and all MAPIE models from the specified directory."""

    # Load model configuration to know which models to load
    with open(os.path.join(model_dir, "model_config.json")) as fp:
        config = json.load(fp)

    # Load XGBoost regressor
    xgb_path = os.path.join(model_dir, "xgb_model.joblib")
    xgb_model = joblib.load(xgb_path)

    # Load all MAPIE models
    mapie_models = {}
    for conf_level in config["confidence_levels"]:
        model_name = f"mapie_{conf_level:.2f}"
        mapie_models[model_name] = joblib.load(os.path.join(model_dir, f"{model_name}.joblib"))

    # Load category mappings if they exist
    category_mappings = {}
    category_path = os.path.join(model_dir, "category_mappings.json")
    if os.path.exists(category_path):
        with open(category_path) as fp:
            category_mappings = json.load(fp)

    # Load median interval width for confidence calculation
    median_interval_width = None
    median_width_path = os.path.join(model_dir, "median_interval_width.json")
    if os.path.exists(median_width_path):
        with open(median_width_path) as fp:
            median_interval_width = json.load(fp)

    return {
        "xgb_model": xgb_model,
        "mapie_models": mapie_models,
        "confidence_levels": config["confidence_levels"],
        "category_mappings": category_mappings,
        "median_interval_width": median_interval_width,
    }


def input_fn(input_data, content_type):
    """Parse input data and return a DataFrame."""
    if not input_data:
        raise ValueError("Empty input data is not supported!")

    # Decode bytes to string if necessary
    if isinstance(input_data, bytes):
        input_data = input_data.decode("utf-8")

    if "text/csv" in content_type:
        return pd.read_csv(StringIO(input_data))
    elif "application/json" in content_type:
        return pd.DataFrame(json.loads(input_data))
    else:
        raise ValueError(f"{content_type} not supported!")


def output_fn(output_df, accept_type):
    """Supports both CSV and JSON output formats."""
    if "text/csv" in accept_type:
        # Convert categorical columns to string to avoid fillna issues
        for col in output_df.select_dtypes(include=["category"]).columns:
            output_df[col] = output_df[col].astype(str)
        csv_output = output_df.fillna("N/A").to_csv(index=False)
        return csv_output, "text/csv"
    elif "application/json" in accept_type:
        return output_df.to_json(orient="records"), "application/json"
    else:
        raise RuntimeError(f"{accept_type} accept type is not supported by this script.")


def predict_fn(df, models) -> pd.DataFrame:
    """Make predictions using XGBoost for point estimates and MAPIE for conformalized intervals

    Args:
        df (pd.DataFrame): The input DataFrame
        models (dict): Dictionary containing XGBoost and MAPIE models

    Returns:
        pd.DataFrame: DataFrame with XGBoost predictions and conformalized intervals
    """

    # Flag for outlier stretch adjustment for the prediction intervals
    # if the predicted values are outside the intervals
    outlier_stretch = False

    # Grab our feature columns (from training)
    model_dir = os.environ.get("SM_MODEL_DIR", "/opt/ml/model")
    with open(os.path.join(model_dir, "feature_columns.json")) as fp:
        model_features = json.load(fp)

    # Match features in a case-insensitive manner
    matched_df = match_features_case_insensitive(df, model_features)

    # Apply categorical mappings if they exist
    if models.get("category_mappings"):
        matched_df, _ = convert_categorical_types(matched_df, model_features, models["category_mappings"])

    # Get features for prediction
    X = matched_df[model_features]

    # Get XGBoost point predictions
    df["prediction"] = models["xgb_model"].predict(X)

    # Get predictions from each MAPIE model for conformalized intervals
    for conf_level in models["confidence_levels"]:
        model_name = f"mapie_{conf_level:.2f}"
        model = models["mapie_models"][model_name]

        # Get conformalized predictions
        y_pred, y_pis = model.predict_interval(X)

        # Map confidence levels to quantile names
        if conf_level == 0.50:  # 50% CI
            df["q_25"] = y_pis[:, 0, 0]
            df["q_75"] = y_pis[:, 1, 0]
            # y_pred is the median prediction
            df["q_50"] = y_pred
        elif conf_level == 0.68:  # 68% CI
            df["q_16"] = y_pis[:, 0, 0]
            df["q_84"] = y_pis[:, 1, 0]
        elif conf_level == 0.80:  # 80% CI
            df["q_10"] = y_pis[:, 0, 0]
            df["q_90"] = y_pis[:, 1, 0]
        elif conf_level == 0.90:  # 90% CI
            df["q_05"] = y_pis[:, 0, 0]
            df["q_95"] = y_pis[:, 1, 0]
        elif conf_level == 0.95:  # 95% CI
            df["q_025"] = y_pis[:, 0, 0]
            df["q_975"] = y_pis[:, 1, 0]

    # Calculate a pseudo-standard deviation from the 68% interval width
    df["prediction_std"] = (df["q_84"] - df["q_16"]).abs() / 2.0

    # Reorder the quantile columns for easier reading
    quantile_cols = ["q_025", "q_05", "q_10", "q_16", "q_25", "q_50", "q_75", "q_84", "q_90", "q_95", "q_975"]
    other_cols = [col for col in df.columns if col not in quantile_cols]
    df = df[other_cols + quantile_cols]

    # Adjust the outer quantiles to ensure they encompass the prediction
    if outlier_stretch:
        # Lower intervals adjustments
        df["q_025"] = np.minimum(df["q_025"], df["prediction"])
        df["q_05"] = np.minimum(df["q_05"], df["prediction"])
        df["q_10"] = np.minimum(df["q_10"], df["prediction"])
        df["q_16"] = np.minimum(df["q_16"], df["prediction"])
        df["q_25"] = np.minimum(df["q_25"], df["prediction"])

        # Upper intervals adjustments
        df["q_75"] = np.maximum(df["q_75"], df["prediction"])
        df["q_84"] = np.maximum(df["q_84"], df["prediction"])
        df["q_90"] = np.maximum(df["q_90"], df["prediction"])
        df["q_95"] = np.maximum(df["q_95"], df["prediction"])
        df["q_975"] = np.maximum(df["q_975"], df["prediction"])

    # Compute confidence scores using pre-computed normalization stats
    df = compute_confidence(
        df,
        lower_q="q_10",
        upper_q="q_90",
        alpha=1.0,
        beta=1.0,
        median_interval_width=models["median_interval_width"],
    )

    return df
