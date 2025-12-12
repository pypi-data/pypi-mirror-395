# coding:utf-8
"""
评价函数
"""
import numpy as np
import pandas as pd


def rmse(real, pred, cap=49500):
    s = 1 - np.sqrt(np.mean((real - pred) ** 2))/cap
    return s*100


def rmse1(real, pred, cap=49500):
    s = np.sqrt(np.mean((real - pred) ** 2))
    return s


def harmonic(real, pred, cap=49500):
    arr = abs(real / (real+pred) - 0.5) * \
        abs(real - pred) / (sum(abs(real - pred)))
    e = 1.0 - 2.0 * arr.sum()
    return e*100


def Racc_AH(real, pred, cap=None):
    """
    适用安徽R_acc准确率
    """
    deviation = []
    cal_point = len(real)
    if len(real[real == 0]) == cal_point:
        acc_val = 0
        score_point = cal_point
    elif len(real[(real > 0) & (real <= 10000)]) == cal_point:
        acc_val = 0.8
        score_point = cal_point
    else:
        score_point = 0
        for i in range(len(pred)):
            if real[i] > 10000:  # 仅大于上限的实测点才参与考核
                score_point = score_point + 1
                d = ((real[i] - pred[i]) / real[i])**2
                deviation.append(d)
        if len(deviation) != 0:
            acc_val = 1 - np.sqrt(np.nanmean(deviation))
        else:
            acc_val = 1

    return acc_val * 100


def Racc_ZJ(real, pred, cap=None):
    # 浙江R_acc准确率
    deviation = []
    for i in range(len(real)):
        if real[i] <= 0:
            if pred[i] == 0:
                deviation.append(0)
            else:
                deviation.append(1)
        else:
            d = ((pred[i] - real[i]) / real[i])**2
            if d > 1:
                d = 1
            deviation.append(d)
    acc_val = 1 - np.sqrt(np.nanmean(deviation))

    return acc_val * 100


def ACC(real, pred, cap=None):
    """ACC准确率，适用于华北区域：冀南、冀北、北京、天津"""
    diff_sum = np.sum(np.abs(real - pred))
    up = (real - pred) * (real - pred) * np.abs(real - pred) / diff_sum
    acc_val = 1 - np.sqrt(np.sum(up)) / cap

    return acc_val * 100


def AD_acc(real, pred, cap=None):
    '''
    AD_acc准确率
    适用四川电网,江西电网,河南电网,湖北电网,湖南电网,重庆电网光伏
    '''
    acc_val = 1 - np.nanmean(np.abs(real - pred)) / cap

    return acc_val * 100


def A_corr(real, pred, cap=None):
    '''
    A_corr_rate相关性系数，目前仅四川考核
    '''
    p_a = np.nanmean(real)
    pr_a = np.nanmean(pred)
    acc_val = np.sum(
        (real - p_a) * (pred - pr_a)) / np.sqrt(
            np.sum((real - p_a)**2) * np.sum((pred - pr_a)**2))
    return acc_val * 100


def MSP_JS(real, pred, cap=None):
    '''
        MSP_jiangsu_rate江苏单点合格率的达标率，即合格率大于等于90%的点占总点的比值
    '''
    score_point = 0
    cal_point = len(real)
    for i in range(cal_point):
        acc_val = 1 - np.abs(float(pred[i]) - float(real[i])) / cap
        if acc_val < 0.9:
            score_point = score_point + 1
    acc_val = 1 - float(score_point) / (float(cal_point + 10e-8))

    return acc_val * 100


def MSP_FJ(real, pred, cap=None):
    '''
        MSP_jiangsu_rate福建单点合格率的达标率，即合格率大于等于75%的点占总点的比值
    '''
    score_point = 0
    cal_point = len(real)
    for i in range(len(real)):
        acc_val = 1 - np.abs(float(pred[i]) - float(real[i])) / cap
        if acc_val < 0.75:
            score_point = score_point + 1
    acc_val = 1 - float(score_point) / (float(cal_point + 10e-8))

    return acc_val * 100


def SPD(real, pred, cap=None):
    '''
        single_diff_Wscore,适用西北风电短期单点绝对偏差SPD考核分的考核，
        得到的是单位容量考核分
    '''
    score_val = 0
    for i in range(len(real)):
        # 先计算单点绝对偏差SPD值
        if (((pred[i] == 0) and (real[i] < 0.03 * cap))
                or ((real[i] == 0) and (pred[i] < 0.03 * cap))):
            # 预测为0，实测在3%cap以内或实测为0预测在3%cap以内时，免考核
            acc_val = 0
        elif (((pred[i] == 0) and (real[i] >= 0.03 * cap))
                or ((real[i] == 0) and (pred[i] >= 0.03 * cap))):
            # 预测为0，实测超出3%cap以外或实测为0预测超出3%cap以外时，全考核
            acc_val = 1
        else:
            acc_val = np.abs((real[i] - pred[i]) / pred[i])
        # 再计算考核分， score_val_temp为单点考核分
        if acc_val > 0.25:
            score_val_temp = (np.abs(pred[i] - real[i]) -
                              0.25 * pred[i]) / 4 * 0.2 / 10000
        else:
            score_val_temp = 0
        score_val = score_val + score_val_temp
    return -float(score_val) / cap * 100 * 1000


# def rmse(y_true, y_pred, cap=49500):
#     s = 1 - np.sqrt(np.mean((y_true - y_pred) ** 2))/cap
#     return s*100


def cal_rmse(real, pred, cap=49500):
    s = np.sqrt(np.mean((real - pred) ** 2))
    return s


def matrix_rmse(real, pred):
    s = np.sqrt(np.mean((real - np.array(pred).reshape(-1, 1)) ** 2, axis=0))
    return s


def corr(real, pred):
    from scipy.stats import pearsonr
    return pearsonr(real, pred)[0]


# def harmonic(real, pred, cap=49500):
#     arr = abs(real / (real+pred) - 0.5) * \
#         abs(real - pred) / (sum(abs(real - pred)))
#     e = 1.0 - 2.0 * arr.sum()
#     return e*100


def normalize(values, min, max):
    qxvalues = (values-min)/(max-min)
    return qxvalues


def rev_normalize(norm_real, max, min):
    revalue = norm_real * (max - min) + min
    return revalue


def eva_daily_score(self, func, df, cap):

    if hasattr(self, 'ranking_accord'):
        ranking_accord = self.ranking_accord
        wfid = self.farm_config['wfid']
    else:
        ranking_accord = self.method_config['ranking_accord']
        wfid = self.method_config['wfid']

    start_dt, end_dt = df.index[0], df.index[-1]
    if ranking_accord == 'AccumulatedEnergy':
        obs_source = 'oms'
        obs_data = self.get_obs_data(wfid=wfid,
                                     start_dt=start_dt, end_dt=end_dt,
                                     obs_source=obs_source)
        obs_data = obs_data.rename(columns={'rectime': 'ptime'})
        df['ptime'] = df.index
        df = pd.merge(df, obs_data, how='inner', on='ptime')
        df.index = df.ptime
        del df['ptime']

        data = []
        for day, gdf in df.groupby(by=lambda x: x.strftime('%Y-%m-%d')):
            if gdf.shape[0] < 10:
                continue
            if self.ranking_accord == 'AccumulatedEnergy':
                if gdf.shape[1] == 5:
                    score = func(gdf.power, gdf.predict, cap)
                else:
                    score = func(gdf.power_y, gdf.predict_power_x, cap)
            else:
                score = func(gdf.iloc[:, 0], gdf.iloc[:, 1], cap)
            data.append([day, score])
    else:
        data = []
        for day, gdf in df.groupby(by=lambda x: x.strftime('%Y-%m-%d')):
            if gdf.shape[0] < 70:
                continue
            score = func(gdf.iloc[:, 0], gdf.iloc[:, 1], cap)
            data.append([day, score])

    return pd.DataFrame(
        data, columns=['day', 'accurate']).set_index(keys='day')


def AccumulatedEnergy(real, pred, cap=49500):
    data = pd.DataFrame()
    data['real'] = real
    data['pred'] = pred
    data['error'] = np.abs((data['real']-data['pred']))/data['pred']
    data.ix[(data['real'] == 0) & (data['pred'] <= 0.03*cap), 'error'] = 0
    data.ix[(data['real'] == 0) & (data['pred'] >= 0.03*cap), 'error'] = 1
    data.ix[(data['real'] <= 0.03*cap) & (data['pred'] == 0), 'error'] = 0
    data.ix[(data['real'] > 0.03*cap) & (data['pred'] == 0), 'error'] = 1
    data = data.reset_index(drop=True)
    data['fenshu'] = 0
    for nn in range(0, len(data)):
        if data.ix[nn, 'error'] > 0.2:
            data.ix[nn, 'fenshu'] = np.abs((np.abs(
                data.ix[nn, 'real']-data.ix[nn, 'pred']
                )-0.2*data.ix[nn, 'pred']))/10000*0.25*0.2
    return -np.sum(data['fenshu'])
