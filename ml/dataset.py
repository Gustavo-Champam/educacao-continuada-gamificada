import numpy as np
import pandas as pd
from pathlib import Path

FEATURES = ["programming_experience_months", "completed_courses", "average_assessment_score", "weekly_study_hours", "rest_knowledge_score", "database_knowledge_score"]
LABELS = ["INICIANTE", "INTERMEDIARIO", "AVANCADO"]

def generate(path: str, n: int = 1500, seed: int = 42):
    rng = np.random.default_rng(seed)
    levels = rng.choice(3, size=n, p=[1/3, 1/3, 1/3])
    records = []
    for i, k in enumerate(levels):
        experience = int(np.clip(rng.normal([3, 19, 52][k], [5, 11, 20][k]), 0, 120))
        completed = int(np.clip(rng.normal([1, 5, 13][k], [2, 3, 5][k]), 0, 35))
        score = float(np.clip(rng.normal([48, 70, 88][k], 13), 0, 100))
        hours = float(np.clip(rng.normal([4, 6, 9][k], 3), 0, 30))
        rest = float(np.clip(rng.normal([27, 63, 86][k], 17), 0, 100))
        db = float(np.clip(rng.normal([30, 60, 85][k], 17), 0, 100))
        records.append([1001+i, experience, completed, round(score,1), round(hours,1), round(rest,1), round(db,1), LABELS[k]])
    df = pd.DataFrame(records, columns=["student_id", *FEATURES, "profile_label"])
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path,index=False)
    return df
