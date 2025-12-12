"""MathTheory Package - Level 1 (25 Principles)"""

from .core_principles import (
    MathTheoryPrinciple,
    ActionMinimizer
)
from .hamiltonian import (
    HamiltonianNetwork,
    ConservationLawConstraints,
    PhysicsInformedTensorNetwork
)
from .entropy import (
    EntropyPrinciple,
    BoltzmannMachine,
    RestrictedBoltzmannMachine,
    DeepBoltzmannMachine,
    EntropyRegularizedNetwork
)
from .symmetry import (
    EquivariantTensorNetwork,
    EquivariantLinear,
    ClebschGordanCoefficients,
    InvariantFeatureExtractor,
    TensorFieldCNN
)
from .variational import (
    VariationalInferenceSystem,
    StochasticActionMinimizer,
    InformationBottleneck,
    HighDimensionalActionMinimizer,
    MultiScaleActionMinimizer,
    EntropyMaximizationRL
)
from .covariance import (
    CovariancePrinciple,
    TensorNetwork,
    LocalityPrinciple,
    LocalityCNN
)
from .invariance import (
    GroupTheory,
    InvarianceLayer,
    EquivariantLayer,
    GroupInvariantNetwork,
    DeepSets
)
from .mdl import (
    MDLPrinciple,
    BayesianInformationCriterion,
    AkaikeInformationCriterion,
    CompressiveNeuralNetwork,
    MDLRegularizer
)
from .homeostasis import (
    HomeostaticSystem,
    HomeostaticPotential,
    HomeostaticNeuron,
    HomeostaticRNN,
    HomeostaticOptimizer,
    AdaptiveHomeostasis
)
from .duality import (
    DualityPrinciple,
    FourierFeatureLayer,
    SpectralConvolution,
    SpectralPooling1D,
    FourierNeuralNetwork,
    WaveletLayer,
    WaveletFilter,
    FrequencyDomainAttention,
    HarmonicAnalysis
)
from .self_similarity import (
    SelfSimilarityPrinciple,
    RenormalizationGroup,
    ScaleInvariantCNN,
    ScaleInvariantConv2d,
    ScaleAdaptiveNorm,
    MultiScaleAggregation,
    ScaleAttention,
    FractalNetwork,
    FractalBlock,
    PowerLawRegularizer,
    MultiFractalAnalysis
)
from .evolution import (
    EvolutionaryOptimizer,
    AdaptiveEvolutionaryStrategy,
    EvolutionaryNeuralNetwork,
    DifferentialEvolution
)
from .gestalt import (
    GestaltAttention,
    MultiHeadAttention,
    SelfAttention,
    CrossAttention,
    PositionalEncoding,
    CausalSelfAttention,
    AttentionVisualization,
    GestaltTransformer
)
from .golden_ratio import (
    PHI,
    GoldenRatio,
    FibonacciSequence,
    GoldenSectionSearch,
    Phyllotaxis,
    GoldenRectangle,
    PhiProportionedNetwork,
    GoldenMeanOptimizer
)
from .cognitive_economy import (
    InformationBottleneck,
    MinimalDescriptionLength,
    OccamsRazorNetwork,
    FeatureSelection
)
from .dependent_emergence import (
    MessagePassingLayer,
    GraphConvolutionalLayer,
    GraphAttentionLayer,
    GraphPooling,
    GraphNeuralNetwork,
    EdgeNetwork,
    DynamicGraph,
    HypergraphConvolution
)
from .resilience import (
    ResilientDynamics,
    AdversarialRobustness,
    SelfHealingNetwork,
    AntiFragileOptimizer,
    CatastrophicForgettingDefense,
    GracefulDegradation
)

from .hierarchy import (
    HierarchicalEncoder,
    UNetArchitecture,
    FeaturePyramidNetwork,
    HierarchicalSoftmax,
    MultiScaleConvolution,
    RecursiveNetwork,
    AttentionHierarchy,
    HierarchicalVAE,
    TreeLSTM
)

from .stability import (
    LyapunovStabilizedNetwork,
    AttractorDynamics,
    StableOptimizer,
    EquilibriumFinder,
    StabilityAnalyzer,
    RobustStability,
    AdaptiveStabilization,
    PhasePortrait
)

from .compositionality import (
    FunctionalComposition,
    TreeStructuredComposition,
    ModularComposition,
    TensorComposition,
    PrimitiveComposition,
    HierarchicalComposition,
    SymbolicComposition,
    CompositeAttention,
    RecursiveComposition,
    CompositionLoss
)

from .causality import (
    StructuralCausalModel,
    InterventionNetwork,
    CounterfactualReasoning,
    CausalGraphLearning,
    InstrumentalVariable,
    DoCalculus,
    CausalAttention,
    TreatmentEffectEstimator
)

from .parsimony import (
    MinimumDescriptionLengthLoss,
    BayesianInformationCriterion,
    AkaikeInformationCriterion,
    StructuralRiskMinimization,
    MinimalAssumptionNetwork,
    SparseCoding,
    PrincipleOfParsimony,
    EarlyStoppingWithParsimony,
    BiasVarianceTradeoff,
    RegularizationScheduler
)

from .modularity import (
    ModularNetwork,
    ExpertMixtureNetwork,
    PluginArchitecture,
    DecoupledRepresentation,
    InterfaceAbstraction,
    LooseCouplingLoss,
    HierarchicalModularity,
    DynamicModuleSelection,
    CrossModuleCommunication,
    ModularityMetrics
)

from .transferability import (
    DomainAdversarialNetwork,
    GradientReversal,
    MaximumMeanDiscrepancy,
    FineTuningStrategy,
    AdapterLayers,
    MetaLearning,
    DomainInvariantFeatures,
    ZeroShotTransfer,
    ContinualLearning,
    FewShotLearning
)

from .interpretability import (
    SaliencyMap,
    GradCAM,
    IntegratedGradients,
    AttentionVisualization,
    FeatureVisualization,
    ConceptActivationVector,
    LocalInterpretableModelExplanations,
    ShapleyValues
)

from .universality import (
    PowerLawScaling,
    NeuralScalingLaw,
    CriticalPhenomena,
    RenormalizationGroup,
    UniversalApproximation,
    ScaleFreeNetwork,
    CentralLimitTheorem,
    EdgeOfChaos,
    UniversalComputationModel
)
from .gestalt import (
    GoldenAttention,
    GestaltAttention,
    MultiHeadAttention,
    SelfAttention,
    CrossAttention,
    PositionalEncoding,
    CausalSelfAttention,
    AttentionVisualization,
    GestaltTransformer
)

__all__ = [
    'MathTheoryPrinciple',
    'ActionMinimizer',
    'HamiltonianNetwork',
    'ConservationLawConstraints',
    'PhysicsInformedTensorNetwork',
    'EntropyPrinciple',
    'BoltzmannMachine',
    'RestrictedBoltzmannMachine',
    'DeepBoltzmannMachine',
    'EntropyRegularizedNetwork',
    'EquivariantTensorNetwork',
    'EquivariantLinear',
    'ClebschGordanCoefficients',
    'InvariantFeatureExtractor',
    'TensorFieldCNN',
    'VariationalInferenceSystem',
    'StochasticActionMinimizer',
    'InformationBottleneck',
    'HighDimensionalActionMinimizer',
    'MultiScaleActionMinimizer',
    'EntropyMaximizationRL',
    'CovariancePrinciple',
    'TensorNetwork',
    'LocalityPrinciple',
    'LocalityCNN',
    'GroupTheory',
    'InvarianceLayer',
    'EquivariantLayer',
    'GroupInvariantNetwork',
    'DeepSets',
    'MDLPrinciple',
    'BayesianInformationCriterion',
    'AkaikeInformationCriterion',
    'CompressiveNeuralNetwork',
    'MDLRegularizer',
    # Homeostasis (6 classes)
    'HomeostaticSystem',
    'HomeostaticPotential',
    'HomeostaticNeuron',
    'HomeostaticRNN',
    'HomeostaticOptimizer',
    'AdaptiveHomeostasis',
    # Duality (9 classes)
    'DualityPrinciple',
    'FourierFeatureLayer',
    'SpectralConvolution',
    'SpectralPooling1D',
    'FourierNeuralNetwork',
    'WaveletLayer',
    'WaveletFilter',
    'FrequencyDomainAttention',
    'HarmonicAnalysis',
    # Self-Similarity (11 classes)
    'SelfSimilarityPrinciple',
    'RenormalizationGroup',
    'ScaleInvariantCNN',
    'ScaleInvariantConv2d',
    'ScaleAdaptiveNorm',
    'MultiScaleAggregation',
    'ScaleAttention',
    'FractalNetwork',
    'FractalBlock',
    'PowerLawRegularizer',
    'MultiFractalAnalysis',
    # Evolution (4 classes)
    'EvolutionaryOptimizer',
    'AdaptiveEvolutionaryStrategy',
    'EvolutionaryNeuralNetwork',
    'DifferentialEvolution',
    # Gestalt (8 classes)
    'GestaltAttention',
    'MultiHeadAttention',
    'SelfAttention',
    'CrossAttention',
    'PositionalEncoding',
    'CausalSelfAttention',
    'AttentionVisualization',
    'GestaltTransformer',
    # Golden Ratio (8 classes + constant)
    'PHI',
    'GoldenRatio',
    'FibonacciSequence',
    'GoldenSectionSearch',
    'Phyllotaxis',
    'GoldenRectangle',
    'PhiProportionedNetwork',
    'GoldenMeanOptimizer',
    # Gestalt (9 classes + PHI constant)
    'GoldenAttention',
    'GestaltAttention',
    'MultiHeadAttention',
    'SelfAttention',
    'CrossAttention',
    'PositionalEncoding',
    'CausalSelfAttention',
    'AttentionVisualization',
    'GestaltTransformer',
]
