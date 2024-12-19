from typing import List, Dict
from .task import Task, Step


class TaskScheduler:
    def __init__(self):
        self.tasks = []

    def add_task(self, task: Task):
        self.tasks.append(task)

    def schedule(self) -> List[Dict]:
        # 简单的调度算法
        timeline = []
        current_time = 0

        # 首先安排需要专注的步骤
        focus_steps = []
        parallel_steps = []

        for task in self.tasks:
            for step in task.steps:
                if step.needs_focus:
                    focus_steps.append((task.name, step))
                else:
                    parallel_steps.append((task.name, step))

        # 安排需要专注的步骤
        for task_name, step in focus_steps:
            timeline.append({
                'start_time': current_time,
                'duration': step.duration,
                'tasks': [(task_name, step.name)],
                'needs_focus': True
            })
            current_time += step.duration

        # 尝试并行安排不需要专注的步骤
        while parallel_steps:
            current_slot = []
            remaining_steps = []
            total_duration = 0

            for task_name, step in parallel_steps:
                if total_duration == 0 or total_duration >= step.duration:
                    current_slot.append((task_name, step))
                    total_duration = max(total_duration, step.duration)
                else:
                    remaining_steps.append((task_name, step))

            if current_slot:
                timeline.append({
                    'start_time': current_time,
                    'duration': total_duration,
                    'tasks': [(tn, s.name) for tn, s in current_slot],
                    'needs_focus': False
                })
                current_time += total_duration

            parallel_steps = remaining_steps

        return timeline