# SPDX-FileCopyrightText: Copyright (c) 2025 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import glob

import pandas as pd
from nemo_evaluator.api.api_dataclasses import (
    EvaluationResult,
    GroupResult,
    MetricResult,
    Score,
    ScoreStats,
    TaskResult,
)
from vlmeval.smp.file import load


def listinstr(lst, s):
    assert isinstance(lst, list)
    for item in lst:
        if item in s:
            return item
    return False


def parse_output(output_dir: str) -> EvaluationResult:
    """Parse the VLMEvalKit evaluation results from score files and return an EvaluationResult object."""
    # Find the score file with any extension and load it
    score_patterns = [f"{output_dir}/*/*_score.*", f"{output_dir}/*/*_acc.*"]
    score_files = []
    for pattern in score_patterns:
        score_files.extend(glob.glob(pattern))

    if not score_files:
        raise FileNotFoundError(f"No score files found in {output_dir}")
    if len(score_files) > 1:
        raise ValueError(
            f"More than one score file found: {score_files}. Expected exactly one score file."
        )
    file_path = score_files[0]
    metrics = load(file_path)

    # Call the appropriate parser based on file path
    if group_name := listinstr(["mmmu", "ai2d"], file_path.lower()):
        tasks_result, groups_result = _parse_imagemcq_output(metrics, group_name)
    elif "chartqa" in file_path.lower():
        tasks_result, groups_result = _parse_chartqa_output(metrics)
    elif "mathvista" in file_path.lower():
        tasks_result, groups_result = _parse_mathvista_output(metrics)
    elif "ocrbench" in file_path.lower():
        tasks_result, groups_result = _parse_ocrbench_output(metrics)
    elif "slidevqa" in file_path.lower():
        tasks_result, groups_result = _parse_slidevqa_output(metrics)
    elif "ocr_reasoning" in file_path.lower():
        tasks_result, groups_result = _parse_ocr_reasoning_output(metrics)
    else:
        raise ValueError(f"No specific parser found for '{file_path}'")

    return EvaluationResult(tasks=tasks_result, groups=groups_result)


def _parse_imagemcq_output(
    metrics: pd.DataFrame, group_name: str
) -> tuple[dict[str, TaskResult], dict[str, GroupResult]]:
    """Parses the output DataFrame specific to the ImageMCQ datasets."""
    # Get all unique split values and map them to split names
    split_mapping = {}
    for split in metrics["split"].unique():
        if split == "none":
            split_mapping[split] = "accuracy"
        elif split == "validation":
            split_mapping[split] = "val"
        else:
            split_mapping[split] = split

    # Parse the groups result
    group_scores = {}
    for split, split_name in split_mapping.items():
        split_row = metrics[metrics["split"] == split].iloc[0]
        group_scores[split_name] = Score(value=float(split_row["Overall"]), stats={})

    groups_result = {
        group_name: GroupResult(metrics={"accuracy": MetricResult(scores=group_scores)})
    }

    # Parse the tasks result
    tasks_result = {}
    # Get all columns except 'split' and 'Overall'
    task_columns = [col for col in metrics.columns if col not in ["split", "Overall"]]
    for task_name in task_columns:
        slug = task_name.lower().replace(" ", "-").replace("_", "-")

        # Create task scores for each split
        task_scores = {}
        for split, split_name in split_mapping.items():
            split_row = metrics[metrics["split"] == split].iloc[0]
            task_scores[split_name] = Score(value=float(split_row[task_name]), stats={})

        tasks_result[slug] = TaskResult(
            metrics={"accuracy": MetricResult(scores=task_scores)}
        )

    return tasks_result, groups_result


def _parse_chartqa_output(
    metrics: pd.DataFrame,
) -> tuple[dict[str, TaskResult], dict[str, GroupResult]]:
    """Parses the output DataFrame specific to ChartQA dataset."""
    # Transform metrics into a Series
    # NOTE: `metrics` is a DataFrame with a single row representing the accuracy
    #       for a given task.
    metrics = metrics.iloc[0]
    # Parse the group result
    group_result = GroupResult(
        metrics={
            "accuracy": MetricResult(
                scores={
                    "accuracy": Score(
                        # Normalize to [0, 1]
                        value=float(metrics["Overall"]) / 100.0,
                        stats={},
                    )
                }
            )
        }
    )

    # Parse the tasks result
    tasks_result = {}
    for task_name, task_accuracy in metrics.items():
        if task_name == "Overall":
            continue
        slug = task_name.lower().replace(" ", "-").replace("_", "-")
        tasks_result[slug] = TaskResult(
            metrics={
                "accuracy": MetricResult(
                    scores={
                        "accuracy": Score(
                            # Normalize to [0, 1]
                            value=float(task_accuracy) / 100.0,
                            stats={},
                        )
                    }
                )
            }
        )

    return tasks_result, {"chartqa": group_result}


def _parse_mathvista_output(
    metrics: pd.DataFrame,
) -> tuple[dict[str, TaskResult], dict[str, GroupResult]]:
    """Parses the output DataFrame specific to MathVista dataset."""
    # Parse the group result
    overall_metrics = metrics[metrics["Task&Skill"] == "Overall"].iloc[0]
    group_result = GroupResult(
        metrics={
            "accuracy": MetricResult(
                scores={
                    "accuracy": Score(
                        # Normalize to [0, 1]
                        value=float(overall_metrics["acc"]) / 100.0,
                        stats=ScoreStats(
                            count=int(overall_metrics["tot"]),
                            sum=float(overall_metrics["hit"]),
                        ),
                    ),
                }
            ),
            "prefetch_rate": MetricResult(
                scores={
                    "prefetch_rate": Score(
                        # Normalize to [0, 1]
                        value=float(overall_metrics["prefetch_rate"]) / 100.0,
                        stats=ScoreStats(
                            count=int(overall_metrics["tot"]),
                            sum=float(overall_metrics["prefetch"]),
                        ),
                    ),
                }
            ),
        }
    )

    # Parse the tasks result
    tasks_metrics = metrics[metrics["Task&Skill"] != "Overall"]
    tasks_result = {}
    for task_name, task_metrics in tasks_metrics.set_index("Task&Skill").iterrows():
        slug = task_name.lower().replace(" ", "-")
        tasks_result[slug] = TaskResult(
            metrics={
                "accuracy": MetricResult(
                    scores={
                        "accuracy": Score(
                            value=float(task_metrics["acc"]),
                            stats=ScoreStats(
                                count=int(task_metrics["tot"]),
                                sum=float(task_metrics["hit"]),
                            ),
                        )
                    }
                ),
                "prefetch_rate": MetricResult(
                    scores={
                        "prefetch_rate": Score(
                            value=float(task_metrics["prefetch_rate"]),
                            stats=ScoreStats(
                                count=int(task_metrics["tot"]),
                                sum=float(task_metrics["prefetch"]),
                            ),
                        )
                    }
                ),
            }
        )

    return tasks_result, {"mathvista": group_result}


def _parse_ocrbench_output(
    metrics: dict[str, dict[str, float]],
) -> tuple[dict[str, TaskResult], dict[str, GroupResult]]:
    """Parses the output dictionary specific to OCRBench dataset."""
    # Parse the group result
    groups_result = {
        "ocrbench": GroupResult(
            metrics={
                "accuracy": MetricResult(
                    scores={
                        "accuracy": Score(
                            value=float(
                                metrics["Final Score"]["sum"]
                                / metrics["Final Score"]["count"]
                            ),
                            stats=ScoreStats(
                                count=int(metrics["Final Score"]["count"]),
                                sum=float(metrics["Final Score"]["sum"]),
                            ),
                        )
                    }
                )
            },
            groups={
                "text-recognition": GroupResult(
                    metrics={
                        "accuracy": MetricResult(
                            scores={
                                "accuracy": Score(
                                    value=float(
                                        metrics["Text Recognition"]["sum"]
                                        / metrics["Text Recognition"]["count"]
                                    ),
                                    stats=ScoreStats(
                                        count=int(metrics["Text Recognition"]["count"]),
                                        sum=float(metrics["Text Recognition"]["sum"]),
                                    ),
                                )
                            }
                        )
                    }
                )
            },
        )
    }

    # Parse the tasks result
    tasks_result = {}
    for task_name, task_metrics in metrics.items():
        if task_name in ["Final Score", "Final Score Norm", "Text Recognition"]:
            continue
        if task_metrics["count"] == 0:
            # It can happen when we limit the number of samples
            continue
        slug = task_name.lower().replace(" ", "-")
        tasks_result[slug] = TaskResult(
            metrics={
                "accuracy": MetricResult(
                    scores={
                        "accuracy": Score(
                            value=float(task_metrics["sum"] / task_metrics["count"]),
                            stats=ScoreStats(
                                count=int(task_metrics["count"]),
                                sum=float(task_metrics["sum"]),
                            ),
                        )
                    }
                )
            }
        )

    return tasks_result, groups_result


def _parse_slidevqa_output(
    metrics: pd.DataFrame,
) -> tuple[dict[str, TaskResult], dict[str, GroupResult]]:
    """Parses the output DataFrame specific to SlideVQA dataset."""
    # Convert DataFrame to a more accessible format
    metrics_dict = {}
    for _, row in metrics.iterrows():
        metrics_dict[row["category"]] = {
            "count": int(row["num"]),
            "value": float(row["avg"]),
        }

    # Create group result with all three metrics
    group_result = GroupResult(
        metrics={
            "anls": MetricResult(
                scores={
                    "anls": Score(
                        value=metrics_dict["anls"]["value"],
                        stats=ScoreStats(count=metrics_dict["anls"]["count"]),
                    )
                }
            ),
            "exact_match": MetricResult(
                scores={
                    "exact_match": Score(
                        value=metrics_dict["EM"]["value"],
                        stats=ScoreStats(count=metrics_dict["EM"]["count"]),
                    )
                }
            ),
            "f1": MetricResult(
                scores={
                    "f1": Score(
                        value=metrics_dict["F1"]["value"],
                        stats=ScoreStats(count=metrics_dict["F1"]["count"]),
                    )
                }
            ),
        }
    )

    # No task-level results needed for this dataset as these are overall metrics
    tasks_result = {}

    return tasks_result, {"slidevqa": group_result}

def _parse_ocr_reasoning_output(
    metrics: pd.DataFrame,
) -> tuple[dict[str, TaskResult], dict[str, GroupResult]]:
    """Parses the output DataFrame specific to OCR_Reasoning dataset."""

    overall_metrics = metrics[metrics["Task"] == "Overall"].iloc[0]
    group_result = GroupResult(
        metrics={
            "accuracy": MetricResult(
                scores={
                    "accuracy": Score(
                        value=float(overall_metrics["acc"]),
                        stats=ScoreStats(
                            count=int(overall_metrics["tot"]),
                            sum=float(overall_metrics["hit"]),
                        ),
                    )
                }
            ),
            "prefetch_rate": MetricResult(
                scores={
                    "prefetch_rate": Score(
                        value=float(overall_metrics["prefetch_rate"]),
                        stats=ScoreStats(
                            count=int(overall_metrics["tot"]),
                            sum=float(overall_metrics["prefetch"]),
                        ),
                    )
                }
            ),
        }
    )

    tasks_df = metrics[metrics["Task"] != "Overall"]
    tasks_df = tasks_df[~tasks_df["Task"].str.endswith("_RP", na=False)]

    tasks_result = {}
    for task_name, task_metrics in tasks_df.set_index("Task").iterrows():
        slug = task_name.lower().replace(" ", "-").replace("_", "-")
        tasks_result[slug] = TaskResult(
            metrics={
                "accuracy": MetricResult(
                    scores={
                        "accuracy": Score(
                            value=float(task_metrics["acc"]),
                            stats=ScoreStats(
                                count=int(task_metrics["tot"]),
                                sum=float(task_metrics["hit"]),
                            ),
                        )
                    }
                ),
                "prefetch_rate": MetricResult(
                    scores={
                        "prefetch_rate": Score(
                            value=float(task_metrics["prefetch_rate"]),
                            stats=ScoreStats(
                                count=int(task_metrics["tot"]),
                                sum=float(task_metrics["prefetch"]),
                            ),
                        )
                    }
                ),
            }
        )

    groups_result = {"ocr_reasoning": group_result}

    return tasks_result, groups_result