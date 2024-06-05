from transformers import AutoTokenizer, AutoModel
import torch
from sklearn.metrics.pairwise import cosine_similarity as sklearn_cosine_similarity
import jieba
from sklearn.feature_extraction.text import TfidfVectorizer
from WebITS import trans_text_main
from scipy.spatial.distance import euclidean
# 加载预训练的多语言模型和分词器
tokenizer = AutoTokenizer.from_pretrained("BAAI/bge-m3")
model = AutoModel.from_pretrained("BAAI/bge-m3")

def get_sentence_embedding(sentence):
    inputs = tokenizer(sentence, return_tensors='pt', truncation=True, padding=True, max_length=128)
    with torch.no_grad():
        outputs = model(**inputs)
    return outputs.last_hidden_state.mean(dim=1)

def cosine_similarity(embedding1, embedding2):
    return torch.nn.functional.cosine_similarity(embedding1, embedding2).item()

def calculate_similarity(standard_answer, student_answer):
    standard_tokens = get_sentence_embedding(standard_answer)
    student_tokens = get_sentence_embedding(student_answer)
    return cosine_similarity(standard_tokens, student_tokens)

def translate_text(text):
    translated_text = trans_text_main(text)
    return translated_text

def tfidf_similarity(text1, text2):
    corpus = [' '.join(jieba.cut(text1)), ' '.join(jieba.cut(text2))]
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(corpus)
    similarity_matrix = sklearn_cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
    return similarity_matrix[0][0]

def euclidean_distance(text1, text2):
    corpus = [' '.join(jieba.cut(text1)), ' '.join(jieba.cut(text2))]
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(corpus)
    return euclidean(tfidf_matrix[0].toarray().flatten(), tfidf_matrix[1].toarray().flatten())

def grade_answer(standard_answer, student_answer, original_question):
    # 初步评分
    score1 = calculate_similarity(standard_answer, student_answer)
    print(f"初步评分：{score1:.2f}")

    # # 翻译学生答案回原文并进行复核评分
    # translated_back = translate_text(student_answer)
    # print(f"翻译回原文的学生答案：{translated_back}")
    
    # score2 = tfidf_similarity(original_question, translated_back)
    # print(f"二次评分：{score2:.2f}")

    # 计算欧氏距离
    distance_score = euclidean_distance(standard_answer, student_answer)
    print(f"欧氏距离评分：{distance_score:.2f}")

    # 综合评分
    final_score = (score1 * 0.5) +(distance_score * 0.5)
    return f'Final Score: {final_score:.2f}'

# 示例文本
standard_answer = "欢迎同学们参与项目！"
student_answer = "欢迎同学们参加！"
original_question = "Students are welcome to participate in the program！"

# 评分
final_result = grade_answer(standard_answer, student_answer, original_question)
print(final_result)
