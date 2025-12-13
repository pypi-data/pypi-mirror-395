from dojo_sdk_core.dojos.model import Dojo


# Add new dojos here
def load_dojos() -> list[Dojo]:
    return []


def collect_tasks(dojos: list[Dojo]) -> list[str]:
    return [dojo.get_id() + "/" + task.id for dojo in dojos for task in dojo.get_tasks_list()]


# TODO: For now this is just a sanity check to make sure the task name is valid.
def run_tasks_by_name(task_names: list[str]) -> list[str]:
    dojos = load_dojos()
    for task_name in task_names:
        found = False
        for dojo in dojos:
            for task in dojo.get_tasks_list():
                if dojo.get_id() + "/" + task.id == task_name:
                    found = True
                    break
        if not found:
            raise ValueError(f"Task {task_name} not found")
    return task_names
