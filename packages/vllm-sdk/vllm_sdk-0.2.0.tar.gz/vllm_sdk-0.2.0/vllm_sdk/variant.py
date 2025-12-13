"""Variant class for model name wrapping with SAE intervention support."""

from typing import List, Literal, Optional, Union

from vllm_sdk.schemas import FeatureItem


class InterventionSpec:
    """Specification for a single SAE feature intervention.

    Attributes:
        index_in_sae: The index in the SAE of the feature to intervene on
        strength: The strength of the intervention (-1.0 to 1.0 or higher depending on the input)
        mode: The intervention mode - "add" (default) or "clamp"
    """

    def __init__(
        self,
        index_in_sae: int,
        strength: float,
        mode: Optional[Literal["add", "clamp"]] = "add",
    ):
        """Initialize an InterventionSpec.

        Args:
            index_in_sae: The SAE feature ID int
            strength: Intervention strength
            mode: "add" to add the intervention, "clamp" to clamp
        """
        self.index_in_sae = index_in_sae
        self.strength = strength
        self.mode = mode

    def to_dict(self) -> dict:
        """Convert to dictionary for API requests."""
        return {
            "index_in_sae": self.index_in_sae,
            "strength": self.strength,
            "mode": self.mode,
        }

    def __repr__(self) -> str:
        """Return string representation."""
        return f"InterventionSpec(index_in_sae={self.index_in_sae}, strength={self.strength}, mode={self.mode!r})"


class Variant:
    """Wrapper class for model names with SAE intervention support.

    Used to pass model identifiers and SAE feature interventions to client methods,
    matching Goodfire's API pattern.

    Example:
        variant = Variant("meta-llama/Llama-3.3-70B-Instruct")
        variant.add_intervention(index_in_sae=28612, strength=0.75)
        client.chat.completions.create(model=variant, messages=[...])
    """

    def __init__(self, model_name: str):
        """Initialize a Variant with a model name.

        Args:
            model_name: The model identifier string (e.g., "meta-llama/Llama-3.3-70B-Instruct")
        """
        self.model_name = model_name
        self.interventions: List[InterventionSpec] = []

    def add_intervention(
        self,
        index_in_sae: int,
        strength: float,
        mode: Optional[Literal["add", "clamp"]] = "add",
    ) -> "Variant":
        """Add a SAE feature intervention to this variant.

        Args:
            index_in_sae: The index in the SAE of the feature to intervene on
            strength: The intervention strength
            mode: "add" (default) or "clamp"

        Returns:
            Self for method chaining
        """
        intervention = InterventionSpec(index_in_sae, strength, mode)
        self.interventions.append(intervention)
        return self

    def add_interventions(self, interventions: List[InterventionSpec]) -> "Variant":
        """Add multiple SAE feature interventions to this variant.

        Args:
            interventions: List of InterventionSpec objects

        Returns:
            Self for method chaining
        """
        self.interventions.extend(interventions)
        return self

    def set(
        self,
        features: Union[List["FeatureItem"], "FeatureItem"],
        strength: float,
        mode: Optional[Literal["add", "clamp"]] = "add",
    ) -> "Variant":
        """Add multiple SAE feature interventions using FeatureItem objects with same strength.
        Args:
            features: List of FeatureItem objects
            strength: The intervention strength (applied to all features)
            mode: "add" (default) or "clamp" (applied to all features)

        Returns:
            Self for method chaining

        Example:
            >>> search_results = client.features.search("humor", model=variant)
            >>> variant.set(search_results.data, strength=0.6)
        """
        if isinstance(features, FeatureItem):
            features = [features]
        for feature in features:
            intervention = InterventionSpec(
                index_in_sae=feature.index_in_sae,
                strength=strength,
                mode=mode,
            )
            self.interventions.append(intervention)
        return self

    def get_interventions(self) -> List[dict]:
        """Get interventions as a list of dictionaries for API requests.

        Returns:
            List of intervention dictionaries
        """
        return [iv.to_dict() for iv in self.interventions]

    def reset(self) -> "Variant":
        """Clear all interventions from this variant.

        Returns:
            Self for method chaining
        """
        self.interventions = []
        return self

    def __str__(self) -> str:
        """Return the model name as a string."""
        return self.model_name

    def __repr__(self) -> str:
        """Return a string representation of the Variant."""
        if self.interventions:
            interventions_str = ", ".join(repr(iv) for iv in self.interventions)
            return f"Variant({self.model_name!r}, interventions=[{interventions_str}])"
        return f"Variant({self.model_name!r})"

    def __eq__(self, other) -> bool:
        """Check equality with another Variant or string."""
        if isinstance(other, Variant):
            return self.model_name == other.model_name
        if isinstance(other, str):
            return self.model_name == other
        return False
