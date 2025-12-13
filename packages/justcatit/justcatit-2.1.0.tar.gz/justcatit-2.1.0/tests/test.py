# import cat as cat
from justcatit import cat as cat

path = r'C:\Users\PetrParik\Source\Repos\lab\lab-ojuci'
summary = cat.invoke_project(path,cat.LoggingLevel.INFORMATION, include_tags="something");
print(summary.PassRate)

# cat.open_project(r'C:\Users\PetrParik\Source\Repos\lab\lab-ojuci', logging_level= cat.LoggingLevel.INFORMATION)
# tests_to_execute = set()
# for test in cat.get_tests():
#     if("flight" in test.TestFullName.lower() and "match" not in test.TestFullName.lower()):
#         tests_to_execute.add(test.TestDefinitionID)
# # cat.invoke_tests(test_ids = tests_to_execute)
# cat.invoke_tests(include_tags="Experiment;SomeTHIng", filter="flight")

# cat.invoke_project(r'C:\Users\PetrParik\Source\Repos\lab\lab-ojuci')


# projectPath = r'C:\Users\PetrParik\Source\Repos\lab\lab-ojuci'
# project = cat.open_project(projectPath, logging_level= cat.LoggingLevel.ERROR);
# for test in project.Tests:
#     print(test.FirstQuery)

# for ds in cat.get_data_sources():
#     print("DS: " + ds.Name)

# for t in cat.get_tests():
#     print("T: " + t.TestFullName)

# for dsl in cat.get_data_source_lists():
#     print("DSL: " + dsl.ProviderNameAndVersion)

# for tl in cat.get_test_lists():
#     print("TL: " + str(tl.IsImplicit))

instance = cat.get_instance()
print(instance.Plan)
print(instance.LicenseKey)

for pt in cat.get_project_templates():
     print("PT: " + pt.TemplateCode + " = " + pt.Description)
# cat.invoke_tests()

# test_results_summary = cat.get_test_results_summary()
# print(test_results_summary.PassRate)

# for test_result in cat.get_test_results():
#     print(test_result.TestFullName + " = " + str(test_result.TestResult))

# queryResult = cat.invoke_command('CsvData', 'select table_schema, table_name from information_schema.tables')

# for row in queryResult["data"]:
#     print(row)

# for m in queryResult["messages"]:
#     print(m);

# cat.close_project()

# print('================================================')
# cat.new_project('somethingToTest', r'C:\Users\PetrParik\Source\Repos\lab\lab-lmpac', template='getStartedWindows', force=True, online=True, logging_level=cat.LoggingLevel.INFORMATION)
# cat.invoke_project(r'C:\Users\PetrParik\Source\Repos\lab\lab-lmpac', loggingLevel=cat.LoggingLevel.INFORMATION)
# # cat.invoke_project(projectPath)
# # testResults = invoke_cat_tests()

# # print(testResults.PassRate)
