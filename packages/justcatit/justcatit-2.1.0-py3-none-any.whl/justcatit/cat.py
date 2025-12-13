from enum import Enum
import sys, pathlib, os;
from pythonnet import get_runtime_info, set_runtime

cat_was_initialized = False
cat_session = None

LoggingLevel = Enum('LoggingLevel', ['NOTHING', 'FATAL', 'ERROR', 'WARNING', 'INFORMATION', 'DEBUG'])

def _logging_level_translate(logging_level: LoggingLevel) -> str:
    if(logging_level == None or logging_level == LoggingLevel.NOTHING):
        return None
    else:
        # Map Python enum names to .NET expected values
        mapping = {
            'ERROR': 'Error',
            'FATAL': 'Fatal', 
            'WARNING': 'Warning',
            'INFORMATION': 'Information',
            'DEBUG': 'Debug',
            'NOTHING': None
        }
        return mapping.get(logging_level.name, logging_level.name) if hasattr(logging_level, 'name') else str(logging_level)

def _initialize_cat_session_if_needed(logging_level = LoggingLevel.INFORMATION):
    """Private function, should not be called by consumers.
    
    Initializes CAT session, loads all DLLs in bin, and imports JC.Cat.Core namespace.
    """
    global cat_session, cat_was_initialized
    if cat_was_initialized == True:
        return
    set_runtime('coreclr') # set runtime to coreclr
    current_file_directory = pathlib.Path(__file__).parent.resolve()
    dllPath = os.path.join(current_file_directory, 'bin/')
    sys.path.append(dllPath)
    import clr # cannot go to top!
    clr.AddReference("JC.Cat.Core")
    import JC.Cat.Core as catCore
    logging_level_string = _logging_level_translate(logging_level)
    if(cat_session == None or cat_session.LoggingSettings.LoggingLevel != logging_level_string):
        cat_session = catCore.CatSession(catCore.CatClient.Python, logging_level_string, "");
    cat_was_initialized = True

def open_project(projectFilePath: str, loggingLevel: LoggingLevel = None):
    """Opens CAT project file (.cat.yaml file)

    In CAT, you define your data sources, tests and other stuff in
    *CAT project files*: https://docs.justcat.it/docs/help/project-files/introduction/

    This function opens the file, loads the tests and data sources, generates tests
    from metadata (if you have any metadata driven tests) etc.
    It "prepares" for running tests.
    """
    global cat_session, cat_was_initialized
    if loggingLevel is None:
        loggingLevelString = None
    elif loggingLevel.name == "DoNotLog":
        loggingLevelString = "None"
    else:
        loggingLevelString = _logging_level_translate(loggingLevel)
    _initialize_cat_session_if_needed(loggingLevelString)
    project = cat_session.OpenProject(projectFilePath, True, True)
    return project

def invoke_tests(filter: str = None, test_ids: set = None, include_tags: str = None, exclude_tags: str = None, skip_outputs: bool = False):
    """Invokes test in the open CAT project file and returns their results.
    
    First, you need to open CAT project using open_project function.
    Once the project is open, you can use invoke_tests to actually exuecte the tests
    in your project.

    :filter: Execute only tests with TestFullName containing string in this parameter. (full name consists of Test suite, order, test case and test name)
    :test_ids: Set of test IDs you want to evaluate. You get them by iterating and filtering tests from `get_tests` function.
    :include_tags: Only execute tests with at least one of the provided tags. To provide more tags, use comma or semicolon in one string.
    :exclude_tags: Skip evaluation of any tests with that have at least one of tags specified in this parameter. Use comma or semicolon to provide more tags.
    :skip_outputs: CAT will not generate any defined outputs (such as MS Excel files, JSON, records to database). Standard output to console is not affected by this setting.
    """
    _get_project() # veryfies there is an open project
    test_guids = None
    if test_ids != None and len(test_ids) > 0:
        from System.Collections.Generic import List
        from System import Guid
        test_guids = List[Guid]()
        for test_id in test_ids:
            test_guids.Add(test_id)
    testResultsSummary = cat_session.ExecuteTests(test_guids, filter,include_tags, exclude_tags, skip_outputs)
    return testResultsSummary

def get_data_sources():
    """Returns list of all data sources in currently open CAT project.
    
    In CAT, you can load data sources definitions from YAML files, MS Excel, databases
    and any other format. Once you open your .cat.yaml project file,
    you can use this command to retrieve list of all data sources that
    were loaded.
    """
    project = _get_project()
    return project.DataSources

def get_tests():
    """Returns list of all tests in currently open CAT project.
    
    In CAT you can load tests definitions from many sources: YAML files, MS Excel,
    databases and many others. You can also generate tests from metadata.

    Once you open you .cat.yaml project file using open_project function, you
    can use get_tests to retrieve list of all tests, including those loaded from
    external sources and generated from metadata.
    """
    project = _get_project()
    return project.Tests

def get_data_source_lists():
    """Returns list of 'locations' from where you loaded data source definitions.
    
    By default CAT looks for "Data sources" node in .cat.yaml project file. But
    you can also load data sources e.g., from other YAML file or from database.
    """
    project = _get_project()
    return project.DataSourceLists

def get_test_lists():
    """Returns list of 'locations' from where you loaded test definitions.
    
    By default CAT looks for "Tests" node in .cat.yaml project file. But
    you can also load test definitions e.g., from other YAML file(s) or from database(s).
    """
    project = _get_project()
    return project.TestLists

def get_instance():
    """Return information about your CAT installation, such as Plan, License key, Installation timestamp, ..."""
    session = _get_session()
    return session.GetCatInstance()

def close_project():
    """Closes CAT project, if there is any open project in your session.
    
    Allows to close a CAT project without closing the session.
    """
    project = _get_project() # veryfies there is an open project
    session = _get_session()
    session.Project = None

def get_project_templates(online: bool = False, logging_level: LoggingLevel = None): 
    """Returns list of templates for creating CAT projects."""
    session = _get_session(logging_level)
    return session.GetProjectTemplates(online)

def get_test_results_summary():
    """Returns summary of last run of tests.
    
    The summary contains number of passed tests, failed tests, etc.
    Also total execution time, pass rate and other information.
    The summary object also contains list of all test runs (details),
    including their test defintiion.
    """
    session = _get_session()
    return session.LatestRunSummary

def get_test_results():
    """Returns list of all test results of the last run of tests.
    
    This function outputs a collection of test results from the last run.
    If you ran e.g., six tests in the last run, you'll get 6 test results,
    with information about when the test evaluation started/finished,
    what wat the test result (passed, failed etc.), all information from test definition
    and other.
    """
    session = _get_session()
    return session.LatestRunSummary.Results

def invoke_command(data_source_name: str, command_text: str, logging_level:LoggingLevel = None) -> dict:
    """Executes a command against a data source and returns results.
    
    Provide SQL, DAX, MDX or whatever your data source understands. CAT will execute it against a data 
    source of your choice. The result is a dictionary with "data" (list of dictionaries), "messages" as list
    of messages the data source sent and "exception" with information about error, if there was any.

    Important: This function is meant mainly for troubleshooting. It is not supported to use it for retrieving 
    large data volumes.

    :data_source_name: Name of one of data sources defined or imported in `.cat.yaml` CAT project file.
    :command_text: What you want to execute against the data source. Typically a SQL query (or DAX, MDX 
    or something else, depending on your data source)
    :logging_level: CAT logging level to be used. Use `None` for default logging levels.
    """
    session = _get_session(logging_level)
    command_result = session.InvokeCommand(command_text, data_source_name);
    data_list = []
    for row in command_result.Data.Rows:
        # Create a dictionary for each row
        row_dict = {command_result.Data.Columns[col].ColumnName: row[col] for col in range(command_result.Data.Columns.Count)}
        # Append the dictionary to the list
        data_list.append(row_dict)
    return {"data": data_list, "messages": command_result.Messages, "exception": command_result.Exception}


def invoke_project(project_file_path: str, loggingLevel: LoggingLevel = None, filter: str = None, test_ids: set = None, include_tags: str = None, exclude_tags: str = None, skip_outputs: bool = False): 
    """Opens a CAT project file (.cat.yaml) and invokes its tests.
    
    This is in fact a "shortcut" for open_project and invoke_tests. The entire definition
    in your project file is evaluated and loaded again and a fresh list of tests is executed.
    The function invoke_tests, on the contrary, only runs again the tests as they were already loaded.

    :project_file_path: path to a `.cat.yaml` file or to a directory containing exactly one such file
    :logging_level: CAT logging level to be used. Use `None` for default logging levels.
    :filter: Execute only tests with TestFullName containing string in this parameter. (full name consists of Test suite, order, test case and test name)
    :test_ids: Set of test IDs you want to evaluate. You get them by iterating and filtering tests from `get_tests` function.
    :include_tags: Only execute tests with at least one of the provided tags. To provide more tags, use comma or semicolon in one string.
    :exclude_tags: Skip evaluation of any tests with that have at least one of tags specified in this parameter. Use comma or semicolon to provide more tags.
    :skip_outputs: CAT will not generate any defined outputs (such as MS Excel files, JSON, records to database). Standard output to console is not affected by this setting.
    """
    open_project(project_file_path, loggingLevel)
    summary = invoke_tests(filter, test_ids, include_tags, exclude_tags, skip_outputs)
    return summary

def new_project(name: str = None, path: str = None, template: str = None, online: bool = False, commented: bool = False, force: bool = False, wrap: bool = False, logging_level: LoggingLevel = None):
    """Creates a new CAT project based on a template.
    
    :name: Name for your new project. Please avoid spaces and fancy characters.
    :path: Path to a directory where you want the new CAT project file created.
    :template: Code of a template you want to use. Get their list using `get_project_templates` function.
    :online: When set to True, CAT searches for project templates online at CAT portal.
    :commented: Add lots of descriptive comments to the project file?
    :force: Use with care! When set to True, CAT deletes everything in the provided `path` (or current directory, if not specified) before creating the project there.
    :wrap: When True, CAT wraps the generated content into a directory (with name same as in `name` parameter) inside provided `path` (or current directory).
    :logging_level: CAT logging level to be used. Use `None` for default logging levels.
    """
    session = _get_session(logging_level)
    session.NewProject(template, name, path, commented, force, online, wrap)

def set_instance(license_key: str, logging_level:LoggingLevel = None):
    """Used for setting license key.
    
    If you have a CAT license key, use this function to apply it.
    You can also use it to remove the license key from you instance,
    in that case just put space or empty string into license_key.

    :license_key: The license key you received when you paid for CAT subscription or when you started a trial.
    :logging_level: CAT logging level to be used. Use `None` for default logging levels.
    """
    session = _get_session(logging_level)
    session.SetLicenseKey(license_key)

def _get_session(logging_level: LoggingLevel = None):
    global cat_session
    _initialize_cat_session_if_needed(logging_level)
    if cat_session == None:
        raise "There is no open CAT session."
    else:
        return cat_session
    
def _get_project():
    cat_session = _get_session()
    if cat_session.Project == None:
        raise "There is no open project. Open a CAT project file first."
    return cat_session.Project

