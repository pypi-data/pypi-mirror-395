"""Task definition and loading system."""

import string
from abc import ABC, abstractmethod
from ast import Tuple
from typing import List, Optional

from datasets import Dataset, load_dataset

from .dojos import Dojo
from .dojos.dojos_loader import load_dojos
from .dojos.rewards import get_reward_function
from .models import TaskDefinition, ValidateTask


class RewardNotFoundError(Exception):
    """Exception raised when a reward function is not found."""

    pass


class TaskLoader(ABC):
    """Abstract base class for task loaders."""

    @abstractmethod
    def load_task(self, task_path: str) -> TaskDefinition:
        """Load a task definition from a JSON file."""
        pass

    @abstractmethod
    def load_dojo_tasks(self, dojo_name: str) -> List[TaskDefinition]:
        """Load all tasks from a benchmark directory."""
        pass

    @abstractmethod
    def list_tasks(self, category: Optional[str] = None) -> dict[str, TaskDefinition]:
        """List all available tasks."""
        pass


class PyTaskLoader:
    """Loads tasks from python-based task registry"""

    @staticmethod
    def _register_all(bms: list[Dojo]) -> dict[string, Dojo]:
        result = {}
        for bm in bms:
            result[bm.get_id()] = bm

        return result

    def __init__(self):
        self.benchmarks_by_name = PyTaskLoader._register_all(load_dojos())

    def load_task(self, benchmark_task_path: str) -> TaskDefinition:
        split_path = benchmark_task_path.split("/")
        benchmark_name = split_path[0]
        task_id = split_path[1]
        tasks = self.load_benchmark_tasks(benchmark_name)
        for task in tasks:
            if task.id == task_id:
                return task
        raise ValueError(f"Task {task_id} not found in benchmark {benchmark_name}")

    def load_benchmark_tasks(self, benchmark_name: str) -> List[TaskDefinition]:
        return self.benchmarks_by_name[benchmark_name].get_tasks_list()

    def list_tasks(self, category: Optional[str] = None) -> dict[str, TaskDefinition]:
        raise NotImplementedError("List tasks not implemented")


class RemoteTaskLoader:
    """Loads tasks from a Hugging Face dataset."""

    def __init__(self, dataset_name: str):
        self.dataset_name = dataset_name
        self.dataset = None
        self.task_definitions = {}
        self.datasets_cache = {}
        self.tasks_without_reward = {}

    def _load_task_definitions(self):
        if self.task_definitions is None:
            self.task_definitions = self._get_all_tasks_definitions()
        return self.task_definitions

    def _load_dataset(self, name: str) -> Dataset:
        """Lazy load the HF dataset."""
        if name not in self.datasets_cache:
            self.datasets_cache[name] = load_dataset(name)["train"]
            print(f"✓ Loaded {len(self.datasets_cache[name])} tasks from HF dataset {name}")
        return self.datasets_cache[name]

    def _import_reward_function(self, function_name: str) -> ValidateTask:
        """Import a ValidateTask by name from the centralized rewards module."""
        if not function_name or function_name == "":
            raise RewardNotFoundError("Reward function name is empty")

        reward = get_reward_function(function_name)
        if reward is None:
            raise RewardNotFoundError(f"Reward function {function_name} not found")
        return reward

    def _get_all_task_definitions(self, dataset_name: str):
        """Load all tasks from HF dataset and convert to TaskDefinition objects."""
        if dataset_name not in self.datasets_cache:
            print(f"Loading tasks from dataset {self.dataset_name}")
            # TODO: Make this configurable
            dataset = self._load_dataset(dataset_name)

            self.task_definitions[dataset_name] = {}
            for row in dataset:
                # Use the clean constructor that handles HF-specific parsing
                try:
                    task = TaskDefinition.from_hf_row(row, reward_importer=self._import_reward_function)
                except RewardNotFoundError:
                    if dataset_name not in self.tasks_without_reward:
                        self.tasks_without_reward[dataset_name] = set()
                    self.tasks_without_reward[dataset_name].add(f"{row['spa']}/{row['id']}")
                    continue

                self.task_definitions[dataset_name][f"{task.spa}/{task.id}"] = task

            print(f"✓ Converted {len(self.task_definitions[dataset_name])} HF tasks to TaskDefinition objects")

        return self.task_definitions[dataset_name]

    def _get_all_tasks(self) -> List[TaskDefinition]:
        self.task_definitions = self._get_all_task_definitions("chakra-labs/dojo-bench-customer-colossus")
        return [task for task in self.task_definitions.values()]

    def load_benchmark_tasks(self, benchmark_name: str) -> Tuple(List[TaskDefinition], Optional[str]):
        dataset = self._load_dataset(benchmark_name)
        task_ids = [i["text"] for i in dataset]
        return ([self.load_task(task_id) for task_id in task_ids], dataset.version)

    def load_task(self, task_path: str) -> TaskDefinition:
        """
        Load a specific task by org/repo/dojo/task_id path or chakra-labs/dojo-bench-customer-colossus/dojo/task_id path
        if org/repo is not provided.
        """
        if "/" not in task_path:
            raise ValueError(f"Invalid task path format: {task_path}. Expected 'dojo/task_id'")

        parts = task_path.split("/")
        if len(parts) == 2:
            org = "chakra-labs"
            repo = "dojo-bench-customer-colossus"
            dojo_name = parts[0]
            task_id = parts[1]
        elif len(parts) == 4:
            org = parts[0]
            repo = parts[1]
            dojo_name = parts[2]
            task_id = parts[3]
        else:
            raise ValueError(f"Invalid task path format: {task_path}. Expected 'dojo/task_id' or 'org/repo/dojo/task_id'")

        if f"{org}/{repo}" not in self.task_definitions:
            self._get_all_task_definitions(f"{org}/{repo}")

        if f"{dojo_name}/{task_id}" in self.tasks_without_reward.get(f"{org}/{repo}", set()):
            raise RewardNotFoundError(
                f"reward for {task_path} not found." + " Please update your dojo-sdk-core package to the latest version",
            )

        if f"{dojo_name}/{task_id}" not in self.task_definitions[f"{org}/{repo}"]:
            raise ValueError(f"Task {task_path} not found in dataset {org}/{repo}")

        return self.task_definitions[f"{org}/{repo}"][f"{dojo_name}/{task_id}"]

    def list_tasks(self, category: Optional[str] = None) -> dict[str, TaskDefinition]:
        raise NotImplementedError("List tasks not implemented")
