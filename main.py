from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
import docx
from models import init_db, add_question, Question, Answer
import os
from pydantic import BaseModel

app = FastAPI()

# 允许跨域请求
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 初始化数据库
db = init_db()

class AnswerUpdate(BaseModel):
    answer: str

@app.post("/api/physics-questions/import-word")
async def import_word(
    file: UploadFile = File(...),
    answer_text: str = Form(...),
    gui_mode: bool = Form(False)
):
    try:
        # 保存上传的文件
        file_location = f"temp_{file.filename}"
        with open(file_location, "wb+") as file_object:
            file_object.write(await file.read())
        
        # 读取Word文档
        doc = docx.Document(file_location)
        
        # 解析答案文本
        answers = {}
        for line in answer_text.strip().split('\n'):
            if ',' in line:
                num, answer, explanation = line.split(',', 2)
                answers[num.strip()] = (answer.strip(), explanation.strip())
        
        # 处理题目
        current_question = ""
        question_number = None
        questions_added = 0
        
        for para in doc.paragraphs:
            text = para.text.strip()
            if not text:
                continue
                
            # 检查是否是题号
            if text[0].isdigit() and '.' in text:
                # 保存之前的题目
                if current_question and question_number:
                    if question_number in answers:
                        answer, explanation = answers[question_number]
                        add_question(
                            db,
                            type="计算题",  # 默认类型
                            content=current_question,
                            answer_content=answer,
                            explanation=explanation,
                            difficulty=3,  # 默认难度
                            chapter="",    # 默认章节
                            tags=["物理"],  # 默认标签
                            extra={"question_number": question_number}  # 保存题号
                        )
                        questions_added += 1
                
                # 开始新题目
                question_number = text.split('.')[0]
                current_question = text
            else:
                # 继续当前题目
                current_question += "\n" + text
        
        # 处理最后一个题目
        if current_question and question_number:
            if question_number in answers:
                answer, explanation = answers[question_number]
                add_question(
                    db,
                    type="计算题",
                    content=current_question,
                    answer_content=answer,
                    explanation=explanation,
                    difficulty=3,
                    chapter="",
                    tags=["物理"],
                    extra={"question_number": question_number}  # 保存题号
                )
                questions_added += 1
        
        # 清理临时文件
        os.remove(file_location)
        
        return {"message": f"成功导入 {questions_added} 道题目"}
        
    except Exception as e:
        return {"error": str(e)}

@app.get("/api/physics-questions/")
async def get_questions():
    questions = db.query(Question).all()
    return [
        {
            "id": q.id,
            "content": q.content,
            "answer": q.answer.content if q.answer else "",
            "analysis": q.answer.explanation if q.answer else "",
            "extra": {
                "question_number": q.extra.get("question_number", str(q.id)) if q.extra else str(q.id),
                "type": q.type,
                "difficulty": q.difficulty,
                "chapter": q.chapter
            }
        }
        for q in questions
    ]

@app.post("/api/physics-questions/{question_id}/answer")
async def update_answer(question_id: int, answer: AnswerUpdate):
    print(f"收到更新答案请求：question_id={question_id}, answer={answer}")
    question = db.query(Question).filter(Question.id == question_id).first()
    if not question:
        print(f"题目不存在：question_id={question_id}")
        return {"error": "题目不存在"}
    
    try:
        # 更新答案
        if not question.answer:
            print("创建新答案")
            # 如果题目还没有答案，创建一个新的答案
            new_answer = Answer(content=answer.answer, explanation="")
            question.answer = new_answer
            db.add(new_answer)
        else:
            print("更新现有答案")
            # 如果题目已有答案，更新现有答案
            question.answer.content = answer.answer
        
        print("提交数据库更改")
        db.commit()
        print("答案更新成功")
        return {"message": "答案已更新"}
    except Exception as e:
        print(f"更新答案时出错：{str(e)}")
        print(f"错误类型：{type(e)}")
        import traceback
        print(f"错误堆栈：{traceback.format_exc()}")
        db.rollback()
        return {"error": str(e)}

@app.delete("/api/physics-questions/{question_id}")
async def delete_question(question_id: int):
    question = db.query(Question).filter(Question.id == question_id).first()
    if question:
        db.delete(question)
        db.commit()
        return {"message": "题目已删除"}
    return {"error": "题目不存在"} 