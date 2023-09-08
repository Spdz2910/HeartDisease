import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.svm import SVC
from sklearn.preprocessing import MinMaxScaler
import joblib

# Đường dẫn đến tập tin CHDdata.csv
file_path = 'processed_data.csv'

# Đọc dữ liệu từ tập tin CSV
data = pd.read_csv(file_path)

# Xác định các đặc trưng và nhãn
X = data.drop('chd', axis=1)
y = data['chd']

# Chuẩn hóa dữ liệu sử dụng Min-Max scaler
scaler = MinMaxScaler()
X_scaled = scaler.fit_transform(X)

# Chia thành tập huấn luyện và tập kiểm tra
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# Định nghĩa các giá trị tham số cần tìm kiếm
param_grid = {
    'C': [0.1, 1, 10],
    'kernel': ['linear', 'rbf'],
    'gamma': [0.1, 1, 10]
}

# Tạo mô hình SVM
svm = SVC()

# Tìm kiếm siêu tham số tốt nhất bằng Grid Search
grid_search = GridSearchCV(estimator=svm, param_grid=param_grid, cv=5)
grid_search.fit(X_train, y_train)

# In ra siêu tham số tốt nhất
print("Siêu tham số tốt nhất:")
print(grid_search.best_params_)

# Lưu mô hình SVM đã được tối ưu vào file joblib
svm_model_file_path = "APP/SVM.joblib"
joblib.dump(grid_search.best_estimator_, svm_model_file_path)
