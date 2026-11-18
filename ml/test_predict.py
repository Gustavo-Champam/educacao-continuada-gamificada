"""Regressão da inferência otimizada contra o pipeline realmente treinado."""
import asyncio
import os
import tempfile
import unittest

data = tempfile.TemporaryDirectory()
os.environ['ML_DATA_DIR'] = data.name
os.environ['ML_AUTO_TRAIN'] = 'false'
import app
from training import train
from dataset import FEATURES


class PredictionTest(unittest.TestCase):
    def test_prediction_matches_pipeline_and_refreshes_after_training(self):
        features = app.Features(programming_experience_months=12, completed_courses=12,
            average_assessment_score=80, weekly_study_hours=6,
            rest_knowledge_score=70, database_knowledge_score=80)
        for seed in (42, 17):
            metadata = train(seed=seed)
            result = asyncio.run(app.predict(features))
            expected = app.model().predict([[getattr(features, key) for key in FEATURES]])[0]
            self.assertEqual(result['profile'], expected)
            self.assertEqual(result['model_version'], metadata['version'])
            self.assertAlmostEqual(sum(result['probabilities'].values()), 1.0, places=5)
            self.assertTrue(result['synthetic_model'])


if __name__ == '__main__':
    unittest.main()
