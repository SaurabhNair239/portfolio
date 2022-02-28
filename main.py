from flask import Flask, request,render_template
from Application_log.log import logger
import pickle
import xgboost

app =Flask(__name__)

@app.route("/", methods=['GET'])
def main_page():

    file = open("Logs/Main Log/main.txt","a+")
    message = "Rendered To Index.html"
    log = logger()
    log.logging(file_obj=file ,log_msg=message)
    file.close()
    return render_template('/index.html')

@app.route("/blackfriday", methods=['GET'])
def blackfriday():
    file = open("Logs/Main Log/main.txt","a+")
    message = "Rendered To Blackfriday.html"
    log = logger()
    log.logging(file_obj=file ,log_msg=message)
    file.close()
    return render_template('/blackfriday.html')
@app.route("/predict",methods=["POST"])
def predict():
    if request.method == 'POST':
            gender = int(request.form['gender'])
            sccy = int(request.form['sccy'])
            ms = int(request.form['ms'])
            pc1 = int(request.form['PC1'])
            pc2 = int(request.form['PC2'])
            pc3 = int(request.form['PC3'])
            cc = request.form['cc']
            if cc == "a":
                b = 0
                c = 0
            elif cc == "b":
                b = 1
                c = 0
            elif cc == "c":
                b = 0
                c = 1
            scalar_filename = "scalar.pickle"
            load_scalar = pickle.load(open(scalar_filename, 'rb'))
            input = [[gender,sccy,ms,pc1,pc2,pc3,b,c]]
            x_scaled = load_scalar.transform(input)

            ml_model_filename = "xgboost_model.pickle"
            load_model = pickle.load(open(ml_model_filename, 'rb'))
            y_pred = load_model.predict(x_scaled)

            file = open("Logs/Main Log/main.txt", "a+")
            message = "Predicting Black friday Data"
            log = logger()
            log.logging(file_obj=file, log_msg=message)
            file.close()

            return render_template('blackfriday.html',prediction = y_pred[0])

@app.route("/loan", methods=['GET'])
def loan():
    file = open("Logs/Main Log/main.txt","a+")
    message = "Rendered To Loan.html"
    log = logger()
    log.logging(file_obj=file ,log_msg=message)
    file.close()
    return render_template('/loan.html')


@app.route("/loan_predict", methods=['POST'])
def loan_predict():
    if request.method == 'POST':

        AI = int(request.form['AI'])
        CAI = int(request.form['CAI'])
        LA = int(request.form['LA'])
        LT = int(request.form['LT'])
        CH = int(request.form['CH'])
        Gender = int(request.form['gender'])
        MS = int(request.form['MS'])
        dep = int(request.form['dep'])
        Edu = int(request.form['Edu'])
        emp = int(request.form['emp'])
        pa = request.form['pa']

        if dep == 0:
            dep1 = 0
            dep2 = 0
            dep3 = 0

        elif dep == 1:
            dep1 = 1
            dep2 = 0
            dep3 = 0

        elif dep == 2:
            dep1 = 0
            dep2 = 1
            dep3 = 0

        elif dep >= 3:
            dep1 = 0
            dep2 = 0
            dep3 = 1

        if pa == 's':
            pas = 1
            pau = 0

        elif pa == 'r':
            pas = 0
            pau = 0
        elif pa == 'u':
            pas = 0
            pau = 1

        scalar_filename = "scale.pkl"
        load_scalar = pickle.load(open(scalar_filename, 'rb'))
        input = [[AI, CAI, LA, LT, CH, Gender, MS, dep1, dep2, dep3, Edu, emp, pas, pau]]
        x_scaled = load_scalar.transform(input)

        ml_model_filename = "svm.pkl"
        load_model = pickle.load(open(ml_model_filename, 'rb'))
        y_pred = load_model.predict(x_scaled)
        if y_pred[0] == 1:
            pred = 'Yes'
        else:
            pred = 'No'
        file = open("Logs/Main Log/main.txt","a+")
        message = "Loan Prediction Model"
        log = logger()
        log.logging(file_obj=file ,log_msg=message)
        file.close()
        return render_template('loan.html', prediction=pred)

if __name__ == "__main__":
    app.run(debug=True)
