### 数据库设计
```json
students:
{
    "student_id":"唯一，标识每一个学生",
    "password":"",
    "role":"student/admin",
    "face_login_enable":"True/False",
}
// subjects:
// {
//     "subject_id": "主键，唯一标识每个科目",
//     "name": "科目名称"
// }
questions:
{
    "question_id": "主键，唯一标识每个题目",
    // "subject_id": "外键，引用科目表的 subject_id",
    "content": "题目内容",
    // "knowledge_point": "知识点",
    "question_type": "type",
    "score":"分值",
    "reference_answer":"参考答案"
}
wrong_answers
{
    "record_id": "主键，唯一标识每条错题记录",
    "student_id": "外键，引用学生表的 student_id",
    "question_id": "外键，引用题目表的 question_id",
    "attempt_time": "尝试时间",
    "answer": "学生的回答",
    "is_correct": "True/False"
}
```

### 题库操作规则 
```python
    if type=="翻译":
        similarity=Taskflow("text_similarity")
        similarity([])

    elif type=="小作文" or type=="大作文":
        
    else:
        if user_input==questions表.reference_answer:
            score=get_score_by_type(type)
        else:
            score=0
        return score

    
```