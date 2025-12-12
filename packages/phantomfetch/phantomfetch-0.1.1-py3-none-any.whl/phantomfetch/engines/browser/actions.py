import logging
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from playwright.async_api import Page
    from ...types import ActionResult

from ...types import Action

logger = logging.getLogger(__name__)


async def execute_actions(page: "Page", actions: list[Action]) -> list["ActionResult"]:
    """
    Execute a list of actions on a Playwright page.

    Args:
        page: Playwright page instance
        actions: List of Action objects

    Returns:
        List of ActionResult objects
    """
    import time
    from ...types import ActionResult

    results = []

    for action in actions:
        logger.debug(f"[browser] Executing: {action.action} {action.selector or ''}")
        start_time = time.perf_counter()
        result = ActionResult(action=action, success=True)

        try:
            match action.action:
                case "wait":
                    if action.selector:
                        await page.wait_for_selector(
                            action.selector,
                            timeout=action.timeout,
                        )

                case "click":
                    if action.selector:
                        await page.click(
                            action.selector,
                            timeout=action.timeout,
                        )

                case "input":
                    if action.selector and action.value is not None:
                        await page.fill(
                            action.selector,
                            str(action.value),
                            timeout=action.timeout,
                        )

                case "scroll":
                    if action.selector:
                        await page.locator(action.selector).scroll_into_view_if_needed(
                            timeout=action.timeout
                        )
                    else:
                        # Scroll to bottom if no selector
                        await page.evaluate(
                            "window.scrollTo(0, document.body.scrollHeight)"
                        )

                case "select":
                    if action.selector and action.value is not None:
                        await page.select_option(
                            action.selector,
                            str(action.value),
                            timeout=action.timeout,
                        )

                case "hover":
                    if action.selector:
                        await page.hover(
                            action.selector,
                            timeout=action.timeout,
                        )

                case "screenshot":
                    # action.value = file path
                    path = str(action.value) if action.value else None
                    img_bytes = await page.screenshot(path=path)
                    if not path:
                        result.data = img_bytes

                case "wait_for_load":
                    await page.wait_for_load_state(
                        "networkidle", timeout=action.timeout
                    )

                case "evaluate":
                    # action.value = JS code
                    if action.value:
                        eval_result = await page.evaluate(str(action.value))
                        result.data = eval_result

                case _:
                    logger.warning(f"[browser] Unknown action: {action.action}")
                    result.success = False
                    result.error = f"Unknown action: {action.action}"

        except Exception as e:
            result.success = False
            result.error = str(e)
            logger.error(f"[browser] Action failed: {action.action} - {e}")

        finally:
            result.duration = time.perf_counter() - start_time
            results.append(result)

    return results


def actions_to_payload(actions: list[Action]) -> list[dict]:
    """
    Convert Action objects to JSON-serializable dicts for BaaS API.

    Args:
        actions: List of Action objects

    Returns:
        List of action dicts
    """
    import msgspec

    return [msgspec.to_builtins(a) for a in actions]
