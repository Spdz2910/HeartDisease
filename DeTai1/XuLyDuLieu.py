import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
import joblib

# Đọc dữ liệu từ tệp CSV
data = pd.read_csv('chdData.csv')

# Chọn chỉ mục cần thiết
selected_columns = ['sbp', 'tobacco', 'ldl', 'adiposity', 'famhist', 'typea', 'obesity', 'alcohol', 'age', 'chd']
data = data[selected_columns]

# Xử lý giá trị thiếu (nếu có)
data = data.dropna()

# Chuyển đổi cột 'famhist' thành dạng số
data['famhist'] = data['famhist'].map({'Present': 1, 'Absent': 0})

# Tạo bản sao của DataFrame gốc để làm việc
data_processed = data.copy()

# Chuẩn hóa dữ liệu sử dụng Min-Max scaler và làm tròn đến 1 chữ số thập phân
scaler = MinMaxScaler()
scaled_columns = ['sbp', 'tobacco', 'ldl', 'adiposity', 'typea', 'obesity', 'alcohol', 'age']
data_processed[scaled_columns] = scaler.fit_transform(data_processed[scaled_columns])
data_processed[scaled_columns] = data_processed[scaled_columns].round(1)

# In thông tin về dữ liệu sau khi tiền xử lý và chuẩn hóa
print("Thông tin về dữ liệu sau khi tiền xử lý và chuẩn hóa:")
print(data_processed.info())
print("\nDữ liệu sau khi tiền xử lý và chuẩn hóa:")
print(data_processed.head())
print(data_processed.corr())

# Lưu tập dữ liệu đã xử lý vào file csv mới
data_processed.to_csv('processed_data.csv', index=False)
print("SAVED SUCCESSFULLY")
