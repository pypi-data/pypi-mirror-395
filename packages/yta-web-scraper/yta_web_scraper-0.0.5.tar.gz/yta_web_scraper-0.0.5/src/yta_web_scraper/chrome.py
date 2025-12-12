from yta_constants.regex import GeneralRegularExpression
from yta_validation.parameter import ParameterValidator
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from typing import Union

import time


class ChromeScraper:
    """
    A class that wraps and simplify the functionality of
    the Google Chrome scrapper, useful to interact with
    websites and navigate through them interacting with
    their elements being able to perform complex actions
    such as downloading files, sending forms, etc.
    """

    do_use_gui: bool = True
    """
    Flag that indicates if the scraper is using the
    GUI or not. Using the GUI will show the web
    navigator in the system screen.
    """
    do_use_ad_blocker: bool = True
    """
    Flag that indicates if the scraper is using the
    ad blocker add-on or not.
    """
    do_disable_popups_and_cookies: bool = True
    """
    Flag that indicates if the scraper is disabling
    the popups and cookies or not.
    """
    additional_options = []
    max_page_load_waiting_time = 10
    options = None
    # TODO: Maybe make 'driver' private attribute in ChromeScraper to
    # avoid exposing it
    driver = None

    @property
    def active_element(
        self
    ) -> Union[WebElement, None]:
        """
        Get the current active element by running the
        'driver.switch_to.active_element' command.
        """
        return (
            self.driver.switch_to.active_element
            if self.driver is not None else
            None
        )
    
    @property
    def current_url(
        self
    ) -> Union[str, None]:
        """
        Get the current url in which the scraper is
        located by using the 'driver.current_url'.
        """
        return (
            self.driver.current_url
            if self.driver is not None else
            None
        )
    
    @property
    def is_page_loading(
        self
    ) -> bool:
        """
        Get the state of the current web page and return
        True if the page is still loading.
        """
        PAGE_STATE_IS_LOADING = 'loading'

        return self.execute_script('return document.readyState;') == PAGE_STATE_IS_LOADING
    
    @property
    def is_page_loaded(
        self
    ) -> bool:
        """
        Get the state of the current web page and return
        True if the page has been loaded.
        """
        PAGE_STATE_IS_COMPLETE = 'complete'

        return self.execute_script('return document.readyState;') == PAGE_STATE_IS_COMPLETE

    @property
    def current_page_y_offset(
        self
        # TODO: Set the type in the return, please
    ):
        """
        Get the current page Y axis offset by executing
        the 'return window.pageYOffset' script. This offset
        represents the amount of pixels moved from the origin
        (top). An offset of 50 pixels mean that the web page
        has been scrolled down 50 pixels. The minimum value
        is 0 when on top of the web page.
        """
        return self.execute_script('return window.pageYOffset')
    
    @property
    def page_height(
        self
        # TODO: Set the type in the return, please
    ):
        """
        Get the current page height by executing the
        'return document.body.scrollHeight' script.
        This means the amount of pixels from top to
        bottom.
        """
        return self.execute_script('return document.body.scrollHeight')
    
    @property
    def page_size(
        self
        # TODO: Set the type in the return, please
    ):
        """
        Get the current page size and return it as a
        (width, height) tuple, attending to the
        screen used within the web navigator.
        """
        size = self.driver.get_window_size()

        # TODO: Is this 'height' the same as 'page_height' (?)
        return (size['width'], size['height'])
    
    @property
    def cookies(
        self
    ):
        return self.driver.get_cookies()
    
    def __init__(
        self,
        do_use_gui: bool = False,
        do_use_ad_blocker: bool = True,
        do_disable_popups_and_cookies: bool = True,
        additional_options = [],
        max_page_load_waiting_time: float = 10
    ):
        # TODO: Make more customizable accepting ad_blocker extension name
        # and stuff like that
        self.do_use_gui = do_use_gui
        self.do_use_ad_blocker = do_use_ad_blocker
        self.do_disable_popups_and_cookies = do_disable_popups_and_cookies
        self.additional_options = additional_options
        self.max_page_load_waiting_time = max_page_load_waiting_time

        self._initialize_options()
        self._initialize_driver()

    def __del__(
        self
    ):
        # We force the driver to be closed to kill 
        # the task that would be running for nothing
        self._close()

    def _close(
        self
    ):
        """
        Force the driver to be closed and the 
        'self.driver' attribute to be None.

        For internal use only.
        """
        try:
            self.driver.close()
        finally:
            self.driver = None

    def _initialize_options(
        self
    ) -> Options:
        """
        Initializes the Google Chrome options and returns them.
        """
        if not self.options:
            # TODO: This must be dynamic and/or given by user
            CHROME_EXTENSIONS_ABSOLUTEPATH = 'C:/Users/dania/AppData/Local/Google/Chrome/User Data/Profile 2/Extensions/'
            # TODO: Extensions versions are updated, so check below line
            AD_BLOCK_ABSOLUTEPATH = CHROME_EXTENSIONS_ABSOLUTEPATH + 'cjpalhdlnbpafiamejdnhcphjbkeiagm/1.64.0_0'
            # TODO: What if 'import undetected_chromedriver.v2 as uc'? Try it

            options = Options()
            
            # TODO: Make this a dynamic option that can be passed through __init__
            option_arguments = ['window-size=1920,1080']
            # option_arguments = ['--start-maximized']

            if len(self.additional_options) > 0:
                for additional_option in self.additional_options:
                    option_arguments.append(additional_option)

            if not self.do_use_gui:
                option_arguments.append('--headless=new')

            if self.do_use_ad_blocker:
                # This loads the ad block 'uBlock' extension that is installed in my pc
                option_arguments.append('load-extension=' + AD_BLOCK_ABSOLUTEPATH)
            
            # Load user profile
            option_arguments.append('user-data-dir=C:/Users/dania/AppData/Local/Google/Chrome/User Data/Profile 2')

            # Ignore certs
            option_arguments.append('--ignore-certificate-errors')
            option_arguments.append('--ignore-ssl-errors')
            option_arguments.append('--ignore-certificate-errors-spki-list')

            for argument in option_arguments:
                options.add_argument(argument)

            if self.do_disable_popups_and_cookies:
                # TODO: Separate this into specific options, not all together. One is for cookies,
                # another one is for popups... Separate them, please
                # This disables popups, cookies and that stuff
                options.add_experimental_option('prefs', {
                    'excludeSwitches': ['enable-automation', 'load-extension', 'disable-popup-blocking'],
                    'profile.default_content_setting_values.automatic_downloads': 1,
                    'profile.default_content_setting_values.media_stream_mic': 1
                })

            self.options = options

        return self.options
    
    def _initialize_driver(
        self
    ):
        """
        Initializes the Google Chrome driver and returns it.
        """
        if not self.driver:
            self.driver = webdriver.Chrome(options = self.options)
            # We force to start a new session due to some problems
            #self.driver.start_session({})

        return self.driver
    
    def _validate_url(
        self,
        url: str
    ):
        """
        Validate the 'url' and raise an Exception if
        invalid.
        """
        ParameterValidator.validate_mandatory_string('url', url, do_accept_empty = False)
        
        """
        When using 'www.google.es' instead of
        'https://www.google.es' it raises an Exception
        showing this in the console:
        [9192:8160:0309/174912.456:ERROR:new_tab_page_handler.cc(1306)] NewTabPage loaded into a non-browser-tab context
        and setting self.driver = None

        Thats why we are validating with this specific
        url regexp.
        """
        if not GeneralRegularExpression.URL.is_valid_regex(url):
            raise Exception('The "url" provided is not a valid url.')

    def reload(
        self
    ) -> None:
        """
        Reload the current web page.
        """
        self.driver.refresh()

    def go_backward(
        self,
        times: int = 1
    ) -> None:
        """
        Go backwards 'times' times in the browser history.
        """
        ParameterValidator.validate_mandatory_positive_int('times', times, do_include_zero = False)

        for _ in range(times):
            self.driver.back()

    def go_forward(
        self,
        times: int = 1
    ) -> None:
        """
        Go forward 'times' times in the browser history.
        """
        ParameterValidator.validate_mandatory_positive_int('times', times, do_include_zero = False)

        for _ in range(times):
            self.driver.forward()

    def go_to_web_and_wait_until_loaded(
        self,
        url: str
    ):
        """
        Navigates to the provided 'url' and checks continuously
        if the page has been loaded or not. It will wait for
        'max_page_load_waiting_time' seconds set when the
        ChromeScraper object was created.

        This method will return True in the moment the page is 
        loaded.
        """
        self._validate_url(url)

        CHECK_TIME = 0.25

        try:
            self.driver.get(url)

            cont = 0
            while (
                not self.is_page_loaded and
                cont < (self.max_page_load_waiting_time / CHECK_TIME)
            ):
                time.sleep(CHECK_TIME)
                cont += 1

            return self.is_page_loaded

        except:
            self._close()

    def wait(
        self,
        seconds: float
    ):
        """
        Waits for the provided 'time' seconds. There is
        no limit in the waiting time, so please use it
        carefully.
        """
        ParameterValidator.validate_mandatory_positive_number('seconds', seconds, do_include_zero = False)

        time.sleep(seconds)

    def press_ctrl_letter(
        self,
        letter: str = 'c'
    ):
        """
        Holds the Ctrl key down, presses the provided 'letter' and 
        releases the Ctrl key. This is useful for Ctrl+C, Ctrl+V
        combinations.
        """
        ParameterValidator.validate_mandatory_string('letter', letter, do_accept_empty = False)
        
        ActionChains(self.driver).key_down(Keys.CONTROL).send_keys(letter[0]).key_up(Keys.CONTROL).perform()

    def press_ctrl_letter_on_element(
        self,
        letter: str,
        element: WebElement
    ):
        """
        Presses the Ctrl + provided 'letter' in the also provided
        'element'. Useful to paste text into text elements.
        """
        ParameterValidator.validate_mandatory_string('letter', letter, do_accept_empty = False)
        ParameterValidator.validate_mandatory_instance_of('element', element, WebElement)
        
        element.send_keys(Keys.CONTROL, letter[0])

    def press_ctrl_c(
        self
    ):
        self.press_ctrl_letter('c')

    def press_ctrl_c_on_element(
        self,
        element: WebElement
    ):
        ParameterValidator.validate_mandatory_instance_of('element', element, WebElement)

        self.press_ctrl_letter_on_element('c', element)

    def press_ctrl_x(
        self
    ):
        self.press_ctrl_letter('x')

    def press_ctrl_x_on_element(
        self,
        element: WebElement
    ):
        ParameterValidator.validate_mandatory_instance_of('element', element, WebElement)

        self.press_ctrl_letter_on_element('x', element)

    def press_ctrl_v(
        self
    ):
        self.press_ctrl_letter('v')

    def press_ctrl_v_on_element(
        self,
        element: WebElement
    ):
        ParameterValidator.validate_mandatory_instance_of('element', element, WebElement)

        self.press_ctrl_letter_on_element('v', element)

    def press_ctrl_a(
        self
    ):
        self.press_ctrl_letter('a')

    def press_ctrl_a_on_element(
        self,
        element: WebElement
    ):
        ParameterValidator.validate_mandatory_instance_of('element', element, WebElement)

        self.press_ctrl_letter_on_element('a', element)

    def press_key_x_times(
        self,
        key: Keys,
        times: int
    ):
        """
        Presses the provided 'key' 'times' times one behind
        the other one. This method is useful to use TAB,
        ENTER or keys like that a lot of times.
        """
        ParameterValidator.validate_mandatory_instance_of('key', key, Keys)
        ParameterValidator.validate_mandatory_positive_int('times', times, do_include_zero = False)

        actions_chain = ActionChains(self.driver)
        for _ in range(times):
            actions_chain.send_keys(key)

        actions_chain.perform()

    def find_element_by_id(
        self,
        id: str,
        element: Union[WebElement, None] = None
    ) -> Union[WebElement, None]:
        """
        This method returns the first WebElement found with
        the provided 'id' or None if not found.

        If you provide the 'element' parameter, the search will 
        be in that element instead of the whole web page.
        """
        ParameterValidator.validate_mandatory_string('id', id, do_accept_empty = False)
        ParameterValidator.validate_instance_of('element', element, WebElement)

        elements = self.find_elements_by_id(id, element)

        return (
            elements[0]
            if len(elements) > 0 else
            None
        )
    
    def find_element_by_id_waiting(
        self,
        id: str,
        time: int = 30
    ) -> Union[WebElement, None]:
        """
        Waits until the WebElement corresponding to the provided 
        'element_type' with also provided 'id' is visible and 
        returns it if it becomes visible in the 'time' seconds 
        of waiting. It returns None if not.
        """
        ParameterValidator.validate_mandatory_string('id', id, do_accept_empty = False)
        ParameterValidator.validate_mandatory_positive_int('time', time, do_include_zero = False)

        return self._find_element_by_waiting(By.ID, id, time)

    def find_elements_by_id(
        self,
        id: str,
        element: Union[WebElement, None] = None
    ) -> list[WebElement]:
        """
        This method returns an array containing the WebElements
        found with the provided 'id'.

        If you provide the 'element' parameter, the search will 
        be in that element instead of the whole web page.
        """
        ParameterValidator.validate_mandatory_string('id', id, do_accept_empty = False)
        ParameterValidator.validate_instance_of('element', element, WebElement)

        root = (
            element
            if element is not None else
            self.driver
        )

        return root.find_elements(By.ID, id)

    def find_element_by_text(
        self,
        # TODO: Create Enum for ElementType (.BUTTON, .INPUT, etc.)
        element_type: str,
        text: str,
        element: Union[WebElement, None] = None
    ) -> Union[WebElement, None]:
        """
        This method uses the 'By.XPATH' finding elements method
        with the '//element_type[contains(text(), 'text')]' 
        structure to find the element, useful for buttons that 
        have 'Save' text or things similar.

        You can use 'element_type' = 'button' and 'text' =
        'Guardar' to find the elements like this one:
        <button>Guardar</button>

        You can also use the wildcard '*'  to find any type of
        element with the specific provided 'text'.

        If you provide the 'element' parameter, the search will 
        be in that element instead of the whole web page.

        This method returns the first found WebElement if 
        existing or None if not found.
        """
        ParameterValidator.validate_mandatory_string('element_type', element_type, do_accept_empty = False)
        ParameterValidator.validate_mandatory_string('text', text, do_accept_empty = False)
        ParameterValidator.validate_instance_of('element', element, WebElement)

        elements = self.find_elements_by_text(element_type, text, element)
        
        return (
            elements[0]
            if len(elements) > 0 else
            None
        )

    def find_element_by_text_waiting(
        self,
        element_type: str,
        text: str,
        time: int = 30
    ) -> Union[WebElement, None]:
        """
        Waits until the WebElement corresponding to the provided 
        'element_type' and 'text' is visible and returns it if 
        it becomes visible in the 'time' seconds of waiting. It 
        returns None if not.
        """
        ParameterValidator.validate_mandatory_string('element_type', element_type, do_accept_empty = False)
        ParameterValidator.validate_mandatory_string('text', text, do_accept_empty = False)
        ParameterValidator.validate_mandatory_positive_int('time', time, do_include_zero = False)

        return self._find_element_by_waiting(
            By.XPATH,
            f"//{element_type}[contains(text(), '{text}')]",
            #"//" + element_type + "[contains(text(), '" + text + "')]",
            time
        )
    
    def find_elements_by_text(
        self,
        element_type: str,
        text: str,
        element: Union[WebElement, None] = None
    ) -> list[WebElement]:
        """
        This method uses the 'By.XPATH' finding elements method
        with the '//element_type[contains(text(), 'text')]' 
        structure to find the element, useful for buttons that 
        have 'Save' text or things similar.

        You can use 'element_type' = 'button' and 'text' =
        'Guardar' to find the elements like this one:
        <button>Guardar</button>

        You can also use the wildcard '*'  to find any type of
        element with the specific provided 'text'.

        If you provide the 'element' parameter, the search will 
        be in that element instead of the whole web page.

        This method returns an array with all the found elements
        or empty if not found.
        """
        ParameterValidator.validate_mandatory_string('element_type', element_type, do_accept_empty = False)
        ParameterValidator.validate_mandatory_string('text', text, do_accept_empty = False)
        ParameterValidator.validate_instance_of('element', element, WebElement)

        root = (
            element
            if element is not None else
            self.driver
        )

        return root.find_elements(
            By.XPATH,
            f"//{element_type}[contains(text(), '{text}')]"
        )
    
    def find_element_by_class(
        self,
        element_type: str,
        class_str: str,
        element: Union[WebElement, None] = None
    ) -> Union[WebElement, None]:
        """
        This method uses the 'By.XPATH' finding elements method
        with the '//element_type[contains(@class, 'class_str')]' 
        structure to find the element, useful for divs with a
        specific class or similar.

        You can use 'element_type' = 'div' and 'class_str' =
        'container-xl' to find the elements like this one:
        <div class='container-xl'>content</div>

        You can also use the wildcard '*'  to find any type of
        element with the specific provided 'class_str'.

        If you provide the 'element' parameter, the search will 
        be in that element instead of the whole web page.

        This method returns the first found WebElement if 
        existing or None if not found.
        """
        ParameterValidator.validate_mandatory_string('element_type', element_type, do_accept_empty = False)
        ParameterValidator.validate_mandatory_string('class_str', class_str, do_accept_empty = False)
        ParameterValidator.validate_instance_of('element', element, WebElement)

        elements = self.find_elements_by_class(element_type, class_str, element)
        
        return (
            elements[0]
            if len(elements) > 0 else
            None
        )
    
    def find_element_by_class_waiting(
        self,
        element_type: str,
        class_str: str,
        time: int = 30
    ) -> Union[WebElement, None]:
        """
        Waits until the WebElement corresponding to the provided 
        'element_type' and class is visible and returns it if it
        becomes visible in the 'time' seconds of waiting. It 
        returns None if not.
        """
        ParameterValidator.validate_mandatory_string('element_type', element_type, do_accept_empty = False)
        ParameterValidator.validate_mandatory_string('class_str', class_str, do_accept_empty = False)
        ParameterValidator.validate_mandatory_positive_int('time', time, do_include_zero = False)
        
        return self._find_element_by_waiting(
            By.XPATH,
            f"//{element_type}[contains(@class, '{class_str}')]",
            #"//" + element_type + "[contains(@class, '" + class_str + "')]",
            time
        )

    def find_elements_by_class(
        self,
        element_type: str,
        class_str: str,
        element: Union[WebElement, None] = None
    ) -> list[WebElement]:
        """
        This method uses the 'By.XPATH' finding elements method
        with the '//element_type[contains(@class, 'class_str')]' 
        structure to find the element, useful for divs with a
        specific class or similar.

        You can use 'element_type' = 'div' and 'class_str' =
        'container-xl' to find the elements like this one:
        <div class='container-xl'>content</div>

        You can also use the wildcard '*'  to find any type of
        element with the specific provided 'class_str'.

        If you provide the 'element' parameter, the search will 
        be in that element instead of the whole web page.

        This method returns an array with all the found elements
        or empty if not found.
        """
        ParameterValidator.validate_mandatory_string('element_type', element_type, do_accept_empty = False)
        ParameterValidator.validate_mandatory_string('class_str', class_str, do_accept_empty = False)
        ParameterValidator.validate_instance_of('element', element, WebElement)

        root = (
            element
            if element is not None else
            self.driver
        )

        return root.find_elements(
            By.XPATH,
            f"//{element_type}[contains(@class, '{class_str}')]"
        )

    def find_element_by_custom_tag(
        self,
        element_type: str,
        custom_tag: str,
        custom_tag_value: str,
        element: Union[WebElement, None] = None
    ) -> Union[WebElement, None]:
        """
        This method uses the 'By.XPATH' finding elements method
        with the '//element_type[@custom-tag='custom_value')]' 
        structure to find the element, useful for divs with a
        specific tag or similar.

        You can use the wildcard '*'  to find any type of
        element with the specific provided 'custom_tag'.

        If you provide the 'element' parameter, the search will 
        be in that element instead of the whole web page.

        This method returns the first found WebElement if 
        existing or None if not found.
        """
        ParameterValidator.validate_mandatory_string('element_type', element_type, do_accept_empty = False)
        ParameterValidator.validate_mandatory_string('custom_tag', custom_tag, do_accept_empty = False)
        ParameterValidator.validate_mandatory_string('custom_tag_value', custom_tag_value, do_accept_empty = True)
        ParameterValidator.validate_instance_of('element', element, WebElement)

        elements = self.find_elements_by_custom_tag(element_type, custom_tag, custom_tag_value, element)
        
        return (
            elements[0]
            if len(elements) > 0 else
            None
        )

    def find_element_by_custom_tag_waiting(
        self,
        element_type: str,
        custom_tag: str,
        custom_tag_value: str,
        time: int = 30
    ) -> Union[WebElement, None]:
        """
        Waits until the WebElement corresponding to the provided 
        'element_type' and custom tag is visible and returns it 
        if it becomes visible in the 'time' seconds of waiting.
        It returns None if not.
        """
        ParameterValidator.validate_mandatory_string('element_type', element_type, do_accept_empty = False)
        ParameterValidator.validate_mandatory_string('custom_tag', custom_tag, do_accept_empty = False)
        ParameterValidator.validate_mandatory_string('custom_tag_value', custom_tag_value, do_accept_empty = True)
        ParameterValidator.validate_mandatory_positive_int('time', time, do_include_zero = False)

        tag = (
            f'@{custom_tag}'
            if custom_tag_value == '' else
            f"@{custom_tag}='{custom_tag_value}'"
        )

        return self._find_element_by_waiting(
            By.XPATH,
            f'//{element_type}[{tag}]',
            #"//" + element_type + "[" + tag + "]"
            time
        )

    def find_elements_by_custom_tag(
        self,
        element_type: str,
        custom_tag: str,
        custom_tag_value: str,
        element: Union[WebElement, None] = None
    ) -> list[WebElement]:
        """
        This method uses the 'By.XPATH' finding elements method
        with the '//element_type[@custom-tag='custom_value')]' 
        structure to find the element, useful for divs with a
        specific tag or similar.

        You can use the wildcard '*'  to find any type of
        element with the specific provided 'custom_tag'.
        
        If you provide the 'element' parameter, the search will 
        be in that element instead of the whole web page.

        This method returns an array with all the found elements
        or empty if not found.
        """
        ParameterValidator.validate_mandatory_string('element_type', element_type, do_accept_empty = False)
        ParameterValidator.validate_mandatory_string('custom_tag', custom_tag, do_accept_empty = False)
        ParameterValidator.validate_mandatory_string('custom_tag_value', custom_tag_value, do_accept_empty = True)
        ParameterValidator.validate_instance_of('element', element, WebElement)

        # @custom-tag or @custom-tag='something'
        tag = (
            f'@{custom_tag}'
            if custom_tag_value == '' else
            f"@{custom_tag}='{custom_tag_value}'"
        )
        
        root = (
            element
            if element is not None else
            self.driver
        )

        return root.find_elements(
            By.XPATH,
            f'//{element_type}[{tag}]'
        )

    def find_element_by_element_type(
        self,
        element_type: str,
        element: Union[WebElement, None] = None
    ) -> Union[WebElement, None]:
        """
        Returns the elements found with the provided 'element_type' tag, that
        is the tag name ('span', 'div', etc.). If you provide the 'element' 
        parameter, the search will be in that element instead of the whole
        web page.
        """
        ParameterValidator.validate_mandatory_string('element_type', element_type, do_accept_empty = False)
        ParameterValidator.validate_instance_of('element', element, WebElement)

        elements = self.find_elements_by_element_type(element_type, element)
        
        return (
            elements[0]
            if len(elements) > 0 else
            None
        )
    
    def find_element_by_element_type_waiting(
        self,
        element_type: str,
        time: int = 30
    ) -> Union[WebElement, None]:
        """
        Waits until the WebElement corresponding to the provided 
        'element_type' tag is visible and returns it if it becomes
        visible in the 'time' seconds of waiting. It returns None
        if not.
        """
        ParameterValidator.validate_mandatory_string('element_type', element_type, do_accept_empty = False)
        ParameterValidator.validate_mandatory_positive_int('time', time, do_include_zero = False)
        
        return self._find_element_by_waiting(
            By.TAG_NAME,
            element_type,
            time
        )
        
    def find_elements_by_element_type(
        self,
        element_type: str,
        element: Union[WebElement, None] = None,
        do_search_only_in_first_level: bool = False
    ) -> list[WebElement]:
        """
        Returns the web elements with the provided 'element_type' tag. 
        This method will search in the 'element' if provided, or in 
        the whole web page if not. It will look for elements only on
        the first level y 'only_first_level' is True, or in any level
        if False.

        If 'do_search_only_in_first_level' is True, this will look
        only in the first child level, horizontally, so a child of
        a child tag won't be returned.
        """
        ParameterValidator.validate_mandatory_string('element_type', element_type, do_accept_empty = False)
        ParameterValidator.validate_instance_of('element', element, WebElement)
        ParameterValidator.validate_mandatory_bool('do_search_only_in_first_level', do_search_only_in_first_level)
        
        root = (
            self.driver
            if element is None else
            element
        )

        element_type = (
            f'./{element_type}'
            if do_search_only_in_first_level else
            element_type
        )

        return root.find_elements(
            By.XPATH,
            element_type
        )
    
    def find_element_by_xpath_waiting(
        self,
        xpath: str,
        time: int = 30
    ) -> Union[WebElement, None]:
        """
        Waits until the WebElement corresponding to the provided 'xpath'
        is visible and returns it if it becomes visible in the 'time' 
        seconds of waiting. It returns None if not.
        """
        ParameterValidator.validate_mandatory_string('xpath', xpath, do_accept_empty = False)
        ParameterValidator.validate_mandatory_positive_int('time', time, do_include_zero = False)

        return self._find_element_by_waiting(
            By.XPATH,
            xpath,
            time
        )
    
    def find_elements_by_xpath(
        self,
        xpath: str,
        element: Union[WebElement, None] = None
    ) -> list[WebElement]:
        """
        This method uses the 'By.XPATH' finding elements method.

        If you provide the 'element' parameter, the search will 
        be in that element instead of the whole web page.

        This method returns an array with all the found elements
        or empty if not found.
        """
        ParameterValidator.validate_mandatory_string('xpath', xpath, do_accept_empty = False)
        ParameterValidator.validate_instance_of('element', element, WebElement)

        root = (
            self.driver
            if element is None else
            element
        )

        return root.find_elements(
            By.XPATH,
            xpath
        )
    
    def _find_element_by_waiting(
        self,
        by: By,
        by_value: str,
        time: int = 30
    ) -> Union[WebElement, None]:
        """
        Internal method to simplify the waiting for element until visible
        code reusability.
        """
        wait = WebDriverWait(self.driver, time)
        element = wait.until(EC.visibility_of_element_located((by, by_value)))

        return (
            None
            if not element else
            element
        )
    
    # TODO: When an element is hidden and you cannot interact you
    # can change the style.display
    # driver.execute_script("arguments[0].style.display = 'block';", field)

    def set_file_input(
        self,
        element: WebElement,
        abspath: str
    ):
        """
        Sends the file to a 'type=file' input web element. The 
        provided 'abspath' must be the absolute path to the file
        you want to send.
        """
        ParameterValidator.validate_mandatory_instance_of('element', element, WebElement)
        ParameterValidator.validate_mandatory_string('abspath', abspath, do_accept_empty = False)
        
        # TODO: Check that it is a valid abspath

        element.send_keys(abspath)
    
    def scroll_down(
        self,
        pixels: int
    ):
        """
        Scrolls down the web page the amount of 'pixels' provided
        as parameter from the current position. This method will
        make a passive waiting until the new position is reached.
        """
        ParameterValidator.validate_mandatory_int('pixels', pixels)

        pixels = abs(pixels) + self.current_page_y_offset

        self.execute_script(f'window.scrollTo(0, {str(pixels)})')

        # We wait until movement is completed
        waiting_times = 300
        while (
            self.current_page_y_offset != pixels and
            waiting_times > 0
        ):
            self.wait(0.1)
            waiting_times -= 1

    def scroll_up(
        self,
        pixels: int
    ):
        """
        Scrolls up the web page the amount of 'pixels' provided
        as parameter from the current position. This method will
        make a passive waiting until the new position is reached.
        """
        ParameterValidator.validate_mandatory_int('pixels', pixels)

        pixels = abs(pixels)
        current_y = self.current_page_y_offset

        pixels = current_y - pixels
        if pixels < 0:
            pixels = 0

        self.execute_script(f'window.scrollTo(0, {str(pixels)}')

        waiting_times = 300
        while (
            self.current_page_y_offset != pixels and
            waiting_times > 0
        ):
            self.wait(0.1)
            waiting_times -= 1

    def scroll_to_element(
        self,
        element: WebElement
    ):
        """
        This method scrolls to 50 pixels above the web element
        to make sure it is on the middle of the web page. This
        is very useful to take screenshots. This method will
        make a passive waiting until the new position is 
        reached.
        """
        ParameterValidator.validate_mandatory_instance_of('element', element, WebElement)

        element_y = element.location['y']
        y = (
            element_y - 50
            if element_y > 50 else
            0
        )

        self.execute_script(f'window.scrollTo(0, {str(y)}')

        # We wait until movement is completed
        waiting_times = 300
        while (
            self.current_page_y_offset != y and
            waiting_times > 0
        ):
            self.wait(0.1)
            waiting_times -= 1

    def screenshot(
        self,
        output_filename: str = None
    ):
        """
        Takes a screenshot of the whole page and returns the 
        it as binary data if no 'output_filename' provided. 
        If 'output_filename' is provided, it will be stored 
        locally with that name.
        """
        # TODO: Make this method return the image as binary
        # data always and store if 'output_filename' is 
        # provided, but you cannot do the 'save_screenshot'
        # twice because the webpage can change in the time
        # elapsed between both screenshots.
        if not output_filename:
            return self.driver.get_screenshot_as_png()
        
        self.driver.save_screenshot(output_filename)

        return output_filename
    
    def screenshot_element(
        self,
        element: WebElement,
        output_filename: str = None
    ):
        """
        Takes a screenshot of the provided 'element', that
        means that only the area occupied by that element
        is shown in the screenshot, and returns it as 
        binary data if no 'output_filename' provided or
        will be stored locally if provided.

        Any element of the web page that is over the 
        element will appear in the screenshot blocking it.

        This method will return the 'output_filename' if it
        was provided, so the file has been stored locally,
        or a dict containing 'size' (width, height) and 
        'data' fields.
        """
        # TODO: Make this method return the image as binary
        # data always and store if 'output_filename' is 
        # provided, but you cannot do the 'save_screenshot'
        # twice because the webpage can change in the time
        # elapsed between both screenshots.
        ParameterValidator.validate_mandatory_instance_of('element', element, WebElement)
        
        if not output_filename:
            return element.screenshot_as_png
        
        element.screenshot(output_filename)

        return output_filename

    def screenshot_web_page(
        self,
        url: Union[str, None] = None
    ):
        """
        This method will take screenshots of the whole
        web page. It will do in the current page if
        no 'url' is provided, or will navigate to the
        provided 'url' and do it in that one.
        """
        ParameterValidator.validate_string('url', url, do_accept_empty = False)

        if url:
            self.go_to_web_and_wait_until_loaded(url)

        # TODO: Screenshot the whole page
        FPS = 60
        # Maybe this should be a parameter
        # TODO: We want to make screenshots for a video
        # so depending on 'duration' it will be slower
        # or more dynamic. This method need testing
        duration = 5

        # TODO: Maybe we want to scroll more, or maybe
        # we should pass this a parameter to make it
        # more customizable
        page_height = self.page_height
        if page_height > 1000:
            page_height = 1000

        screenshots = []
        number_of_screenshots = int(duration * FPS)
        window_size = self.driver.get_window_size()

        # TODO: How much should we scroll?
        new_height = 0
        for i in range(number_of_screenshots):
            screenshots.append(self.driver.get_screenshot_as_png())
            height = self.current_page_y_offset
            new_height += page_height / number_of_screenshots
            # We scroll down the difference
            self.scroll_down(new_height - height)

        # TODO: What if we end before

        return screenshots

    def execute_script(
        self,
        script: str,
        *args
    ) -> any:
        """
        Executes the provided 'script' synchronously with
        the given 'args' if provided.
        """
        ParameterValidator.validate_mandatory_string('script', script, do_accept_empty = False)
        
        return self.driver.execute_script(script, *args)

    def remove_element(
        self,
        element: WebElement
    ):
        ParameterValidator.validate_mandatory_instance_of('element', element, WebElement)
        
        self.execute_script('arguments[0].remove()', element)
    
    def set_element_width(
        self,
        element: WebElement,
        width: int
    ):
        ParameterValidator.validate_mandatory_instance_of('element', element, WebElement)
        ParameterValidator.validate_mandatory_int('width', width)
        ParameterValidator.validate_mandatory_positive_int('width', width, do_include_zero = False)
        
        self.execute_script(f'arguments[0].style = "width: {str(width)}px;"', element)

    def set_element_style(
        self,
        element: WebElement,
        style: str
    ):
        ParameterValidator.validate_mandatory_instance_of('element', element, WebElement)
        ParameterValidator.validate_mandatory_string('style', style, do_accept_empty = False)
        
        self.execute_script(f"arguments[0].style = '{style}'", element)

    def set_element_attribute(
        self,
        element: WebElement,
        attribute: str,
        value: str
    ):
        ParameterValidator.validate_mandatory_instance_of('element', element, WebElement)
        ParameterValidator.validate_mandatory_string('attribute', attribute, do_accept_empty = False)
        ParameterValidator.validate_mandatory_string('value', value, do_accept_empty = False)
        
        self.execute_script(f"arguments[0].setAttribute('{attribute}', '{value}')", element)

    def set_element_inner_text(
        self,
        element: WebElement,
        inner_text: str
    ):
        """
        Sets the provided 'inner_text' in the also provided 'element'
        by applying the script 'element.innerText = "inner_text";'.
        """
        ParameterValidator.validate_mandatory_instance_of('element', element, WebElement)
        ParameterValidator.validate_mandatory_string('inner_text', inner_text, do_accept_empty = True)

        self.execute_script(f"arguments[0].innerText = '{str(inner_text)}';", element)

    def set_page_size(
        self,
        width: int = 1920,
        height: int = 1080
    ):
        """
        This method resizes the web navigator to the provided
        width and height. It is useful to take screenshots from
        webpages or to validate different screen sizes.
        """
        ParameterValidator.validate_mandatory_int('width', width, do_include_zero = False)
        ParameterValidator.validate_positive_int('width', width, do_include_zero = False)
        ParameterValidator.validate_mandatory_int('height', height)
        ParameterValidator.validate_positive_int('height', height, do_include_zero = False)

        self.driver.set_window_size(width, height)

    def add_to_clipboard(
        self,
        text: str
    ):
        """
        Adds the provided 'text' to the clipboard to be able to 
        paste it. This method will create a 'textarea' element,
        write the provided 'text' and copy it to the web
        scrapper clipboard.
        """
        ParameterValidator.validate_mandatory_string('text', text, do_accept_empty = True)

        TEXT_AREA_ID = 'textarea_to_copy_912312' # a random one
        # I create a new element to put the text, copy it and be able to paste
        js_code = "var p = document.createElement('textarea'); p.setAttribute('id', '" + TEXT_AREA_ID + "'); p.value = '" + text + "'; document.getElementsByTagName('body')[0].appendChild(p);"
        self.execute_script(js_code)

        # Focus on textarea
        textarea = self.find_element_by_id(TEXT_AREA_ID)
        textarea.click()
        self.press_ctrl_a_on_element(textarea)
        self.press_ctrl_c_on_element(textarea)
        # TODO: I can use 'textarea.send_keys(Keys.CONTROL, 'c') to copy, validate
        # actions.key_down(Keys.CONTROL).send_keys('A').key_up(Keys.CONTROL).perform()
        # actions.key_down(Keys.CONTROL).send_keys('C').key_up(Keys.CONTROL).perform()

        # Remove the textarea, it is no longer needed
        js_code = "var element = document.getElementById('" + TEXT_AREA_ID + "'); element.parentNode.removeChild(element);"
        # TODO: Update this with the new version
        self.execute_script(js_code)

    # TODO: Maybe automate some 'execute_javascript' to change
    # 'innerHTML' and that stuff (?)



# TODO: Remove all this below when all refactored.
# By now I'm commenting them
# def download_fake_call_image(name, output_filename):
#     # TODO: Move this to the faker
#     URL = 'https://prankshit.com/fake-iphone-call.php'

#     try:
#         driver = start_chrome()
#         go_to_and_wait_loaded(driver, URL)

#         inputs = driver.find_elements(By.TAG_NAME, 'input')
#         name_textarea = driver.find_element(By.TAG_NAME, 'textarea')

#         #operator_input = inputs[4]
#         #hour_input = inputs[5]

#         name_textarea.clear()
#         name_textarea.send_keys(name)

#         image = driver.find_element(By.XPATH, '//div[contains(@class, "modal-content tiktok-body")]')
#         image.screenshot(output_filename)
#     finally:
#         driver.close()

# # Other fake generators (https://fakeinfo.net/fake-twitter-chat-generator) ad (https://prankshit.com/fake-whatsapp-chat-generator.php)
# def download_discord_message_image(text, output_filename):
#     URL = 'https://message.style/app/editor'

#     try:
#         driver = start_chrome()
#         go_to_and_wait_loaded(driver, URL)
        
#         time.sleep(3)

#         clear_embed_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Clear Embeds')]")
#         clear_embed_button.click()

#         time.sleep(3)

#         input_elements = driver.find_elements(By.TAG_NAME, 'input')
#         username_input = input_elements[3]
#         avatar_url_input = input_elements[4]

#         username_input.clear()
#         username_input.send_keys('botsito')

#         avatar_url_input.clear()
#         avatar_url_input.send_keys('https://cdn.pixabay.com/photo/2016/11/18/23/38/child-1837375_640.png')

#         textarea_input = driver.find_element(By.TAG_NAME, 'textarea')
#         textarea_input.clear()
#         textarea_input.send_keys(text)

#         time.sleep(3)

#         # get element div class='discord-message'
#         discord_message = driver.find_element(By.XPATH, "//div[contains(@class, 'discord-message')]")
#         discord_message.screenshot(output_filename)
#     finally:
#         driver.close()



# def test_download_piano_music():
#     # TODO: End this, to make it download music generated by this AI
#     try:
#         options = Options()
#         #option_arguments = ['--start-maximized', '--headless=new']
#         option_arguments = ['--start-maximized']
#         for argument in option_arguments:
#             options.add_argument(argument)

#         driver = webdriver.Chrome(options = options)
#         driver.get('https://huggingface.co/spaces/mrfakename/rwkv-music')
#         wait = WebDriverWait(driver, 30)
#         download_button_element = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@data-testid=\"checkbox\"]')))

#         time.sleep(5)
#         actions = ActionChains(driver)
#         for i in range(11):
#             actions.send_keys(Keys.TAB)
#         actions.perform()
#         actions.send_keys(Keys.SPACE)
#         actions.perform()

#         input_number_element = driver.find_elements_by_xpath('//*[@data-testid="number-input"]')[0]
#         input_number_element.send_keys(14286)

#         actions = ActionChains(driver)
#         actions.send_keys(Keys.TAB)
#         actions.perform()

#         time.sleep(1)

#         driver.execute_script('window.scrollTo(0, 1000)')

#         time.sleep(4)

#         download_button_element = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@title=\"Download\"]')))
#         #download_button_element = driver.find_elements_by_xpath('//*[@title="Download"]')[0]
#         download_button_element.click()

#     finally:
#         driver.close()


# # TODO: Move this method below to the main class
# def get_redicted_url(url, expected_url = None, wait_time = 5):
#     """
#     Navigates to the provided url and waits for a redirection. This method will wait
#     until the 'expected_url' is contained in the new url (if 'expected_url' parameter
#     is provided), or waits 'wait_time' seonds to return the current_url after that.
#     """
#     redirected_url = ''

#     try:
#         options = Options()
#         options.add_argument("--start-maximized")
#         # Remove this line below for debug
#         options.add_argument("--headless=new") # for Chrome >= 109
#         driver = webdriver.Chrome(options = options)
#         driver.get(url)

#         wait = WebDriverWait(driver, 10)

#         if not expected_url:
#             time.sleep(wait_time)
#         else:
#             wait.until(EC.url_contains(expected_url))

#         redirected_url = driver.current_url
#     finally:
#         driver.close()

#     return redirected_url


# def get_youtube_summary(video_id):
#     """
#     Searchs into 'summarize.tech' web to obtain the summary of the video with the 
#     provided 'video_id'. This method returns the summary in English, as it is 
#     provided by that website.
#     """
#     url = f'https://www.summarize.tech/www.youtube.com/watch?v={video_id}'

#     try:
#         options = Options()
#         options.add_argument("--start-maximized")
#         # Remove this line below for debug
#         options.add_argument("--headless=new") # for Chrome >= 109
#         driver = webdriver.Chrome(options = options)
#         driver.get(url)

#         summary = driver.find_element_by_tag_name('section').find_element_by_tag_name('p').get_attribute('innerText')
#     finally:
#         driver.close()

#     return summary

def google_translate(text, input_language = 'en', output_language = 'es') -> str:
    url = 'https://translate.google.com/?hl=es'
    """
    https://translate.google.com/?hl=es&sl=en&tl=es&text=Aporta%20una%20unidad%20de%20traducci%C3%B3n%20(segmento%20y%20traducci%C3%B3n)%20en%20alg%C3%BAn%20par%20de%20idiomas%20a%20MyMemory.%0ASin%20especificar%20ning%C3%BAn%20par%C3%A1metro%20clave%2C%20la%20contribuci%C3%B3n%20est%C3%A1%20disponible%20para%20todos%20(%C2%A1Gracias!).&op=translate

    https://translate.google.com/?hl=es&tab=TT&sl=en&tl=es&op=translate

    https://translate.google.com/?hl=es&tab=TT&sl=en&tl=es&text=La%20%C3%BAnica%20forma%20de%20saberlo%20es%20lo%20que%20t%C3%BA%20digas&op=translate
    """

    url = 'https://translate.google.com/?hl=' + output_language + '&tab=TT&sl=' + input_language + '&tl=' + output_language + '&text=' + text + '&op=translate'

    translation = ''

    # TODO: Verify that this below is working
    driver = ChromeScraper()
    driver.go_to_web_and_wait_until_loaded(url)
    translation = driver.find_element_by_xpath_waiting('//*[@jscontroller="JLEx7e"]', 10).get_attribute('innerText')
    # TODO: Maybe make a method to obtain the inner text from a WebElement (?)
    return translation

    # TODO: Refactor this as we have a better chrome driver lib now
    try:
        options = Options()
        options.add_argument("--start-maximized")
        # Comment this line below for debug (enables GUI)
        options.add_argument("--headless=new") # for Chrome >= 109
        driver = webdriver.Chrome(options = options)
        driver.get(url)

        tries = 0
        while True:
            if tries < 20:
                try:
                    # We try until it doesn't fail (so we have the text)
                    # TODO: This 'jscontroller' changes from time to time, pay atention
                    translation = driver.find_elements('xpath', '//*[@jscontroller="JLEx7e"]')[0].get_attribute('innerText')
                    tries = 20
                except Exception as e:
                    # TODO: Uncomment this to see if code error or scrapper error
                    #print(e)
                    tries += 1
                    time.sleep(0.250)
            else:
                break
    finally:
        driver.close()

    return translation

    """
    # Intersting options: https://github.com/ultrafunkamsterdam/undetected-chromedriver/issues/1726
    # Also this: https://stackoverflow.com/questions/19211006/how-to-enable-cookies-in-chromedriver-with-webdriver
    # What about this: options.AddUserProfilePreference("profile.cookie_controls_mode", 0);
    """