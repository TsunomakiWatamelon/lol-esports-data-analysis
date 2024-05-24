import pandas as pd
from sklearn.preprocessing import StandardScaler
import numpy as np

def create_kpi_split_df(df):
    agreession_time_link = ['Kills', 'Deaths', 'Assists', 'KDA', 'Physical Damage', 'Magic Damage', 'True Damage', 'Total damage to Champion', 'Total damage taken', 'Total heal', 'Time ccing others', 'Damage dealt to turrets']
    agression_df = df[['Kills', 'Deaths', 'Assists', 'KDA', 'Solo kills', 'Double kills', 'Triple kills', 'Quadra kills', 'Penta kills', 'KP%', 'Physical Damage', 'Magic Damage', 'True Damage', 'DPM', 'DMG%', 'Total damage to Champion', 'Total damage taken', 'Total heal', 'Time ccing others', 'Damage dealt to turrets']].copy()
    agression_df[agreession_time_link] = agression_df[agreession_time_link].div(df['Game Duration'], axis=0)

    setup_time_link = ['Vision Score', 'Wards placed', 'Wards destroyed', 'Control Wards Purchased', 'Assists']
    setup_df = df[['Time ccing others', 'Assists', 'Vision Score', 'Wards placed', 'Wards destroyed', 'Control Wards Purchased', 'VSPM', 'WPM', 'VWPM', 'WCPM', 'VS%']].copy()
    setup_df[setup_time_link] = setup_df[setup_time_link].div(df['Game Duration'], axis=0)

    economy_time_link = ['CS', "CS in Team's Jungle", 'Golds']
    economy_df = df[['CS', "CS in Team's Jungle", 'Golds']].copy()
    economy_df[economy_time_link] = economy_df[economy_time_link].div(df['Game Duration'], axis=0)

    early_game_df = df[['GD@15', 'CSD@15', 'XPD@15', 'LVLD@15']]
    return agression_df, setup_df, economy_df, early_game_df

def scale_df(df, scaler=None):
    if scaler is None:
        scaler = StandardScaler()
    return pd.DataFrame(scaler.fit_transform(df), columns=df.columns)

def get_weighted_score(vector, weights, scaler, min_vector, max_vector):
    # check if scaler is fitted
    if scaler.mean_ is None or scaler.var_ is None:
        raise ValueError('Scaler is not fitted')

    scaled = scaler.transform(vector)
    scaled = np.array(scaled)
    min_scaled = scaler.transform(min_vector.reshape(1, -1))
    max_scaled = scaler.transform(max_vector.reshape(1, -1))
    min_score = np.dot(min_scaled, weights)
    max_score = np.dot(max_scaled, weights)
    score = np.dot(scaled, weights)
    if score == min_score:
        return 0
    if score == max_score:
        return 1
    
    score = (score - min_score) / (max_score - min_score)
    return score[0] # return the score as a scalar
