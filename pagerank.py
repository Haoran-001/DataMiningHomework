import pandas as pd
import numpy as np
import json

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('max_colwidth',100)

class PageRank():
    # d represents damping coefficient
    def __init__(self, filepath: str = None, iterater_times: int = 10, d: int = 0.85):
        self.filepath = filepath
        self.iter_times = iterater_times
        self.damping = d


    def read_data(self) -> pd.DataFrame:
        # data_list storages every line's data
        # data_set storages all no-repeating websites
        data_list = []
        data_set = set()
        count = 1
        with open(self.filepath, 'r') as f:
            while True:
                line = f.readline()[:-1]
                if count == 1:
                    count += 1
                    continue
                if line == '':
                    break
                data_list.append(line)
                data_set.add(line.split(" ")[0])
                data_set.add(line.split(" ")[1])
        df = pd.DataFrame(columns = data_set, index = data_set)
        for data in data_list:
            item = data.split(" ")
            df[item[0]][item[1]] = 1.0
        df.fillna(value = 0.0, inplace = True)
        df.to_excel('df.xls')

        return df

    def get_ajacent_and_weight_matrix(self, dataframe: pd.DataFrame):
        adjacent_matrix = dataframe.values
        weight_matrix = dataframe.values.copy()
        length = weight_matrix.shape[0]
        for i in range(length):
            col_sum = np.sum(weight_matrix[:, i])
            # keep two decimal
            weight_matrix[:, i] = np.round(weight_matrix[:, i] / col_sum, 2)

        return adjacent_matrix, weight_matrix

    def iterate_one_time_result(self, weight_matrix: np.ndarray, pr_values: np.ndarray, length: int)->np.ndarray:
        pr_values = weight_matrix.dot(pr_values) * self.damping + (1.0 - self.damping) / length

        return pr_values

    def get_result(self):
        df = self.read_data()
        adjacent_matrix, weight_matrix = self.get_ajacent_and_weight_matrix(df)
        print(adjacent_matrix, weight_matrix)
        length = weight_matrix.shape[0]
        pr_values = np.ones(length)
        for i in range(length):
            pr_values = self.iterate_one_time_result(weight_matrix, pr_values, length)

        return df.columns, pr_values

if __name__ == '__main__':
    filepath = r'pagerank_data.txt'
    pagerank = PageRank(filepath = filepath, iterater_times = 100, d = 0.85)
    result = pagerank.get_result()

    # result_dict storages website and pr_value as key-value pair
    result_dict = {}
    websites = result[0]
    pr_values = result[1]
    for i in range(len(websites)):
        result_dict[websites[i]] = pr_values[i]
    print(result_dict)

    # return the largest K nodes, assume K = 5
    result_order_list = sorted(result_dict.items(), key = lambda x : x[1], reverse = True)
    k = 5
    result_k_dict = dict(result_order_list[0:k])
    print(result_k_dict)

    with open('result_K.txt', 'w') as f:
        f.write(json.dumps(result_k_dict))







