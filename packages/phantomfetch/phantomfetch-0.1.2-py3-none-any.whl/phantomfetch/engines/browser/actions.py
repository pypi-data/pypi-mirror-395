import logging
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from playwright.async_api import Page

    from ...types import ActionResult

from ...types import Action
from ...telemetry import get_tracer

logger = logging.getLogger(__name__)
tracer = get_tracer()


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
    from opentelemetry import trace


    from ...types import ActionResult

    results = []

    for action in actions:
        with tracer.start_as_current_span(f"phantomfetch.action.{action.action}") as span:
            span.set_attribute("phantomfetch.action.type", action.action)
            if action.selector:
                span.set_attribute("phantomfetch.action.selector", action.selector)
            
            logger.debug(f"[browser] Executing: {action.action} {action.selector or ''}")
            start_time = time.perf_counter()
            result = ActionResult(action=action, success=True)

            try:
                match action.action:
                    case "wait":
                        if action.timeout:
                            span.set_attribute("phantomfetch.action.timeout", action.timeout)

                        if action.selector:
                            await page.wait_for_selector(
                                action.selector,
                                timeout=action.timeout,
                            )
                        # Handle wait:time syntax if handled in normalization or here?
                        # normalization usually converts generic waits.
                        # If timeout only (no selector), normalization makes it wait(timeout=...)
                        # But wait action in types has selector/timeout.
                        # If simple wait(2000), it's normalized to Action(action='wait', timeout=2000).
                        # We need to handle that here too if not handled.
                        # CDPEngine doesn't seem to sleep on wait?
                        # Let's check wait logic in previous content.
                        # Ah, case "wait": if action.selector... await page.wait_for_selector.
                        # What if no selector? just timeout?
                        elif action.timeout:
                             await page.wait_for_timeout(action.timeout)

                    case "click":
                        if action.timeout:
                            span.set_attribute("phantomfetch.action.timeout", action.timeout)
                        if action.selector:
                            await page.click(
                                action.selector,
                                timeout=action.timeout,
                            )

                    case "input":
                        if action.timeout:
                            span.set_attribute("phantomfetch.action.timeout", action.timeout)
                        if action.selector and action.value is not None:
                            val_str = str(action.value)
                            span.set_attribute("phantomfetch.action.input.length", len(val_str))
                            await page.fill(
                                action.selector,
                                val_str,
                                timeout=action.timeout,
                            )

                    case "scroll":
                        if action.timeout:
                            span.set_attribute("phantomfetch.action.timeout", action.timeout)
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
                        if action.timeout:
                            span.set_attribute("phantomfetch.action.timeout", action.timeout)
                        if action.selector and action.value is not None:
                            await page.select_option(
                                action.selector,
                                str(action.value),
                                timeout=action.timeout,
                            )

                    case "hover":
                        if action.timeout:
                            span.set_attribute("phantomfetch.action.timeout", action.timeout)
                        if action.selector:
                            await page.hover(
                                action.selector,
                                timeout=action.timeout,
                            )

                    case "screenshot":
                        # action.value = file path
                        path = str(action.value) if action.value else None
                        if path:
                            span.set_attribute("phantomfetch.action.screenshot.path", path)
                        
                        img_bytes = await page.screenshot(path=path)
                        if img_bytes:
                             span.set_attribute("phantomfetch.action.screenshot.size_bytes", len(img_bytes))

                        if not path:
                            result.data = img_bytes

                    case "wait_for_load":
                        if action.timeout:
                            span.set_attribute("phantomfetch.action.timeout", action.timeout)
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
                        span.set_attribute("error", True)
                        span.set_attribute("phantomfetch.action.error", result.error)

            except Exception as e:
                result.success = False
                result.error = str(e)
                logger.error(f"[browser] Action failed: {action.action} - {e}")
                span.record_exception(e)
                span.set_status(trace.Status(trace.StatusCode.ERROR, str(e)))

            finally:
                result.duration = time.perf_counter() - start_time
                span.set_attribute("phantomfetch.action.success", result.success)
                span.set_attribute("phantomfetch.action.duration_ms", result.duration * 1000)
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
