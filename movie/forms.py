from flask_wtf import FlaskForm
from wtforms.fields.choices import SelectField
from wtforms.fields.simple import StringField, TextAreaField, SubmitField, PasswordField, EmailField
from wtforms.validators import DataRequired, Length, EqualTo, Email
from flask_wtf.file import MultipleFileField, FileAllowed


class QuestionForm(FlaskForm):
    subject = StringField('제목', validators=[DataRequired('제목은 필수 입력 항목입니다.')])
    content = TextAreaField('내용', validators=[DataRequired('내용은 필수 입력 항목입니다.')])
    image = MultipleFileField('이미지 업로드', validators=[FileAllowed(['jpg', 'jpeg', 'png', 'gif'], '이미지 파일만 업로드 가능합니다.')])
    submit = SubmitField('등록하기')

class AnswerForm(FlaskForm):
    content = TextAreaField('내용', validators=[DataRequired('내용은 필수 입력 항목입니다.')])
    submit = SubmitField('답변등록')

class UserCreateForm(FlaskForm):
    username = StringField('사용자 이름', validators=[DataRequired(), Length(min=3, max=25)])
    password1 = PasswordField('비밀번호', validators=[DataRequired(), EqualTo('password2', message='비밀번호가 일치하지 않습니다.')])
    password2 = PasswordField('비밀번호 확인', validators=[DataRequired()])
    email = EmailField('이메일', validators=[DataRequired(), Email()])
    submit = SubmitField('저장하기')

class UserLoginForm(FlaskForm):
    username = StringField('사용자 이름', validators=[DataRequired(), Length(min=3, max=25)])
    password = PasswordField('비밀번호', validators=[DataRequired()])
    submit = SubmitField('로그인')

class ReviewCreateForm(FlaskForm):
    rating = SelectField(
        '평점',
        choices=[(str(i), f'{i}점') for i in range(10, 0, -1)],
        validators=[DataRequired()],
        coerce=int,
    )
    content = TextAreaField(
        '관람평',
        validators=[DataRequired('관람평 내용을 입력해주세요.'), Length(min=2, max=1000)],
    )
