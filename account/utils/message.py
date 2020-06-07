from ..models import User, Message
from issue.models import Issue, Answer
from comment.models import Comment


def create_message(Type, obj):
    ''' 创建message，有如下三大类情况：
    1）问题新增回答：obj是Answer实例
    2）文章新增评论：obj是Comment实例
    3）回答新增评论：obj是Comment实例
    '''
    if Type == Message.MsgType.AnswerToIssue:
        content = "在帖子<" + str(obj.issue.title) + '>下，新增一条回答'
        Message.objects.create(Type=Message.MsgType.AnswerToIssue, \
            issue_id=obj.issue.id, answer_id=obj.id, parent_comment_id=-1, comment_id=-1, \
            from_uname = obj.replier.username, receiver=obj.issue.author, \
            pub_date=obj.pub_date, content=content, IsReading=False)
    
    elif Type == Message.MsgType.CommentToArticle:
        if not obj.parent_comment:
            issue = obj.content_object
            content = "在文章<" + str(issue.title) + ">下，新增一条评论"
            Message.objects.create(Type=Message.MsgType.CommentToArticle, \
                issue_id=issue.id, answer_id=-1, parent_comment_id=-1, comment_id=obj.id, \
                from_uname = obj.from_id.username, receiver=obj.to_id, \
                pub_date=obj.pub_date, content=content, IsReading=False)
        else:
            issue = obj.parent_comment.content_object
            content = "在文章<" + str(issue.title) + '>下，对您的评论新增回复'
            Message.objects.create(Type=Message.MsgType.CommentToArticle, \
                issue_id=issue.id, answer_id=-1, parent_comment_id=obj.parent_comment.id, comment_id=obj.id, \
                from_uname = obj.from_id.username, receiver=obj.to_id, \
                pub_date=obj.pub_date, content=content, IsReading=False)
    
    elif Type == Message.MsgType.CommentToAnswer:
        if not obj.parent_comment:
            answer = obj.content_object
            content = "在帖子<" + str(answer.issue.title) + '>的回答下，新增一条评论'
            Message.objects.create(Type=Message.MsgType.CommentToAnswer, \
                issue_id=answer.issue.id, answer_id=answer.id, parent_comment_id=-1, comment_id=obj.id, \
                from_uname=obj.from_id.username, receiver=obj.to_id, \
                pub_date=obj.pub_date, content=content, IsReading=False)
        else:
            answer = obj.parent_comment.content_object
            content = "在帖子<" + str(answer.issue.title) + '>的回答下，对您的评论新增回复'
            Message.objects.create(Type=Message.MsgType.CommentToAnswer, \
                issue_id=answer.issue.id, answer_id=answer.id, parent_comment_id=obj.parent_comment.id, comment_id=obj.id, \
                from_uname=obj.from_id.username, receiver=obj.to_id, \
                pub_date=obj.pub_date, content=content, IsReading=False)


def conduct_message(msg):
    ''' 从真实的Message实例中，构造反馈给前端的消息体obj
    '''
    return {"msg_id":msg.id, "type":msg.Type, \
        "issue_id":msg.issue_id, "answer_id":msg.answer_id, \
        "parent_comment_id":msg.parent_comment_id, "comment_id":msg.comment_id, \
        "from":msg.from_uname, "pub_date":str(msg.pub_date)[0:16], \
        "content":msg.content, "IsReading":msg.IsReading}

