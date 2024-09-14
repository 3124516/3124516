"""
此模块用于计算两个文本文件的相似度，包括文本的读取、预处理和相似度计算。
"""

import re
import argparse
import jieba
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# 定义读取文本内容的函数
def read_text(file_path):
    """
    从指定文件路径读取文本内容。

    :param file_path: 文件路径
    :return: 读取的文本内容
    :raises FileNotFoundError: 如果文件未找到
    :raises IOError: 如果读取文件时发生错误
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file_obj:
            return file_obj.read()
    except FileNotFoundError as error:
        raise FileNotFoundError(f"文件 {file_path} 未找到，请检查文件路径。") from error
    except IOError as error:
        raise IOError(f"读取文件 {file_path} 时发生错误: {error}") from error

# 文本预处理
def preprocess_text(text):
    """
    对输入文本进行预处理，包括去除标点符号和分词。

    :param text: 原始文本
    :return: 处理后的文本
    :raises Exception: 如果预处理文本时发生错误
    """
    try:
        # 去除标点符号
        text = re.sub(r'[^\w\s]', '', text)
        # 分词处理
        words = jieba.cut(text)
        # 将分词结果拼接为字符串
        processed_text = ' '.join(words)
        return processed_text
    except Exception as error:
        raise Exception(f"文本预处理时发生错误: {error}") from error

# 解析命令行参数
def parse_args():
    """
    解析命令行传入的参数。

    :return: 解析后的命令行参数
    """
    parser = argparse.ArgumentParser(description="计算两个文本文件的相似度")
    parser.add_argument('orig_file', type=str, help='原始文件路径')
    parser.add_argument('compare_file', type=str, help='比较文件路径')
    parser.add_argument('output_file', type=str, help='结果保存文件路径')
    return parser.parse_args()

# 主函数
def main():
    """
    主函数，用于执行文本相似度计算的流程。
    """
    try:
        args = parse_args()
        text1 = read_text(args.orig_file)
        text2 = read_text(args.compare_file)

        # 预处理文本
        processed_text1 = preprocess_text(text1)
        processed_text2 = preprocess_text(text2)

        # 检查预处理后的文本是否为空
        if not processed_text1:
            raise ValueError("原文处理后的文本为空，请检查输入文本内容。")
        if not processed_text2:
            raise ValueError("比较文件处理后的文本为空，请检查输入文本内容。")

        # 计算TF-IDF向量
        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform([processed_text1, processed_text2])

        # 计算余弦相似度
        cosine_sim = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
        similarity = cosine_sim[0][0]

        # 保存结果
        result = f"{args.orig_file} 与 {args.compare_file} 的相似度: {similarity}\n"

        # 将结果写入文件
        with open(args.output_file, 'w', encoding='utf-8') as output_file:
            output_file.write(result)

        print("相似度计算完成，结果已保存到目标文件中。")

    except (FileNotFoundError, ValueError, IOError) as error:
        print(f"发生错误: {error}")

if __name__ == "__main__":
    main()
