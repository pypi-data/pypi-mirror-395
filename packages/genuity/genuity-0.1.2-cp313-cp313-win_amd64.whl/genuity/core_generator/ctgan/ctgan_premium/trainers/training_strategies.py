from typing import List, Dict


class CurriculumLearner:
    """Automatic curriculum learning"""

    def __init__(self):
        self.current_difficulty = 0.1
        self.max_difficulty = 1.0
        self.difficulty_increase_rate = 0.01
        self.performance_threshold = 0.8

    def update_difficulty(self, generator_performance: float):
        """Update difficulty based on generator performance"""
        if generator_performance > self.performance_threshold:
            self.current_difficulty = min(
                self.max_difficulty,
                self.current_difficulty + self.difficulty_increase_rate,
            )
        else:
            # Slightly decrease difficulty if performance drops
            self.current_difficulty = max(
                0.1, self.current_difficulty - self.difficulty_increase_rate * 0.5
            )

    def get_difficulty(self) -> float:
        return self.current_difficulty


class ParetoOptimizer:
    """Multi-objective Pareto optimization"""

    def __init__(self, objectives: List[str]):
        self.objectives = objectives
        self.pareto_front = []

    def is_pareto_optimal(self, losses: Dict[str, float]) -> bool:
        """Check if current losses are Pareto optimal"""
        for front_losses in self.pareto_front:
            # Check if dominated by any point in Pareto front
            dominated = True
            for obj in self.objectives:
                if losses[obj] < front_losses[obj]:
                    dominated = False
                    break
            if dominated:
                return False
        return True

    def update_pareto_front(self, losses: Dict[str, float]):
        """Update Pareto front with current losses"""
        if self.is_pareto_optimal(losses):
            self.pareto_front.append(losses.copy())
            # Remove dominated solutions
            self.pareto_front = [
                front_losses
                for front_losses in self.pareto_front
                if not self._is_dominated(front_losses, losses)
            ]

    def _is_dominated(
        self, losses1: Dict[str, float], losses2: Dict[str, float]
    ) -> bool:
        """Check if losses1 is dominated by losses2"""
        for obj in self.objectives:
            if losses1[obj] < losses2[obj]:
                return False
        return True


class ProgressiveTrainer:
    """Progressive training with auto-scaling"""

    def __init__(self, max_stages: int = 3):
        self.max_stages = max_stages
        self.current_stage = 0
        self.stage_epochs = [100, 200, 300]  # Epochs per stage
        self.current_epoch = 0
        self.stage_performance = []  # Track performance per stage

    def should_advance_stage(self) -> bool:
        """Check if should advance to next stage"""
        if self.current_stage >= self.max_stages - 1:
            return False
        return self.current_epoch >= self.stage_epochs[self.current_stage]

    def advance_stage(self):
        """Advance to next stage"""
        if self.should_advance_stage():
            self.current_stage += 1
            self.current_epoch = 0
            return True
        return False

    def get_current_stage(self) -> int:
        return self.current_stage

    def update_performance(self, performance_metric: float):
        """Update performance tracking for current stage"""
        if len(self.stage_performance) <= self.current_stage:
            self.stage_performance.append([])
        self.stage_performance[self.current_stage].append(performance_metric)

    def get_stage_performance(self) -> List[float]:
        """Get performance history for current stage"""
        if self.current_stage < len(self.stage_performance):
            return self.stage_performance[self.current_stage]
        return []
