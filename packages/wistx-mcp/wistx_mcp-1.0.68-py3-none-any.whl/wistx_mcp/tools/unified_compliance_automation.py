"""Unified compliance automation tool - consolidates CI/CD gates, audit sampling, and workpaper generation.

This module provides a single MCP tool interface for compliance automation:
- generate_cicd_gate: Generate CI/CD compliance gate configurations
- calculate_sample: Calculate audit sample sizes (MUS, attribute)
- select_sample: Select sample items from a population
- generate_workpaper: Generate individual audit workpapers
- generate_workpaper_package: Generate complete workpaper packages

Usage:
    # Generate CI/CD compliance gate
    result = await wistx_compliance_automation(
        action="generate_cicd_gate",
        platform="github_actions",
        frameworks=["SOC2", "PCI-DSS"],
        gate_mode="blocking"
    )

    # Calculate audit sample size
    result = await wistx_compliance_automation(
        action="calculate_sample",
        sampling_method="mus",
        population_size=5000,
        population_value=10000000.0,
        tolerable_misstatement=100000.0
    )
"""

import logging
from datetime import datetime
from typing import Any

logger = logging.getLogger(__name__)

# Valid actions
CICD_ACTIONS = ["generate_cicd_gate", "generate_pre_commit"]
SAMPLING_ACTIONS = ["calculate_sample", "select_sample", "evaluate_sample"]
WORKPAPER_ACTIONS = ["generate_workpaper", "generate_workpaper_package"]

ALL_VALID_ACTIONS = CICD_ACTIONS + SAMPLING_ACTIONS + WORKPAPER_ACTIONS


async def wistx_compliance_automation(
    # REQUIRED
    action: str,

    # === CI/CD GATE PARAMETERS ===
    platform: str | None = None,  # github_actions, gitlab_ci, azure_devops, jenkins, bitbucket, circleci
    frameworks: list[str] | None = None,  # SOC2, PCI-DSS, HIPAA, etc.
    gate_mode: str = "blocking",  # blocking, warning, audit
    min_compliance_score: float = 85.0,
    max_critical_findings: int = 0,
    max_high_findings: int = 3,
    fail_on_high: bool = True,
    scan_paths: list[str] | None = None,
    exclude_paths: list[str] | None = None,
    custom_rules: list[dict] | None = None,

    # === SAMPLING PARAMETERS ===
    sampling_method: str | None = None,  # mus, attribute, haphazard
    population_size: int | None = None,
    population_value: float | None = None,
    tolerable_misstatement: float | None = None,
    tolerable_rate: float | None = None,
    expected_rate: float | None = None,
    confidence_level: float = 0.95,
    risk_level: str = "moderate",  # low, moderate, high
    population_items: list[dict] | None = None,  # For select_sample
    value_field: str = "value",
    id_field: str = "id",
    sample_size: int | None = None,  # For haphazard sampling

    # === WORKPAPER PARAMETERS ===
    engagement_name: str | None = None,
    period_start: str | None = None,  # ISO date string
    period_end: str | None = None,  # ISO date string
    preparer: str | None = None,
    workpaper_type: str | None = None,  # control_testing, sampling, evidence_collection, summary
    control_id: str | None = None,
    control_description: str | None = None,
    testing_procedures: list[str] | None = None,
    sample_items: list[dict] | None = None,
    exceptions: list[dict] | None = None,
    conclusion: str | None = None,
    evidence_items: list[dict] | None = None,
    source_description: str | None = None,
    collection_method: str | None = None,
    findings: list[dict] | None = None,
    overall_conclusion: str | None = None,
    controls_tested: list[dict] | None = None,
    sample_results: list[dict] | None = None,
    evidence_collections: list[dict] | None = None,
    output_format: str = "markdown",  # markdown, json
) -> dict[str, Any]:
    """Unified compliance automation tool.

    Args:
        action: Action to perform (generate_cicd_gate, calculate_sample, etc.)
        ... (see parameter groups above)

    Returns:
        dict with action-specific results
    """
    if action not in ALL_VALID_ACTIONS:
        return {
            "success": False,
            "error": f"Invalid action: {action}. Valid actions: {ALL_VALID_ACTIONS}",
        }

    try:
        if action in CICD_ACTIONS:
            return await _handle_cicd_action(
                action=action,
                platform=platform,
                frameworks=frameworks or ["SOC2"],
                gate_mode=gate_mode,
                min_compliance_score=min_compliance_score,
                max_critical_findings=max_critical_findings,
                max_high_findings=max_high_findings,
                fail_on_high=fail_on_high,
                scan_paths=scan_paths,
                exclude_paths=exclude_paths,
                custom_rules=custom_rules,
            )
        elif action in SAMPLING_ACTIONS:
            return await _handle_sampling_action(
                action=action,
                sampling_method=sampling_method,
                population_size=population_size,
                population_value=population_value,
                tolerable_misstatement=tolerable_misstatement,
                tolerable_rate=tolerable_rate,
                expected_rate=expected_rate,
                confidence_level=confidence_level,
                risk_level=risk_level,
                population_items=population_items,
                value_field=value_field,
                id_field=id_field,
                sample_size=sample_size,
            )
        elif action in WORKPAPER_ACTIONS:
            return await _handle_workpaper_action(
                action=action,
                engagement_name=engagement_name,
                period_start=period_start,
                period_end=period_end,
                preparer=preparer,
                workpaper_type=workpaper_type,
                control_id=control_id,
                control_description=control_description,
                testing_procedures=testing_procedures,
                sample_items=sample_items,
                exceptions=exceptions,
                conclusion=conclusion,
                evidence_items=evidence_items,
                source_description=source_description,
                collection_method=collection_method,
                findings=findings,
                overall_conclusion=overall_conclusion,
                controls_tested=controls_tested,
                sample_results=sample_results,
                evidence_collections=evidence_collections,
                output_format=output_format,
            )
    except Exception as e:
        logger.exception("Error in wistx_compliance_automation: %s", e)
        return {"success": False, "error": str(e)}

    return {"success": False, "error": f"Unhandled action: {action}"}


async def _handle_cicd_action(
    action: str,
    platform: str | None,
    frameworks: list[str],
    gate_mode: str,
    min_compliance_score: float,
    max_critical_findings: int,
    max_high_findings: int,
    fail_on_high: bool,
    scan_paths: list[str] | None,
    exclude_paths: list[str] | None,
    custom_rules: list[dict] | None,
) -> dict[str, Any]:
    """Handle CI/CD gate generation actions."""
    from wistx_mcp.tools.lib.cicd_compliance_gate import (
        CICDComplianceGateGenerator,
        ComplianceGateConfig,
        CICDPlatform,
        GateMode,
    )

    # Map string to enum
    mode_map = {"blocking": GateMode.BLOCKING, "warning": GateMode.WARNING, "audit": GateMode.AUDIT}
    gate_mode_enum = mode_map.get(gate_mode.lower(), GateMode.BLOCKING)

    config = ComplianceGateConfig(
        mode=gate_mode_enum,
        frameworks=frameworks,
        min_compliance_score=min_compliance_score,
        max_critical_findings=max_critical_findings,
        max_high_findings=max_high_findings,
    )

    generator = CICDComplianceGateGenerator(config)

    if action == "generate_pre_commit":
        result = generator.generate_pre_commit_hooks()
        return {
            "success": True,
            "action": action,
            "files": result.get("files", {}),
            "instructions": result.get("instructions", ""),
        }

    # generate_cicd_gate
    if not platform:
        # Generate for all platforms
        result = generator.generate_all()
        return {
            "success": True,
            "action": action,
            "platforms": result.get("platforms", {}),
            "pre_commit": result.get("pre_commit", {}),
            "summary": f"Generated compliance gates for {len(result.get('platforms', {}))} platforms",
        }

    # Map platform string to enum
    platform_map = {
        "github_actions": CICDPlatform.GITHUB_ACTIONS,
        "gitlab_ci": CICDPlatform.GITLAB_CI,
        "azure_devops": CICDPlatform.AZURE_DEVOPS,
        "jenkins": CICDPlatform.JENKINS,
        "bitbucket": CICDPlatform.BITBUCKET,
        "circleci": CICDPlatform.CIRCLECI,
    }

    platform_enum = platform_map.get(platform.lower())
    if not platform_enum:
        return {
            "success": False,
            "error": f"Invalid platform: {platform}. Valid: {list(platform_map.keys())}",
        }

    result = generator.generate(platform_enum)
    return {
        "success": True,
        "action": action,
        "platform": platform,
        "files": result.get("files", {}),
        "config": result.get("config", {}),
        "instructions": result.get("instructions", ""),
    }



async def _handle_sampling_action(
    action: str,
    sampling_method: str | None,
    population_size: int | None,
    population_value: float | None,
    tolerable_misstatement: float | None,
    tolerable_rate: float | None,
    expected_rate: float | None,
    confidence_level: float,
    risk_level: str,
    population_items: list[dict] | None,
    value_field: str,
    id_field: str,
    sample_size: int | None,
) -> dict[str, Any]:
    """Handle audit sampling actions."""
    from wistx_mcp.tools.lib.audit_sampling import (
        AuditSamplingCalculator,
        AuditSampler,
        SamplingParameters,
        SamplingMethod,
        RiskLevel,
    )

    # Map risk level
    risk_map = {"low": RiskLevel.LOW, "moderate": RiskLevel.MODERATE, "high": RiskLevel.HIGH}
    risk_enum = risk_map.get(risk_level.lower(), RiskLevel.MODERATE)

    if action == "calculate_sample":
        if not sampling_method:
            return {"success": False, "error": "sampling_method is required (mus, attribute)"}

        if sampling_method.lower() == "mus":
            if not all([population_size, population_value, tolerable_misstatement]):
                return {
                    "success": False,
                    "error": "MUS requires: population_size, population_value, tolerable_misstatement",
                }
            params = SamplingParameters(
                population_size=population_size,
                population_value=population_value,
                tolerable_misstatement=tolerable_misstatement,
                confidence_level=confidence_level,
                risk_of_material_misstatement=risk_enum,
            )
            sample_size_calc = AuditSamplingCalculator.calculate_mus_sample_size(params)
            sampling_interval = population_value / sample_size_calc if sample_size_calc > 0 else 0
            return {
                "success": True,
                "action": action,
                "method": "MUS (Monetary Unit Sampling)",
                "sample_size": sample_size_calc,
                "sampling_interval": round(sampling_interval, 2),
                "parameters": {
                    "population_size": population_size,
                    "population_value": population_value,
                    "tolerable_misstatement": tolerable_misstatement,
                    "confidence_level": confidence_level,
                    "risk_level": risk_level,
                },
                "methodology": "PCAOB AS 2315 compliant",
            }

        elif sampling_method.lower() == "attribute":
            if not all([population_size, tolerable_rate]):
                return {
                    "success": False,
                    "error": "Attribute sampling requires: population_size, tolerable_rate",
                }
            params = SamplingParameters(
                population_size=population_size,
                tolerable_rate=tolerable_rate,
                expected_rate=expected_rate or 0.0,
                confidence_level=confidence_level,
            )
            sample_size_calc = AuditSamplingCalculator.calculate_attribute_sample_size(params)
            return {
                "success": True,
                "action": action,
                "method": "Attribute Sampling",
                "sample_size": sample_size_calc,
                "parameters": {
                    "population_size": population_size,
                    "tolerable_rate": tolerable_rate,
                    "expected_rate": expected_rate or 0.0,
                    "confidence_level": confidence_level,
                },
                "methodology": "PCAOB AS 2315 compliant",
            }
        else:
            return {"success": False, "error": f"Invalid sampling_method: {sampling_method}"}

    elif action == "select_sample":
        if not population_items:
            return {"success": False, "error": "population_items is required for select_sample"}
        if not sampling_method:
            sampling_method = "haphazard"

        params = SamplingParameters(
            population_size=len(population_items),
            population_value=sum(item.get(value_field, 0) for item in population_items),
            tolerable_misstatement=tolerable_misstatement or 0,
            risk_of_material_misstatement=risk_enum,
        )
        sampler = AuditSampler(params)

        if sampling_method.lower() == "mus":
            result = sampler.select_mus_sample(population_items, value_field=value_field, id_field=id_field)
        elif sampling_method.lower() == "haphazard":
            if not sample_size:
                return {"success": False, "error": "sample_size required for haphazard sampling"}
            result = sampler.select_haphazard_sample(
                population_items, sample_size=sample_size, id_field=id_field, value_field=value_field
            )
        else:
            return {"success": False, "error": f"Invalid sampling_method for selection: {sampling_method}"}

        return {
            "success": True,
            "action": action,
            "method": result.method.value,
            "sample_size": len(result.items),
            "selected_items": [
                {"id": item.item_id, "value": item.book_value, "selection_reason": item.selection_reason}
                for item in result.items
            ],
            "sampling_interval": result.sampling_interval,
            "methodology": "PCAOB AS 2315 compliant",
        }

    return {"success": False, "error": f"Unhandled sampling action: {action}"}




async def _handle_workpaper_action(
    action: str,
    engagement_name: str | None,
    period_start: str | None,
    period_end: str | None,
    preparer: str | None,
    workpaper_type: str | None,
    control_id: str | None,
    control_description: str | None,
    testing_procedures: list[str] | None,
    sample_items: list[dict] | None,
    exceptions: list[dict] | None,
    conclusion: str | None,
    evidence_items: list[dict] | None,
    source_description: str | None,
    collection_method: str | None,
    findings: list[dict] | None,
    overall_conclusion: str | None,
    controls_tested: list[dict] | None,
    sample_results: list[dict] | None,
    evidence_collections: list[dict] | None,
    output_format: str,
) -> dict[str, Any]:
    """Handle workpaper generation actions."""
    from wistx_mcp.tools.lib.workpaper_generator import WorkpaperGenerator, WorkpaperType

    # Validate required params
    if not engagement_name:
        return {"success": False, "error": "engagement_name is required"}

    # Parse dates
    try:
        start_dt = datetime.fromisoformat(period_start) if period_start else datetime.now().replace(month=1, day=1)
        end_dt = datetime.fromisoformat(period_end) if period_end else datetime.now()
    except ValueError as e:
        return {"success": False, "error": f"Invalid date format: {e}. Use ISO format (YYYY-MM-DD)"}

    wp_gen = WorkpaperGenerator(
        engagement_name=engagement_name,
        period_start=start_dt,
        period_end=end_dt,
        preparer=preparer or "WISTX Compliance Automation",
    )

    if action == "generate_workpaper":
        if not workpaper_type:
            return {"success": False, "error": "workpaper_type required (control_testing, sampling, evidence_collection, summary)"}

        if workpaper_type == "control_testing":
            if not all([control_id, control_description]):
                return {"success": False, "error": "control_id and control_description required"}
            wp = wp_gen.generate_control_testing_workpaper(
                control_id=control_id,
                control_description=control_description,
                testing_procedures=testing_procedures or [],
                sample_items=sample_items or [],
                exceptions=exceptions or [],
                conclusion=conclusion or "Testing incomplete",
            )
        elif workpaper_type == "evidence_collection":
            if not evidence_items:
                return {"success": False, "error": "evidence_items required"}
            wp = wp_gen.generate_evidence_collection_workpaper(
                evidence_items=evidence_items,
                source_description=source_description or "Various sources",
                collection_method=collection_method or "Manual collection",
            )
        elif workpaper_type == "summary":
            wp = wp_gen.generate_summary_of_findings_workpaper(
                findings=findings or [],
                overall_conclusion=overall_conclusion or "Assessment incomplete",
            )
        else:
            return {"success": False, "error": f"Invalid workpaper_type: {workpaper_type}"}

        # Render output
        if output_format == "markdown":
            content = wp_gen.render_workpaper_markdown(wp)
        else:
            content = {
                "workpaper_id": wp.workpaper_id,
                "title": wp.title,
                "type": wp.workpaper_type.value,
                "status": wp.status.value,
                "objective": wp.objective,
                "procedures_performed": wp.procedures_performed,
                "evidence_examined": wp.evidence_examined,
                "findings": wp.findings,
                "conclusion": wp.conclusion,
                "prepared_by": wp.prepared_by,
                "prepared_date": wp.prepared_date.isoformat() if wp.prepared_date else None,
                "content_hash": wp.content_hash,
            }

        return {
            "success": True,
            "action": action,
            "workpaper_id": wp.workpaper_id,
            "workpaper_type": wp.workpaper_type.value,
            "content": content,
            "methodology": "AICPA AU-C Section 230 / PCAOB AS 1215 compliant",
        }

    elif action == "generate_workpaper_package":
        package = wp_gen.generate_workpaper_package(
            controls_tested=controls_tested or [],
            sample_results=sample_results or [],
            evidence_collections=evidence_collections or [],
            findings=findings or [],
        )

        return {
            "success": True,
            "action": action,
            "engagement": package["engagement"],
            "workpaper_count": package["workpaper_count"],
            "workpapers": [
                {
                    "id": wp["workpaper_id"],
                    "title": wp["title"],
                    "type": wp["type"],
                }
                for wp in package["workpapers"]
            ],
            "generated_at": package["generated_at"],
            "methodology": "AICPA AU-C Section 230 / PCAOB AS 1215 compliant",
        }

    return {"success": False, "error": f"Unhandled workpaper action: {action}"}