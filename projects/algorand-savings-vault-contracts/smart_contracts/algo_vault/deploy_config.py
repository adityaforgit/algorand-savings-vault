import logging
import algokit_utils

logger = logging.getLogger(__name__)


def deploy() -> None:
    from smart_contracts.artifacts.algo_vault.algo_vault_client import (
        AlgoVaultFactory,
    )

    algorand = algokit_utils.AlgorandClient.from_environment()
    deployer_ = algorand.account.from_environment("DEPLOYER")

    factory = algorand.client.get_typed_app_factory(
        AlgoVaultFactory, default_sender=deployer_.address
    )

    app_client, result = factory.deploy(
        on_update=algokit_utils.OnUpdate.AppendApp,
        on_schema_break=algokit_utils.OnSchemaBreak.AppendApp,
    )

    # fund app
    if result.operation_performed in [
        algokit_utils.OperationPerformed.Create,
        algokit_utils.OperationPerformed.Replace,
    ]:
        algorand.send.payment(
            algokit_utils.PaymentParams(
                amount=algokit_utils.AlgoAmount(algo=1),
                sender=deployer_.address,
                receiver=app_client.app_address,
            )
        )

    # ✅ initialize first
    app_client.send.initialize(())

    # ✅ deposit
    app_client.send.deposit((50,))

    # ✅ get savings
    response = app_client.send.get_total_savings(())
    print("Savings:", response.abi_return)

    logger.info(
        f"Deployed {app_client.app_name} with App ID {app_client.app_id}"
    )