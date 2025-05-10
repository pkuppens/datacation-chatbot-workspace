"""Knowledge management for the Titanic dataset analysis."""

import json
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import List, Optional


@dataclass
class DataInsight:
    """A single insight about the data."""

    timestamp: str
    category: str  # e.g., "data_structure", "pattern", "edge_case"
    description: str
    evidence: str  # Code or data that supports the insight
    confidence: float  # 0.0 to 1.0
    source: str  # e.g., "direct_analysis", "user_feedback"


@dataclass
class AnalysisStep:
    """A step in the analysis process."""

    timestamp: str
    question: str
    approach: str
    code: str
    result: str
    insights: List[DataInsight]


class KnowledgeBase:
    """Manages knowledge about the Titanic dataset."""

    def __init__(self, knowledge_dir: Path = Path("knowledge")):
        """Initialize the knowledge base.

        Args:
            knowledge_dir: Directory to store knowledge files
        """
        self.knowledge_dir = knowledge_dir
        self.knowledge_dir.mkdir(parents=True, exist_ok=True)
        self.insights_file = knowledge_dir / "insights.json"
        self.analysis_file = knowledge_dir / "analysis_history.json"
        self._load_knowledge()

    def _load_knowledge(self) -> None:
        """Load existing knowledge from files."""
        self.insights: List[DataInsight] = []
        self.analysis_history: List[AnalysisStep] = []

        if self.insights_file.exists():
            with open(self.insights_file) as f:
                data = json.load(f)
                self.insights = [DataInsight(**item) for item in data]

        if self.analysis_file.exists():
            with open(self.analysis_file) as f:
                data = json.load(f)
                self.analysis_history = [AnalysisStep(**item) for item in data]

    def _save_knowledge(self) -> None:
        """Save knowledge to files."""
        with open(self.insights_file, "w") as f:
            json.dump([asdict(insight) for insight in self.insights], f, indent=2)

        with open(self.analysis_file, "w") as f:
            json.dump([asdict(step) for step in self.analysis_history], f, indent=2)

    def add_insight(self, insight: DataInsight) -> None:
        """Add a new insight to the knowledge base.

        Args:
            insight: The insight to add
        """
        self.insights.append(insight)
        self._save_knowledge()

    def record_analysis(self, step: AnalysisStep) -> None:
        """Record an analysis step.

        Args:
            step: The analysis step to record
        """
        self.analysis_history.append(step)
        self._save_knowledge()

    def get_relevant_insights(self, question: str) -> List[DataInsight]:
        """Get insights relevant to a question.

        Args:
            question: The question to find relevant insights for

        Returns:
            List of relevant insights
        """
        # TODO: Implement semantic search for insights
        return self.insights

    def get_similar_analyses(self, question: str) -> List[AnalysisStep]:
        """Get similar past analyses.

        Args:
            question: The question to find similar analyses for

        Returns:
            List of similar analyses
        """
        # TODO: Implement semantic search for analyses
        return self.analysis_history


# Create global knowledge base instance
knowledge_base = KnowledgeBase()
