from classiq.interface.backend.quantum_backend_providers import (
    PROVIDER_NAME_MAPPER,
    ProviderVendor,
)
from classiq.interface.executor.user_budget import UserBudgets

from classiq._internals.api_wrapper import ApiWrapper
from classiq._internals.async_utils import syncify_function


async def get_budget_async(
    provider: ProviderVendor | None = None,
) -> UserBudgets:

    budgets_list = await ApiWrapper().call_get_all_budgets()
    if provider:
        _provider = PROVIDER_NAME_MAPPER.get(provider, None)
        budgets_list = [
            budget for budget in budgets_list if budget.provider == _provider
        ]

    return UserBudgets(budgets=budgets_list)


def get_budget(
    provider: ProviderVendor | None = None,
) -> UserBudgets:
    """
    Retrieve the user's budget information for quantum computing resources.

    Args:
        provider:
            (Optional) The quantum backend provider to filter budgets by.
            If not provided, budgets for all providers will be returned.

    Returns:
        UserBudgets: An object containing the user's budget information.
    """
    return syncify_function(get_budget_async)(provider)


async def set_budget_limit_async(
    provider: ProviderVendor,
    limit: float,
) -> UserBudgets:
    _provider = PROVIDER_NAME_MAPPER.get(provider, None)
    if not _provider:
        raise ValueError(f"Unsupported provider: {provider}")

    budget = await get_budget_async(provider)
    if budget is None:
        raise ValueError(f"No budget found for provider: {provider}")

    if limit <= 0:
        raise ValueError("Budget limit must be greater than zero.")

    if limit > budget.budgets[0].available_budget:
        print(  # noqa: T201
            f"Budget limit {limit} exceeds available budget {budget.budgets[0].available_budget} for provider {provider}.\n"
            "Setting budget limit to the maximum available budget."
        )
    budgets_list = await ApiWrapper().call_set_budget_limit(_provider, limit)
    return UserBudgets(budgets=[budgets_list])


def set_budget_limit(
    provider: ProviderVendor,
    limit: float,
) -> UserBudgets:
    """
    Set a budget limit for a specific quantum backend provider.

    Args:
        provider:
            The quantum backend provider for which to set the budget limit.
        limit:
            The budget limit to set. Must be greater than zero and not exceed the available budget.

    Returns:
        UserBudgets: An object containing the updated budget information.

    Raises:
        ValueError: If the provider is unsupported, no budget is found, or the limit is invalid.
    """
    return syncify_function(set_budget_limit_async)(provider, limit)


async def clear_budget_limit_async(provider: ProviderVendor) -> UserBudgets:
    _provider = PROVIDER_NAME_MAPPER.get(provider, None)
    if not _provider:
        raise ValueError(f"Unsupported provider: {provider}")

    budgets_list = await ApiWrapper().call_clear_budget_limit(_provider)
    return UserBudgets(budgets=[budgets_list])


def clear_budget_limit(provider: ProviderVendor) -> UserBudgets:
    """
    Clear the budget limit for a specific quantum backend provider.

    Args:
        provider:
            The quantum backend provider for which to clear the budget limit.

    Returns:
        UserBudgets: An object containing the updated budget information.

    Raises:
        ValueError: If the provider is unsupported.
    """
    return syncify_function(clear_budget_limit_async)(provider)
