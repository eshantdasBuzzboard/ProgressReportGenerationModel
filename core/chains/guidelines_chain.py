from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import JsonOutputParser
from dotenv import load_dotenv
import logging
from core.prompts.guidelines_prompts import report_validation_prompt

load_dotenv()


llm = ChatOpenAI(temperature=0, model="gpt-4.1", use_responses_api=True, max_retries=3)


def update_report_with_changes(final_report, changes, verbose=True):
    """
    Updates the final report with changes received from validation.
    The violation_reason key is excluded from the merge and only used for logging.

    Args:
        final_report (dict): The original report dictionary
        changes (list): List of dictionaries with 'slide_name', 'violation_reason', and 'updated_dict'
        verbose (bool): Whether to print violation reasons and update confirmations

    Returns:
        dict: Updated report dictionary
    """
    # Create a deep copy to avoid modifying the original
    import copy

    updated_report = copy.deepcopy(final_report)

    # If no changes, return the original report
    if not changes:
        if verbose:
            print("✓ No violations found. Report is fully compliant with guidelines.")
        return updated_report

    if verbose:
        print("\n" + "=" * 70)
        print("REPORT VALIDATION RESULTS")
        print("=" * 70 + "\n")

    # Apply each change
    for idx, change in enumerate(changes, 1):
        slide_name = change.get("slide_name")
        violation_reason = change.get("violation_reason", "No reason provided")
        updated_dict = change.get("updated_dict")

        if verbose:
            print(f"[{idx}] SLIDE: {slide_name}")
            print(f"    VIOLATION: {violation_reason}")

        if slide_name and updated_dict:
            # Update the specific slide in the report
            # NOTE: violation_reason is NOT merged into the report
            if slide_name in updated_report:
                updated_report[slide_name] = updated_dict
                if verbose:
                    print("    STATUS: ✓ Updated\n")
            else:
                if verbose:
                    print(
                        f"    STATUS: ⚠ Warning - Slide '{slide_name}' not found in report\n"
                    )
        else:
            if verbose:
                print("    STATUS: ⚠ Warning - Missing slide_name or updated_dict\n")

    if verbose:
        print("=" * 70)
        print(f"Total slides updated: {len(changes)}")
        print("=" * 70 + "\n")

    return updated_report


async def changes_after_checking_guidelines(guidelines, final_report, max_retries=3):
    for attempt in range(max_retries):
        try:
            achain = report_validation_prompt | llm | JsonOutputParser()
            input_data = {"report": final_report, "guidelines": guidelines}
            response = await achain.ainvoke(input_data)
            return response
        except Exception as e:
            if attempt == max_retries - 1:
                logging.error(e)
                # Last attempt failed, return empty list
                return []
            # If not the last attempt, the loop will continue to retry
            continue

    return []  # Fallback (though should never reach here)


async def return_updated_report_checking_guidelines(final_report, guidelines):
    current_report = final_report

    for attempt in range(2):
        check = await changes_after_checking_guidelines(
            guidelines=guidelines, final_report=current_report
        )

        if check == []:
            break

        current_report = update_report_with_changes(current_report, check)
    return current_report
