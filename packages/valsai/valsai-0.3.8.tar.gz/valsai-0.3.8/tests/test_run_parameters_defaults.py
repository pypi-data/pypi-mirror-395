from unittest.mock import AsyncMock, MagicMock

import pytest

from vals.sdk.types import RunParameters


def make_mock_defaults():
    mock_defaults = MagicMock()
    mock_defaults.default_parameters.temperature = None
    mock_defaults.default_parameters.max_output_tokens = 2048
    mock_defaults.default_parameters.eval_model = "openai/gpt-4o"
    mock_defaults.default_parameters.maximum_threads = 10
    mock_defaults.default_parameters.eval_concurrency = 1
    return mock_defaults


@pytest.mark.asyncio
async def test_run_parameters_defaults_inherit_parallelism():
    params = RunParameters()
    mock_client = MagicMock()
    mock_client.get_default_parameters = AsyncMock(return_value=make_mock_defaults())

    import vals.sdk.types as types_module

    types_module.get_ariadne_client = MagicMock(return_value=mock_client)
    param_input = await params.to_graphql()

    assert param_input.maximum_threads == params.parallelism == 10
    assert param_input.eval_concurrency == params.parallelism


@pytest.mark.asyncio
async def test_run_parameters_only_parallelism_sets_both():
    params = RunParameters(parallelism=5, eval_concurrency=None)
    mock_client = MagicMock()
    mock_client.get_default_parameters = AsyncMock(return_value=make_mock_defaults())

    import vals.sdk.types as types_module

    types_module.get_ariadne_client = MagicMock(return_value=mock_client)
    param_input = await params.to_graphql()

    assert param_input.maximum_threads == 5
    assert param_input.eval_concurrency == 5


@pytest.mark.asyncio
async def test_run_parameters_parallelism_and_eval_concurrency_respected():
    params = RunParameters(parallelism=8, eval_concurrency=2)
    mock_client = MagicMock()
    mock_client.get_default_parameters = AsyncMock(return_value=make_mock_defaults())

    import vals.sdk.types as types_module

    types_module.get_ariadne_client = MagicMock(return_value=mock_client)
    param_input = await params.to_graphql()

    assert param_input.maximum_threads == 8
    assert param_input.eval_concurrency == 2
