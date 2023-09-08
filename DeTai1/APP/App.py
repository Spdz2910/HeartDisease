from flask import Flask, render_template, request, redirect, session
import joblib
import pandas as pd
import pyodbc

app = Flask(__name__, template_folder='templates')

# Cấu hình Secret Key cho session
app.secret_key = '123'

# Kết nối CSDL SQL Server
conn = pyodbc.connect(
    'DRIVER={SQL Server};'
    'SERVER=DUYTHINH\SQLEXPRESS;'
    'DATABASE=BenhTim;'
    'Trusted_connection=yes;'
)

# Đường dẫn đến tập tin
lr_model_file_path = "SVM.joblib"
# Tải mô hình
lr = joblib.load(lr_model_file_path)

# Các hàm thao tác với CSDL
def execute_query_with_no_result(query, params=None):
    cursor = None
    try:
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
    except Exception as e:
        print(f"Error executing query: {e}")
    finally:
        if cursor is not None:
            cursor.close()


def execute_query_with_result(query, params=None):
    cursor = None
    try:
        cursor = conn.cursor()
        cursor.execute(query, params)
        result = cursor.fetchall()
        return result
    except Exception as e:
        print(f"Error executing query: {e}")
    finally:
        if cursor is not None:
            cursor.close()


# Trang chủ - Đăng nhập hoặc đăng ký
@app.route('/', methods=['GET', 'POST'])
def login_page():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = execute_query_with_result("SELECT * FROM [user] WHERE username = ? AND password = ?",
                                         (username, password))

        if user and user[0][3] == password:
            session['user_id'] = user[0][0]
            return redirect('/dashboard')
        else:
            return render_template('login.html', error="Invalid username or password.")
    return render_template('login.html', error='none')


# Đăng ký
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        fullname = request.form['fullname']
        username = request.form['username']
        password = request.form['password']
        execute_query_with_no_result("INSERT INTO [user] (fullname, username, password) VALUES (?,?,?)",
                                     (fullname, username, password))
        conn.commit()
        return redirect('/')

    return render_template('register.html')


# Trang dashboard
@app.route('/dashboard')
def dashboard():
    if 'user_id' in session:
        return render_template('dashboard.html')
    else:
        return redirect('/')


@app.route('/prediction', methods=['GET', 'POST'])
def prediction():
    if request.method == 'POST':
        sbp = float(request.form['sbp'])
        tobacco = float(request.form['tobacco'])
        ldl = float(request.form['ldl'])
        adiposity = float(request.form['adiposity'])
        famhist = int(request.form['famhist'])
        typea = float(request.form['typea'])
        obesity = float(request.form['obesity'])
        alcohol = float(request.form['alcohol'])
        age = float(request.form['age'])
        new_data = pd.DataFrame(
            [[sbp, tobacco, ldl, adiposity, famhist, typea, obesity, alcohol, age]],
            columns=['sbp', 'tobacco', 'ldl', 'adiposity', 'famhist', 'typea', 'obesity', 'alcohol', 'age']
        )

        # Chuyển đổi kiểu dữ liệu của DataFrame
        new_data = new_data.astype({'sbp': 'float', 'tobacco': 'float', 'ldl': 'float', 'adiposity': 'float',
                                    'famhist': 'int', 'typea': 'float', 'obesity': 'float', 'alcohol': 'float', 'age': 'float'})
        prediction = lr.predict(new_data)
        user_id = session['user_id']
        execute_query_with_no_result(
            "INSERT INTO chd (IDuser, sbp, tobacco, ldl, adiposity, famhist, typea, obesity, alcohol, age, prediction) VALUES (?,?,?,?,?,?,?,?,?,?,?)",
            (int(user_id), float(sbp), float(tobacco), float(ldl), float(adiposity), int(famhist), float(typea),
             float(obesity), float(alcohol), float(age), int(prediction[0])))
        conn.commit()

        if prediction[0] == 0:
            result_message = "Bạn không có dấu hiệu bị tim mạch vành."
        else:
            result_message = "Bạn có nguy cơ cao bị tim mạch vành."

        return render_template('prediction.html', prediction=prediction[0], result_message=result_message)

    return render_template('prediction.html', prediction=None, result_message=None)


@app.route('/profile')
def profile():
    if 'user_id' in session:
        user_id = session['user_id']
        user = execute_query_with_result("SELECT * FROM [user] WHERE IDuser = ?", (user_id,))
        if user:
            user_age = int(user[0][3])  # Chuyển đổi tuổi sang kiểu dữ liệu số nguyên
            chd_data = execute_query_with_result("SELECT * FROM chd WHERE IDuser = ?", (user_id,))
            return render_template('profile.html', user=user[0], user_age=user_age, chd_data=chd_data)
        else:
            return redirect('/')
    else:
        return redirect('/')


# Chi tiết chuẩn đoán bệnh
@app.route('/detail/<int:chd_id>')
def detail(chd_id):
    if 'user_id' in session:
        user_id = session['user_id']
        chd_data = execute_query_with_result("SELECT * FROM chd WHERE IDuser = ? AND IDCHD = ?", (user_id, chd_id))
        if chd_data:
            return render_template('detail.html', chd_data=chd_data[0])
        else:
            return redirect('/profile')
    else:
        return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)
    conn.close()
