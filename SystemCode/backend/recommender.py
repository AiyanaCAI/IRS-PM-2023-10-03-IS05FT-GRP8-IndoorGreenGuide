import json
from nltk.corpus import stopwords
from nltk.corpus import wordnet
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import warnings
from sklearn.metrics.pairwise import cosine_similarity

warnings.filterwarnings('ignore')
# %matplotlib inline

def get_recommendations(keywords):
    print("-----------------This is backend.recommender------------------")
    project_path = 'C:/Users/CZX/Desktop/project/5001project/GRP8/MVP/frontend'

    data_general = pd.read_excel(project_path + '/data/general.csv')
    data_fertilizer = pd.read_excel(project_path + '/data/fertilizer.csv')
    data_light = pd.read_csv(project_path + '/data/light.csv')
    data_measurement = pd.read_excel(project_path + '/data/measurement.csv')
    data_water = pd.read_csv(project_path + '/data/water.csv')
    # data_fertilizer.head()

    # keywords=['shade','Need careful care','Medium','Succulent']

    light_pref = ''
    height_pref = ''
    care_pref = ''
    for keyword in keywords:
        if keyword in ['indirect', 'direct', 'shade']:
            light_pref = keyword
        elif keyword in ['Easy to care','Need careful care']:
            care_pref = keyword
        elif keyword in ['Small','Medium','Large']:
            height_pref = keyword

    # Match user's light, care, height input with the plant dataset
    light_match = data_light[data_light['light'].str.contains(light_pref, case=False)]
    matching_index1 = light_match.index

    if height_pref == 'Small':
        height_match = data_measurement[((data_measurement['Height1'].astype(float).le(35) |
                                        data_measurement['Height2'].astype(float).le(35) |
                                        data_measurement['Height3'].astype(float).le(35) |
                                        data_measurement['Height1'].isna() |
                                        data_measurement['Height2'].isna() |
                                        data_measurement['Height3'].isna()))]
    elif height_pref == 'Medium': # 
        height_match = data_measurement[(
            (
                (data_measurement['Height1'].astype(float).gt(35) & data_measurement['Height1'].astype(float).le(80)) |
                (data_measurement['Height2'].astype(float).gt(35) & data_measurement['Height2'].astype(float).le(80)) |
                (data_measurement['Height3'].astype(float).gt(35) & data_measurement['Height3'].astype(float).le(80))
            ) |
            (data_measurement['Height1'].isna() | data_measurement['Height2'].isna() | data_measurement['Height3'].isna())
        )]
    else:
        height_match = data_measurement[((data_measurement['Height1'].astype(float).gt(80) |
                                        data_measurement['Height2'].astype(float).gt(80) |
                                        data_measurement['Height3'].astype(float).gt(80) |
                                        data_measurement['Height1'].isna() |
                                        data_measurement['Height2'].isna() |
                                        data_measurement['Height3'].isna()))]
    matching_index2 = height_match.index

    care_match1 = data_water[data_water['change'].str.contains('occasionally', case=False)]
    care_match2 = data_fertilizer[data_fertilizer['FERTILIZER'].str.contains('easy', case=False)]
    matching_index3_1 = care_match1.index
    matching_index3_2 = care_match2.index
    matching_index3 = set(matching_index3_1).intersection(matching_index3_2)

    if care_pref == 'Need careful care':
        all_indices = set(range(len(data_measurement)))
        matching_index3 = all_indices.difference(matching_index3)
        

    matching_index = set(matching_index1).intersection(matching_index2).intersection(matching_index3)
    print("--------------matching_index----------------")
    print(matching_index)

    matching_index = list(matching_index) # Converts the matching index from a collection to a list
    final_data = data_general.loc[matching_index]
    keywords = [keyword for keyword in keywords if keyword not in [light_pref, height_pref, care_pref]]

    merged_data = final_data.iloc[:,2:]
    merged_data = merged_data.apply(lambda x: ','.join(x.dropna().astype(str)), axis=1)

    vectorizer = TfidfVectorizer()
    fertilizer_vectorized = vectorizer.fit_transform(merged_data)

    keyword_string = " ".join(keywords)
    keyword_vectorized = vectorizer.transform([keyword_string])

    cos_sim = cosine_similarity(keyword_vectorized, fertilizer_vectorized)

    n = 6  # remark first n similar
    top_n_indices = np.argsort(cos_sim, axis=1)[:, -n:][0][::-1]

##
    # Gets the index of these indexes in the original merged data
    original_indices = merged_data.index[top_n_indices]
    print("--------------------------------original_indices--------------------------------")
    print(original_indices)

    # Get the top n most similar remarks and similarity scores
    top_n_notes = merged_data.iloc[top_n_indices]
    top_n_similarity_scores = cos_sim[0, top_n_indices]

    Recommendations = []
    for i in range(0, n) :
        #original_indices[i]
        plant = {
            "Name:": data_general.loc[original_indices[i] , 'name'],
            "Picture:": data_general.loc[original_indices[i] , 'picture'], 
            "url:": data_general.loc[original_indices[i] , 'url'], 
            "Description:": data_general.loc[original_indices[i] , 'GENERAL INFORMATION'],
            "CosineScore": top_n_similarity_scores[i]
        }
        print(f"Plant {i + 1} Name: {plant['Name:']}")
        Recommendations.append(plant)

    print(json.dumps({'Recommendations': Recommendations}))
    return Recommendations


if __name__ == "__main__":
    print("Script is running.")
    keywords = ['indirect', 'Need careful care', 'Medium']
    get_recommendations(keywords)
    print("Script has finished running.")


