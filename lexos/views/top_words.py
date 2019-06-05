from flask import render_template, Blueprint, session

from lexos.helpers import constants as constants
from lexos.managers import session_manager as session_manager
from lexos.models.filemanager_model import FileManagerModel
from lexos.models.topword_model import TopwordModel

top_words_blueprint = Blueprint("top-words", __name__)


@top_words_blueprint.route("/top-words", methods=["GET"])
def top_words() -> str:
    """ Gets the top words page.
    :return: The top words page.
    """

    # Set the default options
    if "topwordoption" not in session:
        session["topwordoption"] = constants.DEFAULT_TOPWORD_OPTIONS
    if "analyoption" not in session:
        session["analyoption"] = constants.DEFAULT_ANALYZE_OPTIONS

    # Return the top words page
    return render_template("top-words.html")


@top_words_blueprint.route("/top-words/class-divisions", methods=["GET"])
def class_divisions() -> str:
    """ Gets the class divisions.
    :return: The class divisions.
    """

    file_manager = FileManagerModel().load_file_manager()

    return file_manager.get_class_division_map().transpose().to_json()


@top_words_blueprint.route("/top-words/tables", methods=["POST"])
def tables() -> str:
    """ Gets the top words tables.
    :return: The top words tables.
    """

    # Cache the options
    session_manager.cache_analysis_option()
    session_manager.cache_top_word_options()

    # Return the top words tables
    return TopwordModel().get_displayable_result()