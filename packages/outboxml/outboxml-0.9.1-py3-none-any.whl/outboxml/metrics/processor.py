from typing import Dict

import numpy as np
import pandas as pd
from loguru import logger

from outboxml.core.enums import ModelsParams
from outboxml.core.pydantic_models import DataModelConfig, ModelConfig
from outboxml.data_subsets import ModelDataSubset
from outboxml.metrics.base_metrics import BaseMetrics


class ModelMetrics:
    def __init__(self,
                 model_config: ModelConfig,
                 data_subset: ModelDataSubset,
                 data_config: DataModelConfig=None):
        self._data_config = data_config
        self._model_config = model_config
        self._data_subset = data_subset
        if self._model_config.objective == ModelsParams.binary:
            self.model_type = 'classification'
        elif self._model_config.objective == ModelsParams.clustering:
            self.model_type = 'clustering'
        else:
            self.model_type = 'regression'


    def result_dict(self, predictions: Dict[str, pd.Series])->dict:
        logger.debug(f'Model metrics {self.model_type}||{self._model_config.name}')

        result_metrics = {'train': {}, 'test':{}}

        if self._data_config is not None:
            if len(self._data_config.data.targetslices) > 0:
                logger.info('Train metrics for slices')
                result_metrics['train'] = self._metric_loop(X=self._data_subset.X, y_pred=predictions['train'],
                                                            y_true=self._data_subset.y_train)
                logger.info('Test metrics for slices')
                result_metrics['test'] = self._metric_loop(X=self._data_subset.X, y_pred=predictions['test'],
                                                            y_true=self._data_subset.y_test)

        logger.info('Model metrics||Full train metrics')
        result_metrics['train']['full'] = self.calculate_metrics(y_true=self._data_subset.y_train,
                                                                 y_pred=predictions['train'],
                                                                 weights=self._data_subset.exposure_train)
        logger.info('Model metrics||Full test metrics')
        result_metrics['test']['full'] = self.calculate_metrics(y_true=self._data_subset.y_test,
                                                                y_pred=predictions['test'],
                                                                weights=self._data_subset.exposure_test)

        logger.info(result_metrics)
        return result_metrics

    def calculate_metrics(self, y_pred: pd.Series, y_true: pd.Series=None, weights: pd.Series=None):

        logger.debug('Calculating metrics')
        metrics_dict = BaseMetrics(y_true=y_true,y_pred=y_pred, exposure=weights,
                                   ).calculate_metric(model_type=self.model_type)
        logger.info(metrics_dict)
        return metrics_dict

    def _metric_loop(self, X: pd.DataFrame, y_pred: pd.Series, y_true: pd.Series=None, weights: pd.Series=None) -> Dict[str, dict]:
       results = {}
       slicedDf = pd.DataFrame()
       for data_slice in self._data_config.data.targetslices:

            logger.info('Model metrics||Collecting slices')
            logger.info('Metrics for slice ' + data_slice['column'])
            if data_slice['column'] not in X.columns:
                logger.error('No target slice column in X')
                continue
            if data_slice['type'] == 'numerical':
                slicedDf['slice'] = data_slice['column'] + '_' + pd.cut(X[data_slice['column']],
                                                                       data_slice['slices']).astype(str)
            elif data_slice['type'] == 'categorical':
                slicedDf['slice'] =data_slice['column'] + '_' + X[data_slice['column']].astype(str)
            else:
                raise Exception("Unknown slice type")
            for name in slicedDf['slice'].unique():
                logger.info('Slice ' + name)
                slice_index = slicedDf.loc[slicedDf['slice'] == name].index
                y_true_indexed = y_true[y_true.index.isin(slice_index)] if y_true is not None else None
                y_pred_indexed = y_pred[y_pred.index.isin(slice_index)]
                weights_indexed = weights[weights.index.isin(slice_index)] if weights is not None else None
                if y_pred_indexed.empty:
                    results[name] = None
                else:
                    results[name] = self.calculate_metrics(y_pred=y_pred_indexed,
                                                           y_true=y_true_indexed,
                                                           weights=weights_indexed)


       return results


