import unittest
from unittest.mock import patch, mock_open
from main import read_text, preprocess_text, main, parse_args
import argparse
import jieba
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from tabulate import tabulate

class TestMainFunctions(unittest.TestCase):

    def setUp(self):
        self.results = []

    def tearDown(self):
        # 将结果写入 report.txt 并打印到控制台
        with open('report.txt', 'w', encoding='utf-8') as f:
            for result in self.results:
                f.write('\t'.join(result) + '\n')  # 写入文件，使用制表符分隔
                print(f"测试情景: {result[0]}, 测试结果: {result[1]}, 异常原因: {result[2]}, 重复率: {result[3]}")

    def calculate_similarity(self, text1, text2):
        return cosine_similarity(self._tfidf_transform([text1, text2]))[0][1]

    def _tfidf_transform(self, texts):
        vectorizer = TfidfVectorizer()
        return vectorizer.fit_transform(texts).toarray()

    # 测试参数解析错误
    def test_parse_args_error(self):
        with self.assertRaises(SystemExit):
            parse_args()
        self.results.append(["解析参数失败", "成功", "参数解析时应引发系统退出", ""])
        print("测试参数解析错误: 成功")

    # 测试读取路径不存在
    def test_read_text_file_not_found(self):
        with self.assertRaises(FileNotFoundError) as context:
            read_text('non_existent_file.txt')
        self.assertTrue("文件 non_existent_file.txt 未找到，请检查文件路径。" in str(context.exception))
        self.results.append(["读取不存在的文件", "失败", "文件未找到", ""])
        print("测试读取路径不存在: 失败, 原因:", str(context.exception))

    # 测试预处理文本是否去除标点符号
    def test_preprocess_text_remove_punctuation(self):
        result = preprocess_text("测试文本，应该去除标点。")
        self.assertEqual(result, "测试文本 应该去除标点", "标点符号未正确去除")
        self.results.append(["预处理文本去除标点", "成功", "", ""])
        print("测试预处理文本去除标点: 成功")

    # 测试停用词是否正确去除
    def test_preprocess_text_remove_stopwords(self):
        result = preprocess_text("这是一个测试文本，我们的目标是去除停用词。")
        self.assertEqual(result, "测试文本 目标 去除停用词", "停用词未正确去除")
        self.results.append(["预处理文本去除停用词", "成功", "", ""])
        print("测试预处理文本去除停用词: 成功")

    # 测试jieba分词是否正常
    def test_jieba_segmentation(self):
        text = "我喜欢学习人工智能。"
        words = list(jieba.cut(text))
        self.assertIn("学习", words, "jieba未正确分词")
        self.results.append(["jieba分词测试", "成功", "", ""])
        print("测试jieba分词: 成功")

    # 测试对英文文章的分词
    def test_jieba_for_english_text(self):
        text = "I love studying Artificial Intelligence."
        words = list(jieba.cut(text))
        self.assertIn("Artificial", words, "jieba对英文文本未正确分词")
        self.results.append(["jieba对英文文本测试", "成功", "", ""])
        print("测试jieba对英文文本分词: 成功")

    # 测试主函数成功运行
    def test_main_success(self):
        with patch('main.parse_args', return_value=argparse.Namespace(orig_file='orig_file', compare_file='compare_file', output_file='output_file')), \
             patch('main.read_text', side_effect=["test content 1", "test content 2"]), \
             patch('main.preprocess_text', side_effect=["test content 1", "test content 2"]), \
             patch('builtins.open', mock_open()) as mock_file:
            main()
            mock_file.assert_called_once_with('output_file', 'w', encoding='utf-8')
        similarity = self.calculate_similarity("test content 1", "test content 2")
        self.results.append(["main 函数成功运行", "成功", "", f"{similarity:.2f}"])
        print("主函数运行测试: 成功, 相似度为:", f"{similarity:.2f}")

    # 测试空文本的处理
    def test_empty_text_processing(self):
        result = preprocess_text("")
        self.assertEqual(result, "", "空文本处理未返回空字符串")
        self.results.append(["空文本处理", "成功", "", ""])
        print("空文本处理测试: 成功")

    # 测试TF-IDF算法
    def test_tfidf_transformation(self):
        texts = ["这是一个测试文本。", "这是另一个测试文本。"]
        tfidf_matrix = self._tfidf_transform(texts)
        self.assertEqual(tfidf_matrix.shape, (2, 5), "TF-IDF矩阵形状不正确")
        self.results.append(["TF-IDF算法执行成功", "成功", "", ""])
        print("TF-IDF算法测试: 成功, 矩阵形状为:", tfidf_matrix.shape)

    # 测试余弦相似度计算
    def test_cosine_similarity(self):
        text1 = "我喜欢学习机器学习。"
        text2 = "机器学习是我的最爱。"
        similarity = self.calculate_similarity(text1, text2)
        self.assertGreaterEqual(similarity, 0, "余弦相似度计算错误，应大于或等于0")
        self.results.append(["余弦相似度计算成功", "成功", "", f"{similarity:.2f}"])
        print("余弦相似度计算测试: 成功, 相似度为:", f"{similarity:.2f}")

if __name__ == '__main__':
    unittest.main()
