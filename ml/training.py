import json
import os
from datetime import datetime, timezone
from pathlib import Path
import joblib
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, f1_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from dataset import FEATURES, generate

DATA_DIR = Path(os.getenv('ML_DATA_DIR','/data'))
DATASET = DATA_DIR / 'students_synthetic.csv'
MODEL = DATA_DIR / 'student_profile_model.joblib'
METADATA = DATA_DIR / 'model_metadata.json'

def train(job_id='initial', seed=42):
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    # Gerar novamente com semente fixa: experimento reproduzível.
    df = generate(str(DATASET), n=1500, seed=seed)
    # Mesma ordem FEATURES usada na inferência, sem avisos por nomes de colunas.
    X, y = df[FEATURES].to_numpy(), df['profile_label']
    X_dev, X_test, y_dev, y_test = train_test_split(X,y,test_size=.15,random_state=seed,stratify=y)
    X_train, X_val, y_train, y_val = train_test_split(X_dev,y_dev,test_size=15/85,random_state=seed,stratify=y_dev)
    pipe = Pipeline([('scaler',StandardScaler()),('model',LogisticRegression(max_iter=1500,random_state=seed))])
    pipe.fit(X_train,y_train)
    val_pred=pipe.predict(X_val)
    test_pred=pipe.predict(X_test)
    version=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
    meta={
      'job_id':job_id,'version':version,'synthetic_data':True,'seed':seed,'rows':len(df),
      'splits':{'train':len(X_train),'validation':len(X_val),'test':len(X_test)},
      'features':FEATURES,'classes':list(pipe.classes_),
      'validation_accuracy':float(accuracy_score(y_val,val_pred)),
      'test_accuracy':float(accuracy_score(y_test,test_pred)),
      'test_macro_f1':float(f1_score(y_test,test_pred,average='macro')),
      'confusion_matrix_labels':list(pipe.classes_),
      'confusion_matrix':confusion_matrix(y_test,test_pred,labels=pipe.classes_).tolist(),
      'classification_report':classification_report(y_test,test_pred,output_dict=True,zero_division=0)
    }
    # Substituição atômica do artefato e metadados após validação.
    temp_model=MODEL.with_suffix('.joblib.tmp')
    joblib.dump(pipe,temp_model)
    temp_model.replace(MODEL)
    temp_meta=METADATA.with_suffix('.json.tmp')
    temp_meta.write_text(json.dumps(meta,indent=2,ensure_ascii=False),encoding='utf-8')
    temp_meta.replace(METADATA)
    return meta

if __name__=='__main__':
    print(json.dumps(train(),indent=2))
