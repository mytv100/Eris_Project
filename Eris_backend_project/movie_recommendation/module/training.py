from collections import defaultdict
import os
from surprise import SVD
from surprise import Dataset
from surprise import dump
from surprise import accuracy
from surprise import GridSearch
from surprise.model_selection import train_test_split,cross_validate
import surprise
def get_top_n(predictions, n=10):
    '''Return the top-N recommendation for each user from a set of predictions.

    Args:
        predictions(list of Prediction objects): The list of predictions, as
            returned by the test method of an algorithm.
        n(int): The number of recommendation to output for each user. Default
            is 10.

    Returns:
    A dict where keys are user (raw) ids and values are lists of tuples:
        [(raw item id, rating estimation), ...] of size n.
    '''

    # First map the predictions to each user.
    top_n = defaultdict(list)
    for uid, iid, true_r, est, _ in predictions:
        top_n[uid].append((iid, est))

    # Then sort the predictions for each user and retrieve the k highest ones.
    for uid, user_ratings in top_n.items():
        user_ratings.sort(key=lambda x: x[1], reverse=True)
        top_n[uid] = user_ratings[:n]

    return top_n

def find_model():

    """

    data = surprise.Dataset.load_builtin('ml-100k')

    bsl_options = {
        'method': 'als',
        'n_epochs': 5,
        'reg_u': 12,
        'reg_i': 5
    }

    algo = surprise.BaselineOnly(bsl_options)

    np.random.seed(0)
    acc = np.zeros(3)
    cv = KFold(3)
    for i, (trainset, testset) in enumerate(cv.split(data)):
        algo.fit(trainset)
        predictions = algo.test(testset)
        acc[i] = surprise.accuracy.rmse(predictions, verbose=True)
    print(acc.mean())
    """

    """
        추천 시스템 알고리즘
            1. 베이스라인 모형 - 사용자와 상품 특성에 의한 평균 평점의 합
            2. Collaborative Filtering 
                - 모든 사용자의 데이터를 균일하게 사용 X, 평점 행렬이 가진 특정한 패턴을 이용 -> 평점 예측
                2-1. Neighborhood Models - 사용자나 상품 기준으로 평점의 유사성
                    User-based CF - 해당 사용자와 유사한 사용자를 찾는 방법
                    Item-based CF - 특정한 상품에 대해 사용자가 준 점수
                2-2. Latent Factor Models - 행렬의 수치적 특징
                    Matrix Factorization
                    SVD
            3. Content-Based Recommendation
    """
    data = surprise.Dataset.load_builtin('ml-100k')

    """
        위 코드 축약형

        Baseline 모델
    """
    bsl_options = {
        'method': 'als',
        'n_epochs': 5,
        'reg_u': 12,
        'reg_i': 5
    }
    algo = surprise.BaselineOnly(bsl_options)
    print('BaselineOnly : ',cross_validate(algo, data))

    """
        추천성능 평가기준
    """
    # 평균 제곱 차이 유사도 Mean Squared Difference, MSD - 유클리드 공간에서의 거리 제곱에 비례하는 값
    sim_options = {'name': 'msd'}
    algo = surprise.KNNBasic(sim_options=sim_options)
    print('msd : ',cross_validate(algo, data)["test_mae"].mean())

    # 코사인 유사도 Cosine Similarity - 두 특성 벡터의 각도에 대한 코사인 값
    sim_options = {'name': 'cosine'}
    algo = surprise.KNNBasic(sim_options=sim_options)
    print('cosine : ',  cross_validate(algo, data)["test_mae"].mean())

    # 피어슨 유사도 Pearson Similarity - 두 벡터의 상관계수(Pearson correlation coefficient)
    sim_options = {'name': 'pearson'}
    algo = surprise.KNNBasic(sim_options=sim_options)
    print('pearson : ',  cross_validate(algo, data)["test_mae"].mean())


    # 피어슨-베이스라인 유사도 Pearson-Baseline Similarity
    # - 상관계수 + 각 벡터의 기댓값을 단순 평균이 아니라 베이스라인 모형에서 예측한 값
    sim_options = {'name': 'pearson_baseline'}
    algo = surprise.KNNBasic(sim_options=sim_options)
    print('pearson_baseline : ', cross_validate(algo, data)["test_mae"].mean())

    """
        유사도가 구해지면, KNN 기반 가중치 예측 알고리즘 
        1. KNNBasic
        2. KNNWithMeans
        3. KNNBaseline
    """

    sim_options = {'name': 'pearson_baseline'}
    algo = surprise.KNNWithMeans(sim_options=sim_options)
    print('KNNWithMeans_pearson_baseline : ', cross_validate(algo, data)["test_mae"].mean())

    sim_options = {'name': 'pearson_baseline'}
    algo = surprise.KNNBaseline(sim_options=sim_options)
    print('KNNBaseline_pearson_baseline : ',cross_validate(algo, data)["test_mae"].mean())


    # SVD (Singular Value Decomposition)
    algo = surprise.SVD(n_factors=100)
    print('SVD : ',cross_validate(algo, data)["test_mae"].mean())

    # NMF(Non-negative matrix factorization)
    algo = surprise.NMF(n_factors=100)
    print('NMF : ',cross_validate(algo, data)["test_mae"].mean())


def training():
    # First train an SVD algorithm on the movielens dataset.
    data = Dataset.load_builtin('ml-100k')
    trainset, testset = train_test_split(data,test_size=0.20)

    algo = SVD()
    algo.train(trainset)

    # Than predict ratings for all pairs (u, i) that are NOT in the training set.
    predictions = algo.test(testset)
    print(accuracy.rmse(predictions))

    file_name = os.path.expanduser('dump_file')
    dump.dump(file_name, algo=algo)
    _, loaded_algo = dump.load(file_name)


def find_parameter():
    data = Dataset.load_builtin('ml-100k')
    data.split(n_folds=3)
    for i in range(1,11):
        param_grid={'n_epochs':[i+4,],'lr_all':[i*0.001,]}
        #param_grid={'n_epochs':[5,10],'lr_all':[0.002,0.005]}
        grid_search = GridSearch(SVD, param_grid, measures=['RMSE'], verbose=1)
        print(grid_search.best_params)
        print(grid_search.evaluate(data))

"""
    # 저장했던 모델이 일치하는지 확인
    # predictions_loaded_algo = loaded_algo.test(trainset.build_testset())
    predictions_loaded_algo = loaded_algo.test(testset)
    assert predictions == predictions_loaded_algo
    print('Predictions are the same')
"""

if __name__ == '__main__':
    find_model()        # SVD
    find_parameter()    # 13 0.009
    training()

    """
    top_n = get_top_n(predictions, n=10)

    # 학습된 모델 저장 및 불러오기
    file_name = os.path.expanduser('dump_file')
    dump.dump(file_name, algo=algo)
    _, loaded_algo = dump.load(file_name)

    # 저장했던 모델이 일치하는지 확인
    predictions_loaded_algo = loaded_algo.test(trainset.build_testset())
    assert predictions == predictions_loaded_algo
    print('Predictions are the same')

    # 정확도 계산
    accuracy.rmse(predictions)
    # Print the recommended items for each user

    for uid, user_ratings in top_n.items():
        print(uid, [iid for (iid, _) in user_ratings])

    return user_ratings
"""