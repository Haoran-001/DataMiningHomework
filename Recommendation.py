import pandas as pd
import numpy as np

class JaccardRecommendation():
    def __init__(self, df :pd.DataFrame = None):
        self.df = df

    def get_jaccard_similarity_matrix(self) -> np.ndarray:
        user_list = df.index
        data = self.df.values
        shape = df.values.shape
        jaccard_sim_matrix = np.zeros(shape)
        length = len(user_list)

        for i in range(length):
            for j in range(i, length):
                one_jaccard_ans = self.get_inter_div_union(data[i], data[j])
                jaccard_sim_matrix[i][j] = one_jaccard_ans
                jaccard_sim_matrix[j][i] = one_jaccard_ans

        return jaccard_sim_matrix


    def get_inter_div_union(self, vector1: np.ndarray, vector2: np.ndarray):
        same = 0
        diff = 0

        length = vector1.shape[0]
        for i in range(length):
            if vector1[i] != 0 or vector2[i] != 0:
                if vector1[i] & vector2[i]:
                    same += 1
                diff += 1

        ans = round(same / diff, 3)
        return ans

    def get_result(self) -> dict:
        '''
        Recommend the fruit belonging to the three most relevant users but current user doesn't buy.
        Returns: a dict, the key is a user, and the value is a list containing some fruit.
        '''
        jaccard_sim_matrix = self.get_jaccard_similarity_matrix()
        df = pd.DataFrame(data = jaccard_sim_matrix, index = self.df.index, columns = self.df.index)
        user_list = df.index
        relevant_users_dict = {}
        recommend_result = {}

        for user in user_list:
            # df2 doesn't contain jaccard value of itself for every user
            df2 = df.loc[user].drop(user)
            # desceding sort
            df2_sorted = df2.sort_values(ascending = False)
            relevant_users_dict[user] = df2_sorted.index[0:3]

        for user, relevant_users in relevant_users_dict.items():
            fruit_recommend_set = set()
            for relevant_user in relevant_users:
                fruit_recommend_set = fruit_recommend_set.union(self.df.loc[relevant_user].replace(0, np.NaN).dropna().index)
            # filter the fruit user have already bought
            user_bought_fruit = self.df.loc[user].replace(0, np.NaN).dropna().index
            fruit_recommend_set -= set(user_bought_fruit)
            recommend_result[user] = fruit_recommend_set

        return recommend_result

if __name__ == '__main__':
    df = pd.read_excel(r'data.xls', header = 0, index_col = 0)
    jaccard_recommendation = JaccardRecommendation(df)
    result = jaccard_recommendation.get_result()

    for user in result:
        print('向{0}推荐{1}' .format(user, result[user]))