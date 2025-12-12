"""
Unit tests for AWS Step Functions compiler.

These tests verify ASL generation without requiring AWS credentials.
"""

import pytest
from pathlib import Path


class TestStepFunctionsCompiler:
    """Test AWS Step Functions ASL compilation."""

    def test_compiler_import(self):
        """Verify compiler can be imported."""
        from universal_agent_nexus.adapters.aws.step_functions import (
            StepFunctionsCompiler,
        )

        assert StepFunctionsCompiler is not None

    def test_compiler_initialization(self):
        """Test compiler initialization with default settings."""
        from universal_agent_nexus.adapters.aws.step_functions import (
            StepFunctionsCompiler,
        )

        compiler = StepFunctionsCompiler()
        assert compiler.lambda_prefix == "uaa"
        assert compiler.region == "us-east-1"

    def test_compiler_custom_settings(self):
        """Test compiler with custom settings."""
        from universal_agent_nexus.adapters.aws.step_functions import (
            StepFunctionsCompiler,
        )

        compiler = StepFunctionsCompiler(
            lambda_prefix="custom",
            region="eu-west-1",
            account_id="999999999999",
        )
        assert compiler.lambda_prefix == "custom"
        assert compiler.region == "eu-west-1"
        assert compiler.account_id == "999999999999"

    def test_compile_generates_asl(self, sample_manifest_path: Path):
        """Test that compilation generates valid ASL structure."""
        from universal_agent_nexus.adapters.aws.step_functions import (
            StepFunctionsCompiler,
        )
        from universal_agent_nexus.manifest import load_manifest

        manifest = load_manifest(str(sample_manifest_path))
        compiler = StepFunctionsCompiler()

        asl = compiler.compile(manifest, "main")

        # Verify ASL structure
        assert "Comment" in asl
        assert "StartAt" in asl
        assert "States" in asl
        assert "TimeoutSeconds" in asl

        # Verify entry point
        assert asl["StartAt"] == "start"

        # Verify states exist
        assert "start" in asl["States"]
        assert "process" in asl["States"]

    def test_compile_task_state_structure(self, sample_manifest_path: Path):
        """Test task node compiles to correct ASL Task state."""
        from universal_agent_nexus.adapters.aws.step_functions import (
            StepFunctionsCompiler,
        )
        from universal_agent_nexus.manifest import load_manifest

        manifest = load_manifest(str(sample_manifest_path))
        compiler = StepFunctionsCompiler()

        asl = compiler.compile(manifest, "main")

        # Check process task state
        process_state = asl["States"]["process"]
        assert process_state["Type"] == "Task"
        assert "Resource" in process_state
        assert "Parameters" in process_state
        assert "Retry" in process_state

    def test_compile_router_to_choice(self, sample_manifest_path: Path):
        """Test router node compiles to Choice state."""
        from universal_agent_nexus.adapters.aws.step_functions import (
            StepFunctionsCompiler,
        )
        from universal_agent_nexus.manifest import load_manifest

        manifest = load_manifest(str(sample_manifest_path))
        compiler = StepFunctionsCompiler()

        asl = compiler.compile(manifest, "main")

        # Check start router state
        start_state = asl["States"]["start"]
        assert start_state["Type"] == "Choice"

    def test_to_json_output(self, sample_manifest_path: Path):
        """Test JSON serialization of ASL."""
        from universal_agent_nexus.adapters.aws.step_functions import (
            StepFunctionsCompiler,
        )
        from universal_agent_nexus.manifest import load_manifest
        import json

        manifest = load_manifest(str(sample_manifest_path))
        compiler = StepFunctionsCompiler()

        asl = compiler.compile(manifest, "main")
        json_str = compiler.to_json(asl)

        # Should be valid JSON
        parsed = json.loads(json_str)
        assert parsed == asl

    def test_compile_nonexistent_graph_raises(self, sample_manifest_path: Path):
        """Test that compiling nonexistent graph raises ValueError."""
        from universal_agent_nexus.adapters.aws.step_functions import (
            StepFunctionsCompiler,
        )
        from universal_agent_nexus.manifest import load_manifest

        manifest = load_manifest(str(sample_manifest_path))
        compiler = StepFunctionsCompiler()

        with pytest.raises(ValueError, match="not found"):
            compiler.compile(manifest, "nonexistent")

    def test_lambda_arn_construction(self):
        """Test Lambda ARN is constructed correctly."""
        from universal_agent_nexus.adapters.aws.step_functions import (
            StepFunctionsCompiler,
        )

        compiler = StepFunctionsCompiler(
            lambda_prefix="myprefix",
            region="us-west-2",
            account_id="123456789012",
        )

        arn = compiler._build_lambda_arn("my-function")
        expected = "arn:aws:lambda:us-west-2:123456789012:function:myprefix-my-function"
        assert arn == expected
