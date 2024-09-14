import coverage
import unittest

# 初始化 coverage 对象
cov = coverage.Coverage()

# 开始收集覆盖率数据
cov.start()

# 运行测试
loader = unittest.TestLoader()
tests = loader.discover('.', pattern='test*.py')
test_runner = unittest.TextTestRunner()
test_result = test_runner.run(tests)

# 停止收集覆盖率数据
cov.stop()

# 保存覆盖率数据
cov.save()

# 生成 HTML 报告
cov.html_report(directory='coverage_report')

print("覆盖率报告已生成到 coverage_report 目录中。")
