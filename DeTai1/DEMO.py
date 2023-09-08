import joblib
import pandas as pd
from sklearn.preprocessing import StandardScaler

# Đường dẫn đến tập tin
lr_model_file_path = "APP/SVM.joblib"

# Tải mô hình
lr = joblib.load(lr_model_file_path)

# Tạo một DataFrame cho mẫu dữ liệu mới (thứ tự các cột phù hợp)
new_data = pd.DataFrame([[0.28,0.44,0.18,0.59,1,0.72,0.35,0.39,0.69]], columns=['sbp', 'tobacco', 'ldl', 'adiposity', 'famhist', 'typea','obesity', 'alcohol', 'age'])


# Chuẩn hóa dữ liệu cho mẫu dữ liệu mới
scaler = StandardScaler()
new_data_scaled = scaler.fit_transform(new_data)

# Dự đoán kết quả cho mẫu dữ liệu mới
prediction = lr.predict(new_data)
print(f"Dự đoán: {prediction[0]}")
