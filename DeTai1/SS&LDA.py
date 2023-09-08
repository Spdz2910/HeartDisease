import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier


# Đường dẫn đến tập tin CHDdata.csv
file_path = 'processed_data.csv'

# Đọc dữ liệu từ tập tin CSV
data = pd.read_csv(file_path)

# Xác định các đặc trưng và nhãn
X = data.iloc[:, :-1].values
y = data.iloc[:, -1].values

# Chia thành tập huấn luyện và tập kiểm tra
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Chuẩn hóa dữ liệu
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Áp dụng LDA để giảm chiều dữ liệu
lda = LDA(n_components=1)
X_train_lda = lda.fit_transform(X_train, y_train)
X_test_lda = lda.transform(X_test)

# Khởi tạo các mô hình
logistic_regression = LogisticRegression()
decision_tree = DecisionTreeClassifier()
rf = RandomForestClassifier()
svm = SVC()
knn = KNeighborsClassifier()

# Huấn luyện các mô hình
logistic_regression.fit(X_train_lda, y_train)
decision_tree.fit(X_train_lda, y_train)
rf.fit(X_train_lda, y_train)
svm.fit(X_train_lda, y_train)
knn.fit(X_train_lda, y_train)

# Dự đoán nhãn trên tập kiểm tra
y_pred_lr = logistic_regression.predict(X_test_lda)
y_pred_dt = decision_tree.predict(X_test_lda)
y_pred_rf = rf.predict(X_test_lda)
y_pred_svm = svm.predict(X_test_lda)
y_pred_knn = knn.predict(X_test_lda)

# Tính toán độ chính xác trên tập kiểm tra
accuracy_lr = accuracy_score(y_test, y_pred_lr)
accuracy_dt = accuracy_score(y_test, y_pred_dt)
accuracy_rf = accuracy_score(y_test, y_pred_rf)
accuracy_svm = accuracy_score(y_test, y_pred_svm)
accuracy_knn = accuracy_score(y_test, y_pred_knn)


# In kết quả
print("Logistic Regression Accuracy:", accuracy_lr*100)
print("Decision Tree Accuracy:", accuracy_dt*100)
print("Random Forest Accuracy:", accuracy_rf*100)
print("SVM Accuracy:", accuracy_svm*100)
print("KNN Accuracy:", accuracy_knn*100)

# Vẽ biểu đồ cột để so sánh kết quả
models = ['Logistic Regression', 'Decision Tree', 'RF', 'SVM', 'KNN']
accuracies = [accuracy_lr, accuracy_dt, accuracy_rf, accuracy_svm, accuracy_knn]

plt.bar(models, accuracies)
plt.xlabel('Model')
plt.ylabel('Accuracy')
plt.title('Model Comparison')
plt.show()
