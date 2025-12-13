# 一. common.utils.models.LooseModel
## 描述: 别名基类
## 1. 解决问题:
在如下结构中
```python
from pydantic import BaseModel
class User(BaseModel):
    user_id: int
```
即使定义了alias_generator, 也只是model的user_id的别名,但是无法改变初始化时传入的参数名称,比如有些api可能有些接口传递了userId,
有些接口传递的是userID,这种同一个平台的接口返回的同一字段大小写不一致的情况很难考虑周全
## 2. 设计思路
设计了一个LooseModel,通过model_config的alias_generator
把user_id转换成userid,在LooseModel的from_any_dict中将输入的字典所有的键小写去掉下划线,不管是userId还是userID
或者是user_ID, 都会变成userid,这样就可以模糊匹配到model中
## 3. 使用方式
```python
from wmain.common.models import LooseModel

class Person(LooseModel):
    age: int
    s_name: str
    s_id: int

class Teacher(Person):
    students: list[Person]

dic = {
    "age": 18,
    "s_name": "张三",
    "S_Id": 1,
    "students": [
        {
            "age": 18,
            "SName": "张三",
            "SID": 1
        }
    ]
}
model = Teacher.from_any_dict(dic)
print(model)
```
输出
```output
age=18 s_name='张三' s_id=1 students=[Person(age=18, s_name='张三', s_id=1)]
```
## 4. 注意事项
本模块会模糊匹配所有输入键,因此不能同时存在userID和userId这种字母一致的键