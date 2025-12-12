from model_library.registry_utils import get_registry_model
import asyncio

from vals import RunParameters
from vals.sdk.suite import Suite
from vals.sdk.types import Check, QuestionAnswerPair, Test
from dotenv import load_dotenv

load_dotenv()

llm = get_registry_model("openai/gpt-4o")


async def run_agent():
    suite = Suite(
        title="Test Suite",
        global_checks=[Check(operator="grammar")],
        tests=[
            Test(
                input_under_test="What is QSBS?",
                checks=[Check(operator="equals", criteria="QSBS")],
            ),
            Test(
                input_under_test="What is an 83 election?",
                checks=[Check(operator="equals", criteria="QSBS")],
            ),
        ],
    )

    await suite.create()

    if not suite.id:
        raise Exception("Failed to create suite")

    print("Creating empty run object...")
    run = await Suite.create_run(
        suite_id=suite.id,
        parameters=RunParameters(
            eval_model="openai/gpt-4o",
            create_text_summary=False,
            run_confidence_evaluation=False,
        ),
        run_name="Vals Agent Example",
    )
    print(f"Successfully created run object with ID: {run.id}")

    print("Uploading QA pairs...")
    qa_pairs: list[QuestionAnswerPair] = []
    for test in suite.tests:
        query_result = await llm.query(test.input_under_test)
        qa_pairs.append(
            await QuestionAnswerPair.upload(
                run_id=run.id,
                qa_set_id=run.qa_set_id,
                test_id=test._id,
                query_result=query_result,
            )
        )

    print(f"Uploaded {len(qa_pairs)} QA pairs.")

    print("Run is being evaluated on the server.")


if __name__ == "__main__":
    asyncio.run(run_agent())
