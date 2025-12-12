# lounger

Next generation automated testing framework.

## feature

🌟 支持`web`/`api`测试。

🌟 提供脚手架生成自动化项目。

🌟 更好用的数据驱动。

🌟 支持数据库操作。

🌟 已经配置好的测试报告（包含截图、日志）。

🌟 天然支持`API objects`、`Page objects`设计模式。

## framework

lounger不是一个从零开始的自动化测试框架，建立在`pytest`生态的基础上，提供更加简单、方便的使用体验。

![](./images/framework.png)

## Install

* pip安装。

```shell
$ pip install lounger
```

* 体验最新的项目代码。

```shell
$ pip install -U git+https://github.com/SeldomQA/lounger.git@main
```

## scaffold

lounger提供了脚手架，直接创建项目和使用。

```shell
$ lounger --help

Usage: lounger [OPTIONS]

  lounger CLI.

Options:
  --version                Show version.
  -pw, --project-web TEXT  Create an Web automation test project.
  -pa, --project-api TEXT  Create an API automation test project.
  --help                   Show this message and exit.
```

### Web自动化项目

* 首先，请安装测试浏览器（至少一款）。
    ```shell
    $ playwright install chromium[可选]
    $ playwright install firefox[可选]
    $ playwright install webkit[可选]
    ```

* 创建web自动化测试项目。
    ```shell
    $ lounger --project-web myweb
    
    2025-11-18 00:05:00 | INFO     | cli.py | Start to create new test project: myweb
    2025-11-18 00:05:00 | INFO     | cli.py | CWD: D:\github\seldomQA\lounger
    
    2025-11-18 00:05:00 | INFO     | cli.py | 📁 created folder: reports
    2025-11-18 00:05:00 | INFO     | cli.py | 📄 created file: conftest.py
    2025-11-18 00:05:00 | INFO     | cli.py | 📄 created file: pytest.ini
    2025-11-18 00:05:00 | INFO     | cli.py | 📄 created file: test_dir/__init__.py
    2025-11-18 00:05:00 | INFO     | cli.py | 📄 created file: test_dir/test_sample.py
    2025-11-18 00:05:00 | INFO     | cli.py | 🎉 Project 'myweb' created successfully.
    2025-11-18 00:05:00 | INFO     | cli.py | 👉 Go to the project folder and run 'pytest' to start testing.
    ```

* 运行项目
    ```shell
    $ cd myweb
    $ pytest
    ```

* 查看报告
  ![](./images/result_web.png)

### API自动化项目

* 创建api自动化测试项目。
    ```shell
    $ lounger --project-api myapi
    
    2025-10-22 23:36:31 | INFO     | cli.py | Start to create new test project: myapi
    2025-10-22 23:36:31 | INFO     | cli.py | CWD: D:\github\seldomQA\lounger
    
    2025-10-22 23:36:31 | INFO     | cli.py | 📁 created folder: reports
    2025-10-22 23:36:31 | INFO     | cli.py | 📄 created file: conftest.py
    2025-10-22 23:36:31 | INFO     | cli.py | 📄 created file: test_api.py
    2025-10-22 23:36:31 | INFO     | cli.py | 📄 created file: pytest.ini
    2025-10-22 23:36:31 | INFO     | cli.py | 📄 created file: config/config.yaml
    2025-10-22 23:36:31 | INFO     | cli.py | 📄 created file: datas/sample/test_sample.yaml
    2025-10-22 23:36:31 | INFO     | cli.py | 📄 created file: test_dir/__init__.py
    2025-10-22 23:36:31 | INFO     | cli.py | 📄 created file: test_dir/test_sample.py
    2025-10-22 23:36:31 | INFO     | cli.py | 🎉 Project 'myapi' created successfully.
    2025-10-22 23:36:31 | INFO     | cli.py | 👉 Go to the project folder and run 'pytest' to start testing.
    ```
  > 注：项目包含通过YAML管理API测试用例，编写规范参考下面的文档。

* 运行测试
    ```shell
    $ cd myapi
    $ pytest
    ```

* 测试报告
  ![](./images/result.png)

## 项目&文档&示例

1. 如何进行Web自动化测试？👉 [阅读文档](./myweb)
2. 如何进行API自动化测试？👉 [阅读文档](./myapi)
3. 框架集成了哪些功能？ [测试示例](./tests)

## 对比

* seldom VS lounger 👉[详细对比](./seldom_vs_lounger.md)
