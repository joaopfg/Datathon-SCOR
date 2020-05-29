import functools

import warnings
warnings.filterwarnings('ignore')
import pickle
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import xgboost as xgb
import keras
from keras.models import Sequential 
from keras.layers import Dense 
from keras.utils import np_utils
from sklearn.preprocessing import LabelEncoder
from keras.utils.np_utils import to_categorical
from sklearn.utils import shuffle

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from flaskr.db import get_db

bp = Blueprint('data', __name__, url_prefix='/data')

@bp.route('/initialpage', methods=('GET', 'POST'))
def initialpage():
    if request.method == 'POST':
        weight = request.form['weight'];
        bmi = request.form['bmi'];
        pulse = request.form['pulse'];
        age = request.form['age'];
        sleep = request.form['sleep'];
        smoke = request.form['smoke']
        phys_activ = request.form['phys_activ']
        walk_bic = request.form['walk_bic']
        vig_activ = request.form['vig_activ']
        mod_activ = request.form['mod_activ']
        tv_day = request.form['tv_day']
        fat_foods = request.form['fat_foods']
        alcohol_day = request.form['alcohol_day']
        alcohol_year = request.form['alcohol_year']

        db = get_db()
        error = None

        if not weight:
            error = 'Weight is required.'
        elif not bmi:
            error = 'BMI is required.'
        elif not pulse:
            error = 'Pulse is required.'
        elif not age:
            error = 'Age is required.'
        elif not sleep:
            error = 'Sleep is required.'
        elif not smoke:
            error = 'Smoke is required.'
        elif not phys_activ:
            error = 'Physical activity is required.'
        elif not walk_bic:
            error = 'We need to know if you have habit to walk or ride bicycle.'
        elif not vig_activ:
            error = 'We need to know if you have practiced vigorous recreational activities.'
        elif not mod_activ:
            error = 'We need to know if you have practiced moderate recreational activities.'
        elif not tv_day:
            error = 'We need to know how many hours per day you watch tv.'
        elif not fat_foods:
            error = 'We need to know how many bad meals you take per week.'
        elif not alcohol_day:
            error = 'We need to know how many alcohol drinks you take per day.'
        elif not alcohol_year:
            error = 'We need to know how often you drink alcohol per year.'

        if error is None:
            if db.execute('SELECT weight, bmi, pulse, age, sleep, smoke, phys_activ, walk_bic, vig_activ, mod_activ, tv_day, fat_foods, alcohol_day, alcohol_year FROM bq').fetchone() is None:
                db.execute('INSERT INTO bq (weight, bmi, pulse, age, sleep, smoke, phys_activ, walk_bic, vig_activ, mod_activ, tv_day, fat_foods, alcohol_day, alcohol_year) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',(weight, bmi, pulse, age, sleep, smoke, phys_activ, walk_bic, vig_activ, mod_activ, tv_day, fat_foods, alcohol_day, alcohol_year))
                db.commit()

            bq = db.execute('SELECT * FROM bq WHERE (weight, bmi, pulse, age, sleep, smoke, phys_activ, walk_bic, vig_activ, mod_activ, tv_day, fat_foods, alcohol_day, alcohol_year) = (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',(weight, bmi, pulse, age, sleep, smoke, phys_activ, walk_bic, vig_activ, mod_activ, tv_day, fat_foods, alcohol_day, alcohol_year)).fetchone()
            session.clear()
            session['bq_id'] = bq['id']
            return redirect(url_for('data.finalpage'))

        flash(error)

    return render_template('data/initialpage.html')


@bp.route('/finalpage')
def finalpage():
    bq_id = session.get('bq_id')

    if bq_id is None:
        g.bq = None
    else:
        g.bq = get_db().execute('SELECT * FROM bq WHERE id = ?', (bq_id,)).fetchone()

        weight = g.bq['weight']
        bmi = g.bq['bmi']
        pulse = g.bq['pulse']
        age = g.bq['age']
        sleep = g.bq['sleep']
        smoke = g.bq['smoke']
        phys_activ = g.bq['phys_activ']
        walk_bic = g.bq['walk_bic']
        vig_activ = g.bq['vig_activ']
        mod_activ = g.bq['mod_activ']
        tv_day = g.bq['tv_day']
        fat_foods = g.bq['fat_foods']
        alcohol_day = g.bq['alcohol_day']
        alcohol_year = g.bq['alcohol_year']

        if smoke == "Yes":
            smoke = 1
        else:
            smoke = 0

        if phys_activ == "Yes":
            phys_activ = 1
        else:
            phys_activ = 0

        if walk_bic == "Yes":
            walk_bic = 1
        else:
            walk_bic = 0

        if vig_activ == "Yes":
            vig_activ = 1
        else:
            vig_activ = 0

        if mod_activ == "Yes":
            mod_activ = 1
        else:
            mod_activ = 0

        #Filenames for trained models
        filename_death = 'Xgboost_model.sav'
        filename_chol = 'Cholesterol_model.sav'
        filename_diabetes = 'Diabetes_model.sav'
        filename_glyco = 'GlycoHemoglobin_model.sav'
        #Getting the models
        death_cl = pickle.load(open(filename_death, 'rb'))
        chol_reg = pickle.load(open(filename_chol, 'rb'))
        diabetes_cl = pickle.load(open(filename_diabetes, 'rb'))
        glyco_reg = pickle.load(open(filename_glyco, 'rb'))
        #Datasets for cholesterol and diabetes
        X_test_chol = pd.DataFrame([[smoke, phys_activ, walk_bic, vig_activ, mod_activ, fat_foods, alcohol_day, alcohol_year]], columns=['Smoke100', 'PhysActive', 'WalkBic', 'VigActiv', 'ModActiv', 'FatFoods', 'AlcoholDay', 'AlcoholYear'])
        X_test_glyco = pd.DataFrame([[smoke, phys_activ, walk_bic, vig_activ, mod_activ, fat_foods, alcohol_day, alcohol_year]], columns=['Smoke100', 'PhysActive', 'WalkBic', 'VigActiv', 'ModActiv', 'FatFoods', 'AlcoholDay', 'AlcoholYear'])
        X_test_diabetes = pd.DataFrame([[weight, bmi, pulse, sleep, age, smoke, phys_activ, walk_bic, vig_activ, mod_activ, tv_day, fat_foods, alcohol_day, alcohol_year]], columns=['Weight','BMI','Pulse','SleepHrsNight', 'Age', 'Smoke100', 'PhysActive', 'WalkBic', 'VigActiv', 'ModActiv', 'TVHrsDay', 'FatFoods', 'AlcoholDay', 'AlcoholYear'])
        #Gettting initial results for cholesterol and diabetes
        chol_init = chol_reg.predict(X_test_chol)[0]
        glyco_init = glyco_reg.predict(X_test_glyco)[0] 
        prob_diabetes_init = diabetes_cl.predict_proba(X_test_diabetes)[:, 1][0]
        #Datasets for death and age
        if prob_diabetes_init > 0.5:
            X_test_death = pd.DataFrame([[weight, bmi, pulse, chol_init, 1, sleep, smoke, phys_activ, walk_bic, vig_activ, mod_activ, tv_day, fat_foods, alcohol_day, alcohol_year]], columns=['Weight','BMI','Pulse', 'TotChol', 'Diabetes' ,'SleepHrsNight', 'Smoke100', 'PhysActive', 'WalkBic', 'VigActiv', 'ModActiv', 'TVHrsDay', 'FatFoods', 'AlcoholDay', 'AlcoholYear'])
        else:
            X_test_death = pd.DataFrame([[weight, bmi, pulse, chol_init, 0, sleep, smoke, phys_activ, walk_bic, vig_activ, mod_activ, tv_day, fat_foods, alcohol_day, alcohol_year]], columns=['Weight','BMI','Pulse', 'TotChol', 'Diabetes' ,'SleepHrsNight', 'Smoke100', 'PhysActive', 'WalkBic', 'VigActiv', 'ModActiv', 'TVHrsDay', 'FatFoods', 'AlcoholDay', 'AlcoholYear'])
        #Getting initial results for death and age
        prob_death_init = death_cl.predict_proba(X_test_death)[:, 0][0]
        health = True

        if prob_death_init > 0.5:
            health = False

        chol_smoke = chol_init
        glyco_smoke = glyco_init
        prob_death_smoke = prob_death_init
        prob_diabetes_smoke = prob_diabetes_init

        if smoke == 1:
            X_test_chol_smoke = pd.DataFrame([[0, phys_activ, walk_bic, vig_activ, mod_activ, fat_foods, alcohol_day, alcohol_year]], columns=['Smoke100', 'PhysActive', 'WalkBic', 'VigActiv', 'ModActiv', 'FatFoods', 'AlcoholDay', 'AlcoholYear'])
            X_test_glyco_smoke = pd.DataFrame([[0, phys_activ, walk_bic, vig_activ, mod_activ, fat_foods, alcohol_day, alcohol_year]], columns=['Smoke100', 'PhysActive', 'WalkBic', 'VigActiv', 'ModActiv', 'FatFoods', 'AlcoholDay', 'AlcoholYear'])
            X_test_diabetes_smoke = pd.DataFrame([[weight, bmi, pulse, sleep, age, 0, phys_activ, walk_bic, vig_activ, mod_activ, tv_day, fat_foods, alcohol_day, alcohol_year]], columns=['Weight','BMI','Pulse','SleepHrsNight', 'Age', 'Smoke100', 'PhysActive', 'WalkBic', 'VigActiv', 'ModActiv', 'TVHrsDay', 'FatFoods', 'AlcoholDay', 'AlcoholYear'])
            prob_diabetes_smoke = diabetes_cl.predict_proba(X_test_diabetes_smoke)[:, 1][0]
            chol_smoke = chol_reg.predict(X_test_chol_smoke)[0]
            glyco_smoke = glyco_reg.predict(X_test_glyco_smoke)[0]
            if prob_diabetes_smoke > 0.5:
                X_test_death_smoke = pd.DataFrame([[weight, bmi, pulse, chol_init, 1, sleep, 0, phys_activ, walk_bic, vig_activ, mod_activ, tv_day, fat_foods, alcohol_day, alcohol_year]], columns=['Weight','BMI','Pulse', 'TotChol', 'Diabetes' ,'SleepHrsNight', 'Smoke100', 'PhysActive', 'WalkBic', 'VigActiv', 'ModActiv', 'TVHrsDay', 'FatFoods', 'AlcoholDay', 'AlcoholYear'])
                prob_death_smoke = death_cl.predict_proba(X_test_death_smoke)[:, 0][0]
            else:
                X_test_death_smoke = pd.DataFrame([[weight, bmi, pulse, chol_init, 0, sleep, 0, phys_activ, walk_bic, vig_activ, mod_activ, tv_day, fat_foods, alcohol_day, alcohol_year]], columns=['Weight','BMI','Pulse', 'TotChol', 'Diabetes' ,'SleepHrsNight', 'Smoke100', 'PhysActive', 'WalkBic', 'VigActiv', 'ModActiv', 'TVHrsDay', 'FatFoods', 'AlcoholDay', 'AlcoholYear'])
                prob_death_smoke = death_cl.predict_proba(X_test_death_smoke)[:, 0][0]

        chol_vig = chol_init
        glyco_vig = glyco_init
        prob_death_vig = prob_death_init
        prob_diabetes_vig = prob_diabetes_init

        if vig_activ == 0:
            X_test_chol_vig = pd.DataFrame([[smoke, phys_activ, walk_bic, 1, mod_activ, fat_foods, alcohol_day, alcohol_year]], columns=['Smoke100', 'PhysActive', 'WalkBic', 'VigActiv', 'ModActiv', 'FatFoods', 'AlcoholDay', 'AlcoholYear'])
            X_test_glyco_vig = pd.DataFrame([[smoke, phys_activ, walk_bic, 1, mod_activ, fat_foods, alcohol_day, alcohol_year]], columns=['Smoke100', 'PhysActive', 'WalkBic', 'VigActiv', 'ModActiv', 'FatFoods', 'AlcoholDay', 'AlcoholYear'])
            X_test_diabetes_vig = pd.DataFrame([[weight, bmi, pulse, sleep, age, smoke, phys_activ, walk_bic, 1, mod_activ, tv_day, fat_foods, alcohol_day, alcohol_year]], columns=['Weight','BMI','Pulse','SleepHrsNight', 'Age', 'Smoke100', 'PhysActive', 'WalkBic', 'VigActiv', 'ModActiv', 'TVHrsDay', 'FatFoods', 'AlcoholDay', 'AlcoholYear'])
            prob_diabetes_vig = diabetes_cl.predict_proba(X_test_diabetes_vig)[:, 1][0]
            chol_vig = chol_reg.predict(X_test_chol_vig)[0]
            glyco_vig = glyco_reg.predict(X_test_glyco_vig)[0]
            if prob_diabetes_vig > 0.5:
                X_test_death_vig = pd.DataFrame([[weight, bmi, pulse, chol_init, 1, sleep, smoke, phys_activ, walk_bic, 1, mod_activ, tv_day, fat_foods, alcohol_day, alcohol_year]], columns=['Weight','BMI','Pulse', 'TotChol', 'Diabetes' ,'SleepHrsNight', 'Smoke100', 'PhysActive', 'WalkBic', 'VigActiv', 'ModActiv', 'TVHrsDay', 'FatFoods', 'AlcoholDay', 'AlcoholYear'])
                prob_death_vig = death_cl.predict_proba(X_test_death_vig)[:, 0][0]
            else:
                X_test_death_vig = pd.DataFrame([[weight, bmi, pulse, chol_init, 0, sleep, smoke, phys_activ, walk_bic, 1, mod_activ, tv_day, fat_foods, alcohol_day, alcohol_year]], columns=['Weight','BMI','Pulse', 'TotChol', 'Diabetes' ,'SleepHrsNight', 'Smoke100', 'PhysActive', 'WalkBic', 'VigActiv', 'ModActiv', 'TVHrsDay', 'FatFoods', 'AlcoholDay', 'AlcoholYear'])
                prob_death_vig = death_cl.predict_proba(X_test_death_vig)[:, 0][0]

        chol_mod = chol_init
        glyco_mod = glyco_init
        prob_death_mod = prob_death_init
        prob_diabetes_mod = prob_diabetes_init

        if mod_activ == 0:
            X_test_chol_mod = pd.DataFrame([[smoke, phys_activ, walk_bic, vig_activ, 1, fat_foods, alcohol_day, alcohol_year]], columns=['Smoke100', 'PhysActive', 'WalkBic', 'VigActiv', 'ModActiv', 'FatFoods', 'AlcoholDay', 'AlcoholYear'])
            X_test_glyco_mod = pd.DataFrame([[smoke, phys_activ, walk_bic, vig_activ, 1, fat_foods, alcohol_day, alcohol_year]], columns=['Smoke100', 'PhysActive', 'WalkBic', 'VigActiv', 'ModActiv', 'FatFoods', 'AlcoholDay', 'AlcoholYear'])
            X_test_diabetes_mod = pd.DataFrame([[weight, bmi, pulse, sleep, age, smoke, phys_activ, walk_bic, vig_activ, 1, tv_day, fat_foods, alcohol_day, alcohol_year]], columns=['Weight','BMI','Pulse','SleepHrsNight', 'Age', 'Smoke100', 'PhysActive', 'WalkBic', 'VigActiv', 'ModActiv', 'TVHrsDay', 'FatFoods', 'AlcoholDay', 'AlcoholYear'])
            prob_diabetes_mod = diabetes_cl.predict_proba(X_test_diabetes_mod)[:, 1][0]
            chol_mod = chol_reg.predict(X_test_chol_mod)[0]
            glyco_mod = glyco_reg.predict(X_test_glyco_mod)[0]
            if prob_diabetes_mod > 0.5:
                X_test_death_mod = pd.DataFrame([[weight, bmi, pulse, chol_init, 1, sleep, smoke, phys_activ, walk_bic, vig_activ, 1, tv_day, fat_foods, alcohol_day, alcohol_year]], columns=['Weight','BMI','Pulse', 'TotChol', 'Diabetes' ,'SleepHrsNight', 'Smoke100', 'PhysActive', 'WalkBic', 'VigActiv', 'ModActiv', 'TVHrsDay', 'FatFoods', 'AlcoholDay', 'AlcoholYear'])
                prob_death_mod = death_cl.predict_proba(X_test_death_mod)[:, 0][0]
            else:
                X_test_death_mod = pd.DataFrame([[weight, bmi, pulse, chol_init, 0, sleep, smoke, phys_activ, walk_bic, vig_activ, 1, tv_day, fat_foods, alcohol_day, alcohol_year]], columns=['Weight','BMI','Pulse', 'TotChol', 'Diabetes' ,'SleepHrsNight', 'Smoke100', 'PhysActive', 'WalkBic', 'VigActiv', 'ModActiv', 'TVHrsDay', 'FatFoods', 'AlcoholDay', 'AlcoholYear'])
                prob_death_mod = death_cl.predict_proba(X_test_death_mod)[:, 0][0]

        chol_fat = chol_init
        glyco_fat = glyco_init
        prob_death_fat = prob_death_init
        prob_diabetes_fat = prob_diabetes_init

        X_test_chol_fat = pd.DataFrame([[smoke, phys_activ, walk_bic, vig_activ, mod_activ, 0, alcohol_day, alcohol_year]], columns=['Smoke100', 'PhysActive', 'WalkBic', 'VigActiv', 'ModActiv', 'FatFoods', 'AlcoholDay', 'AlcoholYear'])
        X_test_glyco_fat = pd.DataFrame([[smoke, phys_activ, walk_bic, vig_activ, mod_activ, 0, alcohol_day, alcohol_year]], columns=['Smoke100', 'PhysActive', 'WalkBic', 'VigActiv', 'ModActiv', 'FatFoods', 'AlcoholDay', 'AlcoholYear'])
        X_test_diabetes_fat = pd.DataFrame([[weight, bmi, pulse, sleep, age, smoke, phys_activ, walk_bic, vig_activ, mod_activ, tv_day, 0, alcohol_day, alcohol_year]], columns=['Weight','BMI','Pulse','SleepHrsNight', 'Age', 'Smoke100', 'PhysActive', 'WalkBic', 'VigActiv', 'ModActiv', 'TVHrsDay', 'FatFoods', 'AlcoholDay', 'AlcoholYear'])
        prob_diabetes_fat = diabetes_cl.predict_proba(X_test_diabetes_fat)[:, 1][0]
        chol_fat = chol_reg.predict(X_test_chol_fat)[0]
        glyco_fat = glyco_reg.predict(X_test_glyco_fat)[0]
        if prob_diabetes_fat > 0.5:
            X_test_death_fat = pd.DataFrame([[weight, bmi, pulse, chol_init, 1, sleep, smoke, phys_activ, walk_bic, vig_activ, mod_activ, tv_day, 0, alcohol_day, alcohol_year]], columns=['Weight','BMI','Pulse', 'TotChol', 'Diabetes' ,'SleepHrsNight', 'Smoke100', 'PhysActive', 'WalkBic', 'VigActiv', 'ModActiv', 'TVHrsDay', 'FatFoods', 'AlcoholDay', 'AlcoholYear'])
            prob_death_fat = death_cl.predict_proba(X_test_death_fat)[:, 0][0]
        else:
            X_test_death_fat = pd.DataFrame([[weight, bmi, pulse, chol_init, 0, sleep, smoke, phys_activ, walk_bic, vig_activ, mod_activ, tv_day, 0, alcohol_day, alcohol_year]], columns=['Weight','BMI','Pulse', 'TotChol', 'Diabetes' ,'SleepHrsNight', 'Smoke100', 'PhysActive', 'WalkBic', 'VigActiv', 'ModActiv', 'TVHrsDay', 'FatFoods', 'AlcoholDay', 'AlcoholYear'])
            prob_death_fat = death_cl.predict_proba(X_test_death_fat)[:, 0][0]

        chol_alcday = chol_init
        glyco_alcday = glyco_init
        prob_death_alcday = prob_death_init
        prob_diabetes_alcday = prob_diabetes_init

        X_test_chol_alcday = pd.DataFrame([[smoke, phys_activ, walk_bic, vig_activ, mod_activ, fat_foods, 0, 0]], columns=['Smoke100', 'PhysActive', 'WalkBic', 'VigActiv', 'ModActiv', 'FatFoods', 'AlcoholDay', 'AlcoholYear'])
        X_test_glyco_alcday = pd.DataFrame([[smoke, phys_activ, walk_bic, vig_activ, mod_activ, fat_foods, 0, 0]], columns=['Smoke100', 'PhysActive', 'WalkBic', 'VigActiv', 'ModActiv', 'FatFoods', 'AlcoholDay', 'AlcoholYear'])
        X_test_diabetes_alcday = pd.DataFrame([[weight, bmi, pulse, sleep, age, smoke, phys_activ, walk_bic, vig_activ, mod_activ, tv_day, fat_foods, 0, 0]], columns=['Weight','BMI','Pulse','SleepHrsNight', 'Age', 'Smoke100', 'PhysActive', 'WalkBic', 'VigActiv', 'ModActiv', 'TVHrsDay', 'FatFoods', 'AlcoholDay', 'AlcoholYear'])
        prob_diabetes_alcday = diabetes_cl.predict_proba(X_test_diabetes_alcday)[:, 1][0]
        chol_alcday = chol_reg.predict(X_test_chol_alcday)[0]
        glyco_alcday = glyco_reg.predict(X_test_glyco_alcday)[0]
        if prob_diabetes_alcday > 0.5:
            X_test_death_alcday = pd.DataFrame([[weight, bmi, pulse, chol_init, 1, sleep, smoke, phys_activ, walk_bic, vig_activ, mod_activ, tv_day, fat_foods, 0, 0]], columns=['Weight','BMI','Pulse', 'TotChol', 'Diabetes' ,'SleepHrsNight', 'Smoke100', 'PhysActive', 'WalkBic', 'VigActiv', 'ModActiv', 'TVHrsDay', 'FatFoods', 'AlcoholDay', 'AlcoholYear'])
            prob_death_alcday = death_cl.predict_proba(X_test_death_alcday)[:, 0][0]
        else:
            X_test_death_alcday = pd.DataFrame([[weight, bmi, pulse, chol_init, 0, sleep, smoke, phys_activ, walk_bic, vig_activ, mod_activ, tv_day, fat_foods, 0, 0]], columns=['Weight','BMI','Pulse', 'TotChol', 'Diabetes' ,'SleepHrsNight', 'Smoke100', 'PhysActive', 'WalkBic', 'VigActiv', 'ModActiv', 'TVHrsDay', 'FatFoods', 'AlcoholDay', 'AlcoholYear'])
            prob_death_alcday = death_cl.predict_proba(X_test_death_alcday)[:, 0][0]

        get_db().execute('''DELETE FROM bq WHERE id = ? ''', (bq_id,))
        get_db().commit()

    return render_template('data/finalpage.html', prob_death_init = prob_death_init, glyco_init = glyco_init, age = age, smoke = smoke, vig_activ = vig_activ, mod_activ = mod_activ, fat_foods = fat_foods, alcohol_day = alcohol_day, health = health, chol_init = chol_init, prob_diabetes_init = prob_diabetes_init, prob_death_smoke = prob_death_smoke, glyco_smoke = glyco_smoke, chol_smoke = chol_smoke, prob_diabetes_smoke = prob_diabetes_smoke, prob_death_vig = prob_death_vig, glyco_vig = glyco_vig, chol_vig = chol_vig, prob_diabetes_vig = prob_diabetes_vig, prob_death_mod = prob_death_mod, glyco_mod = glyco_mod, chol_mod = chol_mod, prob_diabetes_mod = prob_diabetes_mod, prob_death_fat = prob_death_fat, glyco_fat = glyco_fat, chol_fat = chol_fat, prob_diabetes_fat = prob_diabetes_fat, prob_death_alcday = prob_death_alcday, glyco_alcday = glyco_alcday, chol_alcday = chol_alcday, prob_diabetes_alcday = prob_diabetes_alcday)