import pandas as pd


def xlsx_to_csv_pd():
    # sheet_name=None表示读取全部sheet，或者sheet_name=[0,10]，此处用sheet_name，而不是用sheetname
    data_xls = pd.read_excel('b站1.xlsx', sheet_name=None, index_col=0)
    for key in data_xls:
        data_xls[key].to_csv('bili/' + key + '.csv', encoding='utf-8')


if __name__ == '__main__':
    xlsx_to_csv_pd()
