import pytest
from _pytest._code.code import ExceptionInfo
from .soft_assert import SoftAssert, SoftAssertionError


#
# Definition of test options
#
def pytest_addoption(parser):
    parser.addini(
        "soft_assert_mode",
        type="string",
        default="xfail",
        help="The mode soft assertion should fail. Accepted values: fail, xfail"
    )


#
# Fixtures
#
@pytest.fixture(scope="session")
def _fx_soft_assert_mode(request):
    """ The mode soft assertion should fail """
    return request.config.getini("soft_assert_mode")


@pytest.fixture(scope="function")
def soft(_fx_soft_assert_mode):
    return SoftAssert(_fx_soft_assert_mode)


#
# Pytest Hooks
#
@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if call.when == "call":
        if "soft" in item.funcargs:
            try:
                feature_request = item.funcargs["request"]
                fx_soft = feature_request.getfixturevalue("soft")
            except pytest.FixtureLookupError:
                pass
            msg = "\n".join(fx_soft.errors)
            exc = SoftAssertionError(msg)
            excinfo = ExceptionInfo.from_exc_info((type(exc), exc, exc.__traceback__))
            if fx_soft.errors:
                if fx_soft.already_failed and fx_soft.failure_mode == "xfail":
                    call.excinfo = excinfo

                if not fx_soft.already_failed:
                    report.longrepr = msg
                    call.excinfo = excinfo
                    fx_soft.already_failed = True
                    if fx_soft.failure_mode == "fail":
                        report.outcome = "failed"
                    else:
                        report.outcome = "skipped"
                        report.wasxfail = msg
