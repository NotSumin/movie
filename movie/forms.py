from flask_wtf import FlaskForm
from wtforms.fields.choices import SelectField, RadioField
from wtforms.fields.simple import StringField, TextAreaField, SubmitField, PasswordField, EmailField
from wtforms.validators import DataRequired, Length, EqualTo, Email, Regexp, Optional
from flask_wtf.file import MultipleFileField, FileAllowed


class QuestionForm(FlaskForm):
    kind = RadioField('종류', choices=[('영화관 문의', '영화관 문의'), ('기타 문의', '기타 문의')], validators=[DataRequired('종류는 필수 입력 항목입니다.')])
    title = StringField('제목', validators=[DataRequired('제목은 필수 입력 항목입니다.')])
    content = TextAreaField('내용', validators=[DataRequired('내용은 필수 입력 항목입니다.')])
    image = MultipleFileField('첨부파일', validators=[FileAllowed(['jpg', 'jpeg', 'png', 'gif'], '이미지 파일만 업로드 가능합니다.')])
    submit = SubmitField('확인')

class AnswerForm(FlaskForm):
    content = TextAreaField('내용', validators=[DataRequired('내용은 필수 입력 항목입니다.')])
    submit = SubmitField('답변등록')

class UserCreateForm(FlaskForm):
    username = StringField('아이디', validators=[DataRequired('아이디는 필수 입력 항목입니다.'), Length(min=3, max=25, message='3-25자리의 문자를 입력해주세요.')])
    password1 = PasswordField('비밀번호', validators=[DataRequired('비밀번호 필수 입력 항목입니다.'), EqualTo('password2', message='비밀번호가 일치하지 않습니다.')])
    password2 = PasswordField('비밀번호 확인', validators=[DataRequired('비밀번호를 재입력해 주세요.')])
    email = EmailField('이메일', validators=[DataRequired('이메일은 필수 입력 항목입니다.'), Email('이메일 형식이 올바르지 않습니다.')])
    contact = StringField('전화번호', validators=[Optional(), Regexp(r'^\d+$', message='전화번호 형식이 올바르지 않습니다.')])
    submit = SubmitField('저장하기')

class UserLoginForm(FlaskForm):
    username = StringField('아이디', validators=[DataRequired(), Length(min=3, max=25)])
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
