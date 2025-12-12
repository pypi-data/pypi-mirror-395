from PipeGraphPy.constants import DATATYPE
from . import DatachartsBase


class DataView(DatachartsBase):
    INPUT = [DATATYPE.DATAFRAME]
    OUTPUT = []
    TEMPLATE = [{
        "key": "selected_columns",
        "name": "选择的列",
        "type": "string",
        "plugin": "input",
        "need": False,
        "value": "",
        "desc": "要传递的列(多选)"
    }]

    def run(self, df):
        # 获取要传递的X值
        if self.params.get('selected_columns'):
            X = df[self.params.get('selected_columns')]
        else:
            X = df
        df = X
        return df

    def predict(self, df):
        return df
