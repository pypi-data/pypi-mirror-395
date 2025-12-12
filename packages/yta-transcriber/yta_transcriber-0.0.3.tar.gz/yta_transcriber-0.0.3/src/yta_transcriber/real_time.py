from yta_transcriber.web import TRANSCRIBER_HTML_ABSPATH, download_web_file
from yta_text import TextFinder, TextHandler
from yta_web_scraper.chrome import ChromeScraper
from yta_validation.parameter import ParameterValidator
from typing import Union

import time


class WebRealTimeAudioTranscriptor:
    """
    Class to wrap a functionality related to real
    time audio transcription by using a web scraper.

    This class uses local files to create a simple
    web page that uses the chrome speech recognition
    to get the transcription.
    """

    _LOCAL_URL: str = f'file:///{TRANSCRIBER_HTML_ABSPATH}'
    _REMOTE_URL: str = 'https://iridescent-pie-f24ff0.netlify.app/'
    _WAITING_TIME: float = 0.1
    """
    The url to our local web page file.
    """
    max_time_to_wait: Union[float, None]
    """
    The maximum time the software will be waiting
    to detect an audio transcription before exiting
    with an empty result.
    """
    time_to_stop: float
    """
    The time that has to be spent once a final
    transcription has been found to consider it
    as a definitive one. There can be more final
    transcriptions after that one due to some 
    logic that I still don't understand properly.
    """
    do_use_local_web_page: bool
    """
    Flag that indicates if the resource must be a
    local web page (that will be loaded from a file
    in our system) or from a remote url.
    """

    def __init__(
        self,
        max_time_to_wait: Union[float, None] = 15.0,
        time_to_stop: float = 1.5,
        do_use_local_web_page: bool = True
    ):
        ParameterValidator.validate_positive_float('max_time_to_wait', max_time_to_wait, do_include_zero = True)
        ParameterValidator.validate_mandatory_float('time_to_stop', time_to_stop)
        ParameterValidator.validate_positive_float('time_to_stop', time_to_stop, do_include_zero = False)

        self.scraper = ChromeScraper()
        self.max_time_to_wait = (
            9999 # TODO: This is risky if no microphone or something
            if (
                max_time_to_wait == 0 or
                max_time_to_wait is None
            ) else
            max_time_to_wait
        )
        self.time_to_stop = time_to_stop
        self.do_use_local_web_page = do_use_local_web_page

        if self.do_use_local_web_page:
            # We need to make sure the file exist
            download_web_file()

        self._load()

    @property
    def url(
        self
    ) -> str:
        """
        The url that must be used to interact with the
        web page that is able to catch the audio and to
        transcribe it.
        """
        return (
            self._LOCAL_URL
            if self.do_use_local_web_page else
            self._REMOTE_URL
        )
    
    @property
    def is_listening(
        self
    ) -> bool:
        """
        Indicate if the microphone is activated and the
        web page is listening to the user's speech.
        """
        self._toggle_narration_button.text == 'Click to stop'

    @property
    def _toggle_narration_button(
        self
    ) -> 'WebElement':
        """
        Get the main narration button WebElement.
        """
        return self.scraper.find_element_by_id('toggle')
    
    @property
    def _reset_narration_button(
        self
    ) -> 'WebElement':
        """
        Get the reset narration button WebElement.
        """
        return self.scraper.find_element_by_id('reset_button')

    @property
    def _final_transcription_paragraph(
        self
    ) -> 'WebElement':
        """
        Get the final transcription paragraph WebElement.
        """
        return self.scraper.find_element_by_id('final_transcription')

    @property
    def _temp_transcription_paragraph(
        self
    ) -> 'WebElement':
        """
        Get the temporary transcription paragraph WebElement.
        """
        return self.scraper.find_element_by_id('temp_transcription')

    def _load(
        self
    ):
        """
        Navigates to the web page when not yet on it.

        For internal use only.
        """
        if self.scraper.current_url != self.url:
            self.scraper.go_to_web_and_wait_until_loaded(self.url)

    def reload(
        self
    ):
        """
        Force a refresh in the web page to reload it.
        """
        #self.scraper.reload()
        # Force to wait until completely loaded
        self.scraper.go_to_web_and_wait_until_loaded(self.url)

    def get_transcription(
        self
    ) -> str:
        """
        Get the text that has been transcripted from the
        audio.
        """
        self._load()

        return self._final_transcription_paragraph.text
    
    def empty_transcription(
        self
    ) -> None:
        """
        Set the definitive transcription as an empty
        string.
        """
        self._load()

        self.scraper.set_element_inner_text(
            self._final_transcription_paragraph,
            ''
        )
    
    def get_temp_transcription(
        self
    ) -> str:
        """
        Get the text that has been temporary transcripted 
        from the audio but is not still definitive.
        """
        self._load()

        return self._temp_transcription_paragraph.text

    def _get_number_of_results(
        self
    ) -> int:
        """
        Get the amount of results that have been detected
        until the moment in which it is requested. This
        count is needed to check if the user is still
        talking or not.
        """
        self._load()

        return int(self.scraper.find_element_by_id('number_of_results').text)
    
    def activate_transcription(
        self
    ) -> None:
        """
        Click the toggle button to activate the narration
        if it is not listening.
        """
        self._load()
        
        if not self.is_listening:
            self._toggle_narration_button.click()

    def deactivate_transcription(
        self
    ) -> None:
        """
        Click the toggle button to deactivate the
        narration if it is listening.
        """
        self._load()
        
        if self.is_listening:
            self._toggle_narration_button.click()

    def reset_transcription(
        self
    ) -> None:
        """
        Click the reset button that aborts the
        recognition and resets the engine instance
        so the microphone is still active but 
        ignoring the previous context and removing
        the temporary transcription text (but not
        the definitive).
        """
        self._load()

        self._reset_narration_button.click()

    def is_text_in_temporary_transcription(
        self,
        text: str
    ) -> bool:
        """
        Check if the given 'text' has been said by looking
        for in the temporary transcription.
        """
        return len(TextFinder.find_in_text(
            text,
            self.get_temp_transcription()
        )) > 0

    def is_text_in_definitive_transcription(
        self,
        text: str
    ) -> bool:
        """
        Check if the given 'text' has been said by looking
        for in the definitive transcription.
        """
        return len(TextFinder.find_in_text(
            text,
            self.get_transcription()
        )) > 0

    def is_text_in_transcription(
        self,
        text: str
    ) -> bool:
        """
        Check if the given 'text' has been said by looking
        for in the temporary and definitive transcription.
        """
        return (
            self.is_text_in_temporary_transcription(text) or
            self.is_text_in_definitive_transcription(text)
        )

    def detect_text(
        self,
        text: str
    ) -> bool:
        """
        Detect the given 'text' in the temporary or
        definitive audio transcription.
        
        This method doesn't load the web page nor click
        any button, it has to be made manually.
        """
        final_transcription = self.get_transcription()
        temp_transcription = self.get_temp_transcription()

        while (
            len(TextFinder.find_in_text(text, final_transcription)) == 0 and
            len(TextFinder.find_in_text(text, temp_transcription)) == 0
            # TODO: Append a time limit please
        ):
            time.sleep(self._WAITING_TIME)
            final_transcription = self.get_transcription()
            temp_transcription = self.get_temp_transcription()

        return True

    def detect_fast(
        self,
        text: str
    ) -> bool:
        """
        This method will load the web page and will
        activate the audio transcription and check
        the temporary results until the provided 
        'text' appears, and a True will be 
        inmediately returned in that case.

        This is called 'detect_fast' because of
        the way the web pages processed the audio
        narration. Temporary results are detected
        almost as fast as the user speaks, but the
        definitive ones last a few seconds to 
        appear. This will be checking the temporary
        results, thats why it is fast.

        TODO: By now, the 'text' is forced to be
        lowercase and without any exclamation mark,
        comma, etc.
        """
        # TODO: Refactor and improve the way we handle
        # this by checking '.', ',', etc.
        # Text must be lowercase with accents
        text = TextHandler.remove_non_ascii_characters(text.lower(), do_remove_accents = True)

        self.activate_transcription()

        final_transcription = self.get_transcription()
        temp_transcription = self.get_temp_transcription()

        while (
            len(TextFinder.find_in_text(text, final_transcription)) == 0 and
            len(TextFinder.find_in_text(text, temp_transcription)) == 0
            # TODO: Append a time limit please
        ):
            time.sleep(self._WAITING_TIME)
            final_transcription = self.get_transcription()
            temp_transcription = self.get_temp_transcription()

        self.deactivate_transcription()

        return True
    
    def transcribe(
        self
    ) -> str:
        """
        A web scraper instance loads the internal web
        that uses the Chrome speech recognition to get
        the audio transcription, by pressing the
        button, waiting for audio input through the
        microphone, and pressing the button again.

        If the page was previously loaded it won't be
        loaded again.

        This method will wait until no new temporary
        nor definitive results are being analyzed and
        returned to the web page, and will return the
        last definitive result found.
        """
        self.activate_transcription()

        time_elapsed = 0
        final_transcription_time_elapsed = 0
        transcription = ''
        number_of_results = 0
        while (
            time_elapsed < self.max_time_to_wait and
            (
                (
                    final_transcription_time_elapsed != 0 and
                    (final_transcription_time_elapsed + self.time_to_stop) > time_elapsed
                ) or
                final_transcription_time_elapsed == 0
            )
        ):
            tmp_final_transcription = self.get_transcription()
            tmp_number_of_results = self._get_number_of_results()
            """
            If temporary transcription is changing,
            we are still getting audio transcripted
            so we need to keep waiting for the 
            final transcription. We are indicating
            the amount of words detected, so if that
            number keeps increasing, we need to keep
            waiting.
            """
            if (
                tmp_number_of_results > number_of_results or
                tmp_final_transcription != transcription
            ):
                # If final transcription has changed or the
                # amount of events keeps increasing, we 
                # keep waiting
                final_transcription_time_elapsed = time_elapsed

                if tmp_number_of_results > number_of_results:
                    number_of_results = tmp_number_of_results

                if tmp_final_transcription != transcription:
                    transcription = tmp_final_transcription
                
            time.sleep(self._WAITING_TIME)
            time_elapsed += self._WAITING_TIME

        self.deactivate_transcription()

        return transcription
