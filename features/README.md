# BDD

基于 behave, 使用标准 Gherkin.

## 代码调用顺序

    before_all
    for feature in all_features:
        before_feature
        for scenario in feature.scenarios:
            before_scenario
            for step in scenario.steps:
                before_step
                    step.run()
                after_step
            after_scenario
        after_feature
    after_all

## 目录结构

    behave.ini
    app/
    features/
    features/environment.py
    features/demo_add.feature
    features/demo_add_more.feature
    features/steps/
    features/steps/demo_add.py
    features/steps/demo_add_more.py

## 文档

- https://github.com/behave/behave.example
- https://behave.readthedocs.io/en/latest/usecase_flask.html