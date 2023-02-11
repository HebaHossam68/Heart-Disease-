import streamlit as st
import requests
from streamlit_lottie import st_lottie
import joblib
import numpy as np
from sklearn.utils import check_array



loaded_model=joblib.load(open('C:/Users/future/Downloads/deployment/Heart_Disease_model','rb'))

st.set_page_config(page_title='Heart Disease',page_icon='::star::')

def load_lottie(url):
    r=requests.get(url)
    if r.status_code!=200:
        return None
    return r.json()

def prepare_input_data_for_model(age,sex,cp,trestbps,chol,fbs,restecg,thalach,exang,oldpeak,slope,ca,thal):
     #sex = sex.map(s)
    if sex == 'Female':
        s =0
    else:
        s = 1
    #cpa = cp.map(c)
    if cp =='typical angina':
        cpa=0
    elif cp == 'atypical angina':
        cpa=1
    elif cp =='non-anginal pain':
        cpa=2
    else:
        cpa=3
    #fbss = fbs.map(f)
    if fbs =='YES':
        fbss=1
    else:
        fbss=0
    #r = restecg.map(r)
    if restecg =='normal':
        r=0
    elif restecg=='having ST-T wave abnormality':
        r=1
    else:
        r=2
    #e = exang.map(e)
    if exang=='YES':
        e=1
    else:
        e=0
    #ss = slope.map(ss)
    if slope=='upsloping':
        ss=0
    elif slope=='flat':
        ss=1
    else:
        ss=2
    #cca = ca.map(cca)
    if ca =='aortic':
        cca=0
    elif ca=='pulmonary':
        cca=1
    elif ca=='mitral':
        cca=2
    else:
        cca=3
    
    #thaal = thal.map(thaal)
    if thal=='normal':
        thaal=0
    elif thal=='fixed defect':
        thaal=1
    elif thal=='reversable defect':
        thaal=2
    else:
        thaal=3
    
     
    A = [age,s,cpa,trestbps,chol,fbss,r,thalach,e,oldpeak,ss,cca,thaal]
    sample = np.array(A).reshape(-1,len(A))
    return sample
   # b=np.array(sample, dtype=float)
    



#st.write('##Heart Disease Deployment')
st.header('Heart Disease Deployment')
lottie_link="https://assets4.lottiefiles.com/packages/lf20_kU5CYh.json"
animation=load_lottie(lottie_link)

st.write('---')
st.subheader('Enter details of patient')

with st.container():
    right_column,left_column=st.columns(2)
    with right_column:
        name=st.text_input('Name:')
        age = st.number_input('Age : ', min_value=0.0,value=0.0, step=1.0)
        sex=st.radio('Sex :',['Female','Male'])
        cp = st.selectbox('chest pain type : ', ('typical angina', 'atypical angina', 'non-anginal pain','asymptomatic'))
        trestbps = st.number_input('blood pressure : ', min_value=0.0,value=0.0, step=1.0)
        chol = st.number_input('cholestoral : ', min_value=0.0,value=0.0, step=1.0)
        fbs=st.radio('(Fasting blood sugar > 120 mg/dl) :',['YES','NO'])
        restecg = st.selectbox('Electrocardiographic results: ', ('normal', 'having ST-T wave abnormality ', ' left ventricular hypertrophy'))
        thalach=st.number_input('Maximum heart rate: ',min_value=0.0,value=0.0,step=1.0)
        exang=st.radio('Exercise induced angina: ',['YES','NO'])
        oldpeak=st.number_input('ST depression induced by exercise relative to rest:',min_value=0.0,max_value=10.0,value=0.0,step=0.1)
        slope=st.radio('Slope:',['upsloping','flat','downsloping'])
        ca=st.selectbox('Major vessels',('aortic', 'pulmonary', 'mitral', 'tricuspid valves'))
        thal=st.selectbox('Thal',('normal', 'fixed defect', 'reversable defect', 'label'))

        sample= prepare_input_data_for_model(age,sex,cp,trestbps,chol,fbs,restecg,thalach,exang,oldpeak,slope,ca,thal)
    with left_column:
        st_lottie(animation, speed=1, height=400, key="initial")

    if st.button('Predict'):
            prediction = loaded_model.predict(sample)
            
            if prediction == 0:
                #st.write("## Predicted Status : ", result)
                st.write('### Fine, ', name, '!! Well,You are healty.')
                st.balloons()
            else:
                st.write('### Sorry ', name, '!! You need to see a doctor.')