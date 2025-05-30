from sqlalchemy import create_engine, Column, Integer, String, Text, ForeignKey, Table, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

Base = declarative_base()

# 题目-标签关联表
question_tag = Table('question_tag', Base.metadata,
    Column('question_id', Integer, ForeignKey('questions.id')),
    Column('tag_id', Integer, ForeignKey('tags.id'))
)

class Question(Base):
    __tablename__ = 'questions'
    
    id = Column(Integer, primary_key=True)
    type = Column(String(50))  # 题目类型：选择题、计算题、填空题等
    content = Column(Text)     # 题目内容
    difficulty = Column(Integer)  # 难度等级：1-5
    chapter = Column(String(100))  # 所属章节
    extra = Column(JSON)    # 元数据，用于存储题号等信息
    
    # 关联
    answer = relationship("Answer", back_populates="question", uselist=False)
    tags = relationship("Tag", secondary=question_tag, back_populates="questions")

class Answer(Base):
    __tablename__ = 'answers'
    
    id = Column(Integer, primary_key=True)
    question_id = Column(Integer, ForeignKey('questions.id'))
    content = Column(Text)     # 答案内容，支持HTML格式
    explanation = Column(Text)  # 解析
    
    # 关联
    question = relationship("Question", back_populates="answer")

class Tag(Base):
    __tablename__ = 'tags'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    
    # 关联
    questions = relationship("Question", secondary=question_tag, back_populates="tags")

def init_db(db_url="sqlite:///questions.db"):
    """初始化数据库"""
    engine = create_engine(db_url)
    Base.metadata.create_all(engine)
    return sessionmaker(bind=engine)()

def add_question(session, type, content, answer_content, explanation, difficulty=3, chapter="", tags=None, extra=None):
    """添加新题目"""
    question = Question(
        type=type,
        content=content,
        difficulty=difficulty,
        chapter=chapter,
        extra=extra or {}
    )
    
    answer = Answer(
        content=answer_content,
        explanation=explanation
    )
    
    question.answer = answer
    
    if tags:
        for tag_name in tags:
            tag = session.query(Tag).filter_by(name=tag_name).first()
            if not tag:
                tag = Tag(name=tag_name)
            question.tags.append(tag)
    
    session.add(question)
    session.commit()
    return question

def get_questions(session, type=None, chapter=None, tag=None, difficulty=None):
    """查询题目"""
    query = session.query(Question)
    
    if type:
        query = query.filter(Question.type == type)
    if chapter:
        query = query.filter(Question.chapter == chapter)
    if difficulty:
        query = query.filter(Question.difficulty == difficulty)
    if tag:
        query = query.join(Question.tags).filter(Tag.name == tag)
        
    return query.all() 