
使用Python Tornado编写的链接收藏网站，使用Mongodb作为数据库。

并非基于tag或者分类来收集书签，而是基于话题。首先创建一个话题，然后在话题下添加书签。

以下功能：

* 添加话题和书签
* 多用户
* 收藏其他用户的话题和书签
* 评论话题和书签（多说）
* 等等


已经具备基本功能。

**代码尚未重构，且不再完善和维护。**


简单的使用指南：

1、安装mongodb后，创建数据库`pastlink`，并为数据库设置用户和密码。

2、在`ptool.py`的`db.authenticate('username', 'password')`处修改用户和密码。在`controller/tools/DB.py`中的`db = motor.MotorClient('mongodb://username:password@localhost:27017/pastlink').pastlink`处修改用户和密码。

3、使用`ptool.py`中的`init_db()`函数初始化数据库，使用`add_user()`函数添加一个用户（pastlink的用户）。

4、执行：

	$ python server.py

浏览器访问`http://your-ip:8888`。
