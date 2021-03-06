# Author: Nicolas Legrand <nicolas.legrand@cfin.au.dk>

import unittest
from unittest import TestCase

import numpy as np
import pandas as pd
import pytest

from metadPy import load_dataset
from metadPy.sdt import criterion, dprime, metad, rates, roc_auc, scores

data = pd.DataFrame(
    {
        "Stimuli": np.concatenate(
            (np.ones(20), np.ones(5), np.zeros(10), np.zeros(15))
        ).astype(bool),
        "Responses": np.concatenate(
            (np.ones(20), np.zeros(5), np.ones(10), np.zeros(15))
        ).astype(bool),
    }
)


class Testsdt(TestCase):
    def test_scores(self):
        """Test scores function"""
        data.scores()
        assert (20, 5, 10, 15) == scores(data=data)
        assert (20, 5, 10, 15) == data.scores()
        assert (20, 5, 10, 15) == scores(
            stimuli=data.Stimuli.to_numpy(), responses=data.Responses.to_numpy()
        )
        with pytest.raises(ValueError):
            scores(data=None, stimuli=None, responses=None)

    def test_rates(self):
        """Test rates function"""
        assert (0.8, 0.4) == data.rates()
        assert (0.8, 0.4) == rates(hits=20, misses=5, fas=10, crs=15)
        rates(hits=0, misses=5, fas=0, crs=15)
        rates(hits=5, misses=5, fas=5, crs=5)

    def test_dprime(self):
        """Test d prime function"""
        assert 1.095 == round(dprime(hit_rate=0.8, fa_rate=0.4), 3)
        assert 1.095 == round(data.dprime(), 3)

    def test_criterion(self):
        """Test criterion function"""
        assert 0.294 == -round(criterion(hit_rate=0.8, fa_rate=0.4), 3)
        assert 0.294 == -round(data.criterion(), 3)

    def test_metad(self):
        """Test fit_meta_d_MLE function"""
        nR_S1 = np.array([52, 32, 35, 37, 26, 12, 4, 2])
        nR_S2 = np.array([2, 5, 15, 22, 33, 38, 40, 45])
        fit = metad(nR_S1=nR_S1, nR_S2=nR_S2)
        assert round(fit["meta_da"], 3) == 1.634
        with pytest.raises(ValueError):
            fit = metad(nR_S1=np.zeros(7), nR_S2=nR_S2)
        with pytest.raises(ValueError):
            fit = metad(nR_S1=nR_S1[:1], nR_S2=nR_S2)
        with pytest.raises(ValueError):
            fit = metad(nR_S1=nR_S1, nR_S2=nR_S2, padding=True, collapse=2)
        df = load_dataset("rm")
        fit = metad(
            data=df[df.Subject == 0],
            nRatings=4,
            stimuli="Stimuli",
            accuracy="Accuracy",
            confidence="Confidence",
            output_df=True,
            padding=False,
            collapse=2,
        )
        assert round(fit["meta_da"].iloc[0], 1) == 0.8

    def test_roc_auc(self):
        """Test roc_auc function"""
        nR_S1 = [52, 32, 35, 37, 26, 12, 4, 2]
        nR_S2 = [2, 5, 15, 22, 33, 38, 40, 45]
        auc = roc_auc(nR_S1=nR_S1, nR_S2=nR_S2)
        assert round(auc, 3) == 0.728

        df = load_dataset("rm")
        assert round(df.roc_auc(nRatings=4), 3) == 0.621


if __name__ == "__main__":
    unittest.main(argv=["first-arg-is-ignored"], exit=False)
