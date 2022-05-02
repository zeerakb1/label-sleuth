from typing import Sequence
import numpy as np
from lrtc_lib.active_learning.core.active_learning_api import ActiveLearner
from lrtc_lib.data_access.core.data_structs import TextElement
from lrtc_lib.models.core.model_api import Prediction


class HardMiningLearner(ActiveLearner):
    """
    This active learning module suggests "hard" examples, i.e. examples that the model is most uncertain about.
    The highest active learning scores are given to examples which were given model scores closest to the
    decision threshold of 0.5.
    """
    def get_recommended_items_for_labeling(self, workspace_id, dataset_name, category_name,
                                           candidate_text_elements: Sequence[TextElement],
                                           candidate_text_element_predictions: Sequence[Prediction], sample_size=1):
        uncertainty_scores = self.get_per_element_score(candidate_text_elements, candidate_text_element_predictions,
                                                        workspace_id, dataset_name, category_name)
        sorted_indices = np.argsort(uncertainty_scores)[::-1]
        top_indices = sorted_indices[:sample_size]
        recommended_items = np.array(candidate_text_elements)[np.array(top_indices)].tolist()
        return recommended_items

    def get_per_element_score(self, candidate_text_elements: Sequence[TextElement],
                              candidate_text_element_predictions: Sequence[Prediction], workspace_id: str,
                              dataset_name: str, category_name: str) -> Sequence[float]:
        return [2*(0.5-abs(pred.score-0.5)) for pred in candidate_text_element_predictions]
