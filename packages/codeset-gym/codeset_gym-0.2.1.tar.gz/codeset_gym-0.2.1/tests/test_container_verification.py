"""Test verification of containers using codeset-gym."""

import pytest
import docker
from codeset_gym.main import (
    start_instance,
    run_verifier,
    get_test_results,
    stop_instance,
)


def test_barrust_pyprobables_117_verification():
    """Test that we can verify barrust__pyprobables-117:latest container."""
    instance_id = "barrust__pyprobables-117"
    repository = "codeset"
    version = "latest"
    dataset_name = "codeset-gym-python"

    try:
        container = start_instance(repository, instance_id, version, dataset_name)

        # Run /verifier.sh inside the container
        result = run_verifier(instance_id, container)

        # Verify the verifier failed (some tests are failing)
        assert result["exit_code"] != 0

        # Extract test results from the container
        test_results = get_test_results(instance_id, container, "python")

        # Verify we got test results
        assert test_results is not None
        assert len(test_results) > 0, "No test results found"

        # Print some basic info about the results
        total_tests = sum(len(suite) for suite in test_results)
        print(f"Successfully extracted {total_tests} test results from {instance_id}")

        # Check that we can iterate through the test cases
        for test_suite in test_results:
            for test_case in test_suite:
                print(f"Test: {test_case.classname}::{test_case.name}")
                if test_case.result:
                    print(f"  Status: FAILED - {test_case.result}")
                else:
                    print(f"  Status: PASSED")

    finally:
        # Clean up the container
        if 'container' in locals():
            stop_instance(container)


def test_container_start_and_stop():
    """Test basic container lifecycle management."""
    instance_id = "barrust__pyprobables-117"
    repository = "codeset"
    version = "latest"
    dataset_name = "codeset-gym-python"

    # Start the container
    container = start_instance(repository, instance_id, version, dataset_name)

    try:
        # Verify container is running
        container.reload()
        assert container.status == "running"

        # Verify we can execute commands
        result = container.exec_run("echo 'test'")
        assert result.exit_code == 0
        assert b"test" in result.output

    finally:
        # Stop and remove the container
        stop_instance(container)

        # Verify container is stopped/removed
        client = docker.from_env()
        try:
            client.containers.get(container.id)
            # If we get here, container still exists - this is unexpected
            assert False, "Container should have been removed"
        except docker.errors.NotFound:
            # This is expected - container was successfully removed
            pass


if __name__ == "__main__":
    pytest.main([__file__, "-v"])