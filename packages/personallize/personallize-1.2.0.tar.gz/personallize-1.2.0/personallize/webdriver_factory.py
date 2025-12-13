import logging
import platform
import subprocess
import time
import warnings
import zipfile
from io import BytesIO
from pathlib import Path
from typing import Any

import requests
from selenium import webdriver
from selenium.common.exceptions import (
    InvalidSelectorException,
    MoveTargetOutOfBoundsException,
    NoSuchElementException,
    TimeoutException,
)
from selenium.webdriver import ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from .simple_log import LogManager

log_manager = LogManager()
logger, exception = log_manager.get_logger()
plogger, _ = log_manager.get_logger(logging_level=logging.INFO)

warnings.filterwarnings(action="ignore")


if platform.system() == "Windows":
    import winreg


class CustomChromeDriverManager:
    """
    Manages the automated download and installation of ChromeDriver, ensuring
    compatibility with the installed version of Google Chrome.
    Works on Windows, Linux, and macOS.
    """

    CHROME_DRIVER_JSON_URL = "https://googlechromelabs.github.io/chrome-for-testing/last-known-good-versions-with-downloads.json"

    def __init__(self, path: str | Path | None = None, verify_ssl: bool = True):
        self.verify_ssl = verify_ssl
        self.system = platform.system()
        self.root_path = Path(path) if path else Path.cwd()
        self.driver_filename = "chromedriver.exe" if self.system == "Windows" else "chromedriver"
        # Inicialmente sem versão - será definido após detectar a versão do Chrome
        self.driver_path = None
        self.chrome_version = None

    def install(self) -> str:
        """
        Orquestra o processo de verificação e instalação para o Chromedriver.

        Retorna o caminho (string) para o driver executável.
        """
        value_error = "Could not find installed Google Chrome version."
        runtime_not_found = "Could not find a ChromeDriver download URL for version {}"
        runtime_failed_download = "Failed to download and extract ChromeDriver."

        # Detectar versão do Chrome
        chrome_version = self._get_installed_chrome_version()
        if not chrome_version:
            raise ValueError(value_error)

        self.chrome_version = chrome_version
        plogger.info("Google Chrome version %s detected.", chrome_version)

        # Definir o caminho do driver com a versão
        version_clean = chrome_version.replace(".", "_")
        driver_filename_with_version = (
            f"chromedriver_{version_clean}.exe"
            if self.system == "Windows"
            else f"chromedriver_{version_clean}"
        )
        self.driver_path = self.root_path / driver_filename_with_version

        # Verificar se já existe um driver com a versão correta
        if self.driver_path.exists():
            plogger.info(
                "ChromeDriver for version %s already exists at: %s",
                chrome_version,
                self.driver_path,
            )
            return str(self.driver_path)

        # Limpar drivers antigos de outras versões
        self._cleanup_old_drivers()

        download_url = self._get_driver_download_url()
        if not download_url:
            raise RuntimeError(runtime_not_found.format(chrome_version))

        driver_executable_path = self._download_and_place_driver(download_url)
        if not driver_executable_path:
            raise RuntimeError(runtime_failed_download)

        return str(driver_executable_path)

    def _get_installed_chrome_version(self) -> str | None:
        """Checks the version of Google Chrome installed on the system."""
        version_checkers = {
            "Windows": self._get_chrome_version_windows,
            "Linux": self._get_chrome_version_linux_or_mac,
            "Darwin": self._get_chrome_version_linux_or_mac,
        }
        checker = version_checkers.get(self.system)
        if checker:
            return checker()
        return None

    def _get_chrome_version_windows(self) -> str | None:
        """Checks the installed Google Chrome version on Windows by reading the registry."""
        for root_key in [winreg.HKEY_CURRENT_USER, winreg.HKEY_LOCAL_MACHINE]:
            try:
                with winreg.OpenKey(root_key, r"Software\Google\Chrome\BLBeacon") as key:
                    version, _ = winreg.QueryValueEx(key, "version")
                    if version:
                        return version
            except (FileNotFoundError, NameError):
                continue
        return None

    def _get_chrome_version_linux_or_mac(self) -> str | None:
        """Checks the installed Google Chrome version on Linux or macOS using command line."""
        commands = {
            "Linux": ["google-chrome", "--version"],
            "Darwin": ["/Applications/Google Chrome.app/Contents/MacOS/Google Chrome", "--version"],
        }

        command = commands.get(self.system)
        if not command:
            return None

        try:
            result = subprocess.run(command, capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                # Extract version from output like "Google Chrome 120.0.6099.109"
                version_line = result.stdout.strip()
                if "Google Chrome" in version_line:
                    return version_line.split()[-1]
        except (subprocess.TimeoutExpired, FileNotFoundError, subprocess.SubprocessError):
            pass
        return None

    def _get_driver_download_url(self) -> str | None:
        """Gets the download URL for ChromeDriver compatible with the given Chrome version."""
        try:
            response = requests.get(self.CHROME_DRIVER_JSON_URL, verify=self.verify_ssl, timeout=30)
            response.raise_for_status()
            data = response.json()

            # Get the stable version info
            stable_version = data.get("channels", {}).get("Stable", {})
            downloads = stable_version.get("downloads", {}).get("chromedriver", [])

            # Find the appropriate download for the current platform
            platform_map = {
                "Windows": "win64" if platform.machine().endswith("64") else "win32",
                "Linux": "linux64",
                "Darwin": "mac-x64" if platform.machine() == "x86_64" else "mac-arm64",
            }

            target_platform = platform_map.get(self.system)
            if not target_platform:
                return None

            for download in downloads:
                if download.get("platform") == target_platform:
                    return download.get("url")

        except (requests.RequestException, KeyError, ValueError) as e:
            plogger.exception("Error fetching ChromeDriver download URL")
        return None

    def _download_and_place_driver(self, url: str) -> Path | None:
        """Downloads and extracts the ChromeDriver to the specified path."""
        try:
            plogger.info("Downloading ChromeDriver from: %s", url)
            response = requests.get(url, verify=self.verify_ssl, timeout=60)
            response.raise_for_status()

            # Extract the zip file
            with zipfile.ZipFile(BytesIO(response.content)) as zip_file:
                plogger.info("ZIP contents: %s", [f.filename for f in zip_file.filelist])

                # Find the chromedriver executable in the zip
                chromedriver_file = None
                for file_info in zip_file.filelist:
                    # Check specifically for chromedriver.exe or chromedriver executable
                    filename_lower = file_info.filename.lower()
                    if filename_lower.endswith("chromedriver.exe") or (
                        filename_lower.endswith("chromedriver")
                        and not filename_lower.endswith(".chromedriver")
                    ):
                        chromedriver_file = file_info
                        plogger.info("Found ChromeDriver executable: %s", file_info.filename)
                        break

                if chromedriver_file:
                    plogger.info("Extracting ChromeDriver from: %s", chromedriver_file.filename)

                    # Extract the file content directly to the target location
                    with zip_file.open(chromedriver_file) as source:
                        # Ensure parent directory exists
                        self.driver_path.parent.mkdir(parents=True, exist_ok=True)

                        # Write the content directly to the target file
                        with open(self.driver_path, "wb") as target:
                            target.write(source.read())

                    # Make executable on Unix systems
                    if self.system != "Windows":
                        self.driver_path.chmod(0o755)

                    plogger.info("ChromeDriver successfully placed at: %s", self.driver_path)
                    return str(self.driver_path)
                else:
                    plogger.error("ChromeDriver executable not found in ZIP file")
                    plogger.error("Available files: %s", [f.filename for f in zip_file.filelist])
                    return None

        except (requests.RequestException, zipfile.BadZipFile, OSError):
            plogger.exception("Error downloading/extracting ChromeDriver")
            return None

    def _cleanup_old_drivers(self):
        """Remove drivers antigos de outras versões do Chrome."""
        try:
            # Padrão para encontrar drivers antigos
            pattern = "chromedriver_*.exe" if self.system == "Windows" else "chromedriver_*"

            for old_driver in self.root_path.glob(pattern):
                if old_driver != self.driver_path:  # Não remover o driver atual
                    plogger.info("Removing old ChromeDriver: %s", old_driver)
                    old_driver.unlink()

            # Também remover o driver sem versão (formato antigo)
            old_driver_path = self.root_path / self.driver_filename
            if old_driver_path.exists() and old_driver_path != self.driver_path:
                plogger.info("Removing old ChromeDriver (legacy format): %s", old_driver_path)
                old_driver_path.unlink()

        except Exception as e:
            plogger.warning("Failed to cleanup old drivers: %s", e)


class WebDriverManipulator:
    """
    A WebDriver wrapper class that automates driver management and provides a simplified
    interface for browser interaction. Designed to be extensible.
    """

    def __init__(
        self,
        driver_path: str | Path | None = None,
        options: ChromeOptions | None = None,
        default_timeout: int = 30,
        verify_ssl: bool = False,
    ):
        # Use the module-level logger instead of creating a new one
        self.exception_decorator = exception
        self.default_timeout = default_timeout

        try:
            self.driver: WebDriver = self._initialize_driver(driver_path, options, verify_ssl)
            self.action_chains = ActionChains(self.driver)
            logger.info("Web session initialized successfully.")
        except Exception:
            logger.exception("Failed to navigate to URL")
            raise

    def _initialize_driver(
        self,
        driver_path: str | Path | None,
        options: ChromeOptions | None,
        verify_ssl: bool,
    ) -> WebDriver:
        logger.debug("Initializing WebDriver.")

        if not driver_path:
            logger.info("No driver_path provided. Using automatic driver manager.")
            manager = CustomChromeDriverManager(verify_ssl=verify_ssl)
            driver_path = manager.install()

        if not Path(driver_path).is_file():
            raise FileNotFoundError(f"ChromeDriver executable not found at: {driver_path}")

        service = ChromeService(executable_path=str(driver_path))
        return webdriver.Chrome(service=service, options=options)

    def quit(self):
        if hasattr(self, "driver") and self.driver:
            logger.info("Closing WebDriver session.")
            self.driver.quit()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.quit()

    def _get_by_strategy(self, selector_type: str) -> By:
        strategy_map = {
            "id": By.ID,
            "name": By.NAME,
            "class": By.CLASS_NAME,
            "xpath": By.XPATH,
            "tag_name": By.TAG_NAME,
            "css_selector": By.CSS_SELECTOR,
            "link_text": By.LINK_TEXT,
            "partial_link_text": By.PARTIAL_LINK_TEXT,
        }
        normalized_type = selector_type.lower().strip()
        if normalized_type not in strategy_map:
            logger.exception("Unsupported selector type: '%s'", selector_type)
            raise ValueError(
                f"Selector '{selector_type}' is not supported. Use one of {list(strategy_map.keys())}."
            )
        return strategy_map[normalized_type]

    def find_element(
        self,
        selector_value: str,
        selector_type: str = "xpath",
        timeout: int | None = None,
        raise_exception: bool = True,
    ) -> WebElement | None:
        current_timeout = timeout if timeout is not None else self.default_timeout
        by_strategy = self._get_by_strategy(selector_type)

        try:
            wait = WebDriverWait(self.driver, current_timeout)
            element = wait.until(EC.presence_of_element_located((by_strategy, selector_value)))
            logger.debug("Element '%s' found by %s.", selector_value, selector_type)
            return element
        except (TimeoutException, NoSuchElementException):
            if raise_exception:
                logger.exception(
                    f"Element '{selector_value}' not found by {selector_type} within {current_timeout}s."
                )
                raise
            logger.warning(
                f"Element '{selector_value}' not found by {selector_type} (exception suppressed)."
            )
            return None
        except InvalidSelectorException:
            logger.exception("Invalid selector: '%s' (%s).", selector_value, selector_type)
            if raise_exception:
                raise
            return None

    def find_elements(
        self,
        selector_value: str,
        selector_type: str = "xpath",
        timeout: int | None = None,
        min_elements: int = 0,
    ) -> list[WebElement]:
        current_timeout = timeout if timeout is not None else self.default_timeout
        by_strategy = self._get_by_strategy(selector_type)

        try:
            wait = WebDriverWait(self.driver, current_timeout)
            if min_elements > 0:
                wait.until(
                    lambda d: len(d.find_elements(by_strategy, selector_value)) >= min_elements
                )

            elements = self.driver.find_elements(by_strategy, selector_value)
            logger.debug(
                f"Found {len(elements)} elements for '{selector_value}' by {selector_type}."
            )
            return elements
        except TimeoutException:
            logger.warning(
                f"Minimum {min_elements} elements not found for '{selector_value}' within {current_timeout}s."
            )
            return []
        except InvalidSelectorException:
            logger.exception("Invalid selector: '%s' (%s).", selector_value, selector_type)
            return []

    def find_element_in_frames(
        self,
        selector_value: str,
        selector_type: str = "xpath",
        timeout: int | None = None,
        raise_exception: bool = True,
    ) -> WebElement | None:
        current_timeout = timeout if timeout is not None else self.default_timeout
        by_strategy = self._get_by_strategy(selector_type)
        end_time = time.time() + current_timeout

        # Try to find in current frame first
        try:
            element = self.driver.find_element(by_strategy, selector_value)
            if element:
                return element
        except (NoSuchElementException, InvalidSelectorException):
            pass

        # Search recursively in frames
        element = self._search_in_frame_recursively(selector_value, by_strategy, end_time)

        if element:
            return element
        elif raise_exception:
            logger.exception(
                "Element '%s' not found in any frame within %ss.", selector_value, current_timeout
            )
            raise NoSuchElementException(f"Element not found in any frame: {selector_value}")
        else:
            logger.warning(
                "Element '%s' not found in any frame (exception suppressed).", selector_value
            )
            return None

    def _search_in_frame_recursively(
        self, selector: str, by: By, end_time: float
    ) -> WebElement | None:
        if time.time() > end_time:
            return None

        # Get all frames in current context
        frames = self.driver.find_elements(By.TAG_NAME, "iframe") + self.driver.find_elements(
            By.TAG_NAME, "frame"
        )

        for frame in frames:
            try:
                self.driver.switch_to.frame(frame)

                # Try to find element in this frame
                try:
                    element = self.driver.find_element(by, selector)
                    if element:
                        return element
                except (NoSuchElementException, InvalidSelectorException):
                    pass

                # Recursively search in nested frames
                nested_element = self._search_in_frame_recursively(selector, by, end_time)
                if nested_element:
                    return nested_element

            except Exception:
                pass
            finally:
                # Always switch back to parent frame
                try:
                    self.driver.switch_to.parent_frame()
                except Exception:
                    self.driver.switch_to.default_content()

        return None

    def click(self, element: WebElement, use_action_chains: bool = False):
        """Clicks on the given WebElement."""
        try:
            if use_action_chains:
                self.action_chains.click(element).perform()
                logger.debug("Element clicked using ActionChains.")
            else:
                element.click()
                logger.debug("Element clicked directly.")
        except MoveTargetOutOfBoundsException:
            logger.warning("Element out of bounds, trying with ActionChains.")
            self.action_chains.click(element).perform()
        except Exception:
            logger.exception("Failed to navigate to URL")
            raise

    def send_keys(self, element: WebElement, *values: str, clear_first: bool = False):
        """Sends keys to the given WebElement."""
        try:
            if clear_first:
                element.clear()
            element.send_keys(*values)
            logger.debug("Keys sent to element: %s", values)
        except Exception:
            logger.exception("Failed to refresh page")
            raise

    def get_text(self, element: WebElement) -> str:
        """Gets the text content of the given WebElement."""
        try:
            text = element.text
            logger.debug("Text retrieved from element: '%s'", text)
            return text
        except Exception as e:
            logger.exception(e)
            raise

    def get_attribute(self, element: WebElement, attribute_name: str) -> str:
        """Gets the specified attribute value from the given WebElement."""
        try:
            attribute_value = element.get_attribute(attribute_name)
            logger.debug(
                "Attribute '%s' retrieved from element: '%s'", attribute_name, attribute_value
            )
            return attribute_value if attribute_value else ""
        except Exception as e:
            logger.exception(e)
            raise

    def wait_for_visibility(
        self,
        selector_value: str,
        selector_type: str = "xpath",
        timeout: int | None = None,
    ) -> WebElement:
        """Waits for an element to be visible and returns it."""
        current_timeout = timeout if timeout is not None else self.default_timeout
        by_strategy = self._get_by_strategy(selector_type)

        try:
            wait = WebDriverWait(self.driver, current_timeout)
            element = wait.until(EC.visibility_of_element_located((by_strategy, selector_value)))
            logger.debug("Element '%s' became visible.", selector_value)
            return element
        except TimeoutException:
            logger.exception(
                "Element '%s' did not become visible within %ss.", selector_value, current_timeout
            )
            raise

    def wait_for_clickable(
        self,
        selector_value: str,
        selector_type: str = "xpath",
        timeout: int | None = None,
    ) -> WebElement:
        """Waits for an element to be clickable and returns it."""
        current_timeout = timeout if timeout is not None else self.default_timeout
        by_strategy = self._get_by_strategy(selector_type)

        try:
            wait = WebDriverWait(self.driver, current_timeout)
            element = wait.until(EC.element_to_be_clickable((by_strategy, selector_value)))
            logger.debug("Element '%s' became clickable.", selector_value)
            return element
        except TimeoutException:
            logger.exception(
                "Element '%s' did not become clickable within %ss.", selector_value, current_timeout
            )
            raise

    def execute_script(self, script: str, *args: Any) -> Any:
        """Executes JavaScript in the browser."""
        try:
            result = self.driver.execute_script(script, *args)
            logger.debug("JavaScript executed: %s...", script[:50])
            return result
        except Exception:
            logger.exception("Failed to execute JavaScript")
            raise

    def get(self, url: str):
        """Navigates to the specified URL."""
        try:
            self.driver.get(url)
            logger.info("Navigated to: %s", url)
        except Exception:
            logger.exception("Failed to navigate to URL")
            raise

    @property
    def current_url(self) -> str:
        """Returns the current URL."""
        return self.driver.current_url

    def refresh(self):
        """Refreshes the current page."""
        try:
            self.driver.refresh()
            logger.debug("Page refreshed.")
        except Exception:
            logger.exception("Failed to refresh page")
            raise

    def switch_to_tab(self, tab_index: int):
        """Switches to the specified tab by index."""
        try:
            handles = self.driver.window_handles
            if 0 <= tab_index < len(handles):
                self.driver.switch_to.window(handles[tab_index])
                logger.debug("Switched to tab %s.", tab_index)
            else:
                msg = f"Tab index {tab_index} out of range. Available tabs: {len(handles)}"
                raise IndexError(msg)
        except Exception:
            logger.exception("Failed to switch to tab %s", tab_index)
            raise

    def take_screenshot(self, file_path: str = "screenshot.png"):
        """Takes a screenshot and saves it to the specified path."""
        try:
            self.driver.save_screenshot(file_path)
            logger.info("Screenshot saved to: %s", file_path)
        except Exception:
            logger.exception("Failed to take screenshot")
            raise
