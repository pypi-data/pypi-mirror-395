from yta_web_scraper.chrome import google_translate
from yta_constants.lang import Language
from yta_validation.parameter import ParameterValidator


# TODO: Do we want this here? I think it should be
# some additional (and optional) library
class GoogleTranslator:
    """
    Class to wrap the functionality that allows
    translating a text by using the Google Translator
    official web page with a web scrapper.
    """

    @staticmethod
    def translate(
        text: str,
        input: Language = Language.ENGLISH,
        output: Language = Language.SPANISH
    ) -> str:
        """
        Get the translation of the given 'text' from the
        provided 'input' language to the 'output' language.

        This method is using the Google Translator web
        page to navigate to it and obtain the translation
        from that service, so it needs internet connection
        and a compatible Chrome web navigator.
        """
        ParameterValidator.validate_mandatory_string('text', text, do_accept_empty = False)
        input = Language.to_enum(input)
        output = Language.to_enum(output)

        return google_translate(text, input.value, output.value)
    
__all__ = [
    'GoogleTranslator',
    'Language'
]