from transformers import BertTokenizer, BertModel, pipeline
import torch
import jieba
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity as sklearn_cosine_similarity

# 加载预训练的中文BERT模型和分词器
tokenizer = BertTokenizer.from_pretrained('bert-base-chinese')
model = BertModel.from_pretrained('bert-base-chinese')

# 加载机器翻译模型（假设使用Hugging Face的翻译模型）
translator = pipeline('translation', model='Helsinki-NLP/opus-mt-zh-en')

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

def translate_text(text, src_lang='zh', tgt_lang='en', max_length=512):
    # 将文本分割成较短的段落
    sentences = text.split('。')
    translated_text = ''
    for sentence in sentences:
        if sentence.strip():
            translated = translator(sentence, src_lang=src_lang, tgt_lang=tgt_lang, max_length=max_length)
            translated_text += translated[0]['translation_text'] + ' '
    return translated_text.strip()

def tfidf_similarity(text1, text2):
    corpus = [' '.join(jieba.cut(text1)), ' '.join(jieba.cut(text2))]
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(corpus)
    similarity_matrix = sklearn_cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
    return similarity_matrix[0][0]

def grade_answer(standard_answer, student_answer, original_question):
    # 初步评分
    score1 = calculate_similarity(standard_answer, student_answer)
    print(f"初步评分：{score1:.2f}")

    # 翻译学生答案回原文并进行复核评分
    translated_back = translate_text(student_answer, src_lang='zh', tgt_lang='en')
    print(f"翻译回原文的学生答案：{translated_back}")
    
    score2 = tfidf_similarity(original_question, translated_back)
    print(f"二次评分：{score2:.2f}")

    # 判断两者评分的差异
    if abs(score1 - score2) <= 0.25:
        final_score = (score1 + score2) / 2
        return f'Final Score: {final_score:.2f}'
    else:
        return '差距过大，请进行人工评判'

# 示例文本
standard_answer = ""
student_answer = "自然语言处理在计算机科学中非常重要。"
original_question = "Natural language processing is an important field in computer science."

# 评分
final_result = grade_answer(standard_answer, student_answer, original_question)
print(final_result)
