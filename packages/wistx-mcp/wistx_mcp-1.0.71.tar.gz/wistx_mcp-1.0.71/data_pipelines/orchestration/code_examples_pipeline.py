"""Code examples pipeline orchestrator.

Coordinates Collection → Processing → Enrichment → Mapping → Embedding → Loading stages
for code examples.
"""

import logging
import uuid
from typing import Any, AsyncIterator, Callable

from data_pipelines.collectors.github_collector import GitHubCodeExamplesCollector
from data_pipelines.loaders.compliance_mapping_loader import ComplianceMappingLoader
from data_pipelines.loaders.mongodb_loader import MongoDBLoader
from data_pipelines.processors.code_processor import CodeProcessor
from data_pipelines.processors.embedding_generator import EmbeddingGenerator
from data_pipelines.processors.parsers import (
    ArgoCDParser,
    ArgoWorkflowsParser,
    BackstageParser,
    BashParser,
    CDK8sParser,
    CDKParser,
    CircleCIParser,
    CrossplaneParser,
    DatadogParser,
    DockerParser,
    FluxParser,
    GitHubActionsParser,
    GitLabCIParser,
    GrafanaParser,
    HelmParser,
    JenkinsParser,
    KarpenterParser,
    KubernetesParser,
    OpenTelemetryParser,
    PowerShellParser,
    PrometheusParser,
    SAMParser,
    ServerlessParser,
    SpinnakerParser,
    TektonParser,
)
from data_pipelines.processors.parsers.iac import (
    AnsibleParser,
    ARMParser,
    BicepParser,
    CloudFormationParser,
    OpenTofuParser,
    PulumiParser,
    TerraformParser,
)
from data_pipelines.services.code_enrichment_service import CodeEnrichmentService

logger = logging.getLogger(__name__)


class CodeExamplesPipeline:
    """Orchestrates the code examples processing pipeline."""

    def __init__(
        self,
        min_stars: int | None = None,
        max_repos: int | None = None,
        max_files: int | None = None,
        use_paginated_collection: bool | None = None,
        use_streaming_pipeline: bool | None = None,
        enable_checkpointing: bool | None = None,
        collection_batch_size: int | None = None,
        checkpoint_interval: int | None = None,
    ):
        """Initialize code examples pipeline.
        
        Args:
            min_stars: Minimum stars for repositories (overrides settings)
            max_repos: Maximum repositories to process (overrides settings)
            max_files: Maximum files per repository (overrides settings)
            use_paginated_collection: Use paginated collection (default: from settings)
            use_streaming_pipeline: Use streaming pipeline (default: from settings)
            enable_checkpointing: Enable checkpointing (default: from settings)
            collection_batch_size: Batch size for paginated collection (default: from settings)
            checkpoint_interval: Checkpoint save interval (default: from settings)
        """
        from data_pipelines.utils.config import PipelineSettings
        from data_pipelines.utils.pipeline_progress import PipelineProgress
        
        settings = PipelineSettings()
        self.collector = GitHubCodeExamplesCollector(
            github_token=settings.github_internal_token,
            min_stars=min_stars if min_stars is not None else settings.github_min_stars,
            max_repos_per_query=max_repos if max_repos is not None else settings.github_max_repos_per_query,
            max_files_per_repo=max_files if max_files is not None else settings.github_max_files_per_repo,
            max_depth=settings.github_repo_max_depth,
        )
        self.processor = CodeProcessor()
        self.enrichment_service = CodeEnrichmentService()
        self.embedding_generator = EmbeddingGenerator(save_intermediate=False)
        self.mongodb_loader = MongoDBLoader()
        self.mapping_loader = ComplianceMappingLoader(mongodb_loader=self.mongodb_loader)
        
        self.use_paginated_collection = (
            use_paginated_collection
            if use_paginated_collection is not None
            else settings.github_use_paginated_collection
        )
        self.use_streaming_pipeline = (
            use_streaming_pipeline
            if use_streaming_pipeline is not None
            else settings.github_use_streaming_pipeline
        )
        self.enable_checkpointing = (
            enable_checkpointing
            if enable_checkpointing is not None
            else settings.github_enable_checkpointing
        )
        self.collection_batch_size = (
            collection_batch_size
            if collection_batch_size is not None
            else settings.github_collection_batch_size
        )
        self.checkpoint_interval = (
            checkpoint_interval
            if checkpoint_interval is not None
            else settings.github_checkpoint_interval
        )
        
        self.pipeline_progress: PipelineProgress | None = None
        self.pipeline_id: str | None = None
        
        self._progress_callback: Callable[[str, float, dict[str, Any], dict[str, Any]], None] | None = None
        
        self._register_parsers()

    def set_progress_callback(
        self,
        callback: Callable[[str, float, dict[str, Any], dict[str, Any]], None] | None,
    ) -> None:
        """Set progress callback for pipeline updates.
        
        Args:
            callback: Async callback function(stage, progress, stats, stages)
        """
        self._progress_callback = callback

    async def _report_progress(
        self,
        stage: str,
        progress: float,
        stats: dict[str, Any],
        stages: dict[str, Any] | None = None,
    ) -> None:
        """Report progress via callback if set.
        
        Args:
            stage: Current stage name
            progress: Overall progress (0.0-1.0)
            stats: Pipeline statistics
            stages: Stage progress information
        """
        if self._progress_callback:
            try:
                await self._progress_callback(stage, progress, stats, stages or {})
            except Exception as e:
                logger.warning("Progress callback failed: %s", e)

    def _register_parsers(self) -> None:
        """Register all parsers with the code processor."""
        parsers = {
            "terraform": TerraformParser(),
            "opentofu": OpenTofuParser(),
            "pulumi": PulumiParser(),
            "ansible": AnsibleParser(),
            "cloudformation": CloudFormationParser(),
            "bicep": BicepParser(),
            "arm": ARMParser(),
            "cdk": CDKParser(),
            "cdk8s": CDK8sParser(),
            "github_actions": GitHubActionsParser(),
            "gitlab_ci": GitLabCIParser(),
            "jenkins": JenkinsParser(),
            "circleci": CircleCIParser(),
            "argo_workflows": ArgoWorkflowsParser(),
            "tekton": TektonParser(),
            "argocd": ArgoCDParser(),
            "flux": FluxParser(),
            "spinnaker": SpinnakerParser(),
            "kubernetes": KubernetesParser(),
            "docker": DockerParser(),
            "helm": HelmParser(),
            "prometheus": PrometheusParser(),
            "grafana": GrafanaParser(),
            "datadog": DatadogParser(),
            "opentelemetry": OpenTelemetryParser(),
            "crossplane": CrossplaneParser(),
            "karpenter": KarpenterParser(),
            "backstage": BackstageParser(),
            "sam": SAMParser(),
            "serverless": ServerlessParser(),
            "bash": BashParser(),
            "powershell": PowerShellParser(),
        }
        
        for code_type, parser in parsers.items():
            self.processor.register_parser(code_type, parser)

    async def run_pipeline(
        self,
        max_examples: int | None = None,
        pipeline_id: str | None = None,
        resume_from_checkpoint: bool = False,
    ) -> dict[str, Any]:
        """Run the complete code examples pipeline.
        
        Args:
            max_examples: Maximum number of examples to process (None for all)
            pipeline_id: Unique pipeline identifier for checkpointing (auto-generated if None)
            resume_from_checkpoint: If True, attempt to resume from latest checkpoint
            
        Returns:
            Pipeline execution results
        """
        logger.info("Starting code examples pipeline...")
        logger.info("Paginated collection: %s", self.use_paginated_collection)
        logger.info("Streaming pipeline: %s", self.use_streaming_pipeline)
        logger.info("Checkpointing: %s", self.enable_checkpointing)
        
        if pipeline_id is None:
            pipeline_id = f"code-examples-{uuid.uuid4().hex[:8]}"
        self.pipeline_id = pipeline_id
        
        if self.enable_checkpointing:
            from data_pipelines.utils.pipeline_progress import PipelineProgress
            self.pipeline_progress = PipelineProgress(pipeline_id, collection_name="code_examples_pipeline_progress")
            logger.info("Pipeline ID: %s (checkpointing enabled)", pipeline_id)
            
            if resume_from_checkpoint:
                latest_checkpoint = await self.pipeline_progress.get_latest_checkpoint()
                if latest_checkpoint:
                    logger.info(
                        "Resuming from checkpoint: stage=%s, timestamp=%s",
                        latest_checkpoint.get("stage"),
                        latest_checkpoint.get("timestamp")
                    )
        
        if self.use_paginated_collection and self.use_streaming_pipeline:
            return await self._run_streaming_pipeline(max_examples=max_examples)
        else:
            return await self._run_legacy_pipeline(max_examples=max_examples)
    
    async def _run_legacy_pipeline(
        self,
        max_examples: int | None = None,
    ) -> dict[str, Any]:
        """Run pipeline in legacy mode (backward compatibility).
        
        Args:
            max_examples: Maximum number of examples to process (None for all)
            
        Returns:
            Pipeline execution results
        """
        logger.info("Running pipeline in legacy mode (non-streaming)")
        
        results = {
            "collected": 0,
            "processed": 0,
            "enriched": 0,
            "mappings_generated": 0,
            "mappings_loaded": 0,
            "embeddings_generated": 0,
            "loaded_to_mongodb": 0,
            "errors": [],
        }
        
        try:
            await self._report_progress("collection", 0.0, results, {"collection": {"status": "running", "items_processed": 0}})
            
            collection_result = await self.collector.collect(max_examples=max_examples)
            results["collected"] = len(collection_result.items)
            
            logger.info("Collected %d code examples", results["collected"])
            
            await self._report_progress("collection", 0.2, results, {"collection": {"status": "completed", "items_processed": results["collected"]}})
            
            processed_examples = []
            
            for raw_example in collection_result.items:
                if max_examples and len(processed_examples) >= max_examples:
                    break
                
                try:
                    processed = self.processor.process_raw_data(raw_example)
                    processed_examples.append(processed)
                    results["processed"] += 1
                except Exception as e:
                    logger.warning("Failed to process example: %s", e)
                    results["errors"].append({"stage": "processing", "error": str(e)})
                    continue
            
            logger.info("Processed %d code examples", results["processed"])
            
            await self._report_progress("processing", 0.4, results, {
                "collection": {"status": "completed", "items_processed": results["collected"]},
                "processing": {"status": "completed", "items_processed": results["processed"]},
            })
            
            enriched_examples = []
            all_mappings = []
            
            for processed in processed_examples:
                try:
                    enriched = await self.enrichment_service.enrich_code_example(
                        processed=processed,
                        generate_mappings=True,
                    )
                    enriched_examples.append(enriched)
                    results["enriched"] += 1
                    
                    mappings = enriched.get("compliance_mappings", [])
                    if mappings:
                        from data_pipelines.models.compliance_mapping import ComplianceMapping
                        
                        mapping_objects = [
                            ComplianceMapping(**mapping) for mapping in mappings
                        ]
                        all_mappings.extend(mapping_objects)
                        results["mappings_generated"] += len(mapping_objects)
                
                except Exception as e:
                    logger.warning("Failed to enrich example: %s", e)
                    results["errors"].append({"stage": "enrichment", "error": str(e)})
                    continue
            
            logger.info("Enriched %d code examples", results["enriched"])
            logger.info("Generated %d compliance mappings", results["mappings_generated"])
            
            await self._report_progress("enrichment", 0.6, results, {
                "collection": {"status": "completed", "items_processed": results["collected"]},
                "processing": {"status": "completed", "items_processed": results["processed"]},
                "enrichment": {"status": "completed", "items_processed": results["enriched"]},
            })
            
            if all_mappings:
                try:
                    mapping_stats = self.mapping_loader.load_mappings(all_mappings)
                    results["mappings_loaded"] = mapping_stats.get("inserted", 0) + mapping_stats.get("updated", 0)
                    logger.info("Loaded %d compliance mappings to MongoDB", results["mappings_loaded"])
                except Exception as e:
                    logger.error("Failed to load compliance mappings: %s", e)
                    results["errors"].append({"stage": "mapping_loading", "error": str(e)})
            
            examples_with_embeddings = []
            
            logger.info("Generating embeddings for %d enriched examples...", len(enriched_examples))
            
            try:
                items_with_embeddings, failed_items = await self.embedding_generator.generate_embeddings(
                    items=enriched_examples,
                    data_type="code",
                )
                
                examples_with_embeddings = items_with_embeddings
                results["embeddings_generated"] = len(items_with_embeddings)
                
                await self._report_progress("embedding", 0.8, results, {
                    "collection": {"status": "completed", "items_processed": results["collected"]},
                    "processing": {"status": "completed", "items_processed": results["processed"]},
                    "enrichment": {"status": "completed", "items_processed": results["enriched"]},
                    "embedding": {"status": "completed", "items_processed": results["embeddings_generated"]},
                })
                
                if failed_items:
                    logger.warning("Failed to generate embeddings for %d examples", len(failed_items))
                    results["errors"].extend([
                        {"stage": "embedding", "error": failed.get("error", "Unknown error")}
                        for failed in failed_items
                    ])
            
            except Exception as e:
                logger.error("Error generating embeddings: %s", e)
                results["errors"].append({"stage": "embedding", "error": str(e)})
            
            logger.info("Generated %d embeddings", results["embeddings_generated"])
            
            if examples_with_embeddings:
                try:
                    self.mongodb_loader.load_code_examples(examples_with_embeddings)
                    results["loaded_to_mongodb"] = len(examples_with_embeddings)
                    logger.info("Loaded %d code examples to MongoDB and Pinecone", results["loaded_to_mongodb"])
                    
                    await self._report_progress("loading", 1.0, results, {
                        "collection": {"status": "completed", "items_processed": results["collected"]},
                        "processing": {"status": "completed", "items_processed": results["processed"]},
                        "enrichment": {"status": "completed", "items_processed": results["enriched"]},
                        "embedding": {"status": "completed", "items_processed": results["embeddings_generated"]},
                        "loading": {"status": "completed", "items_processed": results["loaded_to_mongodb"]},
                    })
                except Exception as e:
                    logger.error("Failed to load code examples: %s", e)
                    results["errors"].append({"stage": "loading", "error": str(e)})
        
        except Exception as e:
            logger.error("Pipeline execution failed: %s", e, exc_info=True)
            results["errors"].append({"stage": "pipeline", "error": str(e)})
        
        logger.info("Pipeline complete: %d examples processed, %d errors", results["processed"], len(results["errors"]))
        
        return results
    
    async def _run_streaming_pipeline(
        self,
        max_examples: int | None = None,
    ) -> dict[str, Any]:
        """Run pipeline with streaming processing (memory-efficient).
        
        Processes batches as collected: Collect → Process → Enrich → Map → Embed → Load
        
        Args:
            max_examples: Maximum number of examples to process (None for all)
            
        Returns:
            Pipeline execution results
        """
        logger.info("Running streaming pipeline (memory-efficient)")
        
        results = {
            "collected": 0,
            "processed": 0,
            "enriched": 0,
            "mappings_generated": 0,
            "mappings_loaded": 0,
            "embeddings_generated": 0,
            "loaded_to_mongodb": 0,
            "errors": [],
        }
        
        try:
            await self._report_progress("collection", 0.0, results, {"collection": {"status": "running", "items_processed": 0}})
            
            total_processed = 0
            
            async for batch_examples in self.collector.collect_paginated(
                batch_size=self.collection_batch_size,
                max_examples=max_examples,
            ):
                batch_size = len(batch_examples)
                results["collected"] += batch_size
                
                logger.info(
                    "Processing batch: %d examples (total collected: %d/%s)",
                    batch_size,
                    results["collected"],
                    max_examples if max_examples else "unlimited"
                )
                
                processed_batch = []
                for raw_example in batch_examples:
                    if max_examples and total_processed >= max_examples:
                        break
                    
                    try:
                        processed = self.processor.process_raw_data(raw_example)
                        processed_batch.append(processed)
                        results["processed"] += 1
                        total_processed += 1
                    except Exception as e:
                        logger.warning("Failed to process example: %s", e)
                        results["errors"].append({"stage": "processing", "error": str(e)})
                        continue
                
                enriched_batch = []
                mappings_batch = []
                
                for processed in processed_batch:
                    if max_examples and total_processed >= max_examples:
                        break
                    
                    try:
                        enriched = await self.enrichment_service.enrich_code_example(
                            processed=processed,
                            generate_mappings=True,
                        )
                        enriched_batch.append(enriched)
                        results["enriched"] += 1
                        
                        mappings = enriched.get("compliance_mappings", [])
                        if mappings:
                            from data_pipelines.models.compliance_mapping import ComplianceMapping
                            
                            mapping_objects = [
                                ComplianceMapping(**mapping) for mapping in mappings
                            ]
                            mappings_batch.extend(mapping_objects)
                            results["mappings_generated"] += len(mapping_objects)
                    
                    except Exception as e:
                        logger.warning("Failed to enrich example: %s", e)
                        results["errors"].append({"stage": "enrichment", "error": str(e)})
                        continue
                
                if mappings_batch:
                    try:
                        mapping_stats = self.mapping_loader.load_mappings(mappings_batch)
                        results["mappings_loaded"] += mapping_stats.get("inserted", 0) + mapping_stats.get("updated", 0)
                    except Exception as e:
                        logger.error("Failed to load compliance mappings: %s", e)
                        results["errors"].append({"stage": "mapping_loading", "error": str(e)})
                
                if enriched_batch:
                    try:
                        items_with_embeddings, failed_items = await self.embedding_generator.generate_embeddings(
                            items=enriched_batch,
                            data_type="code",
                        )
                        
                        results["embeddings_generated"] += len(items_with_embeddings)
                        
                        if failed_items:
                            results["errors"].extend([
                                {"stage": "embedding", "error": failed.get("error", "Unknown error")}
                                for failed in failed_items
                            ])
                        
                        if items_with_embeddings:
                            self.mongodb_loader.load_code_examples(items_with_embeddings)
                            results["loaded_to_mongodb"] += len(items_with_embeddings)
                    
                    except Exception as e:
                        logger.error("Error generating embeddings: %s", e)
                        results["errors"].append({"stage": "embedding", "error": str(e)})
                
                if self.enable_checkpointing and self.pipeline_progress:
                    if total_processed % self.checkpoint_interval == 0:
                        await self.pipeline_progress.save_checkpoint(
                            stage="processing",
                            stats=results.copy(),
                            metadata={"total_processed": total_processed},
                        )
                        logger.debug("Checkpoint saved: %d examples processed", total_processed)
                
                await self._report_progress(
                    "processing",
                    min(0.9, total_processed / max_examples) if max_examples else 0.5,
                    results,
                    {
                        "collection": {"status": "completed", "items_processed": results["collected"]},
                        "processing": {"status": "running", "items_processed": total_processed},
                    }
                )
                
                if max_examples and total_processed >= max_examples:
                    logger.info("Reached max_examples limit (%d), stopping pipeline", max_examples)
                    break
            
            if self.enable_checkpointing and self.pipeline_progress:
                await self.pipeline_progress.save_checkpoint(
                    stage="completed",
                    stats=results.copy(),
                    metadata={"total_processed": total_processed},
                )
                logger.info("Final checkpoint saved")
            
            await self._report_progress("loading", 1.0, results, {
                "collection": {"status": "completed", "items_processed": results["collected"]},
                "processing": {"status": "completed", "items_processed": results["processed"]},
                "enrichment": {"status": "completed", "items_processed": results["enriched"]},
                "embedding": {"status": "completed", "items_processed": results["embeddings_generated"]},
                "loading": {"status": "completed", "items_processed": results["loaded_to_mongodb"]},
            })
        
        except Exception as e:
            logger.error("Pipeline execution failed: %s", e, exc_info=True)
            results["errors"].append({"stage": "pipeline", "error": str(e)})
            
            if self.enable_checkpointing and self.pipeline_progress:
                await self.pipeline_progress.save_checkpoint(
                    stage="failed",
                    stats=results.copy(),
                    metadata={"error": str(e)},
                )
        
        logger.info("Pipeline complete: %d examples processed, %d errors", results["processed"], len(results["errors"]))
        
        return results

